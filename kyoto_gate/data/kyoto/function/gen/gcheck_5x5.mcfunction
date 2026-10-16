# Can a 5x5 garden go here? Returns 1 if blocked. Gardens only need the ground clear.
execute if block ^-2 ^-1 ^1 #kyoto:built run return 1
execute if block ^-2 ^ ^1 #kyoto:built run return 1
execute if block ^-2 ^2 ^1 #kyoto:built run return 1
execute if block ^-2 ^-1 ^1 #kyoto:path run return 1
execute if block ^-2 ^ ^1 #minecraft:logs run return 1
execute if block ^-2 ^-1 ^3 #kyoto:built run return 1
execute if block ^-2 ^ ^3 #kyoto:built run return 1
execute if block ^-2 ^2 ^3 #kyoto:built run return 1
execute if block ^-2 ^-1 ^3 #kyoto:path run return 1
execute if block ^-2 ^ ^3 #minecraft:logs run return 1
execute if block ^-2 ^-1 ^5 #kyoto:built run return 1
execute if block ^-2 ^ ^5 #kyoto:built run return 1
execute if block ^-2 ^2 ^5 #kyoto:built run return 1
execute if block ^-2 ^-1 ^5 #kyoto:path run return 1
execute if block ^-2 ^ ^5 #minecraft:logs run return 1
execute if block ^ ^-1 ^1 #kyoto:built run return 1
execute if block ^ ^ ^1 #kyoto:built run return 1
execute if block ^ ^2 ^1 #kyoto:built run return 1
execute if block ^ ^-1 ^1 #kyoto:path run return 1
execute if block ^ ^ ^1 #minecraft:logs run return 1
execute if block ^ ^-1 ^3 #kyoto:built run return 1
execute if block ^ ^ ^3 #kyoto:built run return 1
execute if block ^ ^2 ^3 #kyoto:built run return 1
execute if block ^ ^-1 ^3 #kyoto:path run return 1
execute if block ^ ^ ^3 #minecraft:logs run return 1
execute if block ^ ^-1 ^5 #kyoto:built run return 1
execute if block ^ ^ ^5 #kyoto:built run return 1
execute if block ^ ^2 ^5 #kyoto:built run return 1
execute if block ^ ^-1 ^5 #kyoto:path run return 1
execute if block ^ ^ ^5 #minecraft:logs run return 1
execute if block ^2 ^-1 ^1 #kyoto:built run return 1
execute if block ^2 ^ ^1 #kyoto:built run return 1
execute if block ^2 ^2 ^1 #kyoto:built run return 1
execute if block ^2 ^-1 ^1 #kyoto:path run return 1
execute if block ^2 ^ ^1 #minecraft:logs run return 1
execute if block ^2 ^-1 ^3 #kyoto:built run return 1
execute if block ^2 ^ ^3 #kyoto:built run return 1
execute if block ^2 ^2 ^3 #kyoto:built run return 1
execute if block ^2 ^-1 ^3 #kyoto:path run return 1
execute if block ^2 ^ ^3 #minecraft:logs run return 1
execute if block ^2 ^-1 ^5 #kyoto:built run return 1
execute if block ^2 ^ ^5 #kyoto:built run return 1
execute if block ^2 ^2 ^5 #kyoto:built run return 1
execute if block ^2 ^-1 ^5 #kyoto:path run return 1
execute if block ^2 ^ ^5 #minecraft:logs run return 1
execute positioned ^-2 ^ ^1 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.probe"]}
execute positioned ^-2 ^ ^5 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.probe"]}
execute positioned ^2 ^ ^1 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.probe"]}
execute positioned ^2 ^ ^5 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.probe"]}
execute store result score #py ky.var run data get entity @s Pos[1]
execute as @e[type=marker,tag=ky.probe] store result score @s ky.var run data get entity @s Pos[1]
execute as @e[type=marker,tag=ky.probe] run scoreboard players operation @s ky.var -= #py ky.var
scoreboard players set #bad ky.var 0
execute if entity @e[type=marker,tag=ky.probe,scores={ky.var=4..}] run scoreboard players set #bad ky.var 1
execute if entity @e[type=marker,tag=ky.probe,scores={ky.var=..-4}] run scoreboard players set #bad ky.var 1
execute as @e[type=marker,tag=ky.probe] at @s if block ~ ~-1 ~ #kyoto:water run scoreboard players set #bad ky.var 1
kill @e[type=marker,tag=ky.probe]
execute if score #bad ky.var matches 1 run return 1
return 0
