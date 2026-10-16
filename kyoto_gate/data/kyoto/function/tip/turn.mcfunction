# Blocked: turn left or right; three blocked turns in a row and the street ends
scoreboard players add @s ky.turns 1
execute if score @s ky.turns matches 3.. run return run function kyoto:tip/die
execute store result score #r ky.var run random value 0..1
execute if score #r ky.var matches 0 run scoreboard players add @s ky.dir 1
execute if score #r ky.var matches 1 run scoreboard players add @s ky.dir 3
scoreboard players operation @s ky.dir %= #4 ky.var
function kyoto:tip/face
