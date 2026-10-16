# A pot, barrel or the like on a free cell beside a house, only if there is ground under it
execute unless block ~ ~ ~ #kyoto:clearable run return 0
execute if block ~ ~-1 ~ #kyoto:fillable run return 0
execute if block ~ ~-1 ~ #kyoto:path run return 0
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..16 run return 0
execute store result score #r ky.var run random value 1..9
execute if score #r ky.var matches 1 run return run setblock ~ ~ ~ potted_fern
execute if score #r ky.var matches 2 run return run setblock ~ ~ ~ potted_bamboo
execute if score #r ky.var matches 3 run return run setblock ~ ~ ~ potted_azalea_bush
execute if score #r ky.var matches 4 run return run setblock ~ ~ ~ potted_red_tulip
execute if score #r ky.var matches 5 run return run setblock ~ ~ ~ potted_spruce_sapling
execute if score #r ky.var matches 6 run return run setblock ~ ~ ~ barrel[facing=up]
execute if score #r ky.var matches 7 run return run setblock ~ ~ ~ composter
execute if score #r ky.var matches 8 run return run setblock ~ ~ ~ decorated_pot
setblock ~ ~ ~ potted_flowering_azalea_bush
