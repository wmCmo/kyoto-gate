schedule function kyoto:pulse 10t replace
execute unless score #running ky.var matches 1 run return 0
execute as @e[type=marker,tag=ky.offering] at @s run function kyoto:offer/check
scoreboard players set #awake ky.var 1
execute if score #night ky.var matches 1 run function kyoto:haunt/check
function kyoto:offer/gate
execute if score #awake ky.var matches 0 run return 0
execute store result score #tips ky.var if entity @e[type=marker,tag=ky.tip]
execute store result score #nodes ky.var if entity @e[type=marker,tag=ky.node]
execute store result score #houses ky.var if entity @e[type=marker,tag=ky.house]
execute store result score #life ky.var if entity @e[tag=ky.life]
execute as @e[type=marker,tag=ky.node] at @s run function kyoto:node/tick
execute if score #tips ky.var matches ..3 run function kyoto:grow/sprout
# keep the trail count bounded
execute store result score #trails ky.var if entity @e[type=marker,tag=ky.trail]
execute if score #trails ky.var matches 301.. run kill @e[type=marker,tag=ky.trail,sort=random,limit=1]
function kyoto:grow/batch
execute if score #rate ky.var matches 4.. run function kyoto:grow/batch
execute if score #rate ky.var matches 8.. run function kyoto:grow/batch
execute if score #rate ky.var matches 8.. run function kyoto:grow/batch
