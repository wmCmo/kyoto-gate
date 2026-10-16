execute if block ~ ~-1 ~ #kyoto:built run return 0
# no lantern within 2 blocks of another
execute if block ~-2 ~1 ~-2 lantern run return 0
execute if block ~-2 ~1 ~-1 lantern run return 0
execute if block ~-2 ~1 ~ lantern run return 0
execute if block ~-2 ~1 ~1 lantern run return 0
execute if block ~-2 ~1 ~2 lantern run return 0
execute if block ~-1 ~1 ~-2 lantern run return 0
execute if block ~-1 ~1 ~-1 lantern run return 0
execute if block ~-1 ~1 ~ lantern run return 0
execute if block ~-1 ~1 ~1 lantern run return 0
execute if block ~-1 ~1 ~2 lantern run return 0
execute if block ~ ~1 ~-2 lantern run return 0
execute if block ~ ~1 ~-1 lantern run return 0
execute if block ~ ~1 ~1 lantern run return 0
execute if block ~ ~1 ~2 lantern run return 0
execute if block ~1 ~1 ~-2 lantern run return 0
execute if block ~1 ~1 ~-1 lantern run return 0
execute if block ~1 ~1 ~ lantern run return 0
execute if block ~1 ~1 ~1 lantern run return 0
execute if block ~1 ~1 ~2 lantern run return 0
execute if block ~2 ~1 ~-2 lantern run return 0
execute if block ~2 ~1 ~-1 lantern run return 0
execute if block ~2 ~1 ~ lantern run return 0
execute if block ~2 ~1 ~1 lantern run return 0
execute if block ~2 ~1 ~2 lantern run return 0
fill ~ ~-2 ~ ~ ~-6 ~ stone_bricks replace #kyoto:fillable
fill ~ ~ ~ ~ ~3 ~ air replace #kyoto:diggable
setblock ~ ~-1 ~ polished_andesite
setblock ~ ~ ~ stone_brick_wall
setblock ~ ~1 ~ lantern
setblock ~ ~2 ~ stone_brick_slab
