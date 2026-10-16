execute store result score #r ky.var run random value 0..10
execute if score #r ky.var matches 0 run summon cat ~ ~ ~ {variant:"minecraft:tabby",PersistenceRequired:1b,Tags:["ky.life"]}
execute if score #r ky.var matches 1 run summon cat ~ ~ ~ {variant:"minecraft:black",PersistenceRequired:1b,Tags:["ky.life"]}
execute if score #r ky.var matches 2 run summon cat ~ ~ ~ {variant:"minecraft:red",PersistenceRequired:1b,Tags:["ky.life"]}
execute if score #r ky.var matches 3 run summon cat ~ ~ ~ {variant:"minecraft:siamese",PersistenceRequired:1b,Tags:["ky.life"]}
execute if score #r ky.var matches 4 run summon cat ~ ~ ~ {variant:"minecraft:british_shorthair",PersistenceRequired:1b,Tags:["ky.life"]}
execute if score #r ky.var matches 5 run summon cat ~ ~ ~ {variant:"minecraft:calico",PersistenceRequired:1b,Tags:["ky.life"]}
execute if score #r ky.var matches 6 run summon cat ~ ~ ~ {variant:"minecraft:persian",PersistenceRequired:1b,Tags:["ky.life"]}
execute if score #r ky.var matches 7 run summon cat ~ ~ ~ {variant:"minecraft:ragdoll",PersistenceRequired:1b,Tags:["ky.life"]}
execute if score #r ky.var matches 8 run summon cat ~ ~ ~ {variant:"minecraft:white",PersistenceRequired:1b,Tags:["ky.life"]}
execute if score #r ky.var matches 9 run summon cat ~ ~ ~ {variant:"minecraft:jellie",PersistenceRequired:1b,Tags:["ky.life"]}
execute if score #r ky.var matches 10 run summon cat ~ ~ ~ {variant:"minecraft:all_black",PersistenceRequired:1b,Tags:["ky.life"]}
