# Nibwrite brand

Renamed from Longhand on 2026-10-13. The cursive ℓ files below (`longhand-*.svg`) were the Longhand mark and are retired; the Nibwrite mark is not drawn yet. The Nib Rider character and sting live in `exploration/nib-rider-round-4.html`.

Everything needed to represent Nibwrite consistently. Use the files here rather than redrawing.

## The mark

A cursive ℓ drawn in one stroke with round ends, ending in a small flourish. It is the first letter of the name written the way the name describes: by hand, in full. It works from 16 pixels up and needs no container. Chosen 2026-09-11 from the rounds kept in `exploration/`.

| File | Use |
|---|---|
| `logo/longhand-mark.svg` | The mark in ink on any light ground. |
| `logo/longhand-mark-paper.svg` | The mark in paper colour for dark grounds. |
| `logo/longhand-tile.svg` | The mark on a rounded ink tile. App icons, avatars, favicons at 32 px and up. |
| `logo/longhand-tile-paper.svg` | The tile in paper with a hairline, for light grounds. |
| `logo/favicon.svg` | Heavier stroke on the tile, for 16 to 32 px. |
| `logo/longhand-lockup.svg` | Mark plus wordmark, ink. The wordmark is live text set in Newsreader with Georgia fallback; convert to outlines before sending to print. |
| `logo/longhand-lockup-paper.svg` | Same, for dark grounds. |
| `logo/nib-mark.svg`, `logo/nib-tile.svg` | Nib, the Nibwrite assistant. A pen nib over a line of writing. Nib is a character, not a product mark: never use it to represent Longhand itself, and never show it without the Longhand mark somewhere on the same surface. |
| `social/social-preview.png` | 1280 by 640 social preview for GitHub repos and link unfurls. Rendered from `social-preview.html` with headless Chrome so Newsreader is real: `chrome --headless=new --window-size=1280,640 --virtual-time-budget=8000 --screenshot=social-preview.png social-preview.html`. |

Clear space around the mark: at least the width of the loop on every side. Never stretch it, outline it, add a shadow, or set it in any colour other than ink or paper.

## Colour

| Name | Hex | Role |
|---|---|---|
| Ink | `#1E2432` | Text, the mark, dark grounds |
| Paper | `#F3F4F1` | Page ground, the mark on ink |
| Paper deep | `#E9EBE6` | Code blocks, selected rows |
| Graphite | `#676B72` | Secondary text |
| Rule | `#CFD2CC` | Hairlines and borders |
| Removed | `#A8322B` on `#F4DEDC` | Deletions in a compare view |
| Added | `#2F6F4E` on `#DCEBE2` | Insertions in a compare view |

Red and green appear only inside a compare. They are not accent colours.

Label colours for cards and threads, muted so they sit on paper: `#B65A52` red, `#4C6A9A` blue, `#5E8A5C` green, `#C9A24A` yellow.

## Type

One family: Newsreader (Google Fonts), optical sizing on, weights 400, 500, 600, italic 400. Fallback Georgia, then Times New Roman. Body 18 px at 1.55 line height, measure 66 characters. Headlines 500 weight with slightly negative tracking. Monospace for commit messages and commands only: the system UI monospace stack.

## Nib's voice

Nib speaks in the second person, briefly, and only when asked or when it has something specific. It names the file, the snapshot, or the scene it means. It never praises the writing. It is allowed exactly one joke, and it is the Clippy one, once.

## Voice

Plain verbs, sentence case, no exclamation marks. Say what the thing does, not how good it is. "Take snapshot", not "Snapshot now!". Name features by what a writer would call them: binder, snapshot, thread, corkboard, compile.

## Ownership

The names Nibwrite, Longhand, and Nib and the marks in this folder are trademarks of 0xSpectra LLC. The brand kit files may be used to refer to Longhand; see TRADEMARKS.md in the longhand repository for what that covers.

## Affiliation

Nibwrite is independent. It is not affiliated with or endorsed by Literature & Latte, the makers of Scrivener, or by Obsidian. Do not use their logos in Longhand material.
