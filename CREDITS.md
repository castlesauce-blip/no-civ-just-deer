# Credits & Licenses — Deer Colony Sim

## Audio — Kenney (CC0)

Sound effects and music jingles are from **Kenney** (https://kenney.nl), released under the **Creative Commons Zero (CC0 1.0 Universal)** public-domain dedication — free for personal, educational, and commercial use. Crediting Kenney is not required by the license, but we do so gladly.

License: https://creativecommons.org/publicdomain/zero/1.0/

Packs used:
- **Interface Sounds** (Kenney, CC0) — `confirm.ogg`, `gather.ogg`, `place.ogg`, `alert.ogg`
- **UI Audio** (Kenney, CC0) — `click.ogg`
- **Music Jingles** (Kenney, CC0) — `uprising.ogg`, `win.ogg`

The original Kenney CC0 license text ships alongside the audio at `assets/audio/KENNEY-CC0-LICENSE.txt`.

Suggested attribution line: *"Sound effects & music by Kenney (kenney.nl) — CC0."*

## Art — project-original

All sprites and terrain (deer, buildings, terrain tiles, resource icons, UI, FX) are **original to this project**, generated with OpenAI's ChatGPT/DALL-E image tools and processed by the project's own extraction pipeline. This art is **not** a third-party licensed asset and is **not** CC0; ownership and reuse follow OpenAI's usage terms for generated content. Do not credit it as Kenney or as CC0.

## Code & tooling

- Game: hand-written single-file HTML5 canvas (no engine/framework). No third-party code, engine, or runtime library ships in the game — nothing to attribute at runtime.
- Sprite extraction: the project's own magenta chroma-key + unmix keyer (`art/keyer.py`).

## Build tooling (not shipped in the game)

The keyer (`art/keyer.py`) runs on these Python libraries at build time only; none are distributed with the game, but listed for completeness:
- **NumPy** — BSD 3-Clause License — https://numpy.org
- **SciPy** — BSD 3-Clause License — https://scipy.org
- **Pillow (PIL fork)** — HPND (MIT-CMU) License — https://python-pillow.org

## Asset sourcing

Kenney packs were located via the game-forge asset library (`find-game-asset` skill). The full CC0 Kenney library is catalogued in the Game Builder project.

---
*Per project policy, sources are cited both here and in-game (start **and** end/win screen footers).*
