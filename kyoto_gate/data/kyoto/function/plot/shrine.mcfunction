# As a plot: a hokora set back from the street, a torii on the approach. Returns 1 if built.
scoreboard players set #ok ky.var 0
execute store result score #blocked ky.var run function kyoto:gen/gcheck_5x5
execute if score #blocked ky.var matches 1 run return 0
fill ^-3 ^ ^ ^3 ^7 ^6 air replace #kyoto:diggable
fill ^-2 ^-2 ^1 ^2 ^-9 ^5 stone_bricks replace #kyoto:fillable
function kyoto:util/rot
function kyoto:senbon/shrine_place with storage kyoto:tmp
function kyoto:senbon/torii
execute positioned ^ ^ ^3 run summon marker ~ ~ ~ {Tags:["ky.house"]}
return 1
