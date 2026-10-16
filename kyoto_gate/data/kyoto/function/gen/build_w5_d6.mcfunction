# Builds a 5x6 house. Macro args: f (floors), front, roof, seed, rot
# 1) cut terrain out of the volume, 2) stone foundation down to the ground, 3) parts
fill ^-3 ^ ^ ^3 ^13 ^7 air replace #kyoto:diggable
execute unless score #stilt ky.var matches 1 run fill ^-2 ^-2 ^1 ^2 ^-8 ^6 stone_bricks replace #kyoto:fillable
execute if score #stilt ky.var matches 1 run function kyoto:gen/stilts_w5_d6
$place template kyoto:house/body_w5_d6_f$(f) ^-3 ^-1 ^ $(rot)
$place template kyoto:house/interior_w5_d6_f$(f)_$(interior) ^-3 ^-1 ^ $(rot)
$place template kyoto:house/front_w5_d6_f$(f)_$(front) ^-3 ^-1 ^ $(rot)
$execute if score #front ky.var matches 3 run place template kyoto:house/namako_w5_d6 ^-3 ^-1 ^ $(rot)
$execute if score #corner ky.var matches 1 run place template kyoto:house/sidel_w5_d6_f$(f) ^-3 ^-1 ^ $(rot)
$execute if score #corner ky.var matches 2 run place template kyoto:house/sider_w5_d6_f$(f) ^-3 ^-1 ^ $(rot)
$place template kyoto:house/roof_w5_d6_f$(f)_$(roof) ^-3 ^-1 ^ $(rot)
$place template kyoto:house/deco_w5_d6_f$(f) ^-3 ^-1 ^ $(rot) none 0.35 $(seed)
$place template kyoto:house/windows_w5_d6_f$(f)_v$(win) ^-3 ^-1 ^ $(rot)
$fill ^-2 ^ ^1 ^2 ^13 ^6 $(wall) replace white_terracotta
summon marker ^ ^ ^3 {Tags:["ky.house"]}
execute if score #cush ky.var matches 1 positioned ^-1 ^ ^3 run function kyoto:life/cushion
execute if score #cush ky.var matches 1 positioned ^1 ^ ^3 run function kyoto:life/cushion
# pots, barrels and the like: only where there is ground to stand on
execute positioned ^-3 ^ ^ run function kyoto:deco/ground
execute positioned ^-2 ^ ^ run function kyoto:deco/ground
execute positioned ^-1 ^ ^ run function kyoto:deco/ground
execute positioned ^ ^ ^ run function kyoto:deco/ground
execute positioned ^1 ^ ^ run function kyoto:deco/ground
execute positioned ^2 ^ ^ run function kyoto:deco/ground
execute positioned ^3 ^ ^ run function kyoto:deco/ground
execute positioned ^-3 ^ ^1 run function kyoto:deco/ground
execute positioned ^-3 ^ ^2 run function kyoto:deco/ground
execute positioned ^-3 ^ ^3 run function kyoto:deco/ground
execute positioned ^-3 ^ ^4 run function kyoto:deco/ground
execute positioned ^-3 ^ ^5 run function kyoto:deco/ground
execute positioned ^-3 ^ ^6 run function kyoto:deco/ground
execute positioned ^3 ^ ^1 run function kyoto:deco/ground
execute positioned ^3 ^ ^2 run function kyoto:deco/ground
execute positioned ^3 ^ ^3 run function kyoto:deco/ground
execute positioned ^3 ^ ^4 run function kyoto:deco/ground
execute positioned ^3 ^ ^5 run function kyoto:deco/ground
execute positioned ^3 ^ ^6 run function kyoto:deco/ground
