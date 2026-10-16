execute unless block ~ ~ ~ #kyoto:diggable run return 0
execute if block ~ ~ ~ #kyoto:open run return 0
execute if block ^ ^ ^1 #kyoto:open run return 0
execute if block ^ ^ ^-1 #kyoto:open run return 0
execute if block ^-1 ^ ^ #kyoto:open run setblock ^-1 ^ ^ stone_bricks
execute if block ^-1 ^ ^ #kyoto:diggable run setblock ^-1 ^ ^ stone_bricks
execute if block ^1 ^ ^ #kyoto:open run setblock ^1 ^ ^ stone_bricks
execute unless block ~ ~-1 ~ #kyoto:water run setblock ~ ~-1 ~ stone_bricks
fill ~ ~1 ~ ~ ~3 ~ air replace #kyoto:clearable
setblock ~ ~ ~ water
