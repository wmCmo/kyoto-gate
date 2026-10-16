# Sets #district from @s tags: 0 town, 1 stream, 2 senbon torii, 3 shop alley
scoreboard players set #district ky.var 0
execute if entity @s[tag=ky.stream] run scoreboard players set #district ky.var 1
execute if entity @s[tag=ky.senbon] run scoreboard players set #district ky.var 2
execute if entity @s[tag=ky.alley] run scoreboard players set #district ky.var 3
