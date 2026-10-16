# Only on natural ground, never on a building or the street
execute unless block ~ ~-1 ~ #minecraft:dirt run return 0
execute if entity @e[type=marker,tag=ky.house,distance=..5] run return 0
function kyoto:deco/tree
