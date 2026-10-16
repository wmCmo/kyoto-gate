# Builds a 9x5 house. Macro args: f (floors), front, roof, seed, rot
# 1) cut terrain out of the volume, 2) stone foundation down to the ground, 3) parts
fill ^-5 ^ ^ ^5 ^13 ^6 air replace #kyoto:diggable
execute unless score #stilt ky.var matches 1 run fill ^-4 ^-2 ^1 ^4 ^-8 ^5 stone_bricks replace #kyoto:fillable
execute if score #stilt ky.var matches 1 run function kyoto:gen/stilts_w9_d5
$place template kyoto:house/body_w9_d5_f$(f) ^-5 ^-1 ^ $(rot)
$place template kyoto:house/interior_w9_d5_f$(f)_$(interior) ^-5 ^-1 ^ $(rot)
$place template kyoto:house/front_w9_d5_f$(f)_$(front) ^-5 ^-1 ^ $(rot)
$execute if score #front ky.var matches 3 run place template kyoto:house/namako_w9_d5 ^-5 ^-1 ^ $(rot)
$execute if score #corner ky.var matches 1 run place template kyoto:house/sidel_w9_d5_f$(f) ^-5 ^-1 ^ $(rot)
$execute if score #corner ky.var matches 2 run place template kyoto:house/sider_w9_d5_f$(f) ^-5 ^-1 ^ $(rot)
$place template kyoto:house/roof_w9_d5_f$(f)_$(roof) ^-5 ^-1 ^ $(rot)
$place template kyoto:house/deco_w9_d5_f$(f) ^-5 ^-1 ^ $(rot) none 0.35 $(seed)
$place template kyoto:house/windows_w9_d5_f$(f)_v$(win) ^-5 ^-1 ^ $(rot)
$fill ^-4 ^ ^1 ^4 ^13 ^5 $(wall) replace white_terracotta
summon marker ^ ^ ^3 {Tags:["ky.house"]}
execute if score #cush ky.var matches 1 positioned ^-1 ^ ^3 run function kyoto:life/cushion
execute if score #cush ky.var matches 1 positioned ^1 ^ ^3 run function kyoto:life/cushion
execute if score #cush ky.var matches 1 positioned ^-2 ^ ^2 run function kyoto:life/cushion
# pots, barrels and the like: only where there is ground to stand on
execute positioned ^-5 ^ ^ run function kyoto:deco/ground
execute positioned ^-4 ^ ^ run function kyoto:deco/ground
execute positioned ^-3 ^ ^ run function kyoto:deco/ground
execute positioned ^-2 ^ ^ run function kyoto:deco/ground
execute positioned ^-1 ^ ^ run function kyoto:deco/ground
execute positioned ^ ^ ^ run function kyoto:deco/ground
execute positioned ^1 ^ ^ run function kyoto:deco/ground
execute positioned ^2 ^ ^ run function kyoto:deco/ground
execute positioned ^3 ^ ^ run function kyoto:deco/ground
execute positioned ^4 ^ ^ run function kyoto:deco/ground
execute positioned ^5 ^ ^ run function kyoto:deco/ground
execute positioned ^-5 ^ ^1 run function kyoto:deco/ground
execute positioned ^-5 ^ ^2 run function kyoto:deco/ground
execute positioned ^-5 ^ ^3 run function kyoto:deco/ground
execute positioned ^-5 ^ ^4 run function kyoto:deco/ground
execute positioned ^-5 ^ ^5 run function kyoto:deco/ground
execute positioned ^5 ^ ^1 run function kyoto:deco/ground
execute positioned ^5 ^ ^2 run function kyoto:deco/ground
execute positioned ^5 ^ ^3 run function kyoto:deco/ground
execute positioned ^5 ^ ^4 run function kyoto:deco/ground
execute positioned ^5 ^ ^5 run function kyoto:deco/ground
