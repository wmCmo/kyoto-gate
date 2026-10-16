# Night mode: the town only grows between dusk and dawn (you can still watch it happen)
execute store result score #time ky.var run time query daytime
execute unless score #time ky.var matches 12500..23500 run scoreboard players set #awake ky.var 0
