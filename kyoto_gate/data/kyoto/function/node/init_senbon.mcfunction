# Senbon torii: no gate of its own, one path that becomes a tunnel of torii up to a shrine
scoreboard players set @s ky.step 99
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players set #c ky.var 70
scoreboard players set #district ky.var 2
execute at @s run summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
tellraw @a {"text":"Somewhere, a line of torii begins to climb.","color":"gold","italic":true}
