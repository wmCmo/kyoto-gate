execute store result storage kyoto:tmp cushion.x int 1 run data get entity @s Pos[0]
execute store result storage kyoto:tmp cushion.z int 1 run data get entity @s Pos[2]
execute store result score #cy ky.var run data get entity @s Pos[1]
scoreboard players remove #cy ky.var 1
execute store result storage kyoto:tmp cushion.by int 1 run scoreboard players get #cy ky.var
