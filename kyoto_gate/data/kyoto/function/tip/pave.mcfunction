# Charge sets the width: wide near the gate, single stones further out, stepping stones at the edge
execute if score @s ky.charge matches 45.. run return run function kyoto:tip/pave_wide
execute if score @s ky.charge matches 15..44 run return run function kyoto:tip/stone
scoreboard players operation #p ky.var = @s ky.step
scoreboard players operation #p ky.var %= #2 ky.var
execute if score #p ky.var matches 0 run function kyoto:tip/stone
