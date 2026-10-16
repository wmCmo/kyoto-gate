# Overlap check for a 5x6 house. Returns 1 (blocked) if any core sample hits
# another building, a path, water or ground too far from street level.
# Cores are tested; eaves (the margin) are not, so neighbours may share them.
execute if block ^-2 ^-1 ^1 #kyoto:built run return 1
execute if block ^-2 ^1 ^1 #kyoto:built run return 1
execute if block ^-2 ^3 ^1 #kyoto:built run return 1
execute if block ^-2 ^6 ^1 #kyoto:built run return 1
execute if block ^-2 ^-1 ^1 #kyoto:path run return 1
execute if block ^-2 ^-1 ^3 #kyoto:built run return 1
execute if block ^-2 ^1 ^3 #kyoto:built run return 1
execute if block ^-2 ^3 ^3 #kyoto:built run return 1
execute if block ^-2 ^6 ^3 #kyoto:built run return 1
execute if block ^-2 ^-1 ^3 #kyoto:path run return 1
execute if block ^-2 ^-1 ^6 #kyoto:built run return 1
execute if block ^-2 ^1 ^6 #kyoto:built run return 1
execute if block ^-2 ^3 ^6 #kyoto:built run return 1
execute if block ^-2 ^6 ^6 #kyoto:built run return 1
execute if block ^-2 ^-1 ^6 #kyoto:path run return 1
execute if block ^ ^-1 ^1 #kyoto:built run return 1
execute if block ^ ^1 ^1 #kyoto:built run return 1
execute if block ^ ^3 ^1 #kyoto:built run return 1
execute if block ^ ^6 ^1 #kyoto:built run return 1
execute if block ^ ^-1 ^1 #kyoto:path run return 1
execute if block ^ ^-1 ^3 #kyoto:built run return 1
execute if block ^ ^1 ^3 #kyoto:built run return 1
execute if block ^ ^3 ^3 #kyoto:built run return 1
execute if block ^ ^6 ^3 #kyoto:built run return 1
execute if block ^ ^-1 ^3 #kyoto:path run return 1
execute if block ^ ^-1 ^6 #kyoto:built run return 1
execute if block ^ ^1 ^6 #kyoto:built run return 1
execute if block ^ ^3 ^6 #kyoto:built run return 1
execute if block ^ ^6 ^6 #kyoto:built run return 1
execute if block ^ ^-1 ^6 #kyoto:path run return 1
execute if block ^2 ^-1 ^1 #kyoto:built run return 1
execute if block ^2 ^1 ^1 #kyoto:built run return 1
execute if block ^2 ^3 ^1 #kyoto:built run return 1
execute if block ^2 ^6 ^1 #kyoto:built run return 1
execute if block ^2 ^-1 ^1 #kyoto:path run return 1
execute if block ^2 ^-1 ^3 #kyoto:built run return 1
execute if block ^2 ^1 ^3 #kyoto:built run return 1
execute if block ^2 ^3 ^3 #kyoto:built run return 1
execute if block ^2 ^6 ^3 #kyoto:built run return 1
execute if block ^2 ^-1 ^3 #kyoto:path run return 1
execute if block ^2 ^-1 ^6 #kyoto:built run return 1
execute if block ^2 ^1 ^6 #kyoto:built run return 1
execute if block ^2 ^3 ^6 #kyoto:built run return 1
execute if block ^2 ^6 ^6 #kyoto:built run return 1
execute if block ^2 ^-1 ^6 #kyoto:path run return 1
# ground height under the footprint
execute positioned ^-2 ^ ^1 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.probe"]}
execute positioned ^-2 ^ ^6 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.probe"]}
execute positioned ^2 ^ ^1 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.probe"]}
execute positioned ^2 ^ ^6 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.probe"]}
execute store result score #py ky.var run data get entity @s Pos[1]
execute as @e[type=marker,tag=ky.probe] store result score @s ky.var run data get entity @s Pos[1]
execute as @e[type=marker,tag=ky.probe] run scoreboard players operation @s ky.var -= #py ky.var
scoreboard players set #bad ky.var 0
execute if entity @e[type=marker,tag=ky.probe,scores={ky.var=7..}] run scoreboard players set #bad ky.var 1
execute if entity @e[type=marker,tag=ky.probe,scores={ky.var=..-17}] run scoreboard players set #bad ky.var 1
execute as @e[type=marker,tag=ky.probe] at @s if block ~ ~-1 ~ #kyoto:water run scoreboard players set #bad ky.var 1
scoreboard players set #deep ky.var 0
execute if entity @e[type=marker,tag=ky.probe,scores={ky.var=..-6}] run scoreboard players set #deep ky.var 1
kill @e[type=marker,tag=ky.probe]
execute if score #bad ky.var matches 1 run return 1
# 2 = the ground drops away under part of it: build out over the drop on stilts
execute if score #deep ky.var matches 1 run return 2
return 0
