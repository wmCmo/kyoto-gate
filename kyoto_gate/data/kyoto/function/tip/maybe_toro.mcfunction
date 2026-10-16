# Stone lanterns: every 7 steps alternating sides; every 4 in shop alleys; streams keep theirs off the water side
scoreboard players operation #p ky.var = @s ky.step
execute if entity @s[tag=ky.alley] run return run function kyoto:tip/toro_alley
scoreboard players operation #p ky.var %= #14 ky.var
execute if score #p ky.var matches 0 positioned ^2 ^ ^ run function kyoto:tip/toro
execute if score #p ky.var matches 7 unless entity @s[tag=ky.stream] positioned ^-2 ^ ^ run function kyoto:tip/toro
execute if score #p ky.var matches 7 if entity @s[tag=ky.stream] positioned ^2 ^ ^ run function kyoto:tip/toro
