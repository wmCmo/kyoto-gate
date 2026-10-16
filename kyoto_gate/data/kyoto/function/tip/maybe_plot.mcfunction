# Houses follow the street: sometimes mark a plot beside it, facing away from the street.
# Shop alleys fill up faster.
execute if entity @e[type=marker,tag=ky.wants_pagoda,distance=..40] unless entity @e[type=marker,tag=ky.pagoda] run return run function kyoto:tip/maybe_pagoda
execute if score #houses ky.var >= #maxhouses ky.var run return 0
execute store result score #r ky.var run random value 1..100
execute if entity @s[tag=ky.alley] if score #r ky.var matches 31..55 run scoreboard players set #r ky.var 1
execute unless score #r ky.var matches 1..30 run return 0
scoreboard players operation #c ky.var = @s ky.charge
scoreboard players operation #d ky.var = @s ky.dir
execute store result score #side ky.var run random value 0..1
execute if score #side ky.var matches 0 run scoreboard players add #d ky.var 3
execute if score #side ky.var matches 1 run scoreboard players add #d ky.var 1
scoreboard players operation #d ky.var %= #4 ky.var
execute if score @s ky.charge matches 45.. if score #side ky.var matches 0 positioned ^3 ^ ^ run function kyoto:tip/plot_here
execute if score @s ky.charge matches 45.. if score #side ky.var matches 1 positioned ^-3 ^ ^ run function kyoto:tip/plot_here
execute if score @s ky.charge matches ..44 if score #side ky.var matches 0 positioned ^2 ^ ^ run function kyoto:tip/plot_here
execute if score @s ky.charge matches ..44 if score #side ky.var matches 1 positioned ^-2 ^ ^ run function kyoto:tip/plot_here
