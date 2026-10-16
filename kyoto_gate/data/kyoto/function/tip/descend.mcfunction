# Ground drops away: build a staircase down on a stone footing
tp @s ^ ^-1 ^1
scoreboard players set @s ky.turns 0
function kyoto:util/rot
data modify storage kyoto:tmp stair.facing set from storage kyoto:tmp back
execute at @s run function kyoto:tip/stairs
