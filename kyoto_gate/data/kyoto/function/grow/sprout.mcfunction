# A quiet town: a side street sprouts from a random point it has already grown through
execute if score #houses ky.var >= #maxhouses ky.var run return 0
execute if score #tips ky.var >= #maxtips ky.var run return 0
execute store result score #trails ky.var if entity @e[type=marker,tag=ky.trail]
execute if score #trails ky.var matches 1.. as @e[type=marker,tag=ky.trail,sort=random,limit=1] at @s run return run function kyoto:grow/sprout_here
# towns grown before trails existed: let a gate send streets out again
execute as @e[type=marker,tag=ky.node,sort=random,limit=1] run scoreboard players set @s ky.step 0
