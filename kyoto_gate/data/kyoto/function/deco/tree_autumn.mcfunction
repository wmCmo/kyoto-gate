execute store result score #r ky.var run random value 1..3
execute if score #r ky.var matches 1 run return run place feature minecraft:red_poplar
execute if score #r ky.var matches 2 run return run place feature minecraft:orange_poplar
place feature minecraft:yellow_poplar
