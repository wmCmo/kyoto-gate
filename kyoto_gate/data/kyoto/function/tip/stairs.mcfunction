scoreboard players set #w ky.var 0
execute if score @s ky.charge matches 45.. run scoreboard players set #w ky.var 1
execute store result storage kyoto:tmp stair.w int 1 run scoreboard players get #w ky.var
function kyoto:tip/stairs_place with storage kyoto:tmp stair
function kyoto:tip/extras
