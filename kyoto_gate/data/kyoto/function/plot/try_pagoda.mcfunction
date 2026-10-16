execute unless loaded ^ ^ ^14 run return 0
function kyoto:util/rot
data modify storage kyoto:tmp house.rot set from storage kyoto:tmp rot
scoreboard players set #ok ky.var 0
execute store result score #ok ky.var run function kyoto:gen/try_pagoda with storage kyoto:tmp house
execute if score #ok ky.var matches 1 as @e[type=marker,tag=ky.wants_pagoda] run tag @s add ky.has_pagoda
execute if score #ok ky.var matches 1 as @e[type=marker,tag=ky.has_pagoda] run tag @s remove ky.wants_pagoda
execute if score #ok ky.var matches 1 run tellraw @a {"text":"Somewhere above the roofs, a pagoda rises.","color":"gold","italic":true}
kill @s
