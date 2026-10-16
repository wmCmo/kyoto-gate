# From @s ky.dir: template rotation and the compass names of forward and back
execute if score @s ky.dir matches 0 run data merge storage kyoto:tmp {rot:"none",fwd:"south",back:"north"}
execute if score @s ky.dir matches 1 run data merge storage kyoto:tmp {rot:"clockwise_90",fwd:"west",back:"east"}
execute if score @s ky.dir matches 2 run data merge storage kyoto:tmp {rot:"180",fwd:"north",back:"south"}
execute if score @s ky.dir matches 3 run data merge storage kyoto:tmp {rot:"counterclockwise_90",fwd:"east",back:"west"}
