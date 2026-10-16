execute if entity @s[tag=ky.senbon] run return run function kyoto:senbon/extras
# every 12 steps, leave a trail marker the town can sprout from later
scoreboard players operation #p ky.var = @s ky.step
scoreboard players operation #p ky.var %= #12 ky.var
execute if score #p ky.var matches 0 run function kyoto:tip/trail
execute if score @s ky.charge matches 15.. run function kyoto:tip/maybe_toro
execute if score @s ky.charge matches 25.. unless entity @s[tag=ky.alley] run function kyoto:tip/maybe_branch
execute if score @s ky.charge matches 18.. run function kyoto:tip/maybe_plot
execute if score @s ky.charge matches 15.. unless entity @s[tag=ky.alley] run function kyoto:tip/maybe_sakura
execute if score @s ky.charge matches ..20 run function kyoto:tip/maybe_bamboo
