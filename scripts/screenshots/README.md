# Screenshot helper

A small terminal app. You pick a module, look at each picture, and choose Keep, WebP, or Retake.

## Start

```bash
cd ~/GIT/observability-workshop
python3 scripts/retake-screenshots.py
```

No extra words after that. A menu appears.

1. Type the **module number** (Introduction is 1).
2. It lists the pictures. Type the **starting number** (or press Enter).
3. Preview opens the picture. Then:

| Choice | What it does |
| --- | --- |
| **1 Keep** | Leave this file alone. Next picture. |
| **2 WebP** | Convert this PNG to WebP and update the lesson page. Skip if it is already WebP. |
| **3 Retake** | You take a new screenshot. When you have saved it, press Enter. |
| **0 Stop** | Back to the module list. |

## Retake

Preview keeps showing the **old** picture so you can match it.

1. Capture in Shottr or Monosnap and add arrows/notes.
2. Save as **PNG** using the name the app printed (it is also on the clipboard).
3. Put that file in `scripts/screenshots/inbox`.
4. Come back to the terminal and **press Enter**. That is how you tell the app you are done.

The app turns it into WebP, updates the page, and opens the next picture.

Point Shottr/Monosnap’s save folder at `scripts/screenshots/inbox` once so you do not have to hunt for the file.

`c` then Enter cancels a retake and puts the old picture back.
