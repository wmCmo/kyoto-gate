scoreboard players operation #d ky.var = @s ky.dir
scoreboard players operation #c ky.var = @s ky.charge
function kyoto:util/district_of
summon marker ~ ~ ~ {Tags:["ky.trail","ky.new"]}
execute as @e[type=marker,tag=ky.trail,tag=ky.new] run function kyoto:tip/trail_init
