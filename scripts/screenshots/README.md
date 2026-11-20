# Screenshot helper

A small terminal app. You pick a module, look at each picture, and choose **Keep**, **WebP**, or **Retake**.

**Use Shottr.** Set a keyboard shortcut for **Grab Section** so you can open menus and panes first, then capture just that area.

## Start

Need `cwebp` once: `brew install webp`

```bash
cd ~/GIT/observability-workshop
python3 scripts/retake-screenshots.py
```

No extra words after that. A menu appears.

1. Type the **module number** (Introduction is 1). Type **0** to quit.
2. It lists every picture that a lesson page actually uses. Type the **starting number**, or press Enter.
3. Preview opens the picture. Then pick 1, 2, 3, or 0.

The module line may say `(36 pictures, 2 unused)`. Unused files are on disk but no page points at them.

## Picture list

Each row is one screenshot, in lesson order:

| Column | Meaning |
| --- | --- |
| `#` | Number you type to start there |
| `type` | `webp`, `png`, or `stash` (original moved aside while you retake) |
| `file` | Filename in the lesson `images/` folder |

**Unused** (under the list) means files sitting in an `images/` folder that **no markdown page uses**. They are grouped by lesson. The helper does not delete them.

## Choices for each picture

You can type the number or the letter.

| Choice | What it does |
| --- | --- |
| **1** or **k** — Keep | Leave this file alone. Next picture. |
| **2** or **w** — WebP | Convert this PNG to WebP and update the lesson page. If it is already WebP, this is the same as Keep. |
| **3** or **r** — Retake | You take a new screenshot. Save **PNG** in Shottr. The app overwrites the lesson file as WebP (works even if it is already WebP). |
| **0** or **q** — Stop | Back to the module list. If a retake was in progress, the old picture is put back. |

Default is **1 Keep**. Press Enter to keep and move on.

## Retake

Preview keeps showing the **old** picture so you can match it.

1. In Shottr, capture the area (see Shottr below) and add arrows or notes.
2. Save as **PNG** using the name the app printed (it is also on the clipboard).
3. Put that file in `scripts/screenshots/inbox`.
4. Come back to the terminal and **press Enter**. That is how you tell the app you are done.

The app always goes **PNG → WebP**. If the lesson already has a `.webp`, that file is replaced. Markdown is pointed at `.webp` if it still said `.png`. Then the next picture opens.

`c` then Enter **cancels** a retake and puts the old picture back.

## Shottr (recommended)

Shottr is the right tool for this workshop. Monosnap also works, but Shottr is better for grabbing a region after you have opened extra panes.

**Do not use delayed fullscreen capture.** That grabs the whole screen. Lesson pictures should be a section.

### Grab Section shortcut (best for open panes)

1. In Shottr: **Settings → Hotkeys**.
2. Give **Grab Section** (sometimes called Grab Area) a shortcut you can hit with one hand, for example `⌃⇧S`.
3. In the product UI, open the menus, flyouts, or side panes you need.
4. Press that shortcut, then drag around **only** the area that should be in the lesson.
5. Annotate in Shottr (arrows, numbers, notes).
6. Save as PNG into `scripts/screenshots/inbox` with the filename the helper copied to the clipboard.

The shortcut matters because a delay-timer capture in Shottr is fullscreen-only. With a hotkey you can get the UI looking right, then grab the section immediately.

### Repeat Area

After you have grabbed a section once, **Repeat Area** (`shottr://grab/repeat`, or assign it a hotkey too) recaptures the **same rectangle**. Use that when you need another take of the same spot without dragging again.

### Save folder

Point Shottr’s save folder at `scripts/screenshots/inbox` once so you do not have to hunt for the file. Always save **PNG**. The helper turns it into WebP.

## How it finds pictures

It reads the **markdown**, not the `images/` folder listing.

- Every `.md` file in the module, in Hugo order (`_index.md` first, then `weight`).
- Image paths in the page (`../images/foo.webp`, `images/bar.png`, and similar).
- PNG, JPG, JPEG, and WebP that live inside that module.
- The same file used on two pages is still one item.

A file that sits in `images/` but is never mentioned in markdown is **Unused**, not a numbered picture. Remote `https://…` images are ignored.

## Optional CLI

The usual way is no arguments (the menu). These still work if you want a single step:

```bash
python3 scripts/retake-screenshots.py list
python3 scripts/retake-screenshots.py start 03
python3 scripts/retake-screenshots.py keep
python3 scripts/retake-screenshots.py ingest
python3 scripts/retake-screenshots.py restore 03
```

| Command | What it does |
| --- | --- |
| `list` | Print numbered shots. `--remaining` hides ones already WebP. Unused files are listed too. |
| `start NN` | Stash original, open Preview, copy the save-as name. |
| `next` | Start the next shot that is not finished. |
| `open NN` | Open Preview for that shot. |
| `keep [NN]` | Convert existing pixels to WebP, no recapture. |
| `skip [NN]` | Leave the file, do not retake now. |
| `ingest` | Convert PNGs waiting in the inbox. |
| `watch` | Keep watching the inbox until you press Ctrl+C. |
| `restore NN` | Put the stashed original back. |

`--section`, `--inbox`, `--backup`, and `--quality` change the folder or WebP quality. `--dry-run` on `ingest` only prints matches.
