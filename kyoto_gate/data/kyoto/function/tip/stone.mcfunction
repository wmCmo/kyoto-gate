# One paving stone at this column, with footing below and headroom above
execute if block ~ ~-1 ~ #kyoto:built run return 0
fill ~ ~-2 ~ ~ ~-6 ~ stone_bricks replace #kyoto:fillable
fill ~ ~ ~ ~ ~2 ~ air replace #kyoto:diggable
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..38 run return run setblock ~ ~-1 ~ stone_bricks
execute if score #r ky.var matches 39..56 run return run setblock ~ ~-1 ~ andesite
execute if score #r ky.var matches 57..70 run return run setblock ~ ~-1 ~ polished_andesite
execute if score #r ky.var matches 71..84 run return run setblock ~ ~-1 ~ mossy_stone_bricks
execute if score #r ky.var matches 85..93 run return run setblock ~ ~-1 ~ cracked_stone_bricks
setblock ~ ~-1 ~ cobblestone
