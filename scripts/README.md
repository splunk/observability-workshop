# PNG to WebP

`png-to-webp.py` converts workshop PNG assets to WebP, rewrites Markdown references to match, and reports size savings plus unused PNGs.

It is a CLI. Preview with `--dry-run` before writing files.

## Requirements

- Python 3.9+
- [`cwebp`](https://developers.google.com/speed/webp/docs/cwebp) from the WebP tools

```bash
# macOS
brew install webp

# Debian / Ubuntu
sudo apt install webp

# Fedora
sudo dnf install libwebp-tools

# Arch
sudo pacman -S libwebp

# Windows
choco install webp
# or
scoop install libwebp
```

Confirm with `cwebp -version`. If `cwebp` is missing, the script prints these install commands and exits.

## Usage

Run from the repository root:

```bash
# Preview the default scan (content/)
python3 scripts/png-to-webp.py --dry-run

# Convert one workshop
python3 scripts/png-to-webp.py --yes content/en/splunk4rookies/o11y-rookies-26

# Convert only PNGs that Markdown actually links to
python3 scripts/png-to-webp.py --referenced-only --dry-run content/en

# Keep the original PNGs
python3 scripts/png-to-webp.py --keep --yes content/en/splunk4rookies/o11y-rookies-26/modules/4-im
```

Without `--dry-run` or `--yes`, the script asks for confirmation. Non-interactive runs must pass one of those flags.

## Options

| Flag | Meaning |
| --- | --- |
| `paths` | Directories or files to convert. Defaults to `content/`. |
| `--dir DIR` | Extra directory to convert. Repeatable. |
| `--dry-run` | Measure and report without writing or deleting files. |
| `--yes`, `-y` | Apply changes without a prompt. |
| `--quality N` | `cwebp` quality 0–100. Default: `80`. |
| `--keep` | Leave the original PNG in place after a successful convert. |
| `--force` | Reconvert even when a `.webp` file already exists. |
| `--referenced-only` | Convert only PNGs referenced by Markdown. Unused files are still listed. |
| `--markdown-root DIR` | Tree used to find Markdown references. Default: `content/`. |
| `--jobs N`, `-j N` | Parallel `cwebp` workers. Default: all CPU cores. Use `1` for sequential. |

## What it updates

PNGs under the path you pass are converted. Markdown updates search the whole `--markdown-root` tree so a scoped convert cannot leave stale links in another section.

These reference forms are rewritten when they resolve to a converted file:

- Front matter: `images/foo.png`
- Markdown images: `![alt](../images/foo.png)`
- HTML / shortcodes: `src="images/foo.png"`
- Query strings are kept: `foo.png?width=20vw` becomes `foo.webp?width=20vw`

External `http://` / `https://` URLs are left alone.

Leaf pages such as `section/page.md` are served as `section/page/`, so `../images/foo.png` is treated as `section/images/foo.png`.

## Unused PNGs

Every run lists PNGs under the scan path that no Markdown file references, with file sizes. That report is independent of conversion.

- Default: unused PNGs are converted as well, and still appear under **Unused PNGs**.
- `--referenced-only`: unused PNGs are listed and not converted.

## Report

The script prints each converted file (before/after size), each updated `.md`, unused PNGs, and a summary with worker count and total savings.

A progress bar and spinner appear on stderr in an interactive terminal. They are omitted when output is piped or when `NO_PROGRESS=1`. Set `NO_COLOR=1` to disable colour.

## Notes

- Existing `.webp` files are skipped unless you pass `--force`.
- Successful converts delete the PNG unless you pass `--keep`.
- Dry-run still runs `cwebp` into a temp directory so the savings numbers are real. Nothing in `content/` is written.
