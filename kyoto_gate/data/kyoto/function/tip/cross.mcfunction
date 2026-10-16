# Crossing: corner houses may claim the corners on this side, with a second front facing the crossing street
scoreboard players set @s ky.cross 6
execute if score #houses ky.var >= #maxhouses ky.var run return 0
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..45 run return 0
scoreboard players operation #c ky.var = @s ky.charge
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players add #d ky.var 3
scoreboard players operation #d ky.var %= #4 ky.var
execute positioned ^3 ^ ^-5 run summon marker ~ ~ ~ {Tags:["ky.plot","ky.corner_l","ky.new"]}
execute as @e[type=marker,tag=ky.plot,tag=ky.new] at @s run function kyoto:plot/init
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players add #d ky.var 1
scoreboard players operation #d ky.var %= #4 ky.var
execute positioned ^-3 ^ ^-5 run summon marker ~ ~ ~ {Tags:["ky.plot","ky.corner_r","ky.new"]}
execute as @e[type=marker,tag=ky.plot,tag=ky.new] at @s run function kyoto:plot/init
