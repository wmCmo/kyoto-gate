# In some larger gardens, a tree in the middle (the ground under it becomes moss)
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..40 run return 0
execute if block ~ ~-1 ~ #kyoto:water run return 0
execute unless block ~ ~ ~ #kyoto:clearable run return 0
setblock ~ ~-1 ~ moss_block
function kyoto:deco/tree
