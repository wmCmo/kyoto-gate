# Run by a player (or by eating a Torii Seed): opens a gate 4 blocks ahead, facing the way they look.
execute store result score #yaw ky.var run data get entity @s Rotation[0]
scoreboard players add #yaw ky.var 405
scoreboard players operation #yaw ky.var /= #90 ky.var
scoreboard players operation #yaw ky.var %= #4 ky.var
scoreboard players set #c0 ky.var 100
scoreboard players set #variant ky.var 0
execute at @s rotated ~ 0 positioned ^ ^ ^4 align xyz positioned ~.5 ~ ~.5 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.node","ky.new"]}
execute as @e[type=marker,tag=ky.node,tag=ky.new] at @s run function kyoto:node/init
tellraw @a {"text":"A gate opens.","color":"gold","italic":true}
