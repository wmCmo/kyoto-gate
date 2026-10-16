# Water ahead: keep the street level and build a bridge across
tp @s ^ ^ ^1
scoreboard players add @s ky.bridge 1
execute if score @s ky.bridge matches 24.. run return run function kyoto:tip/die
execute at @s run function kyoto:tip/bridge_deck
