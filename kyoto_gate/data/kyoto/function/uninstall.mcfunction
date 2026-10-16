# Leaves every building; removes everything the pack keeps in the world so the folder can be deleted
schedule clear kyoto:pulse
kill @e[type=marker,tag=ky.tip]
kill @e[type=marker,tag=ky.plot]
kill @e[type=marker,tag=ky.node]
kill @e[type=marker,tag=ky.probe]
kill @e[type=marker,tag=ky.house]
kill @e[type=marker,tag=ky.offering]
kill @e[type=marker,tag=ky.trail]
scoreboard objectives remove ky.charge
scoreboard objectives remove ky.dir
scoreboard objectives remove ky.step
scoreboard objectives remove ky.turns
scoreboard objectives remove ky.bridge
scoreboard objectives remove ky.cross
scoreboard objectives remove ky.var
data remove storage kyoto:tmp house
data remove storage kyoto:pool offers
tellraw @a {"text":"Kyoto Gate removed its markers and scores. Delete the datapack folder, then /reload.","color":"gold"}
