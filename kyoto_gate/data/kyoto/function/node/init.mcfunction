# As a new node. #yaw = direction, #c0 = charge, #variant = district (0 town, 1 stream, 2 senbon, 3 alley)
tag @s remove ky.new
execute if score #c0 ky.var matches 100.. run tag @s add ky.heart
execute if score #variant ky.var matches 1 run tag @s add ky.stream
execute if score #variant ky.var matches 2 run tag @s add ky.senbon
execute if score #variant ky.var matches 3 run tag @s add ky.alley
scoreboard players operation @s ky.dir = #yaw ky.var
scoreboard players operation @s ky.charge = #c0 ky.var
execute if entity @s[tag=ky.alley] run scoreboard players set @s ky.charge 40
scoreboard players set @s ky.step 0
function kyoto:tip/face
execute if entity @s[tag=ky.senbon] run return run function kyoto:node/init_senbon
execute at @s run function kyoto:node/torii
function kyoto:util/district_of
# the first two streets run straight through the torii, both ways
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players operation #c ky.var = @s ky.charge
execute at @s run summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
scoreboard players add #d ky.var 2
scoreboard players operation #d ky.var %= #4 ky.var
execute at @s run summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
