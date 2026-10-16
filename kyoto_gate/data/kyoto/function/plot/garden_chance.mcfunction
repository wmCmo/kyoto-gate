# Where a house would not fit, the space often becomes a garden instead
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..65 run function kyoto:plot/garden
