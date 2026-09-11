#!/usr/bin/env python3
"""Convert PNG workshop assets to WebP and rewrite Markdown references.

Default scan root is content/. Pass one or more directories to limit which
PNGs are converted. Markdown updates still search the whole content tree so
a scoped conversion cannot leave stale links elsewhere.

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
from collections import defaultdict
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from pathlib import Path

PNG_REF = re.compile(
    r"(?P<path>(?:https?://[^\s)\"']+|(?:\.{1,2}/|/?[\w@.-])[\w./@-]*)\.png)"
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
        "Unused PNGs are still listed in the report.",
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


def find_pngs(targets: list[Path]) -> list[Path]:
    found: set[Path] = set()
    for target in targets:
        if target.is_file():
            if target.suffix.lower() == ".png":
                found.add(target.resolve())
            continue
        for png in target.rglob("*.png"):
            if png.is_file() and png.stem:
                found.add(png.resolve())
        for png in target.rglob("*.PNG"):
            if png.is_file() and png.stem:
                found.add(png.resolve())
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
    candidates = [(md_file.parent / path).resolve()]
    if md_file.name != "_index.md":
        candidates.append((md_file.parent / md_file.stem / path).resolve())
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
        for match in PNG_REF.finditer(text):
            resolved = resolve_png_ref(md, match.group("path"))
            if resolved is not None:
                refs[resolved].append(md)
    for png, files in refs.items():
        refs[png] = sorted(set(files))
    return refs


def rewrite_markdown(md_file: Path, converted: set[Path], dry_run: bool) -> bool:
    try:
        text = md_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False

    def replace(match: re.Match[str]) -> str:
        resolved = resolve_png_ref(md_file, match.group("path"))
        if resolved is None or resolved not in converted:
            return match.group(0)
        path = match.group("path")
        updated = re.sub(r"\.png$", ".webp", path, flags=re.IGNORECASE)
        return updated + (match.group("query") or "")

    new_text = PNG_REF.sub(replace, text)
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


def confirm(count: int) -> bool:
    if not sys.stdin.isatty():
        raise SystemExit("refusing to apply without a TTY; pass --yes or --dry-run")
    answer = input(f"Convert {count} PNG file(s)? [y/N] ").strip().lower()
    return answer in {"y", "yes"}


def print_report(
    rows: list[Conversion],
    unused: list[Path],
    dry_run: bool,
    keep: bool,
    jobs: int,
) -> None:
    converted = [r for r in rows if r.status == "converted"]
    skipped = [r for r in rows if r.status == "skipped"]
    failed = [r for r in rows if r.status == "failed"]
    updated_md: set[Path] = set()
    for row in converted:
        updated_md.update(row.markdown)

    if rows:
        print()
        print(color("Files", "1"))
        for row in rows:
            rel_png = rel_to_repo(row.png)
            if row.status == "converted":
                saved = row.png_bytes - row.webp_bytes
                print(
                    color("  converted  ", "32")
                    + f"{rel_png}  {human(row.png_bytes)} -> {human(row.webp_bytes)}  "
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

    unused_bytes = 0
    print()
    print(color("Unused PNGs", "1"))
    if not unused:
        print("  none")
    else:
        for png in unused:
            size = png.stat().st_size if png.exists() else 0
            unused_bytes += size
            print(color("  unused     ", "33") + f"{rel_to_repo(png)}  {human(size)}")

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
    found_pngs = find_pngs(targets)
    md_files = discover_markdown(Path(args.markdown_root), targets)
    refs = index_references(md_files)
    unused = [png for png in found_pngs if png not in refs]
    pngs = [png for png in found_pngs if png in refs] if args.referenced_only else found_pngs

    if not pngs and not unused:
        print("No PNG files found.")
        return 0

    if not pngs:
        print("No PNG files to convert.")
        print_report([], unused, args.dry_run, args.keep, args.jobs)
        return 0

    rows: list[Conversion] = []
    for png in pngs:
        rows.append(
            Conversion(
                png=png,
                webp=png.with_suffix(".webp"),
                png_bytes=png.stat().st_size,
                markdown=refs.get(png, []),
            )
        )

    apply = not args.dry_run
    if apply and not args.yes and not confirm(len(rows)):
        print("Aborted.")
        return 1

    converted_paths: set[Path] = set()
    pending: list[tuple[int, Path]] = []
    tmp_dir: tempfile.TemporaryDirectory[str] | None = None
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

    workers = min(args.jobs, max(1, len(pending)))
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

    for md in md_files:
        rewrite_markdown(md, converted_paths, args.dry_run)

    for row in rows:
        if row.status == "converted":
            row.markdown = refs.get(row.png, [])

    if apply and not args.keep:
        for row in rows:
            if row.status == "converted" and row.png.exists():
                row.png.unlink()

    print_report(rows, unused, args.dry_run, args.keep, workers if pending else args.jobs)
    return 1 if any(row.status == "failed" for row in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
