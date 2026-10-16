# As a trail marker, on the street: start a street at right angles to it, with enough life for houses
scoreboard players operation #d ky.var = @s ky.dir
execute store result score #r ky.var run random value 0..1
execute if score #r ky.var matches 0 run scoreboard players add #d ky.var 1
execute if score #r ky.var matches 1 run scoreboard players add #d ky.var 3
scoreboard players operation #d ky.var %= #4 ky.var
scoreboard players set #c ky.var 50
execute if score @s ky.charge matches 51.. run scoreboard players operation #c ky.var = @s ky.charge
function kyoto:util/district_of
summon marker ~ ~ ~ {Tags:["ky.tip","ky.new","ky.sprouted"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..20 as @e[type=marker,tag=ky.sprouted] at @s positioned ^ ^ ^3 positioned over motion_blocking_no_leaves run function kyoto:senbon/torii
tag @e[type=marker,tag=ky.sprouted] remove ky.sprouted
scoreboard players add #tips ky.var 1
kill @s
