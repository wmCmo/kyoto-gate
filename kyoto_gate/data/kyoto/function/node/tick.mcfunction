# The heart gate wants a pagoda once its town has 10 houses within 48 blocks
scoreboard players set #near ky.var 0
execute if entity @s[tag=ky.heart,tag=!ky.has_pagoda,tag=!ky.wants_pagoda] store result score #near ky.var if entity @e[type=marker,tag=ky.house,distance=..48]
execute if score #near ky.var matches 10.. run tag @s add ky.wants_pagoda
function kyoto:node/emit
