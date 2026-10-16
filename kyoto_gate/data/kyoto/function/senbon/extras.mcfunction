scoreboard players operation #p ky.var = @s ky.step
scoreboard players operation #p ky.var %= #2 ky.var
execute if score #p ky.var matches 0 run function kyoto:senbon/torii
