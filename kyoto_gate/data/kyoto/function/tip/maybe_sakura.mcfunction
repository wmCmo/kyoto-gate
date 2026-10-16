# Now and then a tree beside the street (a little less often than before)
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..2 run return 0
execute store result score #side ky.var run random value 0..1
execute if score #side ky.var matches 0 positioned ^4 ^ ^ positioned over motion_blocking_no_leaves run function kyoto:deco/street_tree
execute if score #side ky.var matches 1 positioned ^-4 ^ ^ positioned over motion_blocking_no_leaves run function kyoto:deco/street_tree
