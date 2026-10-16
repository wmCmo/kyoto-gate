# A street that ran far takes root as a new gate, sometimes of a special kind
scoreboard players operation #yaw ky.var = @s ky.dir
scoreboard players set #c0 ky.var 60
scoreboard players set #variant ky.var 0
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 46..65 run scoreboard players set #variant ky.var 1
execute if score #r ky.var matches 66..85 run scoreboard players set #variant ky.var 2
execute if score #r ky.var matches 86..100 run scoreboard players set #variant ky.var 3
summon marker ~ ~ ~ {Tags:["ky.node","ky.new"]}
execute as @e[type=marker,tag=ky.node,tag=ky.new] at @s run function kyoto:node/init
scoreboard players add #nodes ky.var 1
