# Kyoto Gate

A Minecraft data pack (Java Edition 26.3, data format 121). You plant one torii, and a Kyoto town grows out of it across whatever terrain is there. Streets come first, the way the Upside Down's vines do, and houses follow the streets.

## Install

1. Download **[kyoto_gate.zip](https://github.com/wmCmo/kyoto-gate/releases/latest/download/kyoto_gate.zip)** (the latest release).
2. Put the zip in your world's `datapacks` folder: `saves/<your world>/datapacks`.
3. In the game, run `/reload`.
4. Craft a Torii Seed, or run `/function kyoto:gate`.

Releases are built by `.github/workflows/release.yml` whenever a `v*` tag is pushed.

## What grows

- **Streets** of mixed stone creep out from the gate. They follow the ground, become stone stairs on slopes, cross rivers on bridges with piers and lanterns, and fell trees in their way. Near the gate they are wide; they narrow to single stones and then stepping stones at the edge. Streets branch, cross each other to make crossroads, or end in T-junctions.
- **Houses (町家)** line the streets, facing them. Each is assembled from parts:
  - 3 widths, 2 depths, 1 or 2 storeys
  - 5 fronts: lattice (two door sides), shop with noren, storehouse with a namako band, tea house with an engawa
  - 3 roofs: tile, copper, hip-and-gable
  - 4 wall finishes and 4 window layouts at any height
  - 5 interiors: tatami home with a hearth, earthen kitchen, tea room, storehouse, shop
  - Houses on a corner get a second front. Where the ground drops away, they stand on timber stilts.
- **Gardens** fill gaps where a house doesn't fit, and sometimes grow behind houses: dry gardens (枯山水), moss gardens, and ponds fed by a small waterfall. Some get a tree.
- **Trees follow the biome's season:**
  - sakura in spring biomes (Cherry Grove, Meadow, Flower Forest)
  - red, orange and yellow poplars in the autumn Dappled Forest
  - spruce in snow
  - pine everywhere else
- **A five-storey pagoda** rises once 10 houses have grown near the first gate.
- **New gates** take root where streets ran far. Some are special districts:
  - a **stream district**: a stone channel of water runs beside the street
  - **senbon torii**: a tunnel of torii that climbs to a small shrine
  - a **shop alley**: narrow, lantern-heavy, every house a shop
- **Weird shops** are kept by villagers selling things nobody can identify. The wares are named in the enchanting-table script, with odd prices.
- **Life**: bamboo groves, cats, the odd villager, and cushions (zabuton) around the low tables. Cushions are entities, so they appear only when you're close, which suits interiors.

## Use

- `/function kyoto:gate` opens a gate 4 blocks ahead of you, facing the way you look.
- In survival, craft a **Torii Seed** and hold right-click with it. The recipe is a torii in the grid: a lantern hangs under the lintel, and a sakura sapling is planted between the pillars.
  ```
  B B B      B = polished blackstone
  R L R      R = red concrete
  R S R      L = lantern,  S = cherry sapling
  ```

- `/function kyoto:settings` opens a clickable menu with these options:
  - growth speed: slow, normal, fast
  - mode: *always*, or *night* (grows only between dusk and dawn)
  - rules: *survival* (offerings after the pagoda) or *endless*
  - town size: village, town, city
  - pause and resume
  - status
  - get a seed
  - clear growth
  - uninstall

**Clear growth** removes the invisible markers that drive growth. **Uninstall** removes every score and marker so you can delete the folder. Both keep every building.

## Survival rules

A town grows freely until its pagoda rises. After that it rests, and you wake it by offering gold in the box (a barrel under a shrine bell) inside the pagoda:
- 1 gold ingot = 1 blessing
- 1 gold block = 10 blessings

Each new house spends one blessing, and the bell rings when an offering is accepted. To grow without offerings, set the rules to **endless** in the settings.

## Building it

The pack in `kyoto_gate/` is generated; don't edit it by hand.

```
python src_files.py      # growth logic, tags, recipe, advancement
python build.py          # every structure (houses, gardens, pagoda, torii, shrine) and size-specific functions
python validate.py <path to 26.3.jar>   # checks every block, block state, tag and function reference against the game
```

## Performance

Growth runs every 10 ticks and touches only a few markers each time: 2 to 8 street steps and 1 to 4 plots, depending on speed. A busy gate measured 7.6 ms per tick on an integrated server.
