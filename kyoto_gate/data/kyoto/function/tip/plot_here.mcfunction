summon marker ~ ~ ~ {Tags:["ky.plot","ky.new"]}
execute if entity @s[tag=ky.alley] run tag @e[type=marker,tag=ky.plot,tag=ky.new] add ky.alley
execute as @e[type=marker,tag=ky.plot,tag=ky.new] at @s run function kyoto:plot/init
