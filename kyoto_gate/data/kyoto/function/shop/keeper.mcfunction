# Inside the shop, facing the street (the plot faces away from it)
summon villager ~ ~ ~ {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,Tags:["ky.keeper","ky.newkeeper"],VillagerData:{type:"minecraft:plains",profession:"minecraft:cleric",level:5},Offers:{Recipes:[]}}
tp @e[type=villager,tag=ky.newkeeper,limit=1] ~ ~ ~ ~180 0
execute store result score #r ky.var run random value 1..4
execute if score #r ky.var matches 2 run data modify entity @e[type=villager,tag=ky.newkeeper,limit=1] VillagerData.profession set value "minecraft:librarian"
execute if score #r ky.var matches 3 run data modify entity @e[type=villager,tag=ky.newkeeper,limit=1] VillagerData.profession set value "minecraft:cartographer"
execute if score #r ky.var matches 4 run data modify entity @e[type=villager,tag=ky.newkeeper,limit=1] VillagerData.profession set value "minecraft:mason"
data modify storage kyoto:tmp shop.offers set value []
function kyoto:shop/pick
function kyoto:shop/pick
function kyoto:shop/pick
execute store result score #r ky.var run random value 1..2
execute if score #r ky.var matches 2 run function kyoto:shop/pick
data modify entity @e[type=villager,tag=ky.newkeeper,limit=1] Offers.Recipes set from storage kyoto:tmp shop.offers
function kyoto:shop/name
tag @e[type=villager,tag=ky.newkeeper] remove ky.newkeeper
