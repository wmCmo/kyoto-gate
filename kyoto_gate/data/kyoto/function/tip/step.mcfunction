# One step of a street tip: read the ground ahead and decide how the street continues
scoreboard players add @s ky.step 1
scoreboard players remove @s ky.charge 1
execute if score @s ky.cross matches 1.. run scoreboard players remove @s ky.cross 1
execute if score @s ky.charge matches ..0 run return run function kyoto:tip/die
execute unless loaded ^ ^ ^3 run return 0
scoreboard players set #water ky.var 0
scoreboard players set #blocked ky.var 0
scoreboard players set #street ky.var 0
execute positioned ^ ^ ^1 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.probe"]}
# another street ahead (a junction), or one running alongside 3 blocks over
execute positioned ^3 ^ ^1 positioned over motion_blocking_no_leaves if block ~ ~-1 ~ #kyoto:path run scoreboard players set #street ky.var 2
execute positioned ^-3 ^ ^1 positioned over motion_blocking_no_leaves if block ~ ~-1 ~ #kyoto:path run scoreboard players set #street ky.var 2
execute store result score #y0 ky.var run data get entity @s Pos[1]
execute as @e[type=marker,tag=ky.probe,limit=1] store result score #y1 ky.var run data get entity @s Pos[1]
execute as @e[type=marker,tag=ky.probe,limit=1] at @s if block ~ ~-1 ~ #kyoto:water run scoreboard players set #water ky.var 1
execute as @e[type=marker,tag=ky.probe,limit=1] at @s if block ~ ~-1 ~ #kyoto:path run scoreboard players set #street ky.var 1
execute as @e[type=marker,tag=ky.probe,limit=1] at @s if block ~ ~-1 ~ #kyoto:built unless block ~ ~-1 ~ #kyoto:path run scoreboard players set #blocked ky.var 1
execute as @e[type=marker,tag=ky.probe,limit=1] at @s if block ~ ~-1 ~ #minecraft:logs run scoreboard players set #blocked ky.var 2
kill @e[type=marker,tag=ky.probe]
scoreboard players operation #dy ky.var = #y1 ky.var
scoreboard players operation #dy ky.var -= #y0 ky.var
# street awareness starts once a street has left its parent (branches begin on top of one),
# and pauses while it crosses another street
execute if score @s ky.step matches 5.. if score @s ky.cross matches ..0 if score #street ky.var matches 1 run function kyoto:tip/junction
execute if score #street ky.var matches 9 run return 0
execute if score @s ky.step matches 5.. if score @s ky.cross matches ..0 if score #street ky.var matches 2 run return run function kyoto:tip/turn
execute if score #blocked ky.var matches 2 run return run function kyoto:tip/chop
execute if score #blocked ky.var matches 1 run return run function kyoto:tip/turn
execute if score #water ky.var matches 1 run return run function kyoto:tip/bridge
execute if score #dy ky.var matches 0 run return run function kyoto:tip/walk
execute if score #dy ky.var matches 1..12 run return run function kyoto:tip/climb
execute if score #dy ky.var matches -12..-1 run return run function kyoto:tip/descend
function kyoto:tip/turn
