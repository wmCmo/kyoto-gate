# One attempt per plot: pick a house, try to fit it, and the plot is gone either way
execute if entity @s[tag=ky.pagoda] run return run function kyoto:plot/try_pagoda
execute if entity @s[tag=ky.garden] run return run function kyoto:plot/try_garden
execute unless loaded ^ ^ ^12 run return 0
scoreboard players set #ok ky.var 0
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..5 if score @s ky.charge matches 25.. unless entity @s[tag=ky.alley] store result score #ok ky.var run function kyoto:plot/shrine
execute if score #r ky.var matches 1..5 if score #ok ky.var matches 1 run return run kill @s
execute store result score #w ky.var run random value 0..2
scoreboard players operation #w ky.var *= #2 ky.var
scoreboard players add #w ky.var 5
execute store result score #hd ky.var run random value 5..6
data modify storage kyoto:tmp house.f set value 1
execute if score @s ky.charge matches 50.. store result storage kyoto:tmp house.f int 1 run random value 1..2
execute store result storage kyoto:tmp house.seed int 1 run random value 1..2000000000
execute store result storage kyoto:tmp house.win int 1 run random value 0..3
# street front: 0 lattice, 1 lattice (door right), 2 shop, 3 storehouse, 4 tea house. Alleys are all shops.
execute store result score #front ky.var run random value 0..4
execute if entity @s[tag=ky.alley] run scoreboard players set #front ky.var 2
execute if score #front ky.var matches 0 run data modify storage kyoto:tmp house.front set value "koshi"
execute if score #front ky.var matches 1 run data modify storage kyoto:tmp house.front set value "koshi_r"
execute if score #front ky.var matches 2 run data modify storage kyoto:tmp house.front set value "shop"
execute if score #front ky.var matches 3 run data modify storage kyoto:tmp house.front set value "kura"
execute if score #front ky.var matches 4 run data modify storage kyoto:tmp house.front set value "engawa"
# inside follows the front
execute store result score #r ky.var run random value 1..100
data modify storage kyoto:tmp house.interior set value "home"
execute if score #r ky.var matches 61..100 run data modify storage kyoto:tmp house.interior set value "kitchen"
execute if score #front ky.var matches 2 run data modify storage kyoto:tmp house.interior set value "shop"
execute if score #front ky.var matches 3 run data modify storage kyoto:tmp house.interior set value "store"
execute if score #front ky.var matches 4 run data modify storage kyoto:tmp house.interior set value "tea"
scoreboard players set #cush ky.var 0
execute if data storage kyoto:tmp house{interior:"home"} run scoreboard players set #cush ky.var 1
execute if data storage kyoto:tmp house{interior:"tea"} run scoreboard players set #cush ky.var 1
# roof: tile, sometimes copper or hip-and-gable
execute store result score #r ky.var run random value 1..100
data modify storage kyoto:tmp house.roof set value "tile"
execute if score #r ky.var matches 1..15 run data modify storage kyoto:tmp house.roof set value "copper"
execute if score #r ky.var matches 16..30 run data modify storage kyoto:tmp house.roof set value "irimoya"
# wall finish (storehouses are always white plaster)
execute store result score #r ky.var run random value 1..100
data modify storage kyoto:tmp house.wall set value "spruce_planks"
execute if score #r ky.var matches 36..65 run data modify storage kyoto:tmp house.wall set value "white_terracotta"
execute if score #r ky.var matches 66..85 run data modify storage kyoto:tmp house.wall set value "packed_mud"
execute if score #r ky.var matches 86..100 run data modify storage kyoto:tmp house.wall set value "stripped_spruce_wood"
execute if score #front ky.var matches 3 run data modify storage kyoto:tmp house.wall set value "white_terracotta"
# corner houses get a second front on the side facing the crossing street
scoreboard players set #corner ky.var 0
execute if entity @s[tag=ky.corner_l] run scoreboard players set #corner ky.var 1
execute if entity @s[tag=ky.corner_r] run scoreboard players set #corner ky.var 2
function kyoto:util/rot
data modify storage kyoto:tmp house.rot set from storage kyoto:tmp rot
scoreboard players set #ok ky.var 0
execute store result score #ok ky.var run function kyoto:gen/plot
execute if score #ok ky.var matches 0 if score @s ky.charge matches 20.. unless entity @s[tag=ky.alley] run function kyoto:plot/garden_chance
execute if score #ok ky.var matches 1 run function kyoto:plot/after_house
kill @s
