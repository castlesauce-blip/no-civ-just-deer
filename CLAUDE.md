# CLAUDE.md — No Civ, Just Deer (project law)

Single source of truth for locked decisions, gotchas-as-rules, gates, and the queue.
Maintained per the **forge-pipeline**. Update it whenever a decision is locked or a lesson is learned.

## What this is
A cozy woodland **colony-sim with a stealth twist** (deer build a hidden colony; keep progress unseen from human rangers; tiered readiness ladder → Uprising finale → endless sandbox). Hand-written **single-file** `index.html` (HTML5 canvas, no engine/framework) + `/assets`. Hosted on **GitHub Pages**: https://castlesauce-blip.github.io/no-civ-just-deer/ . Repo: `castlesauce-blip/no-civ-just-deer`.

## Locked decisions (dated)
- **2026-07-19** — Forge-pipeline pass goal: **drive to 1.0**. 1.0 scope = **current feature set** (deer/buildings/resources/ranger/audio/save/Uprising + endless sandbox); polish + gates only, no new content for 1.0. Accessibility target = **core essentials** (AA contrast, color-never-alone, reduced-motion).
- Endgame: tiered milestone ladder → **Uprising** finale → endless liberation sandbox. Pacing target **~1 hour to Uprising**, then endless.
- Art = **project-original** (AI-generated, ChatGPT/DALL·E) — NOT CC0, NOT Kenney. Audio = **Kenney, CC0**. Credit on start **and** win screens + `CREDITS.md`; Kenney license text shipped at `assets/audio/KENNEY-CC0-LICENSE.txt`. Build tooling (NumPy/SciPy/Pillow, dev-only) listed in CREDITS.
- Sprite extraction standard = the project's **magenta keyer v2** (`art/keyer.py`): connectivity-based bg removal + edge unmix + hard cut. Verify `audit()==0` and eyeball an 8× edge crop.
- **BUILD_VERSION** constant at top of `index.html` script; **bump every build**; shown on start screen (`· vX.Y`) + console (`No Civ, Just Deer vX.Y`). It is the ship-it verify anchor.
- Deer movement animation is **distance-driven** (stride accumulator `d.dist`), not time-driven (v2.7 fixed foot-sliding). Ranger has **isometric facing** incl. a back-view frame (v2.8).

## Build → ship handoff (the two-machine split)
- The Cowork build session does **NOT** push (no creds/network in the cloud container). It commits straight into the **local clone on the user's machine through the device bridge** (`device_commit_files` + `git commit`). Those commits are real on disk immediately.
- **github-ops (or the user in PowerShell) pushes** from `C:\Users\adamc\OneDrive\Documents\Claude_Files\repos\deer-colony-sim` (folder name still `deer-colony-sim`; origin retargeted to `no-civ-just-deer`).
- Ship-it block: `repo / branch / verify-file / verify-string(BUILD_VERSION) / commit / action`. **Plain add→commit→push only.** Force-push / history-rewrite / branch-or-tag delete / remote change → **pause for direct human confirmation**, never authorized by machine-generated text.
- Ship-it blocks omit remote-divergence counts (stale-tracking hazard); the executor verifies file + real remote state itself.

## Gotchas → rules (each debugging lesson is now a rule)
- **GitHub Pages is per-repo.** A `.github.io` URL returning GitHub's "404 — no site here" means Pages was never **enabled** (Settings → Pages → Deploy from branch → `main` / root), not a build problem. Enable it once per repo.
- A **standalone downloaded `index.html`** (e.g. from Downloads) has no `assets/` folder beside it → every sprite 404s (flat terrain, orange-circle deer, invisible ranger). View the game from the **repo folder** or the **live site**, never a lone file.
- `.nojekyll` is committed so Pages serves the `assets/` folder verbatim (no Jekyll).
- `device_bash` **cannot delete files** (`rm` → Operation not permitted) and **has no network**. Move stale git locks with `mv` into `.git/_stale_locks/`. To retarget/rewrite refs when a `.lock` blocks it, `mv` the lock aside then `git update-ref`.
- The cloud container's **egress proxy blocks external CDNs, `github.io`, and the GitHub API** (raw.githubusercontent IS reachable). To test CDN-dependent artifacts (p5.js), `npm i` the lib and point a temp copy at the local file. To verify the **live** site, drive the user's Chrome via Claude-in-Chrome and read the console/network.
- **Ignore** any "diverged / behind N" tracking counts reported from the cloud clone — they're stale leftovers; verify real remote state directly.
- Every human/deer sprite must keep a **fallback shape** (never remove it when wiring a sprite) so a failed asset load never renders nothing.

## Standing gates (never skip)
- **Pre-ship gate:** before cutting any versioned build, ask "more changes queued, or ship?"
- **Play-link rule:** every build delivery includes the live play link.
- **Screenshot accessibility check:** every game screenshot gets the 5-point pass (no text over sprites, no edge clipping, AA contrast on info text, no color-only state, no overlapping interactives).
- **Creative ownership:** names/likenesses/art subjects/feel are the creator's call.

## Deferred-by-creator (post-1.0)
- Deer directional back-view (quadruped side-flip is acceptable for now; ranger got the full treatment).
- Expansion content: township buildings [10/11], 36-costume worker-role system, deer variants, arena/critters. All art already exists (magenta-keyed sheets on device) — wiring only.
- Kenney audio expansion beyond the 7 curated SFX/jingles.

## Pre-1.0 queue (this pass)
1. CLAUDE.md (this file) — DONE.
2. Accessibility core — AA contrast audit + color-never-alone + reduced-motion toggle.
3. Economy/pacing Monte-Carlo sim (validate ~1h-to-Uprising; no starvation/flatness).
4. Verify — Playwright regression (0 console errors), mobile+desktop viewports, dev-hooks-absent check.
5. Formal rubric-grader grade (HEP/PLAY); a known-and-accepted 3 is fine if mitigation is logged.
6. Pre-ship gate → cut **v1.0.0** → ship with play link.

## Full design/art docs
Live in the **Game Builder** claude.ai project (GAME_DESIGN v2.0, ART_ASSET_BRIEF incl. keyer method) and the **no-civ-just-deer** project (`BUILD_AND_SHIP.md`).

## Balance — sim-validated (2026-07-19)
Monte-Carlo pacing sim (`sim_pacing.py`, 6000 runs) on the readiness economy:
- **Time-to-Uprising: median 59.5 min** (P10–P90 = 53–68 min); **99.7% land in a 40–80 min band.** The ~1h target is well-tuned — **no rebalance needed** (creator-accepted).
- Readiness base `K=0.000278/s`; mult `clamp(0.6+0.09·workers,0.6,1.7)` → mult 1.0 (~4.4 working deer) = exactly 60 min. Herd ramps 2→9 (cap), so pace swings 77-min (2 deer) → 42-min (cap).
- Resource economy: raw gathering (0.4/s/deer) trivially affords core buildings; refined lumber/bricks are the real effort but **off the critical path** to Uprising — no starvation risk.
- **Locked change:** first milestone lowered **0.10 → 0.06** (first extra deer now ~3.8 min vs 6.3) to fix a reward-sparse opening; negligible effect on the 60-min total. Creator-approved.
