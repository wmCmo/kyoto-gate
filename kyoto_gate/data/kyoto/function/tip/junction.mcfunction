# Met another street: about half the time cross it (a crossroads), otherwise end here (a T)
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..55 run return run function kyoto:tip/cross
scoreboard players set #street ky.var 9
function kyoto:tip/die
