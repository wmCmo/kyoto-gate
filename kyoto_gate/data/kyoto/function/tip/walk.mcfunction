execute positioned ^ ^ ^1 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
scoreboard players set @s ky.turns 0
scoreboard players set @s ky.bridge 0
execute at @s run function kyoto:tip/pave
execute if entity @s[tag=ky.stream] at @s positioned ^-2 ^-1 ^-1 run function kyoto:stream/cell
execute at @s run function kyoto:tip/extras
