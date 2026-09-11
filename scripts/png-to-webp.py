#!/usr/bin/env python3
"""Convert PNG workshop assets to WebP and rewrite Markdown references.

Default scan root is content/. Pass one or more directories to limit which
PNGs are converted. Markdown updates still search the whole content tree so
a scoped conversion cannot leave stale links elsewhere. Every run also lists
unused PNG and WebP files under the scan path, and renames mixed-case image
filenames to lowercase.

This is a CLI, not a TUI: the job is batch conversion, needs --dry-run, and
must run on macOS/Linux without whiptail or extra UI packages.
"""

from __future__ import annotations

import argparse
import itertools
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from collections import defaultdict
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from pathlib import Path

IMG_REF = re.compile(
    r"(?P<path>(?:https?://[^\s)\"']+|(?:\.{1,2}/|/?[\w@.-])[\w./@-]*)\.(?:png|webp))"
    r"(?P<query>\?[^\s)\"']*)?",
    re.IGNORECASE,
)

INSTALL_HINTS = """cwebp not found. Install the WebP tools, then re-run this script.

  macOS:          brew install webp
  Debian/Ubuntu:  sudo apt install webp
  Fedora:         sudo dnf install libwebp-tools
  Arch:           sudo pacman -S libwebp
  Windows:        choco install webp
                  or scoop install libwebp

Confirm with:  cwebp -version
"""


@dataclass
class Conversion:
    png: Path
    webp: Path
    png_bytes: int
    webp_bytes: int = 0
    status: str = "pending"
    markdown: list[Path] = field(default_factory=list)
    detail: str = ""


@dataclass
class Rename:
    src: Path
    dest: Path
    markdown: list[Path] = field(default_factory=list)
    status: str = "pending"
    detail: str = ""


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def human(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if abs(size) < 1024 or unit == "GB":
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{n} B"


def color(text: str, code: str) -> str:
    if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
        return text
    return f"\033[{code}m{text}\033[0m"


def progress_enabled() -> bool:
    return sys.stderr.isatty() and not os.environ.get("NO_PROGRESS")


def _progress_line(done: int, total: int, label: str, spin: str) -> str:
    cols = shutil.get_terminal_size((80, 20)).columns
    width = min(28, max(10, cols - 42))
    filled = int(width * done / total) if total else 0
    bar = "#" * filled + "-" * (width - filled)
    text = f"  {spin} [{bar}] {done}/{total}  {label}"
    if len(text) > cols - 1:
        text = text[: cols - 2] + "…"
    return text.ljust(max(0, cols - 1))


def draw_progress(done: int, total: int, label: str, spin: str = " ") -> None:
    if not progress_enabled():
        return
    sys.stderr.write("\r" + _progress_line(done, total, label, spin))
    sys.stderr.flush()


def clear_progress() -> None:
    if not progress_enabled():
        return
    cols = shutil.get_terminal_size((80, 20)).columns
    sys.stderr.write("\r" + " " * max(0, cols - 1) + "\r")
    sys.stderr.flush()


def require_cwebp() -> str:
    path = shutil.which("cwebp")
    if path:
        return path
    sys.stderr.write(INSTALL_HINTS)
    raise SystemExit(1)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(
        description="Convert PNG assets to WebP and update Markdown references.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  %(prog)s --dry-run
  %(prog)s content/en/splunk4rookies/o11y-rookies-26
  %(prog)s --quality 85 --yes modules/4-im
  %(prog)s --jobs 8 --dry-run content/en
  %(prog)s --referenced-only --keep content/en
""",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Directories (or files) to convert. Defaults to content/.",
    )
    parser.add_argument(
        "--dir",
        dest="dirs",
        action="append",
        default=[],
        help="Additional directory to convert. Repeatable.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files.",
    )
    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Apply changes without a confirmation prompt.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=80,
        metavar="N",
        help="cwebp quality 0-100 (default: 80).",
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep the original PNG after a successful conversion.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reconvert even when a .webp file already exists.",
    )
    parser.add_argument(
        "--referenced-only",
        action="store_true",
        help="Convert only PNGs that are referenced by a Markdown file. "
        "Unused PNG and WebP files are still listed in the report.",
    )
    parser.add_argument(
        "--markdown-root",
        default=str(root / "content"),
        help="Root used to discover Markdown references (default: content/).",
    )
    parser.add_argument(
        "--jobs",
        "-j",
        type=int,
        default=os.cpu_count() or 4,
        metavar="N",
        help="Parallel cwebp workers (default: all CPU cores). Use 1 to disable.",
    )
    return parser.parse_args(argv)


def collect_targets(raw_paths: list[str], root: Path) -> list[Path]:
    if not raw_paths:
        raw_paths = ["content"]
    targets: list[Path] = []
    for raw in raw_paths:
        path = Path(raw)
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve()
            if not path.exists():
                fallback = (root / raw).resolve()
                if fallback.exists():
                    path = fallback
        if not path.exists():
            raise SystemExit(f"path not found: {raw}")
        targets.append(path)
    return targets


def find_images(targets: list[Path], suffix: str) -> list[Path]:
    suffix = suffix.lower().lstrip(".")
    found: set[Path] = set()
    for target in targets:
        if target.is_file():
            if target.suffix.lower() == f".{suffix}" and target.stem:
                found.add(target.resolve())
            continue
        for img in target.rglob(f"*.{suffix}"):
            if img.is_file() and img.stem:
                found.add(img.resolve())
        upper = suffix.upper()
        if upper != suffix:
            for img in target.rglob(f"*.{upper}"):
                if img.is_file() and img.stem:
                    found.add(img.resolve())
    return sorted(found)


def discover_markdown(markdown_root: Path, extra: list[Path]) -> list[Path]:
    roots = {markdown_root.resolve()}
    for path in extra:
        roots.add(path.resolve() if path.is_dir() else path.parent.resolve())
    files: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        if root.is_file() and root.suffix.lower() == ".md":
            files.add(root)
            continue
        for md in root.rglob("*.md"):
            if md.is_file():
                files.add(md)
    return sorted(files)


def same_inode(left: Path, right: Path) -> bool:
    try:
        a = left.stat()
        b = right.stat()
    except OSError:
        return False
    return a.st_ino == b.st_ino and a.st_dev == b.st_dev


def lowercase_dest(path: Path) -> Path:
    return path.with_name(path.name.lower())


def needs_lowercase(path: Path) -> bool:
    return bool(path.stem) and path.name != path.name.lower()


def collect_renames(images: list[Path], refs: dict[Path, list[Path]]) -> list[Rename]:
    rows: list[Rename] = []
    for src in images:
        if not needs_lowercase(src):
            continue
        dest = lowercase_dest(src)
        detail = ""
        if dest.exists() and not same_inode(src, dest):
            detail = "lowercase name already exists"
        rows.append(Rename(src=src, dest=dest, markdown=refs.get(src, []), detail=detail))
    return rows


def move_to_lowercase(src: Path, dest: Path) -> None:
    if src.name == dest.name:
        return
    if dest.exists() and not same_inode(src, dest):
        raise RuntimeError(f"lowercase name already exists: {dest.name}")
    tmp = src.with_name(f".{uuid.uuid4().hex}{src.suffix}")
    src.rename(tmp)
    try:
        tmp.rename(dest)
    except OSError:
        tmp.rename(src)
        raise


def remap_path(path: Path, mapping: dict[Path, Path]) -> Path:
    return mapping.get(path, path)


def resolve_png_ref(md_file: Path, ref: str) -> Path | None:
    if ref.startswith(("http://", "https://", "//")):
        return None
    cleaned = ref.split("?", 1)[0]
    path = Path(cleaned)
    if path.is_absolute():
        return path if path.exists() else None

    # File-relative first. Then Hugo leaf-page URL-relative: a page at
    # section/page.md is served as section/page/, so ../images/foo.png
    # means section/images/foo.png, not the parent section's images/.
    relatives = [path]
    lowered = path.with_name(path.name.lower())
    if lowered != path:
        relatives.append(lowered)
    candidates: list[Path] = []
    for relative in relatives:
        candidates.append((md_file.parent / relative).resolve())
        if md_file.name != "_index.md":
            candidates.append((md_file.parent / md_file.stem / relative).resolve())
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def index_references(md_files: list[Path]) -> dict[Path, list[Path]]:
    refs: dict[Path, list[Path]] = defaultdict(list)
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in IMG_REF.finditer(text):
            resolved = resolve_png_ref(md, match.group("path"))
            if resolved is not None:
                refs[resolved].append(md)
    for image, files in refs.items():
        refs[image] = sorted(set(files))
    return refs


def _managed_match(resolved: Path, managed: set[Path]) -> Path | None:
    for path in managed:
        if resolved == path or same_inode(resolved, path):
            return path
    return None


def _replace_filename(path: str, new_name: str) -> str:
    old_name = Path(path).name
    if path.endswith(old_name):
        return path[: -len(old_name)] + new_name
    return path


def rewrite_markdown(
    md_file: Path,
    converted: set[Path],
    renamed: set[Path],
    dry_run: bool,
) -> bool:
    try:
        text = md_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False

    def replace(match: re.Match[str]) -> str:
        path = match.group("path")
        resolved = resolve_png_ref(md_file, path)
        if resolved is None:
            return match.group(0)
        will_webp = _managed_match(resolved, converted) is not None
        if not will_webp and _managed_match(resolved, renamed) is None:
            return match.group(0)
        new_name = Path(path).name.lower()
        if will_webp:
            new_name = re.sub(r"\.png$", ".webp", new_name, flags=re.IGNORECASE)
        if Path(path).name == new_name:
            return match.group(0)
        return _replace_filename(path, new_name) + (match.group("query") or "")

    new_text = IMG_REF.sub(replace, text)
    if new_text == text:
        return False
    if not dry_run:
        md_file.write_text(new_text, encoding="utf-8")
    return True


def convert_png(cwebp: str, src: Path, dest: Path, quality: int) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [cwebp, "-q", str(quality), "-m", "6", "-quiet", str(src), "-o", str(dest)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not dest.exists() or dest.stat().st_size == 0:
        if dest.exists():
            dest.unlink()
        err = (result.stderr or result.stdout or "cwebp failed").strip()
        raise RuntimeError(err)
    return dest.stat().st_size


def convert_one(cwebp: str, src: str, dest: str, quality: int) -> tuple[str, int, str]:
    """Worker for the thread pool. cwebp releases the GIL via subprocess."""
    try:
        size = convert_png(cwebp, Path(src), Path(dest), quality)
        return "converted", size, ""
    except RuntimeError as exc:
        return "failed", 0, str(exc)


def rel_to_repo(path: Path) -> Path:
    try:
        return path.relative_to(repo_root())
    except ValueError:
        return path


def confirm(convert_count: int, rename_count: int) -> bool:
    if not sys.stdin.isatty():
        raise SystemExit("refusing to apply without a TTY; pass --yes or --dry-run")
    parts: list[str] = []
    if convert_count:
        parts.append(f"convert {convert_count} PNG file(s)")
    if rename_count:
        parts.append(f"lowercase {rename_count} image name(s)")
    if not parts:
        return True
    label = " and ".join(parts)
    answer = input(f"{label[0].upper()}{label[1:]}? [y/N] ").strip().lower()
    return answer in {"y", "yes"}


def _print_unused(title: str, unused: list[Path]) -> int:
    unused_bytes = 0
    print()
    print(color(title, "1"))
    if not unused:
        print("  none")
        return 0
    for image in unused:
        size = image.stat().st_size if image.exists() else 0
        unused_bytes += size
        print(color("  unused     ", "33") + f"{rel_to_repo(image)}  {human(size)}")
    return unused_bytes


def print_report(
    rows: list[Conversion],
    unused: list[Path],
    unused_webp: list[Path],
    renames: list[Rename],
    dry_run: bool,
    keep: bool,
    jobs: int,
) -> None:
    converted = [r for r in rows if r.status == "converted"]
    skipped = [r for r in rows if r.status == "skipped"]
    failed = [r for r in rows if r.status == "failed"]
    renamed = [r for r in renames if r.status == "renamed"]
    updated_md: set[Path] = set()
    for row in converted:
        updated_md.update(row.markdown)
    for row in renamed:
        updated_md.update(row.markdown)

    if rows:
        print()
        print(color("Files", "1"))
        for row in rows:
            rel_png = rel_to_repo(row.png)
            if row.status == "converted":
                saved = row.png_bytes - row.webp_bytes
                rel_webp = rel_to_repo(row.webp)
                print(
                    color("  converted  ", "32")
                    + f"{rel_png} -> {rel_webp}  "
                    f"{human(row.png_bytes)} -> {human(row.webp_bytes)}  "
                    f"(saved {human(saved)})"
                )
                for md in row.markdown:
                    print(color("    updated   ", "36") + str(rel_to_repo(md)))
                if not row.markdown:
                    print(color("    note      ", "33") + "no Markdown references found")
            elif row.status == "skipped":
                print(color("  skipped    ", "33") + f"{rel_png}  {row.detail}")
            else:
                print(color("  failed     ", "31") + f"{rel_png}  {row.detail}")

    converted_keys = {(row.png.parent.resolve(), row.png.stem.lower()) for row in converted}
    case_only = [
        row
        for row in renames
        if (row.src.parent.resolve(), row.src.stem.lower()) not in converted_keys
    ]

    print()
    print(color("Lowercased", "1"))
    if not case_only:
        print("  none")
    else:
        for row in case_only:
            rel_src = rel_to_repo(row.src)
            rel_dest = rel_to_repo(row.dest)
            if row.status == "renamed":
                print(color("  renamed    ", "32") + f"{rel_src} -> {rel_dest}")
                for md in row.markdown:
                    print(color("    updated   ", "36") + str(rel_to_repo(md)))
                if not row.markdown:
                    print(color("    note      ", "33") + "no Markdown references found")
            else:
                print(color("  failed     ", "31") + f"{rel_src}  {row.detail}")

    unused_bytes = _print_unused("Unused PNGs", unused)
    unused_webp_bytes = _print_unused("Unused WebPs", unused_webp)

    png_total = sum(r.png_bytes for r in converted)
    webp_total = sum(r.webp_bytes for r in converted)
    saved = png_total - webp_total
    pct = (saved / png_total * 100) if png_total else 0

    print()
    print(color("Summary", "1"))
    mode = "dry-run" if dry_run else "applied"
    print(f"  mode:            {mode}")
    print(f"  workers:         {jobs}")
    print(f"  converted:       {len(converted)}")
    print(f"  skipped:         {len(skipped)}")
    print(f"  failed:          {len(failed)}")
    print(f"  unused pngs:     {len(unused)} ({human(unused_bytes)})")
    print(f"  unused webps:    {len(unused_webp)} ({human(unused_webp_bytes)})")
    print(f"  lowercased:      {len([r for r in case_only if r.status == 'renamed'])}")
    print(f"  markdown files:  {len(updated_md)}")
    if not keep and not dry_run:
        print(f"  pngs removed:    {len(converted)}")
    elif dry_run and not keep:
        print(f"  pngs to remove:  {len(converted)}")
    print(f"  before:          {human(png_total)}")
    print(f"  after:           {human(webp_total)}")
    print(f"  saved:           {human(saved)} ({pct:.1f}%)")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not 0 <= args.quality <= 100:
        raise SystemExit("--quality must be between 0 and 100")
    if args.jobs < 1:
        raise SystemExit("--jobs must be at least 1")

    cwebp = require_cwebp()
    root = repo_root()
    targets = collect_targets(args.paths + args.dirs, root)
    found_pngs = find_images(targets, "png")
    found_webps = find_images(targets, "webp")
    md_files = discover_markdown(Path(args.markdown_root), targets)
    refs = index_references(md_files)
    unused = [png for png in found_pngs if png not in refs]
    unused_webp = [webp for webp in found_webps if webp not in refs]
    pngs = [png for png in found_pngs if png in refs] if args.referenced_only else found_pngs
    renames = collect_renames([*found_pngs, *found_webps], refs)
    pending_renames = [row for row in renames if not row.detail]

    if not pngs and not unused and not unused_webp and not found_webps and not renames:
        print("No PNG or WebP files found.")
        return 0

    apply = not args.dry_run
    if apply and not args.yes and not confirm(len(pngs), len(pending_renames)):
        print("Aborted.")
        return 1

    rename_map: dict[Path, Path] = {}
    for row in renames:
        if row.detail:
            row.status = "failed"
            continue
        if apply:
            try:
                move_to_lowercase(row.src, row.dest)
                row.status = "renamed"
                rename_map[row.src] = row.dest
            except OSError as exc:
                row.status = "failed"
                row.detail = str(exc)
        else:
            row.status = "renamed"

    if apply and rename_map:
        found_pngs = [remap_path(path, rename_map) for path in found_pngs]
        found_webps = [remap_path(path, rename_map) for path in found_webps]
        pngs = [remap_path(path, rename_map) for path in pngs]
        unused = [remap_path(path, rename_map) for path in unused]
        unused_webp = [remap_path(path, rename_map) for path in unused_webp]
        refs = {remap_path(path, rename_map): files for path, files in refs.items()}

    rows: list[Conversion] = []
    converted_paths: set[Path] = set()
    pending: list[tuple[int, Path]] = []
    tmp_dir: tempfile.TemporaryDirectory[str] | None = None
    workers = args.jobs

    if pngs:
        for png in pngs:
            dest = lowercase_dest(png).with_suffix(".webp")
            rows.append(
                Conversion(
                    png=png,
                    webp=dest,
                    png_bytes=png.stat().st_size,
                    markdown=refs.get(png, []),
                )
            )
        if args.dry_run:
            tmp_dir = tempfile.TemporaryDirectory(prefix="png-to-webp-")
        for index, row in enumerate(rows):
            if row.webp.exists() and not args.force:
                row.status = "skipped"
                row.detail = "webp already exists (use --force to reconvert)"
                row.webp_bytes = row.webp.stat().st_size
                continue
            dest = row.webp
            if tmp_dir is not None:
                dest = Path(tmp_dir.name) / f"{index}-{row.png.stem}.webp"
            pending.append((index, dest))
        workers = min(args.jobs, max(1, len(pending))) if pending else args.jobs
    elif not pending_renames:
        print("No PNG files to convert.")
        print_report(
            [], unused, unused_webp, renames, args.dry_run, args.keep, args.jobs
        )
        return 0
    else:
        print("No PNG files to convert.")

    if pending:
        print(f"Converting {len(pending)} PNG file(s) with {workers} worker(s)...")
        spinner = itertools.cycle("|/-\\")
        done = 0
        label = "starting…"
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(convert_one, cwebp, str(rows[index].png), str(dest), args.quality): index
                for index, dest in pending
            }
            outstanding = set(futures)
            draw_progress(done, len(pending), label)
            while outstanding:
                finished, outstanding = wait(
                    outstanding, timeout=0.1, return_when=FIRST_COMPLETED
                )
                if not finished:
                    draw_progress(done, len(pending), label, next(spinner))
                    continue
                for future in finished:
                    index = futures[future]
                    status, size, detail = future.result()
                    rows[index].status = status
                    rows[index].webp_bytes = size
                    rows[index].detail = detail
                    if status == "converted":
                        converted_paths.add(rows[index].png)
                    done += 1
                    label = rows[index].png.name
                    draw_progress(done, len(pending), label, next(spinner))
        clear_progress()

    if tmp_dir is not None:
        tmp_dir.cleanup()

    renamed_paths = {row.src for row in renames if row.status == "renamed"}
    renamed_paths.update(row.dest for row in renames if row.status == "renamed")
    for md in md_files:
        rewrite_markdown(md, converted_paths, renamed_paths, args.dry_run)

    for row in rows:
        if row.status == "converted":
            row.markdown = refs.get(row.png, [])

    if apply and not args.keep:
        for row in rows:
            if row.status == "converted" and row.png.exists():
                row.png.unlink()

    print_report(
        rows,
        unused,
        unused_webp,
        renames,
        args.dry_run,
        args.keep,
        workers if pending else args.jobs,
    )
    return 1 if any(row.status == "failed" for row in rows) or any(
        row.status == "failed" for row in renames
    ) else 0


if __name__ == "__main__":
    raise SystemExit(main())
