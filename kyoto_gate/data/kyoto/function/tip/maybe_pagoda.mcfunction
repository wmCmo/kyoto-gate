execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..25 run return 0
scoreboard players operation #c ky.var = @s ky.charge
scoreboard players operation #d ky.var = @s ky.dir
execute store result score #side ky.var run random value 0..1
execute if score #side ky.var matches 0 run scoreboard players add #d ky.var 3
execute if score #side ky.var matches 1 run scoreboard players add #d ky.var 1
scoreboard players operation #d ky.var %= #4 ky.var
execute if score #side ky.var matches 0 positioned ^3 ^ ^ run summon marker ~ ~ ~ {Tags:["ky.plot","ky.pagoda","ky.new"]}
execute if score #side ky.var matches 1 positioned ^-3 ^ ^ run summon marker ~ ~ ~ {Tags:["ky.plot","ky.pagoda","ky.new"]}
execute as @e[type=marker,tag=ky.plot,tag=ky.new] at @s run function kyoto:plot/init
