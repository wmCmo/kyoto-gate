fill ^-2 ^-1 ^ ^2 ^-1 ^ dark_oak_planks replace #kyoto:fillable
fill ^-1 ^ ^ ^1 ^2 ^ air replace #kyoto:clearable
execute if block ^2 ^ ^ #kyoto:fillable run setblock ^2 ^ ^ dark_oak_fence
execute if block ^-2 ^ ^ #kyoto:fillable run setblock ^-2 ^ ^ dark_oak_fence
scoreboard players operation #p ky.var = @s ky.bridge
scoreboard players operation #p ky.var %= #4 ky.var
execute if score #p ky.var matches 0 run fill ^2 ^-2 ^ ^2 ^-16 ^ dark_oak_log replace #kyoto:fillable
execute if score #p ky.var matches 0 run fill ^-2 ^-2 ^ ^-2 ^-16 ^ dark_oak_log replace #kyoto:fillable
execute if score #p ky.var matches 2 if block ^2 ^1 ^ #kyoto:fillable run setblock ^2 ^1 ^ lantern
