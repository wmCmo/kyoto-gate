# As a new tip. #d = direction, #c = charge, #district = what kind of street it is
tag @s remove ky.new
scoreboard players operation @s ky.dir = #d ky.var
scoreboard players operation @s ky.charge = #c ky.var
scoreboard players set @s ky.step 0
scoreboard players set @s ky.turns 0
scoreboard players set @s ky.bridge 0
scoreboard players set @s ky.cross 0
execute if score #district ky.var matches 1 run tag @s add ky.stream
execute if score #district ky.var matches 2 run tag @s add ky.senbon
execute if score #district ky.var matches 3 run tag @s add ky.alley
function kyoto:tip/face
