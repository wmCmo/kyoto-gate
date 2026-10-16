# Sometimes a small garden grows behind a new house (a tsuboniwa)
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..30 run return 0
execute positioned ^ ^ ^9 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.plot","ky.garden","ky.new"]}
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players operation #c ky.var = @s ky.charge
execute as @e[type=marker,tag=ky.plot,tag=ky.new] at @s run function kyoto:plot/init
