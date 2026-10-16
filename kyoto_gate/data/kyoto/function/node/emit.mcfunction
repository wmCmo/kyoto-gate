# A gate keeps sending out new streets for a while (up to 8), each in a random direction
execute if score #tips ky.var >= #maxtips ky.var run return 0
execute if score @s ky.step matches 8.. run return 0
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..6 run return 0
scoreboard players add @s ky.step 1
execute store result score #d ky.var run random value 0..3
scoreboard players operation #c ky.var = @s ky.charge
function kyoto:util/district_of
summon marker ~ ~ ~ {Tags:["ky.tip","ky.new","ky.fresh"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
execute as @e[type=marker,tag=ky.fresh] at @s positioned ^ ^ ^2 positioned over motion_blocking_no_leaves if block ~ ~-1 ~ #kyoto:path as @e[type=marker,tag=ky.fresh] at @s run function kyoto:tip/turn_right
tag @e[type=marker,tag=ky.fresh] remove ky.fresh
scoreboard players add #tips ky.var 1
