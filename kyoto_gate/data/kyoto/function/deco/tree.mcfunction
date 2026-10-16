# Plant the tree that belongs to this biome's season: sakura in spring biomes, poplars in the
# autumn forest, spruce in snow, pale oak in the pale garden, and pine (the garden evergreen) elsewhere
execute if biome ~ ~ ~ #kyoto:spring run return run function kyoto:deco/tree_spring
execute if biome ~ ~ ~ #kyoto:autumn run return run function kyoto:deco/tree_autumn
execute if biome ~ ~ ~ #kyoto:snowy run return run place feature minecraft:spruce
execute if biome ~ ~ ~ minecraft:pale_garden run return run place feature minecraft:pale_oak
place feature minecraft:pine
