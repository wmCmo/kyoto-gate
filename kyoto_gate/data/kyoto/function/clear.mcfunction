# Removes every growth marker. Everything already built stays.
kill @e[type=marker,tag=ky.tip]
kill @e[type=marker,tag=ky.plot]
kill @e[type=marker,tag=ky.node]
kill @e[type=marker,tag=ky.probe]
kill @e[type=marker,tag=ky.trail]
tellraw @a {"text":"Kyoto Gate: growth cleared (buildings kept)","color":"gold"}
