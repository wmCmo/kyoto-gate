# Called each pulse: with survival rules on and a pagoda standing, growth waits for blessings
execute unless score #rules ky.var matches 1 run return 0
# (keyed to the offering box, so pagodas built before boxes existed keep growing freely)
execute unless entity @e[type=marker,tag=ky.offering] run return 0
execute if score #fuel ky.var matches 1.. run return 0
scoreboard players set #awake ky.var 0
execute unless score #warned ky.var matches 1 run tellraw @a [{"text":"The town rests. ","color":"gold","italic":true},{"text":"Offer gold in the box inside the pagoda to wake it.","color":"gray","italic":true}]
scoreboard players set #warned ky.var 1
