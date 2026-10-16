# Where the town thins out, bamboo groves
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..4 run return 0
execute store result score #side ky.var run random value 0..1
execute if score #side ky.var matches 0 positioned ^5 ^ ^ positioned over motion_blocking_no_leaves if block ~ ~-1 ~ #minecraft:dirt run place feature minecraft:bamboo_some_podzol
execute if score #side ky.var matches 1 positioned ^-5 ^ ^ positioned over motion_blocking_no_leaves if block ~ ~-1 ~ #minecraft:dirt run place feature minecraft:bamboo_some_podzol
