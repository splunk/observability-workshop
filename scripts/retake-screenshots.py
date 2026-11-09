#!/usr/bin/env python3
"""Workshop screenshot helper.

No arguments: numbered menu in the terminal (pick a module, walk pictures).
With a command: the older one-shot CLI. See scripts/screenshots/README.md.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
DEFAULT_SECTION = (
    "content/en/splunk4rookies/o11y-rookies-26/modules/1-intro"
)
FRONT_MATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.DOTALL)
WEIGHT = re.compile(r"^weight:\s*(\d+)\s*$", re.MULTILINE)
TITLE = re.compile(r"^title:\s*[\"']?(.*?)[\"']?\s*$", re.MULTILINE)
ROOKIES_MODULES = (
    "content/en/splunk4rookies/o11y-rookies-26/modules"
)
ALT_MD_BEFORE = re.compile(r"!\[([^\]]*)\]\(\s*$")
ALT_HTML = re.compile(r"alt=[\"']([^\"']*)[\"']", re.IGNORECASE)
NUM_STEM = re.compile(r"^(?:shot[-_])?0*(\d+)(?:[-_.].+)?$", re.IGNORECASE)
MANIFEST_VERSION = 1


def load_png_to_webp():
    path = Path(__file__).resolve().parent / "png-to-webp.py"
    spec = importlib.util.spec_from_file_location("png_to_webp", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


p2w = load_png_to_webp()


@dataclass
class Shot:
    number: int
    image: Path
    markdown: Path
    alt: str
    extra_pages: list[Path] = field(default_factory=list)

    @property
    def stem(self) -> str:
        return self.image.stem.lower()

    @property
    def save_as(self) -> str:
        return f"{self.number:02d}-{self.stem}.png"


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_inbox() -> Path:
    return repo_root() / "scripts" / "screenshots" / "inbox"


def default_backup() -> Path:
    return repo_root() / "scripts" / "screenshots" / "backup"


def rel(path: Path) -> Path:
    try:
        return path.relative_to(repo_root())
    except ValueError:
        return path


def front_matter(text: str) -> str:
    match = FRONT_MATTER.match(text)
    return match.group(1) if match else ""


def page_weight(text: str) -> int:
    match = WEIGHT.search(front_matter(text))
    return int(match.group(1)) if match else 999


def hugo_url(md: Path) -> str:
    try:
        rel_md = md.resolve().relative_to((repo_root() / "content").resolve())
    except ValueError:
        rel_md = rel(md)
    parts = list(rel_md.parts)
    if parts[-1] == "_index.md":
        parts = parts[:-1]
    else:
        parts[-1] = Path(parts[-1]).stem
    return "/" + "/".join(parts) + "/"


def sort_key(md: Path, text: str) -> tuple:
    rel_md = rel(md)
    parent = str(rel_md.parent)
    is_index = 0 if md.name == "_index.md" else 1
    return (parent, is_index, page_weight(text), md.name.lower())


def alt_near(text: str, start: int) -> str:
    before = text[max(0, start - 120) : start]
    md = ALT_MD_BEFORE.search(before)
    if md and md.group(1).strip():
        return md.group(1).strip()
    tag_start = text.rfind("<img", 0, start)
    if tag_start != -1:
        tag = text[tag_start : start + 80]
        html = ALT_HTML.search(tag)
        if html and html.group(1).strip():
            return html.group(1).strip()
    return ""


def resolve_ref(md_file: Path, ref: str) -> Path | None:
    found = p2w.resolve_png_ref(md_file, ref)
    if found is not None:
        return found
    if ref.startswith(("http://", "https://", "//")):
        return None
    cleaned = ref.split("?", 1)[0]
    path = Path(cleaned)
    if path.is_absolute():
        return path
    file_rel = (md_file.parent / path).resolve()
    if md_file.name == "_index.md":
        return file_rel
    # Leaf pages are served as section/page/, so ../images/foo.png means
    # section/images/foo.png. Use that when the original has been stashed.
    return (md_file.parent / md_file.stem / path).resolve()


def discover_shots(section: Path) -> list[Shot]:
    md_files = sorted(section.rglob("*.md"))
    loaded: list[tuple[Path, str]] = []
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        loaded.append((md, text))
    loaded.sort(key=lambda item: sort_key(item[0], item[1]))

    by_image: dict[Path, Shot] = {}
    order: list[Path] = []
    for md, text in loaded:
        for match in p2w.IMG_REF.finditer(text):
            resolved = resolve_ref(md, match.group("path"))
            if resolved is None:
                continue
            try:
                resolved.relative_to(section.resolve())
            except ValueError:
                continue
            if resolved.suffix.lower() not in IMG_EXTS:
                continue
            if resolved in by_image:
                extra = by_image[resolved]
                if md not in extra.extra_pages and md != extra.markdown:
                    extra.extra_pages.append(md)
                continue
            shot = Shot(
                number=0,
                image=resolved,
                markdown=md,
                alt=alt_near(text, match.start()),
            )
            by_image[resolved] = shot
            order.append(resolved)

    shots = []
    for index, image in enumerate(order, start=1):
        shot = by_image[image]
        shot.number = index
        shots.append(shot)
    return shots


class Manifest:
    def __init__(self, backup_dir: Path) -> None:
        self.backup_dir = backup_dir
        self.path = backup_dir / "manifest.json"
        self.data: dict[str, Any] = {"version": MANIFEST_VERSION, "shots": {}}
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(loaded, dict) and isinstance(loaded.get("shots"), dict):
                    self.data = loaded
            except json.JSONDecodeError:
                pass

    def get(self, number: int) -> dict[str, Any] | None:
        entry = self.data.get("shots", {}).get(str(number))
        return entry if isinstance(entry, dict) else None

    def put(self, number: int, entry: dict[str, Any]) -> None:
        self.data.setdefault("shots", {})[str(number)] = entry
        self.save()

    def save(self) -> None:
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2) + "\n", encoding="utf-8")

    def backup_file(self, shot: Shot) -> Path:
        return self.backup_dir / f"{shot.number:02d}-{shot.image.name.lower()}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Workshop screenshot helper. Run with no arguments for the menu.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  %(prog)s                   # menu: pick module, walk pictures
  %(prog)s list
  %(prog)s start 03
""",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=("list", "start", "next", "open", "keep", "skip", "ingest", "watch", "restore"),
        help="Optional. Omit this to open the numbered terminal menu.",
    )
    parser.add_argument(
        "shot",
        nargs="?",
        help="Shot number. keep/skip default to the currently stashed shot.",
    )
    parser.add_argument(
        "--section",
        default=DEFAULT_SECTION,
        help="Workshop section to retake (default: o11y-rookies-26 intro).",
    )
    parser.add_argument(
        "--inbox",
        default=str(default_inbox()),
        help="Folder Shottr/Monosnap should save into.",
    )
    parser.add_argument(
        "--backup",
        default=str(default_backup()),
        help="Where originals are moved while you recapture.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=85,
        metavar="N",
        help="cwebp quality passed to png-to-webp.py (default: 85).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show ingest matches without copying or converting.",
    )
    parser.add_argument(
        "--remaining",
        action="store_true",
        help="With list: hide shots that are already WebP.",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not open Preview (useful for scripts).",
    )
    parser.add_argument(
        "--poll",
        type=float,
        default=1.5,
        metavar="SEC",
        help="watch: seconds between inbox scans (default: 1.5).",
    )
    return parser.parse_args(argv)


def resolve_section(raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
        if not path.exists():
            fallback = (repo_root() / raw).resolve()
            if fallback.exists():
                path = fallback
    if not path.is_dir():
        raise SystemExit(f"section not found: {raw}")
    return path


FINISHED = {"webp", "skip", "keep"}


def shot_state(shot: Shot, manifest: Manifest) -> str:
    entry = manifest.get(shot.number)
    status = (entry or {}).get("status")
    if status == "skipped":
        return "skip"
    if status == "kept":
        return "keep"
    if status == "done":
        return "webp"
    if shot.image.exists():
        return shot.image.suffix.lower().lstrip(".")
    if entry:
        return "stash"
    return "miss"


def print_list(shots: list[Shot], manifest: Manifest, remaining: bool) -> None:
    rows = []
    for shot in shots:
        state = shot_state(shot, manifest)
        if remaining and state in FINISHED:
            continue
        rows.append((shot, state))
    if not rows:
        print("All shots in this section are already WebP.")
        return
    print(f"{'#':<4} {'st':<6} {'save as':<36} {'page'}")
    print("-" * 92)
    for shot, state in rows:
        print(f"{shot.number:02d}   {state:<6} {shot.save_as:<36} {rel(shot.markdown)}")
        if shot.alt:
            print(f"       {shot.alt}")
    still = sum(1 for s in shots if shot_state(s, manifest) not in FINISHED)
    print()
    print(f"{len(shots)} shots, {still} still open.")
    print("next      →  stash original, open it as reference")
    print("keep      →  original is fine: convert to WebP, no recapture")
    print("skip      →  leave PNG, don't retake now")
    print("save      →  Shottr/Monosnap PNG into the inbox as NN-name.png")
    print("ingest    →  new capture → WebP + rewrite Markdown   (or: watch)")


def find_shot(shots: list[Shot], token: str) -> Shot:
    token = token.strip()
    if token.isdigit():
        number = int(token)
        for shot in shots:
            if shot.number == number:
                return shot
        raise SystemExit(f"no shot {token:0>2}")
    lowered = token.lower().removesuffix(".png").removesuffix(".webp")
    matches = [s for s in shots if s.stem == lowered or s.save_as.startswith(lowered)]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise SystemExit(f"no shot matching {token!r}")
    raise SystemExit(
        "ambiguous name "
        + token
        + "; use the number: "
        + ", ".join(f"{s.number:02d}" for s in matches)
    )


def copy_filename(name: str) -> None:
    pbcopy = shutil.which("pbcopy")
    if not pbcopy:
        return
    subprocess.run([pbcopy], input=name, text=True, check=False)


def open_preview(path: Path) -> None:
    subprocess.run(["open", "-a", "Preview", str(path)], check=False)


def print_shot_banner(shot: Shot, backup: Path, inbox: Path, state: str) -> None:
    print(f"shot   {shot.number:02d}  {state}")
    print(f"page   {rel(shot.markdown)}")
    print(f"hugo   {hugo_url(shot.markdown)}")
    if shot.alt:
        print(f"show   {shot.alt}")
    print(f"old    {rel(backup) if backup.exists() else '(no backup yet)'}")
    print(f"dest   {rel(shot.image)}")
    print(f"save   {shot.save_as}")
    print(f"inbox  {rel(inbox)}")
    print()
    print("1. Original is in Preview — that is the reference.")
    print("2. Recapture in Shottr/Monosnap, add arrows/notes.")
    print(f"3. Save PNG as {shot.save_as} into the inbox.")
    print("4. ingest or watch converts to WebP and rewrites Markdown.")


def stash_original(shot: Shot, manifest: Manifest) -> Path:
    backup = manifest.backup_file(shot)
    backup.parent.mkdir(parents=True, exist_ok=True)
    if shot.image.exists():
        if backup.exists():
            backup.unlink()
        shutil.move(str(shot.image), str(backup))
        status = "stashed"
    elif backup.exists():
        status = "stashed"
    else:
        raise SystemExit(f"shot {shot.number:02d}: nothing to stash at {rel(shot.image)}")
    manifest.put(
        shot.number,
        {
            "number": shot.number,
            "original": str(rel(shot.image)),
            "backup": str(rel(backup)),
            "markdown": str(rel(shot.markdown)),
            "status": status,
            "stashed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    )
    return backup


def cmd_start(
    shot: Shot,
    manifest: Manifest,
    inbox: Path,
    no_open: bool,
) -> int:
    inbox.mkdir(parents=True, exist_ok=True)
    backup = stash_original(shot, manifest)
    copy_filename(shot.save_as)
    print_shot_banner(shot, backup, inbox, "stashed")
    print(f"(filename {shot.save_as} copied to clipboard)")
    if not no_open:
        open_preview(backup)
    return 0


def cmd_next(shots: list[Shot], manifest: Manifest, inbox: Path, no_open: bool) -> int:
    stashed = [s for s in shots if shot_state(s, manifest) == "stash"]
    if stashed:
        shot = stashed[0]
        backup = manifest.backup_file(shot)
        copy_filename(shot.save_as)
        print("already stashed — recapture, or: keep  |  skip  |  restore NN")
        print_shot_banner(shot, backup, inbox, "stash")
        if not no_open and backup.exists():
            open_preview(backup)
        return 0
    for shot in shots:
        if shot_state(shot, manifest) not in FINISHED:
            return cmd_start(shot, manifest, inbox, no_open)
    print("Nothing left to retake in this section.")
    return 0


def current_shot(shots: list[Shot], manifest: Manifest, token: str | None) -> Shot:
    if token:
        return find_shot(shots, token)
    stashed = [s for s in shots if shot_state(s, manifest) == "stash"]
    if len(stashed) == 1:
        return stashed[0]
    if len(stashed) > 1:
        raise SystemExit(
            "several shots are stashed; pass a number: "
            + ", ".join(f"{s.number:02d}" for s in stashed)
        )
    raise SystemExit("no stashed shot — pass a number, e.g. keep 03")


def put_backup_back(shot: Shot, manifest: Manifest) -> Path:
    entry = manifest.get(shot.number) or {}
    backup = manifest.backup_file(shot)
    if entry.get("backup"):
        listed = repo_root() / entry["backup"]
        if listed.exists():
            backup = listed
    if not backup.exists():
        if shot.image.exists():
            return shot.image
        raise SystemExit(f"shot {shot.number:02d}: no backup and dest is missing")
    dest = shot.image.with_name(backup.name.split("-", 1)[-1])
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.resolve() != backup.resolve():
        dest.unlink()
    shutil.copy2(backup, dest)
    return dest


def cmd_keep(
    shot: Shot,
    shots: list[Shot],
    manifest: Manifest,
    inbox: Path,
    quality: int,
    no_open: bool,
) -> int:
    """Keep the original pixels: convert to WebP, no recapture, then next."""
    dest = put_backup_back(shot, manifest)
    if dest.suffix.lower() == ".webp":
        mark_done(shot, manifest, dest)
        entry = manifest.get(shot.number) or {}
        entry["status"] = "kept"
        manifest.put(shot.number, entry)
        print(f"kept    {shot.number:02d} already WebP  {rel(dest)}")
        return cmd_next(shots, manifest, inbox, no_open)
    png = dest if dest.suffix.lower() == ".png" else dest.with_name(dest.stem.lower() + ".png")
    if dest.suffix.lower() != ".png":
        to_png(dest, png)
    code = convert_png(png, quality)
    if code != 0:
        raise SystemExit(f"png-to-webp failed for {png.name} (exit {code})")
    webp = png.with_suffix(".webp")
    mark_done(shot, manifest, webp)
    entry = manifest.get(shot.number) or {}
    entry["status"] = "kept"
    manifest.put(shot.number, entry)
    print(f"kept    {shot.number:02d} → {rel(webp)}  (original pixels, no recapture)")
    return cmd_next(shots, manifest, inbox, no_open)


def cmd_skip(
    shot: Shot,
    shots: list[Shot],
    manifest: Manifest,
    inbox: Path,
    no_open: bool,
) -> int:
    """Leave this file as it is. next will not stop on it again."""
    dest = put_backup_back(shot, manifest)
    entry = manifest.get(shot.number) or {}
    entry.update(
        {
            "number": shot.number,
            "original": str(rel(dest)),
            "markdown": str(rel(shot.markdown)),
            "status": "skipped",
            "skipped_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    )
    if "backup" not in entry:
        entry["backup"] = str(rel(manifest.backup_file(shot)))
    manifest.put(shot.number, entry)
    print(f"skipped {shot.number:02d}  left {rel(dest)}  (`keep {shot.number:02d}` later to WebP it)")
    return cmd_next(shots, manifest, inbox, no_open)


def cmd_open(shot: Shot, manifest: Manifest, inbox: Path, no_open: bool) -> int:
    backup = manifest.backup_file(shot)
    reference = backup if backup.exists() else shot.image
    state = shot_state(shot, manifest)
    print_shot_banner(shot, backup, inbox, state)
    if not reference.exists():
        print("no file to show — start NN to stash the original first")
        return 1
    if not no_open:
        open_preview(reference)
    return 0


def inbox_files(inbox: Path) -> list[Path]:
    if not inbox.is_dir():
        return []
    files = []
    for path in inbox.iterdir():
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.suffix.lower() in IMG_EXTS:
            files.append(path)
    return sorted(files)


def match_inbox_file(path: Path, shots: list[Shot], forced: Shot | None) -> Shot | None:
    if forced is not None:
        return forced
    numbered = NUM_STEM.match(path.stem)
    if numbered:
        number = int(numbered.group(1))
        for shot in shots:
            if shot.number == number:
                return shot
        return None
    lowered = path.stem.lower()
    matches = [s for s in shots if s.stem == lowered]
    if len(matches) == 1:
        return matches[0]
    return None


def to_png(src: Path, dest_png: Path) -> None:
    dest_png.parent.mkdir(parents=True, exist_ok=True)
    suffix = src.suffix.lower()
    if suffix == ".png":
        shutil.copy2(src, dest_png)
        return
    if suffix not in {".jpg", ".jpeg", ".webp"}:
        raise RuntimeError(f"unsupported capture type: {src.suffix}")
    sips = shutil.which("sips")
    if not sips:
        raise RuntimeError("sips is required to convert this capture to PNG")
    result = subprocess.run(
        [sips, "-s", "format", "png", str(src), "--out", str(dest_png)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not dest_png.exists():
        raise RuntimeError((result.stderr or result.stdout or "sips failed").strip())


def convert_png(png: Path, quality: int) -> int:
    cmd = [
        sys.executable,
        str(Path(__file__).resolve().parent / "png-to-webp.py"),
        "--quality",
        str(quality),
        "--force",
        "--yes",
        str(png),
    ]
    env = os.environ.copy()
    env.setdefault("NO_PROGRESS", "1")
    return subprocess.run(cmd, check=False, env=env).returncode


def mark_done(shot: Shot, manifest: Manifest, webp: Path) -> None:
    entry = manifest.get(shot.number) or {}
    entry.update(
        {
            "number": shot.number,
            "original": str(rel(webp)),
            "markdown": str(rel(shot.markdown)),
            "status": "done",
            "done_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    )
    if "backup" not in entry:
        entry["backup"] = str(rel(manifest.backup_file(shot)))
    manifest.put(shot.number, entry)


def ingest_one(
    src: Path,
    shot: Shot,
    manifest: Manifest,
    quality: int,
    dry_run: bool,
) -> str:
    dest_png = shot.image.with_name(shot.image.stem.lower() + ".png")
    webp = dest_png.with_suffix(".webp")
    if dry_run:
        return f"would place {src.name} -> {rel(webp)}"
    to_png(src, dest_png)
    code = convert_png(dest_png, quality)
    if code != 0:
        raise RuntimeError(f"png-to-webp failed for {dest_png.name} (exit {code})")
    src.unlink()
    mark_done(shot, manifest, webp)
    return f"{src.name} -> {rel(webp)}"


def cmd_ingest(
    shots: list[Shot],
    manifest: Manifest,
    inbox: Path,
    quality: int,
    dry_run: bool,
    forced_token: str | None,
) -> int:
    files = inbox_files(inbox)
    if not files:
        print(f"inbox is empty: {rel(inbox)}")
        print("Save Shottr/Monosnap captures as 01-name.png")
        return 0
    forced = find_shot(shots, forced_token) if forced_token else None
    if forced is not None and len(files) != 1:
        raise SystemExit("pass a shot number only when the inbox has exactly one capture")

    matched: list[tuple[Path, Shot]] = []
    unmatched: list[Path] = []
    used: set[int] = set()
    for path in files:
        shot = match_inbox_file(path, shots, forced)
        if shot is None or shot.number in used:
            unmatched.append(path)
            continue
        used.add(shot.number)
        matched.append((path, shot))

    if not matched and unmatched:
        print("Could not match inbox files to shots. Rename them to NN-name.png:")
        for path in unmatched:
            print(f"  {path.name}")
        return 1

    failures = 0
    for path, shot in matched:
        try:
            result = ingest_one(path, shot, manifest, quality, dry_run)
            print(("dry-run  " if dry_run else "ingested ") + result)
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"failed   {path.name} ({shot.save_as}): {exc}")
    for path in unmatched:
        print(f"skipped  {path.name}  (rename to NN-name.png from list)")
    return 1 if failures or unmatched else 0


def file_stable(path: Path, settle: float) -> bool:
    try:
        first = path.stat()
        time.sleep(settle)
        second = path.stat()
    except OSError:
        return False
    return first.st_size == second.st_size and first.st_mtime == second.st_mtime and first.st_size > 0


def cmd_watch(
    shots: list[Shot],
    manifest: Manifest,
    inbox: Path,
    quality: int,
    poll: float,
) -> int:
    inbox.mkdir(parents=True, exist_ok=True)
    print(f"Watching {rel(inbox)}")
    print("Save Shottr/Monosnap captures as NN-name.png (Ctrl+C to stop)")
    seen: set[str] = set()
    try:
        while True:
            for path in inbox_files(inbox):
                key = f"{path.name}:{path.stat().st_mtime_ns}:{path.stat().st_size}"
                if key in seen:
                    continue
                if not file_stable(path, min(0.8, poll)):
                    continue
                seen.add(key)
                shot = match_inbox_file(path, shots, None)
                if shot is None:
                    print(f"waiting  {path.name}  (rename to NN-name.png)")
                    continue
                try:
                    result = ingest_one(path, shot, manifest, quality, dry_run=False)
                    print("ingested " + result)
                except Exception as exc:  # noqa: BLE001
                    print(f"failed   {path.name}: {exc}")
            time.sleep(poll)
    except KeyboardInterrupt:
        print("\nstopped")
        return 0


def rewrite_name(md: Path, old: str, new: str) -> bool:
    try:
        text = md.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    if old not in text:
        return False
    md.write_text(text.replace(old, new), encoding="utf-8")
    return True


def cmd_restore(shot: Shot, manifest: Manifest) -> int:
    entry = manifest.get(shot.number) or {}
    backup = manifest.backup_file(shot)
    if entry.get("backup"):
        listed = repo_root() / entry["backup"]
        if listed.exists():
            backup = listed
    if not backup.exists():
        raise SystemExit(f"no backup for shot {shot.number:02d} at {rel(backup)}")

    original_name = backup.name.split("-", 1)[-1]
    if entry.get("original"):
        dest = (repo_root() / entry["original"]).parent / original_name
    else:
        dest = shot.image.parent / original_name
    dest.parent.mkdir(parents=True, exist_ok=True)

    for artifact in (dest.with_suffix(".png"), dest.with_suffix(".webp")):
        if artifact.exists() and artifact != dest:
            artifact.unlink()
    shutil.copy2(backup, dest)

    rolled = False
    if dest.suffix.lower() != ".webp":
        for md in [shot.markdown, *shot.extra_pages]:
            if rewrite_name(md, dest.with_suffix(".webp").name, dest.name):
                rolled = True

    entry["status"] = "restored"
    entry["original"] = str(rel(dest))
    manifest.put(shot.number, entry)
    print(f"restored shot {shot.number:02d} -> {rel(dest)}")
    if rolled:
        print("markdown rolled back to the original filename")
    return 0


def ask(prompt: str, default: str | None = None) -> str:
    extra = f" [{default}]" if default is not None else ""
    try:
        raw = input(f"{prompt}{extra}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nBye.")
        raise SystemExit(0) from None
    if raw == "" and default is not None:
        return default
    return raw


def ask_choice(prompt: str, allowed: set[str], default: str | None = None) -> str:
    while True:
        raw = ask(prompt, default).lower()
        if raw in allowed:
            return raw
        print(f"Please type one of: {', '.join(sorted(allowed))}")


def module_title(path: Path) -> str:
    index = path / "_index.md"
    if not index.exists():
        return path.name
    try:
        text = index.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.name
    match = TITLE.search(front_matter(text))
    if not match:
        return path.name
    return match.group(1).strip().strip('"').strip("'")


def find_modules() -> list[Path]:
    root = repo_root() / ROOKIES_MODULES
    if not root.is_dir():
        return []
    modules = []
    for path in sorted(root.iterdir()):
        if path.is_dir() and not path.name.startswith(".") and discover_shots(path):
            modules.append(path)
    return modules


def close_preview(*paths: Path) -> None:
    if sys.platform != "darwin":
        return
    names = [p.name for p in paths if p]
    if not names:
        subprocess.run(
            ["osascript", "-e", 'tell application "Preview" to close every window'],
            check=False,
            capture_output=True,
        )
        return
    lines = [
        "tell application \"Preview\"",
        "  repeat with w in (every window)",
        "    set n to name of w as string",
    ]
    for name in names:
        lines.append(f"    if n contains {json.dumps(name)} then close w")
    lines.extend(["  end repeat", "end tell"])
    subprocess.run(["osascript", "-e", "\n".join(lines)], check=False, capture_output=True)


def preview_path(shot: Shot, manifest: Manifest) -> Path | None:
    if shot.image.exists():
        return shot.image
    backup = manifest.backup_file(shot)
    if backup.exists():
        return backup
    entry = manifest.get(shot.number) or {}
    if entry.get("backup"):
        listed = repo_root() / entry["backup"]
        if listed.exists():
            return listed
    return None


def convert_existing_to_webp(shot: Shot, manifest: Manifest, quality: int) -> Path:
    dest = shot.image if shot.image.exists() else put_backup_back(shot, manifest)
    if dest.suffix.lower() == ".webp":
        mark_done(shot, manifest, dest)
        return dest
    png = dest if dest.suffix.lower() == ".png" else dest.with_name(dest.stem.lower() + ".png")
    if dest.suffix.lower() != ".png":
        to_png(dest, png)
    code = convert_png(png, quality)
    if code != 0:
        raise RuntimeError(f"could not convert {png.name}")
    webp = png.with_suffix(".webp")
    mark_done(shot, manifest, webp)
    return webp


def wait_for_retake(shot: Shot, shots: list[Shot], manifest: Manifest, inbox: Path, quality: int) -> str:
    """Returns 'ok' or 'cancel'."""
    inbox.mkdir(parents=True, exist_ok=True)
    stash_original(shot, manifest)
    backup = manifest.backup_file(shot)
    close_preview(shot.image, backup)
    if backup.exists():
        open_preview(backup)
    copy_filename(shot.save_as)
    print()
    print("Take a new screenshot in Shottr or Monosnap.")
    print("Add your arrows or notes there.")
    print("Save it as a PNG named:")
    print()
    print(f"    {shot.save_as}")
    print()
    print("in this folder:")
    print()
    print(f"    {rel(inbox)}")
    print()
    print("(That filename is on the clipboard — paste it when you save.)")
    print()
    while True:
        raw = ask("Press Enter when the file is saved, or type c to cancel", "")
        if raw.lower() in {"c", "cancel"}:
            put_backup_back(shot, manifest)
            return "cancel"
        files = inbox_files(inbox)
        match = None
        for path in files:
            found = match_inbox_file(path, shots, None)
            if found is not None and found.number == shot.number:
                match = path
                break
        if match is None and len(files) == 1:
            match = files[0]
        if match is None:
            print("I don't see that file in the folder yet. Save it, then press Enter.")
            continue
        try:
            result = ingest_one(match, shot, manifest, quality, dry_run=False)
        except Exception as exc:  # noqa: BLE001
            print(f"Could not process that file: {exc}")
            continue
        print(f"Saved as WebP: {result}")
        return "ok"


def print_shot_list(shots: list[Shot], manifest: Manifest) -> None:
    print()
    print(f"{'#':<4} {'type':<6} {'file'}")
    print("-" * 50)
    for shot in shots:
        kind = shot_state(shot, manifest)
        if shot.image.exists():
            kind = shot.image.suffix.lower().lstrip(".")
        elif kind == "stash":
            kind = "stash"
        print(f"{shot.number:02d}   {kind:<6} {shot.image.name}")
        if shot.alt:
            print(f"       {shot.alt}")


def review_loop(
    shots: list[Shot],
    start: int,
    manifest: Manifest,
    inbox: Path,
    quality: int,
) -> None:
    index = next((i for i, s in enumerate(shots) if s.number == start), 0)
    while index < len(shots):
        shot = shots[index]
        shown = preview_path(shot, manifest)
        close_preview(shot.image, manifest.backup_file(shot))
        if shown is None:
            print(f"\nPicture {shot.number:02d} is missing. Skipping.")
            index += 1
            continue
        kind = shown.suffix.lower().lstrip(".")
        print()
        print("=" * 56)
        print(f"Picture {shot.number} of {len(shots)}")
        print(f"File:  {shown.name}   ({kind.upper()})")
        print(f"Page:  {rel(shot.markdown)}")
        if shot.alt:
            print(f"Shows: {shot.alt}")
        print("=" * 56)
        print()
        print("Preview should be showing this picture.")
        print()
        print("  1) Keep     — leave it as it is, next picture")
        if kind == "webp":
            print("  2) WebP     — already WebP, same as Keep")
        else:
            print("  2) WebP     — convert this picture to WebP and update the page")
        print("  3) Retake   — you will take a new screenshot")
        print("  0) Stop     — back to the module list")
        print()
        open_preview(shown)
        choice = ask_choice("Your choice", {"1", "2", "3", "0", "k", "w", "r", "q"}, "1")
        close_preview(shown, shot.image, manifest.backup_file(shot))
        if choice in {"0", "q"}:
            if shot_state(shot, manifest) == "stash":
                put_backup_back(shot, manifest)
            return
        if choice in {"1", "k"}:
            if not shot.image.exists():
                put_backup_back(shot, manifest)
            print("Kept. Next picture.")
            index += 1
            continue
        if choice in {"2", "w"}:
            if kind == "webp":
                print("Already WebP. Next picture.")
                index += 1
                continue
            try:
                webp = convert_existing_to_webp(shot, manifest, quality)
            except Exception as exc:  # noqa: BLE001
                print(f"Could not convert: {exc}")
                continue
            print(f"Converted to {rel(webp)}")
            index += 1
            continue
        if choice in {"3", "r"}:
            result = wait_for_retake(shot, shots, manifest, inbox, quality)
            close_preview(shown, shot.image, manifest.backup_file(shot))
            if result == "ok":
                print("New screenshot is in place. Next picture.")
                index += 1
            else:
                print("Cancelled. This picture is unchanged.")
            continue
    print()
    print("That was the last picture in this module.")
    ask("Press Enter to go back to the module list", "")


def run_app(quality: int) -> int:
    inbox = default_inbox()
    backup_dir = default_backup()
    inbox.mkdir(parents=True, exist_ok=True)
    backup_dir.mkdir(parents=True, exist_ok=True)
    manifest = Manifest(backup_dir)
    modules = find_modules()
    if not modules:
        print("I could not find any workshop modules with pictures.")
        return 1
    while True:
        print()
        print("Screenshot helper")
        print("=================")
        print()
        print("Which module?")
        print()
        for i, path in enumerate(modules, start=1):
            count = len(discover_shots(path))
            label = "picture" if count == 1 else "pictures"
            print(f"  {i}) {module_title(path)}  ({count} {label})")
        print("  0) Quit")
        print()
        raw = ask("Number", "1")
        if raw in {"0", "q", "quit"}:
            print("Bye.")
            return 0
        if not raw.isdigit() or not (1 <= int(raw) <= len(modules)):
            print("That is not a module number.")
            continue
        section = modules[int(raw) - 1]
        shots = discover_shots(section)
        print()
        print(module_title(section))
        print_shot_list(shots, manifest)
        first = next(
            (s.number for s in shots if shot_state(s, manifest) == "stash"),
            None,
        )
        if first is None:
            first = next(
                (
                    s.number
                    for s in shots
                    if shot_state(s, manifest) not in {"webp", "keep"}
                ),
                shots[0].number,
            )
        raw_start = ask("Start at which number", f"{first:02d}")
        if raw_start in {"0", "q"}:
            continue
        if not raw_start.isdigit():
            print("Please type a picture number.")
            continue
        start = int(raw_start)
        if not any(s.number == start for s in shots):
            print(f"There is no picture {start:02d} in this module.")
            continue
        review_loop(shots, start, manifest, inbox, quality)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not 0 <= args.quality <= 100:
        raise SystemExit("--quality must be between 0 and 100")
    if args.command is None:
        return run_app(args.quality)
    section = resolve_section(args.section)
    shots = discover_shots(section)
    if not shots:
        raise SystemExit(f"no screenshots found under {rel(section)}")
    inbox = Path(args.inbox).expanduser()
    backup_dir = Path(args.backup).expanduser()
    if not inbox.is_absolute():
        inbox = (Path.cwd() / inbox).resolve()
    if not backup_dir.is_absolute():
        backup_dir = (Path.cwd() / backup_dir).resolve()
    manifest = Manifest(backup_dir)

    if args.command == "list":
        print_list(shots, manifest, args.remaining)
        print(f"inbox:  {rel(inbox)}")
        print(f"backup: {rel(backup_dir)}")
        return 0
    if args.command == "start":
        if not args.shot:
            raise SystemExit("start requires a shot number, e.g. start 03")
        return cmd_start(find_shot(shots, args.shot), manifest, inbox, args.no_open)
    if args.command == "next":
        return cmd_next(shots, manifest, inbox, args.no_open)
    if args.command == "open":
        if not args.shot:
            raise SystemExit("open requires a shot number, e.g. open 03")
        return cmd_open(find_shot(shots, args.shot), manifest, inbox, args.no_open)
    if args.command == "keep":
        shot = current_shot(shots, manifest, args.shot)
        return cmd_keep(shot, shots, manifest, inbox, args.quality, args.no_open)
    if args.command == "skip":
        shot = current_shot(shots, manifest, args.shot)
        return cmd_skip(shot, shots, manifest, inbox, args.no_open)
    if args.command == "ingest":
        inbox.mkdir(parents=True, exist_ok=True)
        return cmd_ingest(shots, manifest, inbox, args.quality, args.dry_run, args.shot)
    if args.command == "watch":
        return cmd_watch(shots, manifest, inbox, args.quality, args.poll)
    if args.command == "restore":
        if not args.shot:
            raise SystemExit("restore requires a shot number, e.g. restore 03")
        return cmd_restore(find_shot(shots, args.shot), manifest)
    raise SystemExit(f"unknown command {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
