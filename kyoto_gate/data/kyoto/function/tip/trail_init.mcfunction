tag @s remove ky.new
scoreboard players operation @s ky.dir = #d ky.var
scoreboard players operation @s ky.charge = #c ky.var
execute if score #district ky.var matches 1 run tag @s add ky.stream
execute if score #district ky.var matches 3 run tag @s add ky.alley
