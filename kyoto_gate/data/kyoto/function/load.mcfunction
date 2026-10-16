scoreboard objectives add ky.charge dummy
scoreboard objectives add ky.dir dummy
scoreboard objectives add ky.step dummy
scoreboard objectives add ky.turns dummy
scoreboard objectives add ky.bridge dummy
scoreboard objectives add ky.cross dummy
scoreboard objectives add ky.var dummy
execute unless score #running ky.var matches 0..1 run scoreboard players set #running ky.var 1
execute unless score #rate ky.var matches 1.. run scoreboard players set #rate ky.var 4
execute unless score #night ky.var matches 0..1 run scoreboard players set #night ky.var 0
execute unless score #rules ky.var matches 0..1 run scoreboard players set #rules ky.var 1
execute unless score #fuel ky.var matches -2147483648.. run scoreboard players set #fuel ky.var 0
execute unless score #maxhouses ky.var matches 1.. run scoreboard players set #maxhouses ky.var 400
scoreboard players set #maxtips ky.var 32
scoreboard players set #maxnodes ky.var 24
scoreboard players set #maxlife ky.var 40
scoreboard players set #2 ky.var 2
scoreboard players set #4 ky.var 4
scoreboard players set #6 ky.var 6
scoreboard players set #8 ky.var 8
scoreboard players set #10 ky.var 10
scoreboard players set #12 ky.var 12
scoreboard players set #14 ky.var 14
scoreboard players set #90 ky.var 90
function kyoto:shop/pool
schedule function kyoto:pulse 10t replace
tellraw @a [{"text":"Kyoto Gate loaded. ","color":"gold"},{"text":"[settings]","color":"yellow","click_event":{"action":"run_command","command":"/function kyoto:settings"},"hover_event":{"action":"show_text","value":"Open the Kyoto Gate settings"}}]
