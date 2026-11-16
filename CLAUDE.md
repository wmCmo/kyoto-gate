# CLAUDE.md

Personal project: artifacts in English. The README covers what the pack does and how to build and validate it.

## Testing
- The pack is junctioned into the world `saves\Testing Kyoto\datapacks\kyoto_gate`, so `/reload` picks up a rebuild.
- Command errors don't appear in `latest.log`. Check results from Zach's screenshots (`.minecraft\screenshots`).
- The pack's counters (`#fuel`, `#tips`, `#nodes`, …, objective `ky.var`) can be read without the game from `saves\<world>\data\minecraft\scoreboard.dat` (gzip NBT; a missing `Score` means 0). That's how the "offering doesn't grow" stall was found: `#tips` was 0.
- For an undocumented 26.3 format, decode a vanilla structure `.nbt` from the jar that already uses it (that's how the cushion entity format was found).

## 26.3 gotchas
- Structure palettes use lowercase `id` / `properties`.
- `chain` is now `iron_chain`.
- Some worldgen features are in code: `minecraft:cherry`, `cherry_bees_005`, `bamboo_some_podzol`.
- Villager trades are still `Offers.Recipes`.
- The `minecraft:alt` font renders the enchanting-table glyphs.

## What Zach responds to
- A balance of straight streets and crossroads he can explore.
- Walkable slopes: every height change gets a stair.
- The organic "beautiful mess": windows at random heights, overlaps.
- Nothing floating.

It belongs to his EXZACHLY universe (vault: `🧊 EXZACHLY — the cube, the character, and geometry that can't exist`): shop items use glyph names, and the lime is `#b8f62a`.

## Pushing
Remote is `wmCmo/kyoto-gate` (private). The repo-local author is already set; push as wmCmo, then switch back: `~/.claude/memory/gh-two-accounts-active-one-flips.md`.
