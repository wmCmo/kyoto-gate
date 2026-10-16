# Just built: spend a blessing (once the pagoda stands), then keeper, life and garden
execute if score #rules ky.var matches 1 if entity @e[type=marker,tag=ky.offering] run scoreboard players remove #fuel ky.var 1
execute if score #front ky.var matches 2 positioned ^ ^ ^2 run function kyoto:shop/keeper
execute if score #life ky.var < #maxlife ky.var store result score #r ky.var run random value 1..100
execute if score #life ky.var < #maxlife ky.var if score #r ky.var matches 1..10 positioned ^ ^ ^ run function kyoto:life/cat
execute if score #life ky.var < #maxlife ky.var if score #r ky.var matches 11..15 positioned ^ ^ ^ run function kyoto:life/villager
function kyoto:plot/back_garden
