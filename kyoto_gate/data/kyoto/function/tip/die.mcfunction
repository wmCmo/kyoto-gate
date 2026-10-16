# A senbon path ends at its shrine; a town street that travelled far may take root as a new gate
execute if entity @s[tag=ky.senbon] at @s run function kyoto:senbon/shrine
scoreboard players set #r ky.var 100
execute unless entity @s[tag=ky.senbon] if score @s ky.step matches 25.. if score #nodes ky.var < #maxnodes ky.var unless entity @e[type=marker,tag=ky.node,distance=..28] store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..40 at @s run function kyoto:tip/root
kill @s
