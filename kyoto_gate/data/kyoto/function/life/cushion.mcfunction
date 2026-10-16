# At the air cell above the floor. The cushion rests on the floor block below and remembers it.
execute unless block ~ ~ ~ air run return 0
execute align xyz run summon marker ~ ~ ~ {Tags:["ky.cpos"]}
execute as @e[type=marker,tag=ky.cpos,limit=1] run function kyoto:life/cushion_pos
kill @e[type=marker,tag=ky.cpos]
execute store result score #r ky.var run random value 1..6
data modify storage kyoto:tmp cushion.color set value "purple"
execute if score #r ky.var matches 2 run data modify storage kyoto:tmp cushion.color set value "red"
execute if score #r ky.var matches 3 run data modify storage kyoto:tmp cushion.color set value "blue"
execute if score #r ky.var matches 4 run data modify storage kyoto:tmp cushion.color set value "brown"
execute if score #r ky.var matches 5 run data modify storage kyoto:tmp cushion.color set value "orange"
execute if score #r ky.var matches 6 run data modify storage kyoto:tmp cushion.color set value "green"
execute align xyz positioned ~.5 ~ ~.5 run function kyoto:life/cushion_m with storage kyoto:tmp cushion
