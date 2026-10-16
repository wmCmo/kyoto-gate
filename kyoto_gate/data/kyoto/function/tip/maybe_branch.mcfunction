execute if score #tips ky.var >= #maxtips ky.var run return 0
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..9 run return 0
scoreboard players operation #c ky.var = @s ky.charge
scoreboard players operation #c ky.var *= #8 ky.var
scoreboard players operation #c ky.var /= #10 ky.var
scoreboard players operation #d ky.var = @s ky.dir
execute store result score #r ky.var run random value 0..1
execute if score #r ky.var matches 0 run scoreboard players add #d ky.var 1
execute if score #r ky.var matches 1 run scoreboard players add #d ky.var 3
scoreboard players operation #d ky.var %= #4 ky.var
function kyoto:util/district_of
summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
scoreboard players add #tips ky.var 1
