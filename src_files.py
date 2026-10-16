"""Hand-written parts of the Kyoto Gate datapack: growth logic, tags and pack metadata.
build.py generates the structures and size-specific functions; this writes everything else.

Run:  python src_files.py
"""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kyoto_gate')

FILES = {}


def fn(name, text):
    FILES[f'data/kyoto/function/{name}.mcfunction'] = text.strip('\n') + '\n'


def tag(kind, name, values):
    FILES[f'data/{name.split(":")[0]}/tags/{kind}/{name.split(":")[1]}.json'] = json.dumps({'values': values}, indent=2) + '\n'


FILES['pack.mcmeta'] = json.dumps({
    'pack': {
        'description': 'Kyoto Gate: a torii that grows a Kyoto town across any terrain',
        'min_format': 121,
        'max_format': 121,
    }
}, indent=2) + '\n'

tag('function', 'minecraft:load', ['kyoto:load'])

# ---------------------------------------------------------------------------
# Block tags
# ---------------------------------------------------------------------------
tag('block', 'kyoto:water', ['minecraft:water'])
tag('block', 'kyoto:clearable', [
    '#minecraft:replaceable', '#minecraft:flowers', '#minecraft:leaves', '#minecraft:saplings',
    'minecraft:sugar_cane', 'minecraft:bamboo', 'minecraft:sweet_berry_bush', 'minecraft:cactus',
    'minecraft:pumpkin', 'minecraft:melon', 'minecraft:moss_carpet', 'minecraft:pink_petals',
])
tag('block', 'kyoto:garden_clear', [
    '#minecraft:replaceable', '#minecraft:flowers', '#minecraft:saplings', '#minecraft:dirt', '#minecraft:sand',
    '#minecraft:base_stone_overworld', '#minecraft:terracotta', 'minecraft:gravel', 'minecraft:snow_block',
    'minecraft:clay', 'minecraft:sandstone', 'minecraft:red_sandstone', 'minecraft:sugar_cane', 'minecraft:pumpkin',
])
tag('block', 'kyoto:fillable', ['minecraft:air', 'minecraft:cave_air', 'minecraft:water', '#kyoto:clearable'])
tag('block', 'kyoto:diggable', [
    '#kyoto:clearable', '#minecraft:dirt', '#minecraft:sand', '#minecraft:base_stone_overworld', '#minecraft:terracotta',
    'minecraft:gravel', 'minecraft:snow_block', 'minecraft:powder_snow', 'minecraft:clay',
    'minecraft:sandstone', 'minecraft:red_sandstone', 'minecraft:dirt_path',
])
tag('block', 'kyoto:path', [
    'minecraft:stone_bricks', 'minecraft:andesite', 'minecraft:polished_andesite', 'minecraft:mossy_stone_bricks',
    'minecraft:cracked_stone_bricks', 'minecraft:cobblestone', 'minecraft:stone_brick_stairs',
    'minecraft:dark_oak_planks',
])
tag('block', 'kyoto:built', [
    'minecraft:spruce_planks', 'minecraft:dark_oak_log', 'minecraft:stripped_dark_oak_log', 'minecraft:dark_oak_planks',
    'minecraft:white_terracotta', 'minecraft:dark_oak_fence', 'minecraft:spruce_fence', 'minecraft:dark_oak_door',
    'minecraft:spruce_door', 'minecraft:white_stained_glass_pane', 'minecraft:iron_bars', 'minecraft:spruce_slab',
    'minecraft:deepslate_tile_stairs', 'minecraft:deepslate_tiles', 'minecraft:deepslate_tile_slab',
    'minecraft:deepslate_tile_wall', 'minecraft:waxed_oxidized_cut_copper_stairs', 'minecraft:waxed_oxidized_cut_copper',
    'minecraft:waxed_oxidized_cut_copper_slab', 'minecraft:waxed_oxidized_copper_bulb',
    'minecraft:red_concrete', 'minecraft:polished_blackstone', 'minecraft:polished_blackstone_bricks',
    'minecraft:polished_blackstone_brick_stairs', 'minecraft:polished_blackstone_brick_slab',
    'minecraft:stone_brick_wall', 'minecraft:stone_brick_slab', 'minecraft:lantern', 'minecraft:barrel',
    'minecraft:iron_chain', 'minecraft:lightning_rod',
    'minecraft:polished_tuff', 'minecraft:calcite', 'minecraft:moss_block', 'minecraft:clay',
    'minecraft:packed_mud', 'minecraft:stripped_spruce_wood',
])

# ---------------------------------------------------------------------------
# Setup and controls
# ---------------------------------------------------------------------------
fn('load', '''
scoreboard objectives add ky.charge dummy
scoreboard objectives add ky.dir dummy
scoreboard objectives add ky.step dummy
scoreboard objectives add ky.turns dummy
scoreboard objectives add ky.bridge dummy
scoreboard objectives add ky.cross dummy
scoreboard objectives add ky.var dummy
execute unless score #running ky.var matches 0..1 run scoreboard players set #running ky.var 1
scoreboard players set #maxtips ky.var 32
scoreboard players set #maxnodes ky.var 8
scoreboard players set #maxhouses ky.var 400
scoreboard players set #2 ky.var 2
scoreboard players set #4 ky.var 4
scoreboard players set #6 ky.var 6
scoreboard players set #10 ky.var 10
scoreboard players set #8 ky.var 8
scoreboard players set #14 ky.var 14
scoreboard players set #90 ky.var 90
schedule function kyoto:pulse 10t replace
tellraw @a [{"text":"Kyoto Gate loaded. ","color":"gold"},{"text":"/function kyoto:gate","color":"yellow"},{"text":" opens a gate where you look.","color":"gray"}]
''')

fn('stop', '''
scoreboard players set #running ky.var 0
tellraw @a {"text":"Kyoto Gate: paused","color":"gold"}
''')

fn('start', '''
scoreboard players set #running ky.var 1
tellraw @a {"text":"Kyoto Gate: growing","color":"gold"}
''')

fn('clear', '''
# Removes every growth marker. Everything already built stays.
kill @e[type=marker,tag=ky.tip]
kill @e[type=marker,tag=ky.plot]
kill @e[type=marker,tag=ky.node]
kill @e[type=marker,tag=ky.probe]
tellraw @a {"text":"Kyoto Gate: growth cleared (buildings kept)","color":"gold"}
''')

fn('status', '''
execute store result score #tips ky.var if entity @e[type=marker,tag=ky.tip]
execute store result score #nodes ky.var if entity @e[type=marker,tag=ky.node]
execute store result score #houses ky.var if entity @e[type=marker,tag=ky.house]
execute store result score #plots ky.var if entity @e[type=marker,tag=ky.plot]
tellraw @a [{"text":"Kyoto Gate: ","color":"gold"},{"score":{"name":"#nodes","objective":"ky.var"},"color":"yellow"},{"text":" gates, ","color":"gray"},{"score":{"name":"#tips","objective":"ky.var"},"color":"yellow"},{"text":" growing streets, ","color":"gray"},{"score":{"name":"#houses","objective":"ky.var"},"color":"yellow"},{"text":" houses, ","color":"gray"},{"score":{"name":"#plots","objective":"ky.var"},"color":"yellow"},{"text":" plots waiting","color":"gray"}]
''')

# ---------------------------------------------------------------------------
# Heartbeat: every 10 ticks, a few tips grow and a couple of plots try to build
# ---------------------------------------------------------------------------
fn('pulse', '''
schedule function kyoto:pulse 10t replace
execute unless score #running ky.var matches 1 run return 0
execute store result score #tips ky.var if entity @e[type=marker,tag=ky.tip]
execute store result score #nodes ky.var if entity @e[type=marker,tag=ky.node]
execute store result score #houses ky.var if entity @e[type=marker,tag=ky.house]
execute as @e[type=marker,tag=ky.node] at @s run function kyoto:node/tick
execute as @e[type=marker,tag=ky.tip,sort=random,limit=4] at @s run function kyoto:tip/step
execute as @e[type=marker,tag=ky.plot,sort=random,limit=2] at @s run function kyoto:plot/try
''')

# ---------------------------------------------------------------------------
# Gates (nodes)
# ---------------------------------------------------------------------------
fn('gate', '''
# Run by a player: opens a gate 4 blocks ahead, facing the way the player looks.
execute store result score #yaw ky.var run data get entity @s Rotation[0]
scoreboard players add #yaw ky.var 405
scoreboard players operation #yaw ky.var /= #90 ky.var
scoreboard players operation #yaw ky.var %= #4 ky.var
scoreboard players set #c0 ky.var 100
execute at @s rotated ~ 0 positioned ^ ^ ^4 align xyz positioned ~.5 ~ ~.5 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.node","ky.new"]}
execute as @e[type=marker,tag=ky.node,tag=ky.new] at @s run function kyoto:node/init
tellraw @a {"text":"A gate opens.","color":"gold","italic":true}
''')

fn('node/init', '''
# As a new node. #yaw = direction (0-3), #c0 = charge its streets start with.
tag @s remove ky.new
execute if score #c0 ky.var matches 100.. run tag @s add ky.heart
scoreboard players operation @s ky.dir = #yaw ky.var
scoreboard players operation @s ky.charge = #c0 ky.var
scoreboard players set @s ky.step 0
function kyoto:tip/face
execute at @s run function kyoto:node/torii
# the first two streets run straight through the torii, both ways
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players operation #c ky.var = @s ky.charge
execute at @s run summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
scoreboard players add #d ky.var 2
scoreboard players operation #d ky.var %= #4 ky.var
execute at @s run summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
''')

fn('node/torii', '''
# At the node, rotated along its axis
fill ^-3 ^ ^ ^3 ^7 ^ air replace #kyoto:clearable
function kyoto:util/rot
function kyoto:node/torii_place with storage kyoto:tmp
''')

fn('node/torii_place', '''
$place template kyoto:torii ^-3 ^ ^ $(rot)
''')

fn('node/init_tip', '''
# As a new tip. #d = direction, #c = charge
tag @s remove ky.new
scoreboard players operation @s ky.dir = #d ky.var
scoreboard players operation @s ky.charge = #c ky.var
scoreboard players set @s ky.step 0
scoreboard players set @s ky.turns 0
scoreboard players set @s ky.bridge 0
scoreboard players set @s ky.cross 0
function kyoto:tip/face
''')

fn('node/emit', '''
# A gate keeps sending out new streets for a while (up to 6), each in a random direction
execute if score #tips ky.var >= #maxtips ky.var run return 0
execute if score @s ky.step matches 8.. run return 0
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..6 run return 0
scoreboard players add @s ky.step 1
execute store result score #d ky.var run random value 0..3
scoreboard players operation #c ky.var = @s ky.charge
summon marker ~ ~ ~ {Tags:["ky.tip","ky.new","ky.fresh"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
execute as @e[type=marker,tag=ky.fresh] at @s positioned ^ ^ ^2 positioned over motion_blocking_no_leaves if block ~ ~-1 ~ #kyoto:path as @e[type=marker,tag=ky.fresh] at @s run function kyoto:tip/turn_right
tag @e[type=marker,tag=ky.fresh] remove ky.fresh
scoreboard players add #tips ky.var 1
''')

fn('node/tick', '''
# The heart gate wants a pagoda once its town has 10 houses within 48 blocks
scoreboard players set #near ky.var 0
execute if entity @s[tag=ky.heart,tag=!ky.has_pagoda,tag=!ky.wants_pagoda] store result score #near ky.var if entity @e[type=marker,tag=ky.house,distance=..48]
execute if score #near ky.var matches 10.. run tag @s add ky.wants_pagoda
function kyoto:node/emit
''')

# ---------------------------------------------------------------------------
# Street tips
# ---------------------------------------------------------------------------
fn('tip/turn_right', '''
scoreboard players add @s ky.dir 1
scoreboard players operation @s ky.dir %= #4 ky.var
function kyoto:tip/face
''')

fn('tip/face', '''
execute if score @s ky.dir matches 0 run tp @s ~ ~ ~ 0 0
execute if score @s ky.dir matches 1 run tp @s ~ ~ ~ 90 0
execute if score @s ky.dir matches 2 run tp @s ~ ~ ~ 180 0
execute if score @s ky.dir matches 3 run tp @s ~ ~ ~ -90 0
''')

fn('tip/step', '''
# One step of a street tip: read the ground ahead and decide how the street continues
scoreboard players add @s ky.step 1
scoreboard players remove @s ky.charge 1
execute if score @s ky.cross matches 1.. run scoreboard players remove @s ky.cross 1
execute if score @s ky.charge matches ..0 run return run function kyoto:tip/die
execute unless loaded ^ ^ ^3 run return 0
scoreboard players set #water ky.var 0
scoreboard players set #blocked ky.var 0
scoreboard players set #street ky.var 0
execute positioned ^ ^ ^1 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.probe"]}
# another street ahead (a junction), or one running alongside 3 blocks over
execute positioned ^3 ^ ^1 positioned over motion_blocking_no_leaves if block ~ ~-1 ~ #kyoto:path run scoreboard players set #street ky.var 2
execute positioned ^-3 ^ ^1 positioned over motion_blocking_no_leaves if block ~ ~-1 ~ #kyoto:path run scoreboard players set #street ky.var 2
execute store result score #y0 ky.var run data get entity @s Pos[1]
execute as @e[type=marker,tag=ky.probe,limit=1] store result score #y1 ky.var run data get entity @s Pos[1]
execute as @e[type=marker,tag=ky.probe,limit=1] at @s if block ~ ~-1 ~ #kyoto:water run scoreboard players set #water ky.var 1
execute as @e[type=marker,tag=ky.probe,limit=1] at @s if block ~ ~-1 ~ #kyoto:path run scoreboard players set #street ky.var 1
execute as @e[type=marker,tag=ky.probe,limit=1] at @s if block ~ ~-1 ~ #kyoto:built unless block ~ ~-1 ~ #kyoto:path run scoreboard players set #blocked ky.var 1
execute as @e[type=marker,tag=ky.probe,limit=1] at @s if block ~ ~-1 ~ #minecraft:logs run scoreboard players set #blocked ky.var 2
kill @e[type=marker,tag=ky.probe]
scoreboard players operation #dy ky.var = #y1 ky.var
scoreboard players operation #dy ky.var -= #y0 ky.var
# street awareness starts once a street has left its parent (branches begin on top of one),
# and pauses while it crosses another street
execute if score @s ky.step matches 5.. if score @s ky.cross matches ..0 if score #street ky.var matches 1 run function kyoto:tip/junction
execute if score #street ky.var matches 9 run return 0
execute if score @s ky.step matches 5.. if score @s ky.cross matches ..0 if score #street ky.var matches 2 run return run function kyoto:tip/turn
execute if score #blocked ky.var matches 2 run return run function kyoto:tip/chop
execute if score #blocked ky.var matches 1 run return run function kyoto:tip/turn
execute if score #water ky.var matches 1 run return run function kyoto:tip/bridge
execute if score #dy ky.var matches 0 run return run function kyoto:tip/walk
execute if score #dy ky.var matches 1..12 run return run function kyoto:tip/climb
execute if score #dy ky.var matches -12..-1 run return run function kyoto:tip/descend
function kyoto:tip/turn
''')

fn('tip/junction', '''
# Met another street: about half the time cross it (a crossroads), otherwise end here (a T)
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..55 run return run scoreboard players set @s ky.cross 6
scoreboard players set #street ky.var 9
function kyoto:tip/die
''')

fn('tip/walk', '''
execute positioned ^ ^ ^1 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
scoreboard players set @s ky.turns 0
scoreboard players set @s ky.bridge 0
execute at @s run function kyoto:tip/pave
execute at @s run function kyoto:tip/extras
''')

fn('tip/climb', '''
# Ground rises steeply: cut a stone staircase up into it
tp @s ^ ^1 ^1
scoreboard players set @s ky.turns 0
function kyoto:util/rot
data modify storage kyoto:tmp stair.facing set from storage kyoto:tmp fwd
execute at @s run function kyoto:tip/stairs
''')

fn('tip/descend', '''
# Ground drops away: build a staircase down on a stone footing
tp @s ^ ^-1 ^1
scoreboard players set @s ky.turns 0
function kyoto:util/rot
data modify storage kyoto:tmp stair.facing set from storage kyoto:tmp back
execute at @s run function kyoto:tip/stairs
''')

fn('tip/stairs', '''
scoreboard players set #w ky.var 0
execute if score @s ky.charge matches 45.. run scoreboard players set #w ky.var 1
execute store result storage kyoto:tmp stair.w int 1 run scoreboard players get #w ky.var
function kyoto:tip/stairs_place with storage kyoto:tmp stair
function kyoto:tip/extras
''')

fn('tip/stairs_place', '''
$fill ^-$(w) ^-2 ^ ^$(w) ^-13 ^ stone_bricks replace #kyoto:fillable
$fill ^-$(w) ^ ^ ^$(w) ^3 ^ air replace #kyoto:diggable
$fill ^-$(w) ^-1 ^ ^$(w) ^-1 ^ stone_brick_stairs[facing=$(facing)]
''')

fn('tip/bridge', '''
# Water ahead: keep the street level and build a bridge across
tp @s ^ ^ ^1
scoreboard players add @s ky.bridge 1
execute if score @s ky.bridge matches 24.. run return run function kyoto:tip/die
execute at @s run function kyoto:tip/bridge_deck
''')

fn('tip/bridge_deck', '''
fill ^-2 ^-1 ^ ^2 ^-1 ^ dark_oak_planks replace #kyoto:fillable
fill ^-1 ^ ^ ^1 ^2 ^ air replace #kyoto:clearable
execute if block ^2 ^ ^ #kyoto:fillable run setblock ^2 ^ ^ dark_oak_fence
execute if block ^-2 ^ ^ #kyoto:fillable run setblock ^-2 ^ ^ dark_oak_fence
scoreboard players operation #p ky.var = @s ky.bridge
scoreboard players operation #p ky.var %= #4 ky.var
execute if score #p ky.var matches 0 run fill ^2 ^-2 ^ ^2 ^-16 ^ dark_oak_log replace #kyoto:fillable
execute if score #p ky.var matches 0 run fill ^-2 ^-2 ^ ^-2 ^-16 ^ dark_oak_log replace #kyoto:fillable
execute if score #p ky.var matches 2 if block ^2 ^1 ^ #kyoto:fillable run setblock ^2 ^1 ^ lantern
''')

fn('tip/chop', '''
# A tree stands in the way: fell it, the street continues next step
fill ^-1 ^-1 ^1 ^1 ^16 ^2 air replace #minecraft:logs
fill ^-3 ^ ^ ^3 ^8 ^4 air replace #minecraft:leaves
''')

fn('tip/turn', '''
# Blocked: turn left or right; three blocked turns in a row and the street ends
scoreboard players add @s ky.turns 1
execute if score @s ky.turns matches 3.. run return run function kyoto:tip/die
execute store result score #r ky.var run random value 0..1
execute if score #r ky.var matches 0 run scoreboard players add @s ky.dir 1
execute if score #r ky.var matches 1 run scoreboard players add @s ky.dir 3
scoreboard players operation @s ky.dir %= #4 ky.var
function kyoto:tip/face
''')

fn('tip/die', '''
# A street that travelled far may take root as a new gate
scoreboard players set #r ky.var 100
execute if score @s ky.step matches 35.. if score #nodes ky.var < #maxnodes ky.var unless entity @e[type=marker,tag=ky.node,distance=..28] store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..30 at @s run function kyoto:tip/root
kill @s
''')

fn('tip/root', '''
scoreboard players operation #yaw ky.var = @s ky.dir
scoreboard players set #c0 ky.var 60
summon marker ~ ~ ~ {Tags:["ky.node","ky.new"]}
execute as @e[type=marker,tag=ky.node,tag=ky.new] at @s run function kyoto:node/init
scoreboard players add #nodes ky.var 1
''')

# ---------------------------------------------------------------------------
# Paving and what grows along the street
# ---------------------------------------------------------------------------
fn('tip/pave', '''
# Charge sets the width: wide near the gate, single stones further out, stepping stones at the edge
execute if score @s ky.charge matches 45.. run return run function kyoto:tip/pave_wide
execute if score @s ky.charge matches 15..44 run return run function kyoto:tip/stone
scoreboard players operation #p ky.var = @s ky.step
scoreboard players operation #p ky.var %= #2 ky.var
execute if score #p ky.var matches 0 run function kyoto:tip/stone
''')

fn('tip/pave_wide', '''
function kyoto:tip/stone
execute positioned ^1 ^ ^ run function kyoto:tip/stone
execute positioned ^-1 ^ ^ run function kyoto:tip/stone
''')

fn('tip/stone', '''
# One paving stone at this column, with footing below and headroom above
execute if block ~ ~-1 ~ #kyoto:built run return 0
fill ~ ~-2 ~ ~ ~-6 ~ stone_bricks replace #kyoto:fillable
fill ~ ~ ~ ~ ~2 ~ air replace #kyoto:diggable
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..38 run return run setblock ~ ~-1 ~ stone_bricks
execute if score #r ky.var matches 39..56 run return run setblock ~ ~-1 ~ andesite
execute if score #r ky.var matches 57..70 run return run setblock ~ ~-1 ~ polished_andesite
execute if score #r ky.var matches 71..84 run return run setblock ~ ~-1 ~ mossy_stone_bricks
execute if score #r ky.var matches 85..93 run return run setblock ~ ~-1 ~ cracked_stone_bricks
setblock ~ ~-1 ~ cobblestone
''')

fn('tip/extras', '''
execute if score @s ky.charge matches 15.. run function kyoto:tip/maybe_toro
execute if score @s ky.charge matches 25.. run function kyoto:tip/maybe_branch
execute if score @s ky.charge matches 18.. run function kyoto:tip/maybe_plot
execute if score @s ky.charge matches 15.. run function kyoto:tip/maybe_sakura
execute if score @s ky.charge matches ..20 run function kyoto:tip/maybe_bamboo
''')

fn('tip/maybe_sakura', '''
# Now and then a cherry tree beside the street, whatever the biome
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..3 run return 0
execute store result score #side ky.var run random value 0..1
execute if score #side ky.var matches 0 positioned ^4 ^ ^ positioned over motion_blocking_no_leaves run function kyoto:deco/street_tree
execute if score #side ky.var matches 1 positioned ^-4 ^ ^ positioned over motion_blocking_no_leaves run function kyoto:deco/street_tree
''')

fn('tip/maybe_bamboo', '''
# Where the town thins out, bamboo groves
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..4 run return 0
execute store result score #side ky.var run random value 0..1
execute if score #side ky.var matches 0 positioned ^5 ^ ^ positioned over motion_blocking_no_leaves if block ~ ~-1 ~ #minecraft:dirt run place feature minecraft:bamboo_some_podzol
execute if score #side ky.var matches 1 positioned ^-5 ^ ^ positioned over motion_blocking_no_leaves if block ~ ~-1 ~ #minecraft:dirt run place feature minecraft:bamboo_some_podzol
''')

fn('deco/street_tree', '''
# Only on natural ground, never on a building or the street
execute unless block ~ ~-1 ~ #minecraft:dirt run return 0
execute if entity @e[type=marker,tag=ky.house,distance=..5] run return 0
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..30 run return run place feature minecraft:cherry_bees_005
place feature minecraft:cherry
''')

fn('deco/garden_tree', '''
# In some larger gardens, a sakura in the middle (the ground under it becomes moss)
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..40 run return 0
execute if block ~ ~-1 ~ #kyoto:water run return 0
execute unless block ~ ~ ~ #kyoto:clearable run return 0
setblock ~ ~-1 ~ moss_block
place feature minecraft:cherry
''')

fn('tip/maybe_toro', '''
# A stone lantern every 7 steps, alternating sides of the street
scoreboard players operation #p ky.var = @s ky.step
scoreboard players operation #p ky.var %= #14 ky.var
execute if score #p ky.var matches 0 positioned ^2 ^ ^ run function kyoto:tip/toro
execute if score #p ky.var matches 7 positioned ^-2 ^ ^ run function kyoto:tip/toro
''')

fn('tip/toro', '''
execute if block ~ ~-1 ~ #kyoto:built run return 0
# no lantern within 2 blocks of another
execute if block ~-2 ~1 ~-2 lantern run return 0
execute if block ~-2 ~1 ~-1 lantern run return 0
execute if block ~-2 ~1 ~ lantern run return 0
execute if block ~-2 ~1 ~1 lantern run return 0
execute if block ~-2 ~1 ~2 lantern run return 0
execute if block ~-1 ~1 ~-2 lantern run return 0
execute if block ~-1 ~1 ~-1 lantern run return 0
execute if block ~-1 ~1 ~ lantern run return 0
execute if block ~-1 ~1 ~1 lantern run return 0
execute if block ~-1 ~1 ~2 lantern run return 0
execute if block ~ ~1 ~-2 lantern run return 0
execute if block ~ ~1 ~-1 lantern run return 0
execute if block ~ ~1 ~1 lantern run return 0
execute if block ~ ~1 ~2 lantern run return 0
execute if block ~1 ~1 ~-2 lantern run return 0
execute if block ~1 ~1 ~-1 lantern run return 0
execute if block ~1 ~1 ~ lantern run return 0
execute if block ~1 ~1 ~1 lantern run return 0
execute if block ~1 ~1 ~2 lantern run return 0
execute if block ~2 ~1 ~-2 lantern run return 0
execute if block ~2 ~1 ~-1 lantern run return 0
execute if block ~2 ~1 ~ lantern run return 0
execute if block ~2 ~1 ~1 lantern run return 0
execute if block ~2 ~1 ~2 lantern run return 0
fill ~ ~-2 ~ ~ ~-6 ~ stone_bricks replace #kyoto:fillable
fill ~ ~ ~ ~ ~3 ~ air replace #kyoto:diggable
setblock ~ ~-1 ~ polished_andesite
setblock ~ ~ ~ stone_brick_wall
setblock ~ ~1 ~ lantern
setblock ~ ~2 ~ stone_brick_slab
''')

fn('tip/maybe_branch', '''
execute if score #tips ky.var >= #maxtips ky.var run return 0
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..9 run return 0
scoreboard players operation #c ky.var = @s ky.charge
scoreboard players operation #c ky.var *= #8 ky.var
scoreboard players operation #c ky.var /= #10 ky.var
scoreboard players operation #d ky.var = @s ky.dir
execute store result score #r ky.var run random value 0..1
execute if score #r ky.var matches 0 run scoreboard players add #d ky.var 1
execute if score #r ky.var matches 1 run scoreboard players add #d ky.var 3
scoreboard players operation #d ky.var %= #4 ky.var
summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
scoreboard players add #tips ky.var 1
''')

fn('tip/maybe_plot', '''
# Houses follow the street: sometimes mark a plot beside it, facing away from the street
execute if entity @e[type=marker,tag=ky.wants_pagoda,distance=..40] unless entity @e[type=marker,tag=ky.pagoda] run return run function kyoto:tip/maybe_pagoda
execute if score #houses ky.var >= #maxhouses ky.var run return 0
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..30 run return 0
scoreboard players operation #c ky.var = @s ky.charge
scoreboard players operation #d ky.var = @s ky.dir
execute store result score #side ky.var run random value 0..1
execute if score #side ky.var matches 0 run scoreboard players add #d ky.var 3
execute if score #side ky.var matches 1 run scoreboard players add #d ky.var 1
scoreboard players operation #d ky.var %= #4 ky.var
execute if score @s ky.charge matches 45.. if score #side ky.var matches 0 positioned ^3 ^ ^ run function kyoto:tip/plot_here
execute if score @s ky.charge matches 45.. if score #side ky.var matches 1 positioned ^-3 ^ ^ run function kyoto:tip/plot_here
execute if score @s ky.charge matches ..44 if score #side ky.var matches 0 positioned ^2 ^ ^ run function kyoto:tip/plot_here
execute if score @s ky.charge matches ..44 if score #side ky.var matches 1 positioned ^-2 ^ ^ run function kyoto:tip/plot_here
''')

fn('tip/maybe_pagoda', '''
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..25 run return 0
scoreboard players operation #c ky.var = @s ky.charge
scoreboard players operation #d ky.var = @s ky.dir
execute store result score #side ky.var run random value 0..1
execute if score #side ky.var matches 0 run scoreboard players add #d ky.var 3
execute if score #side ky.var matches 1 run scoreboard players add #d ky.var 1
scoreboard players operation #d ky.var %= #4 ky.var
execute if score #side ky.var matches 0 positioned ^3 ^ ^ run summon marker ~ ~ ~ {Tags:["ky.plot","ky.pagoda","ky.new"]}
execute if score #side ky.var matches 1 positioned ^-3 ^ ^ run summon marker ~ ~ ~ {Tags:["ky.plot","ky.pagoda","ky.new"]}
execute as @e[type=marker,tag=ky.plot,tag=ky.new] at @s run function kyoto:plot/init
''')

fn('tip/plot_here', '''
summon marker ~ ~ ~ {Tags:["ky.plot","ky.new"]}
execute as @e[type=marker,tag=ky.plot,tag=ky.new] at @s run function kyoto:plot/init
''')

# ---------------------------------------------------------------------------
# Houses
# ---------------------------------------------------------------------------
fn('plot/init', '''
tag @s remove ky.new
scoreboard players operation @s ky.dir = #d ky.var
scoreboard players operation @s ky.charge = #c ky.var
function kyoto:tip/face
''')

fn('plot/try', '''
# One attempt per plot: pick a house, try to fit it, and the plot is gone either way
execute if entity @s[tag=ky.pagoda] run return run function kyoto:plot/try_pagoda
execute if entity @s[tag=ky.garden] run return run function kyoto:plot/try_garden
execute unless loaded ^ ^ ^12 run return 0
execute store result score #w ky.var run random value 0..2
scoreboard players operation #w ky.var *= #2 ky.var
scoreboard players add #w ky.var 5
execute store result score #hd ky.var run random value 5..6
data modify storage kyoto:tmp house.f set value 1
execute if score @s ky.charge matches 50.. store result storage kyoto:tmp house.f int 1 run random value 1..2
execute store result storage kyoto:tmp house.seed int 1 run random value 1..2000000000
execute store result score #r ky.var run random value 0..3
execute if score #r ky.var matches 0 run data modify storage kyoto:tmp house.front set value "koshi"
execute if score #r ky.var matches 1 run data modify storage kyoto:tmp house.front set value "koshi_r"
execute if score #r ky.var matches 2 run data modify storage kyoto:tmp house.front set value "shop"
execute if score #r ky.var matches 3 run data modify storage kyoto:tmp house.front set value "kura"
data modify storage kyoto:tmp house.roof set value "tile"
execute store result storage kyoto:tmp house.win int 1 run random value 0..3
execute store result score #r ky.var run random value 1..100
data modify storage kyoto:tmp house.wall set value "spruce_planks"
execute if score #r ky.var matches 36..65 run data modify storage kyoto:tmp house.wall set value "white_terracotta"
execute if score #r ky.var matches 66..85 run data modify storage kyoto:tmp house.wall set value "packed_mud"
execute if score #r ky.var matches 86..100 run data modify storage kyoto:tmp house.wall set value "stripped_spruce_wood"
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..15 run data modify storage kyoto:tmp house.roof set value "copper"
function kyoto:util/rot
data modify storage kyoto:tmp house.rot set from storage kyoto:tmp rot
scoreboard players set #ok ky.var 0
execute store result score #ok ky.var run function kyoto:gen/plot
execute if score #ok ky.var matches 0 if score @s ky.charge matches 20.. run function kyoto:plot/garden_chance
execute if score #ok ky.var matches 1 run function kyoto:plot/back_garden
kill @s
''')

fn('plot/garden_chance', '''
# Where a house would not fit, the space often becomes a garden instead
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..65 run function kyoto:plot/garden
''')

fn('plot/back_garden', '''
# Sometimes a small garden grows behind a new house (a tsuboniwa)
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..30 run return 0
execute positioned ^ ^ ^9 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.plot","ky.garden","ky.new"]}
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players operation #c ky.var = @s ky.charge
execute as @e[type=marker,tag=ky.plot,tag=ky.new] at @s run function kyoto:plot/init
''')

fn('plot/garden', '''
# As a plot: pick a garden style and fit the largest size that goes (7x6 down to 3x3)
execute store result score #r ky.var run random value 1..100
data modify storage kyoto:tmp garden.kind set value "kare"
execute if score #r ky.var matches 41..75 run data modify storage kyoto:tmp garden.kind set value "moss"
execute if score #r ky.var matches 76..100 run data modify storage kyoto:tmp garden.kind set value "pond"
data modify storage kyoto:tmp garden.small set value "kare"
execute if score #r ky.var matches 51..100 run data modify storage kyoto:tmp garden.small set value "moss"
execute store result storage kyoto:tmp garden.v int 1 run random value 0..2
function kyoto:util/rot
data modify storage kyoto:tmp garden.rot set from storage kyoto:tmp rot
function kyoto:gen/garden
''')

fn('deco/ground', '''
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
''')

fn('plot/try_garden', '''
execute unless loaded ^ ^ ^10 run return 0
function kyoto:plot/garden
kill @s
''')

fn('plot/try_pagoda', '''
execute unless loaded ^ ^ ^14 run return 0
function kyoto:util/rot
data modify storage kyoto:tmp house.rot set from storage kyoto:tmp rot
scoreboard players set #ok ky.var 0
execute store result score #ok ky.var run function kyoto:gen/try_pagoda with storage kyoto:tmp house
execute if score #ok ky.var matches 1 as @e[type=marker,tag=ky.wants_pagoda] run tag @s add ky.has_pagoda
execute if score #ok ky.var matches 1 as @e[type=marker,tag=ky.has_pagoda] run tag @s remove ky.wants_pagoda
execute if score #ok ky.var matches 1 run tellraw @a {"text":"Somewhere above the roofs, a pagoda rises.","color":"gold","italic":true}
kill @s
''')

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
fn('util/rot', '''
# From @s ky.dir: template rotation and the compass names of forward and back
execute if score @s ky.dir matches 0 run data merge storage kyoto:tmp {rot:"none",fwd:"south",back:"north"}
execute if score @s ky.dir matches 1 run data merge storage kyoto:tmp {rot:"clockwise_90",fwd:"west",back:"east"}
execute if score @s ky.dir matches 2 run data merge storage kyoto:tmp {rot:"180",fwd:"north",back:"south"}
execute if score @s ky.dir matches 3 run data merge storage kyoto:tmp {rot:"counterclockwise_90",fwd:"east",back:"west"}
''')


# ---------------------------------------------------------------------------
# Data for v6 (generated): mystery wares, keeper names, the seed
# ---------------------------------------------------------------------------
import random as _random

LIME = '#b8f62a'


def _glyph(text, color=LIME):
    return '{text:"%s",font:"minecraft:alt",color:"%s",italic:false}' % (text, color)


def _offers():
    rng = _random.Random(2017)
    wares = ['paper', 'amethyst_shard', 'echo_shard', 'glass_bottle', 'clock', 'compass', 'ender_eye',
             'heart_of_the_sea', 'prismarine_crystals', 'slime_ball', 'bone', 'nautilus_shell', 'glow_ink_sac',
             'honeycomb', 'chorus_fruit', 'lime_stained_glass']
    currencies = ['pink_petals', 'bamboo', 'cherry_sapling', 'rotten_flesh', 'string', 'feather', 'kelp',
                  'amethyst_shard', 'sweet_berries', 'cocoa_beans', 'bone_meal', 'flint']
    secrets = ['purpose unknown', 'do not open', 'wmcmo', 'exzachly', 'it is still dormant', 'the gate remembers']
    syll = ['ka', 'zu', 'mo', 'ri', 'ne', 'qa', 'vo', 'ti', 'xe', 'lu', 'so', 'yi', 'ha', 'pe', 'wo', 'gi']
    word = lambda n: ''.join(rng.choice(syll) for _ in range(n))
    out = []
    for i, item in enumerate(wares):
        name = 'wmcmo' if item == 'lime_stained_glass' else word(rng.randint(2, 3))
        lore = [_glyph(secrets[i % len(secrets)], 'gray'), _glyph(word(rng.randint(3, 5)), 'dark_gray')]
        sell = ('{id:"minecraft:%s",count:1,components:{"minecraft:custom_name":%s,"minecraft:lore":[%s],'
                '"minecraft:enchantment_glint_override":true}}') % (item, _glyph(name), ','.join(lore))
        buy = '{id:"minecraft:emerald",count:%d}' % rng.randint(1, 9)
        buy_b = '{id:"minecraft:%s",count:%d}' % (rng.choice(currencies), rng.randint(1, 6))
        out.append('{buy:%s,buyB:%s,sell:%s,maxUses:%d,rewardExp:0b,xp:0}' % (buy, buy_b, sell, rng.randint(1, 4)))
    return out


def _names():
    rng = _random.Random(26)
    syll = ['ka', 'zu', 'mo', 'ri', 'ne', 'qa', 'vo', 'ti', 'xe', 'lu', 'so', 'yi', 'ha']
    return [_glyph(''.join(rng.choice(syll) for _ in range(rng.randint(2, 3)))) for _ in range(10)]


_OFFERS = _offers()
_NAMES = _names()

fn('shop/pool', 'data modify storage kyoto:pool offers set value [%s]\ndata modify storage kyoto:pool names set value [%s]\n'
   % (','.join(_OFFERS), ','.join(_NAMES)))

_CATS = ['tabby', 'black', 'red', 'siamese', 'british_shorthair', 'calico', 'persian', 'ragdoll', 'white', 'jellie', 'all_black']
fn('life/cat', 'execute store result score #r ky.var run random value 0..%d\n' % (len(_CATS) - 1) + ''.join(
    'execute if score #r ky.var matches %d run summon cat ~ ~ ~ {variant:"minecraft:%s",PersistenceRequired:1b,Tags:["ky.life"]}\n'
    % (i, c) for i, c in enumerate(_CATS)))

SEED_COMPONENTS = {
    'minecraft:custom_name': {'text': 'Torii Seed', 'color': 'gold', 'italic': False},
    'minecraft:lore': [
        {'text': 'Hold right-click to plant a gate.', 'color': 'gray', 'italic': False},
        {'text': 'purpose unknown', 'font': 'minecraft:alt', 'color': LIME, 'italic': False},
    ],
    'minecraft:consumable': {'consume_seconds': 2.0, 'animation': 'block', 'sound': 'minecraft:block.amethyst_block.chime',
                             'has_consume_particles': False},
    'minecraft:enchantment_glint_override': True,
    'minecraft:max_stack_size': 16,
}



# ===========================================================================
# v6: shops, haunted growth, districts, building types, interiors, life, the seed, settings
# (definitions below replace earlier ones with the same name)
# ===========================================================================
import random as _random

tag('block', 'kyoto:open', [
    'minecraft:air', 'minecraft:cave_air', '#minecraft:flowers', '#minecraft:saplings', '#minecraft:leaves',
    'minecraft:short_grass', 'minecraft:tall_grass', 'minecraft:fern', 'minecraft:large_fern', 'minecraft:dead_bush',
    'minecraft:snow', 'minecraft:vine', 'minecraft:glow_lichen', 'minecraft:sweet_berry_bush', 'minecraft:moss_carpet',
    'minecraft:pink_petals',
])
FILES['data/kyoto/tags/block/built.json'] = FILES['data/kyoto/tags/block/built.json'].replace(
    '"minecraft:packed_mud",', '"minecraft:packed_mud",\n    "minecraft:bamboo_planks",\n    "minecraft:white_concrete",\n    "minecraft:dark_oak_wood",')

# ---------------------------------------------------------------------------
# Setup: settings now survive /reload
# ---------------------------------------------------------------------------
fn('load', """
scoreboard objectives add ky.charge dummy
scoreboard objectives add ky.dir dummy
scoreboard objectives add ky.step dummy
scoreboard objectives add ky.turns dummy
scoreboard objectives add ky.bridge dummy
scoreboard objectives add ky.cross dummy
scoreboard objectives add ky.var dummy
execute unless score #running ky.var matches 0..1 run scoreboard players set #running ky.var 1
execute unless score #rate ky.var matches 1.. run scoreboard players set #rate ky.var 4
execute unless score #haunted ky.var matches 0..1 run scoreboard players set #haunted ky.var 0
execute unless score #maxhouses ky.var matches 1.. run scoreboard players set #maxhouses ky.var 400
scoreboard players set #maxtips ky.var 32
scoreboard players set #maxnodes ky.var 8
scoreboard players set #maxlife ky.var 40
scoreboard players set #2 ky.var 2
scoreboard players set #4 ky.var 4
scoreboard players set #6 ky.var 6
scoreboard players set #8 ky.var 8
scoreboard players set #10 ky.var 10
scoreboard players set #14 ky.var 14
scoreboard players set #90 ky.var 90
function kyoto:shop/pool
schedule function kyoto:pulse 10t replace
tellraw @a [{"text":"Kyoto Gate loaded. ","color":"gold"},{"text":"[settings]","color":"yellow","click_event":{"action":"run_command","command":"/function kyoto:settings"},"hover_event":{"action":"show_text","value":"Open the Kyoto Gate settings"}}]
""")

fn('gate', """
# Run by a player (or by eating a Torii Seed): opens a gate 4 blocks ahead, facing the way they look.
execute store result score #yaw ky.var run data get entity @s Rotation[0]
scoreboard players add #yaw ky.var 405
scoreboard players operation #yaw ky.var /= #90 ky.var
scoreboard players operation #yaw ky.var %= #4 ky.var
scoreboard players set #c0 ky.var 100
scoreboard players set #variant ky.var 0
execute at @s rotated ~ 0 positioned ^ ^ ^4 align xyz positioned ~.5 ~ ~.5 positioned over motion_blocking_no_leaves run summon marker ~ ~ ~ {Tags:["ky.node","ky.new"]}
execute as @e[type=marker,tag=ky.node,tag=ky.new] at @s run function kyoto:node/init
tellraw @a {"text":"A gate opens.","color":"gold","italic":true}
""")

# ---------------------------------------------------------------------------
# Heartbeat: speed setting, haunted mode (grows only at night, only where nobody is near)
# ---------------------------------------------------------------------------
fn('pulse', """
schedule function kyoto:pulse 10t replace
execute unless score #running ky.var matches 1 run return 0
scoreboard players set #awake ky.var 1
execute if score #haunted ky.var matches 1 run function kyoto:haunt/check
execute if score #awake ky.var matches 0 run return 0
execute store result score #tips ky.var if entity @e[type=marker,tag=ky.tip]
execute store result score #nodes ky.var if entity @e[type=marker,tag=ky.node]
execute store result score #houses ky.var if entity @e[type=marker,tag=ky.house]
execute store result score #life ky.var if entity @e[tag=ky.life]
execute as @e[type=marker,tag=ky.node] at @s run function kyoto:node/tick
function kyoto:grow/batch
execute if score #rate ky.var matches 4.. run function kyoto:grow/batch
execute if score #rate ky.var matches 8.. run function kyoto:grow/batch
execute if score #rate ky.var matches 8.. run function kyoto:grow/batch
""")

fn('grow/batch', """
execute if score #haunted ky.var matches 0 as @e[type=marker,tag=ky.tip,sort=random,limit=2] at @s run function kyoto:tip/step
execute if score #haunted ky.var matches 1 as @e[type=marker,tag=ky.tip,sort=random,limit=2] at @s unless entity @a[distance=..40] run function kyoto:tip/step
execute if score #haunted ky.var matches 0 as @e[type=marker,tag=ky.plot,sort=random,limit=1] at @s run function kyoto:plot/try
execute if score #haunted ky.var matches 1 as @e[type=marker,tag=ky.plot,sort=random,limit=1] at @s unless entity @a[distance=..40] run function kyoto:plot/try
""")

fn('haunt/check', """
# Haunted mode: the town only grows between dusk and dawn
execute store result score #time ky.var run time query daytime
execute unless score #time ky.var matches 12500..23500 run scoreboard players set #awake ky.var 0
""")

# ---------------------------------------------------------------------------
# Gates and districts
# ---------------------------------------------------------------------------
fn('util/district_of', """
# Sets #district from @s tags: 0 town, 1 stream, 2 senbon torii, 3 shop alley
scoreboard players set #district ky.var 0
execute if entity @s[tag=ky.stream] run scoreboard players set #district ky.var 1
execute if entity @s[tag=ky.senbon] run scoreboard players set #district ky.var 2
execute if entity @s[tag=ky.alley] run scoreboard players set #district ky.var 3
""")

fn('node/init', """
# As a new node. #yaw = direction, #c0 = charge, #variant = district (0 town, 1 stream, 2 senbon, 3 alley)
tag @s remove ky.new
execute if score #c0 ky.var matches 100.. run tag @s add ky.heart
execute if score #variant ky.var matches 1 run tag @s add ky.stream
execute if score #variant ky.var matches 2 run tag @s add ky.senbon
execute if score #variant ky.var matches 3 run tag @s add ky.alley
scoreboard players operation @s ky.dir = #yaw ky.var
scoreboard players operation @s ky.charge = #c0 ky.var
execute if entity @s[tag=ky.alley] run scoreboard players set @s ky.charge 40
scoreboard players set @s ky.step 0
function kyoto:tip/face
execute if entity @s[tag=ky.senbon] run return run function kyoto:node/init_senbon
execute at @s run function kyoto:node/torii
function kyoto:util/district_of
# the first two streets run straight through the torii, both ways
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players operation #c ky.var = @s ky.charge
execute at @s run summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
scoreboard players add #d ky.var 2
scoreboard players operation #d ky.var %= #4 ky.var
execute at @s run summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
""")

fn('node/init_senbon', """
# Senbon torii: no gate of its own, one path that becomes a tunnel of torii up to a shrine
scoreboard players set @s ky.step 99
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players set #c ky.var 70
scoreboard players set #district ky.var 2
execute at @s run summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
tellraw @a {"text":"Somewhere, a line of torii begins to climb.","color":"gold","italic":true}
""")

fn('node/init_tip', """
# As a new tip. #d = direction, #c = charge, #district = what kind of street it is
tag @s remove ky.new
scoreboard players operation @s ky.dir = #d ky.var
scoreboard players operation @s ky.charge = #c ky.var
scoreboard players set @s ky.step 0
scoreboard players set @s ky.turns 0
scoreboard players set @s ky.bridge 0
scoreboard players set @s ky.cross 0
execute if score #district ky.var matches 1 run tag @s add ky.stream
execute if score #district ky.var matches 2 run tag @s add ky.senbon
execute if score #district ky.var matches 3 run tag @s add ky.alley
function kyoto:tip/face
""")

fn('node/emit', """
# A gate keeps sending out new streets for a while (up to 8), each in a random direction
execute if score #tips ky.var >= #maxtips ky.var run return 0
execute if score @s ky.step matches 8.. run return 0
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..6 run return 0
scoreboard players add @s ky.step 1
execute store result score #d ky.var run random value 0..3
scoreboard players operation #c ky.var = @s ky.charge
function kyoto:util/district_of
summon marker ~ ~ ~ {Tags:["ky.tip","ky.new","ky.fresh"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
execute as @e[type=marker,tag=ky.fresh] at @s positioned ^ ^ ^2 positioned over motion_blocking_no_leaves if block ~ ~-1 ~ #kyoto:path as @e[type=marker,tag=ky.fresh] at @s run function kyoto:tip/turn_right
tag @e[type=marker,tag=ky.fresh] remove ky.fresh
scoreboard players add #tips ky.var 1
""")

fn('tip/root', """
# A street that ran far takes root as a new gate, sometimes of a special kind
scoreboard players operation #yaw ky.var = @s ky.dir
scoreboard players set #c0 ky.var 60
scoreboard players set #variant ky.var 0
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 46..65 run scoreboard players set #variant ky.var 1
execute if score #r ky.var matches 66..85 run scoreboard players set #variant ky.var 2
execute if score #r ky.var matches 86..100 run scoreboard players set #variant ky.var 3
summon marker ~ ~ ~ {Tags:["ky.node","ky.new"]}
execute as @e[type=marker,tag=ky.node,tag=ky.new] at @s run function kyoto:node/init
scoreboard players add #nodes ky.var 1
""")

fn('tip/die', """
# A senbon path ends at its shrine; a town street that travelled far may take root as a new gate
execute if entity @s[tag=ky.senbon] at @s run function kyoto:senbon/shrine
scoreboard players set #r ky.var 100
execute unless entity @s[tag=ky.senbon] if score @s ky.step matches 35.. if score #nodes ky.var < #maxnodes ky.var unless entity @e[type=marker,tag=ky.node,distance=..28] store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..30 at @s run function kyoto:tip/root
kill @s
""")

fn('tip/walk', """
execute positioned ^ ^ ^1 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
scoreboard players set @s ky.turns 0
scoreboard players set @s ky.bridge 0
execute at @s run function kyoto:tip/pave
execute if entity @s[tag=ky.stream] at @s positioned ^-2 ^-1 ^-1 run function kyoto:stream/cell
execute at @s run function kyoto:tip/extras
""")

fn('tip/extras', """
execute if entity @s[tag=ky.senbon] run return run function kyoto:senbon/extras
execute if score @s ky.charge matches 15.. run function kyoto:tip/maybe_toro
execute if score @s ky.charge matches 25.. unless entity @s[tag=ky.alley] run function kyoto:tip/maybe_branch
execute if score @s ky.charge matches 18.. run function kyoto:tip/maybe_plot
execute if score @s ky.charge matches 15.. unless entity @s[tag=ky.alley] run function kyoto:tip/maybe_sakura
execute if score @s ky.charge matches ..20 run function kyoto:tip/maybe_bamboo
""")

fn('tip/maybe_toro', """
# Stone lanterns: every 7 steps alternating sides; every 4 in shop alleys; streams keep theirs off the water side
scoreboard players operation #p ky.var = @s ky.step
execute if entity @s[tag=ky.alley] run return run function kyoto:tip/toro_alley
scoreboard players operation #p ky.var %= #14 ky.var
execute if score #p ky.var matches 0 positioned ^2 ^ ^ run function kyoto:tip/toro
execute if score #p ky.var matches 7 unless entity @s[tag=ky.stream] positioned ^-2 ^ ^ run function kyoto:tip/toro
execute if score #p ky.var matches 7 if entity @s[tag=ky.stream] positioned ^2 ^ ^ run function kyoto:tip/toro
""")

fn('tip/toro_alley', """
scoreboard players operation #p ky.var %= #8 ky.var
execute if score #p ky.var matches 0 positioned ^2 ^ ^ run function kyoto:tip/toro
execute if score #p ky.var matches 4 positioned ^-2 ^ ^ run function kyoto:tip/toro
""")

fn('tip/maybe_branch', """
execute if score #tips ky.var >= #maxtips ky.var run return 0
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..9 run return 0
scoreboard players operation #c ky.var = @s ky.charge
scoreboard players operation #c ky.var *= #8 ky.var
scoreboard players operation #c ky.var /= #10 ky.var
scoreboard players operation #d ky.var = @s ky.dir
execute store result score #r ky.var run random value 0..1
execute if score #r ky.var matches 0 run scoreboard players add #d ky.var 1
execute if score #r ky.var matches 1 run scoreboard players add #d ky.var 3
scoreboard players operation #d ky.var %= #4 ky.var
function kyoto:util/district_of
summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
scoreboard players add #tips ky.var 1
""")

fn('tip/maybe_plot', """
# Houses follow the street: sometimes mark a plot beside it, facing away from the street.
# Shop alleys fill up faster.
execute if entity @e[type=marker,tag=ky.wants_pagoda,distance=..40] unless entity @e[type=marker,tag=ky.pagoda] run return run function kyoto:tip/maybe_pagoda
execute if score #houses ky.var >= #maxhouses ky.var run return 0
execute store result score #r ky.var run random value 1..100
execute if entity @s[tag=ky.alley] if score #r ky.var matches 31..55 run scoreboard players set #r ky.var 1
execute unless score #r ky.var matches 1..30 run return 0
scoreboard players operation #c ky.var = @s ky.charge
scoreboard players operation #d ky.var = @s ky.dir
execute store result score #side ky.var run random value 0..1
execute if score #side ky.var matches 0 run scoreboard players add #d ky.var 3
execute if score #side ky.var matches 1 run scoreboard players add #d ky.var 1
scoreboard players operation #d ky.var %= #4 ky.var
execute if score @s ky.charge matches 45.. if score #side ky.var matches 0 positioned ^3 ^ ^ run function kyoto:tip/plot_here
execute if score @s ky.charge matches 45.. if score #side ky.var matches 1 positioned ^-3 ^ ^ run function kyoto:tip/plot_here
execute if score @s ky.charge matches ..44 if score #side ky.var matches 0 positioned ^2 ^ ^ run function kyoto:tip/plot_here
execute if score @s ky.charge matches ..44 if score #side ky.var matches 1 positioned ^-2 ^ ^ run function kyoto:tip/plot_here
""")

fn('tip/plot_here', """
summon marker ~ ~ ~ {Tags:["ky.plot","ky.new"]}
execute if entity @s[tag=ky.alley] run tag @e[type=marker,tag=ky.plot,tag=ky.new] add ky.alley
execute as @e[type=marker,tag=ky.plot,tag=ky.new] at @s run function kyoto:plot/init
""")

fn('tip/junction', """
# Met another street: about half the time cross it (a crossroads), otherwise end here (a T)
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..55 run return run function kyoto:tip/cross
scoreboard players set #street ky.var 9
function kyoto:tip/die
""")

fn('tip/cross', """
# Crossing: corner houses may claim the corners on this side, with a second front facing the crossing street
scoreboard players set @s ky.cross 6
execute if score #houses ky.var >= #maxhouses ky.var run return 0
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..45 run return 0
scoreboard players operation #c ky.var = @s ky.charge
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players add #d ky.var 3
scoreboard players operation #d ky.var %= #4 ky.var
execute positioned ^3 ^ ^-5 run summon marker ~ ~ ~ {Tags:["ky.plot","ky.corner_l","ky.new"]}
execute as @e[type=marker,tag=ky.plot,tag=ky.new] at @s run function kyoto:plot/init
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players add #d ky.var 1
scoreboard players operation #d ky.var %= #4 ky.var
execute positioned ^-3 ^ ^-5 run summon marker ~ ~ ~ {Tags:["ky.plot","ky.corner_r","ky.new"]}
execute as @e[type=marker,tag=ky.plot,tag=ky.new] at @s run function kyoto:plot/init
""")

# ---------------------------------------------------------------------------
# Stream district: a stone-lined channel beside the street (laid one step behind the tip,
# only where it can be closed in on every side, so the water never runs off)
# ---------------------------------------------------------------------------
fn('stream/cell', """
execute unless block ~ ~ ~ #kyoto:diggable run return 0
execute if block ~ ~ ~ #kyoto:open run return 0
execute if block ^ ^ ^1 #kyoto:open run return 0
execute if block ^ ^ ^-1 #kyoto:open run return 0
execute if block ^-1 ^ ^ #kyoto:open run setblock ^-1 ^ ^ stone_bricks
execute if block ^-1 ^ ^ #kyoto:diggable run setblock ^-1 ^ ^ stone_bricks
execute if block ^1 ^ ^ #kyoto:open run setblock ^1 ^ ^ stone_bricks
execute unless block ~ ~-1 ~ #kyoto:water run setblock ~ ~-1 ~ stone_bricks
fill ~ ~1 ~ ~ ~3 ~ air replace #kyoto:clearable
setblock ~ ~ ~ water
""")

# ---------------------------------------------------------------------------
# Senbon torii: a torii every two steps, a shrine where the path ends
# ---------------------------------------------------------------------------
fn('senbon/extras', """
scoreboard players operation #p ky.var = @s ky.step
scoreboard players operation #p ky.var %= #2 ky.var
execute if score #p ky.var matches 0 run function kyoto:senbon/torii
""")

fn('senbon/torii', """
fill ^2 ^-1 ^ ^2 ^-8 ^ stone_bricks replace #kyoto:fillable
fill ^-2 ^-1 ^ ^-2 ^-8 ^ stone_bricks replace #kyoto:fillable
fill ^-3 ^ ^ ^3 ^5 ^ air replace #kyoto:clearable
function kyoto:util/rot
function kyoto:senbon/torii_place with storage kyoto:tmp
""")

fn('senbon/torii_place', """
$place template kyoto:torii_small ^-3 ^ ^ $(rot)
""")

fn('senbon/shrine', """
fill ^-3 ^ ^ ^3 ^6 ^6 air replace #kyoto:diggable
fill ^-2 ^-2 ^1 ^2 ^-9 ^5 stone_bricks replace #kyoto:fillable
function kyoto:util/rot
function kyoto:senbon/shrine_place with storage kyoto:tmp
tellraw @a {"text":"At the top of the torii, a small shrine.","color":"gold","italic":true}
""")

fn('senbon/shrine_place', """
$place template kyoto:hokora ^-3 ^-1 ^ $(rot)
""")

# ---------------------------------------------------------------------------
# Houses: every building type, and what happens after one is built
# ---------------------------------------------------------------------------
fn('plot/try', """
# One attempt per plot: pick a house, try to fit it, and the plot is gone either way
execute if entity @s[tag=ky.pagoda] run return run function kyoto:plot/try_pagoda
execute if entity @s[tag=ky.garden] run return run function kyoto:plot/try_garden
execute unless loaded ^ ^ ^12 run return 0
execute store result score #w ky.var run random value 0..2
scoreboard players operation #w ky.var *= #2 ky.var
scoreboard players add #w ky.var 5
execute store result score #hd ky.var run random value 5..6
data modify storage kyoto:tmp house.f set value 1
execute if score @s ky.charge matches 50.. store result storage kyoto:tmp house.f int 1 run random value 1..2
execute store result storage kyoto:tmp house.seed int 1 run random value 1..2000000000
execute store result storage kyoto:tmp house.win int 1 run random value 0..3
# street front: 0 lattice, 1 lattice (door right), 2 shop, 3 storehouse, 4 tea house. Alleys are all shops.
execute store result score #front ky.var run random value 0..4
execute if entity @s[tag=ky.alley] run scoreboard players set #front ky.var 2
execute if score #front ky.var matches 0 run data modify storage kyoto:tmp house.front set value "koshi"
execute if score #front ky.var matches 1 run data modify storage kyoto:tmp house.front set value "koshi_r"
execute if score #front ky.var matches 2 run data modify storage kyoto:tmp house.front set value "shop"
execute if score #front ky.var matches 3 run data modify storage kyoto:tmp house.front set value "kura"
execute if score #front ky.var matches 4 run data modify storage kyoto:tmp house.front set value "engawa"
# inside follows the front
execute store result score #r ky.var run random value 1..100
data modify storage kyoto:tmp house.interior set value "home"
execute if score #r ky.var matches 61..100 run data modify storage kyoto:tmp house.interior set value "kitchen"
execute if score #front ky.var matches 2 run data modify storage kyoto:tmp house.interior set value "shop"
execute if score #front ky.var matches 3 run data modify storage kyoto:tmp house.interior set value "store"
execute if score #front ky.var matches 4 run data modify storage kyoto:tmp house.interior set value "tea"
# roof: tile, sometimes copper or hip-and-gable
execute store result score #r ky.var run random value 1..100
data modify storage kyoto:tmp house.roof set value "tile"
execute if score #r ky.var matches 1..15 run data modify storage kyoto:tmp house.roof set value "copper"
execute if score #r ky.var matches 16..30 run data modify storage kyoto:tmp house.roof set value "irimoya"
# wall finish (storehouses are always white plaster)
execute store result score #r ky.var run random value 1..100
data modify storage kyoto:tmp house.wall set value "spruce_planks"
execute if score #r ky.var matches 36..65 run data modify storage kyoto:tmp house.wall set value "white_terracotta"
execute if score #r ky.var matches 66..85 run data modify storage kyoto:tmp house.wall set value "packed_mud"
execute if score #r ky.var matches 86..100 run data modify storage kyoto:tmp house.wall set value "stripped_spruce_wood"
execute if score #front ky.var matches 3 run data modify storage kyoto:tmp house.wall set value "white_terracotta"
# corner houses get a second front on the side facing the crossing street
scoreboard players set #corner ky.var 0
execute if entity @s[tag=ky.corner_l] run scoreboard players set #corner ky.var 1
execute if entity @s[tag=ky.corner_r] run scoreboard players set #corner ky.var 2
function kyoto:util/rot
data modify storage kyoto:tmp house.rot set from storage kyoto:tmp rot
scoreboard players set #ok ky.var 0
execute store result score #ok ky.var run function kyoto:gen/plot
execute if score #ok ky.var matches 0 if score @s ky.charge matches 20.. unless entity @s[tag=ky.alley] run function kyoto:plot/garden_chance
execute if score #ok ky.var matches 1 run function kyoto:plot/after_house
kill @s
""")

fn('plot/after_house', """
# Just built: a shopkeeper for shops, sometimes a cat or a neighbour, sometimes a garden out back
execute if score #front ky.var matches 2 positioned ^ ^ ^2 run function kyoto:shop/keeper
execute if score #life ky.var < #maxlife ky.var store result score #r ky.var run random value 1..100
execute if score #life ky.var < #maxlife ky.var if score #r ky.var matches 1..10 positioned ^ ^ ^ run function kyoto:life/cat
execute if score #life ky.var < #maxlife ky.var if score #r ky.var matches 11..15 positioned ^ ^ ^ run function kyoto:life/villager
function kyoto:plot/back_garden
""")

# ---------------------------------------------------------------------------
# Weird shops: a keeper whose wares are named in a script nobody reads
# ---------------------------------------------------------------------------
fn('shop/keeper', """
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
""")

fn('shop/pick', """
execute store result storage kyoto:tmp shop.i int 1 run random value 0..15
function kyoto:shop/pick_m with storage kyoto:tmp shop
""")

fn('shop/pick_m', """
$data modify storage kyoto:tmp shop.offers append from storage kyoto:pool offers[$(i)]
""")

fn('shop/name', """
execute store result storage kyoto:tmp shop.i int 1 run random value 0..9
function kyoto:shop/name_m with storage kyoto:tmp shop
""")

fn('shop/name_m', """
$data modify entity @e[type=villager,tag=ky.newkeeper,limit=1] CustomName set from storage kyoto:pool names[$(i)]
""")

# ---------------------------------------------------------------------------
# Life
# ---------------------------------------------------------------------------
fn('life/villager', """
summon villager ~ ~ ~ {PersistenceRequired:1b,Tags:["ky.life"],VillagerData:{type:"minecraft:plains",profession:"minecraft:none",level:1}}
""")

# ---------------------------------------------------------------------------
# The Torii Seed (survival), settings, uninstall
# ---------------------------------------------------------------------------
FILES['data/kyoto/recipe/torii_seed.json'] = json.dumps({
    'type': 'minecraft:crafting_shaped',
    'category': 'misc',
    'pattern': ['BBB', 'RLR', 'R R'],
    'key': {'B': 'minecraft:polished_blackstone', 'R': 'minecraft:red_dye', 'L': 'minecraft:lantern'},
    'result': {'id': 'minecraft:red_dye', 'count': 1, 'components': SEED_COMPONENTS},
}, indent=2) + '\n'

FILES['data/kyoto/advancement/plant_gate.json'] = json.dumps({
    'criteria': {'plant': {'trigger': 'minecraft:consume_item', 'conditions': {'item': {'items': 'minecraft:red_dye'}}}},
    'rewards': {'function': 'kyoto:seed/plant'},
}, indent=2) + '\n'

fn('seed/plant', """
# Ran as the player who just used a Torii Seed (red dye is only edible when it is one)
advancement revoke @s only kyoto:plant_gate
function kyoto:gate
""")

fn('give_seed', """
give @s red_dye[custom_name={text:"Torii Seed",color:"gold",italic:false},lore=[{text:"Hold right-click to plant a gate.",color:"gray",italic:false},{text:"purpose unknown",font:"minecraft:alt",color:"#b8f62a",italic:false}],consumable={consume_seconds:2.0f,animation:"block",sound:"minecraft:block.amethyst_block.chime",has_consume_particles:false},enchantment_glint_override=true,max_stack_size=16]
""")

def _menu_btn(label, fn_name, hover):
    return ('{"text":"[%s]","color":"yellow","click_event":{"action":"run_command","command":"/function kyoto:%s"},'
            '"hover_event":{"action":"show_text","value":"%s"}}' % (label, fn_name, hover))

fn('settings', """
tellraw @s {"text":"--- Kyoto Gate ---","color":"gold"}
tellraw @s [{"text":"Growth  ","color":"gray"},%s,{"text":" "},%s,{"text":" "},%s]
tellraw @s [{"text":"Mode    ","color":"gray"},%s,{"text":" "},%s]
tellraw @s [{"text":"Size    ","color":"gray"},%s,{"text":" "},%s,{"text":" "},%s]
tellraw @s [{"text":"        ","color":"gray"},%s,{"text":" "},%s,{"text":" "},%s,{"text":" "},%s]
tellraw @s [{"text":"        ","color":"gray"},%s,{"text":" "},%s]
""" % (
    _menu_btn('slow', 'set/speed_slow', 'A few steps at a time'),
    _menu_btn('normal', 'set/speed_normal', 'The default pace'),
    _menu_btn('fast', 'set/speed_fast', 'Twice the pace'),
    _menu_btn('always', 'set/mode_always', 'Grows all the time, even while you watch'),
    _menu_btn('haunted', 'set/mode_haunted', 'Only at night, only where nobody stands'),
    _menu_btn('village', 'set/size_small', 'Stops at about 120 houses'),
    _menu_btn('town', 'set/size_medium', 'Stops at about 400 houses'),
    _menu_btn('city', 'set/size_large', 'Stops at about 1200 houses'),
    _menu_btn('pause', 'stop', 'Stop growing'),
    _menu_btn('resume', 'start', 'Keep growing'),
    _menu_btn('status', 'status', 'Count gates, streets and houses'),
    _menu_btn('get seed', 'give_seed', 'A Torii Seed: hold right-click to plant a gate'),
    _menu_btn('clear growth', 'clear', 'Remove growth markers, keep every building'),
    _menu_btn('uninstall', 'uninstall', 'Remove all scores and markers so the pack can be deleted'),
))

for name, cmd, msg in (
    ('set/speed_slow', 'scoreboard players set #rate ky.var 2', 'slow'),
    ('set/speed_normal', 'scoreboard players set #rate ky.var 4', 'normal'),
    ('set/speed_fast', 'scoreboard players set #rate ky.var 8', 'fast'),
    ('set/mode_always', 'scoreboard players set #haunted ky.var 0', 'grows all the time'),
    ('set/mode_haunted', 'scoreboard players set #haunted ky.var 1', 'haunted: only at night, only unwatched'),
    ('set/size_small', 'scoreboard players set #maxhouses ky.var 120', 'village (about 120 houses)'),
    ('set/size_medium', 'scoreboard players set #maxhouses ky.var 400', 'town (about 400 houses)'),
    ('set/size_large', 'scoreboard players set #maxhouses ky.var 1200', 'city (about 1200 houses)'),
):
    fn(name, cmd + '\ntellraw @s {"text":"Kyoto Gate: %s","color":"gold"}\n' % msg)

fn('uninstall', """
# Leaves every building; removes everything the pack keeps in the world so the folder can be deleted
schedule clear kyoto:pulse
kill @e[type=marker,tag=ky.tip]
kill @e[type=marker,tag=ky.plot]
kill @e[type=marker,tag=ky.node]
kill @e[type=marker,tag=ky.probe]
kill @e[type=marker,tag=ky.house]
kill @e[type=marker,tag=ky.offering]
scoreboard objectives remove ky.charge
scoreboard objectives remove ky.dir
scoreboard objectives remove ky.step
scoreboard objectives remove ky.turns
scoreboard objectives remove ky.bridge
scoreboard objectives remove ky.cross
scoreboard objectives remove ky.var
data remove storage kyoto:tmp house
data remove storage kyoto:pool offers
tellraw @a {"text":"Kyoto Gate removed its markers and scores. Delete the datapack folder, then /reload.","color":"gold"}
""")


# Test gates: open a district directly instead of waiting for one to take root
for _name, _variant in (('stream', 1), ('senbon', 2), ('alley', 3)):
    fn('gate/' + _name, FILES['data/kyoto/function/gate.mcfunction']
       .replace('scoreboard players set #c0 ky.var 100\nscoreboard players set #variant ky.var 0',
                'scoreboard players set #c0 ky.var 60\nscoreboard players set #variant ky.var %d' % _variant))



# ===========================================================================
# v7: cushions, trees that follow the biome's season, survival offerings, night mode
# ===========================================================================

# Biomes by season, for trees
tag('worldgen/biome', 'kyoto:spring', ['minecraft:cherry_grove', 'minecraft:meadow', 'minecraft:flower_forest'])
tag('worldgen/biome', 'kyoto:autumn', ['minecraft:dappled_forest'])
tag('worldgen/biome', 'kyoto:snowy', [
    'minecraft:snowy_plains', 'minecraft:snowy_taiga', 'minecraft:snowy_slopes', 'minecraft:grove', 'minecraft:ice_spikes',
    'minecraft:frozen_peaks', 'minecraft:jagged_peaks', 'minecraft:frozen_river', 'minecraft:snowy_beach',
])

fn('deco/tree', """
# Plant the tree that belongs to this biome's season: sakura in spring biomes, poplars in the
# autumn forest, spruce in snow, pale oak in the pale garden, and pine (the garden evergreen) elsewhere
execute if biome ~ ~ ~ #kyoto:spring run return run function kyoto:deco/tree_spring
execute if biome ~ ~ ~ #kyoto:autumn run return run function kyoto:deco/tree_autumn
execute if biome ~ ~ ~ #kyoto:snowy run return run place feature minecraft:spruce
execute if biome ~ ~ ~ minecraft:pale_garden run return run place feature minecraft:pale_oak
place feature minecraft:pine
""")

fn('deco/tree_spring', """
execute store result score #r ky.var run random value 1..100
execute if score #r ky.var matches 1..30 run return run place feature minecraft:cherry_bees_005
place feature minecraft:cherry
""")

fn('deco/tree_autumn', """
execute store result score #r ky.var run random value 1..3
execute if score #r ky.var matches 1 run return run place feature minecraft:red_poplar
execute if score #r ky.var matches 2 run return run place feature minecraft:orange_poplar
place feature minecraft:yellow_poplar
""")

fn('tip/maybe_sakura', """
# Now and then a tree beside the street (a little less often than before)
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..2 run return 0
execute store result score #side ky.var run random value 0..1
execute if score #side ky.var matches 0 positioned ^4 ^ ^ positioned over motion_blocking_no_leaves run function kyoto:deco/street_tree
execute if score #side ky.var matches 1 positioned ^-4 ^ ^ positioned over motion_blocking_no_leaves run function kyoto:deco/street_tree
""")

fn('deco/street_tree', """
# Only on natural ground, never on a building or the street
execute unless block ~ ~-1 ~ #minecraft:dirt run return 0
execute if entity @e[type=marker,tag=ky.house,distance=..5] run return 0
function kyoto:deco/tree
""")

fn('deco/garden_tree', """
# In some larger gardens, a tree in the middle (the ground under it becomes moss)
execute store result score #r ky.var run random value 1..100
execute unless score #r ky.var matches 1..40 run return 0
execute if block ~ ~-1 ~ #kyoto:water run return 0
execute unless block ~ ~ ~ #kyoto:clearable run return 0
setblock ~ ~-1 ~ moss_block
function kyoto:deco/tree
""")

# ---------------------------------------------------------------------------
# Cushions (entities): a zabuton on the tatami, colour picked at random
# ---------------------------------------------------------------------------
fn('life/cushion', """
# At the air cell above the floor. The cushion rests on the floor block below and remembers it.
execute unless block ~ ~ ~ air run return 0
execute align xyz run summon marker ~ ~ ~ {Tags:["ky.cpos"]}
execute as @e[type=marker,tag=ky.cpos,limit=1] run function kyoto:life/cushion_pos
kill @e[type=marker,tag=ky.cpos]
execute store result score #r ky.var run random value 1..6
data modify storage kyoto:tmp cushion.color set value "purple"
execute if score #r ky.var matches 2 run data modify storage kyoto:tmp cushion.color set value "red"
execute if score #r ky.var matches 3 run data modify storage kyoto:tmp cushion.color set value "blue"
execute if score #r ky.var matches 4 run data modify storage kyoto:tmp cushion.color set value "brown"
execute if score #r ky.var matches 5 run data modify storage kyoto:tmp cushion.color set value "orange"
execute if score #r ky.var matches 6 run data modify storage kyoto:tmp cushion.color set value "green"
execute align xyz positioned ~.5 ~ ~.5 run function kyoto:life/cushion_m with storage kyoto:tmp cushion
""")

fn('life/cushion_pos', """
execute store result storage kyoto:tmp cushion.x int 1 run data get entity @s Pos[0]
execute store result storage kyoto:tmp cushion.z int 1 run data get entity @s Pos[2]
execute store result score #cy ky.var run data get entity @s Pos[1]
scoreboard players remove #cy ky.var 1
execute store result storage kyoto:tmp cushion.by int 1 run scoreboard players get #cy ky.var
""")

fn('life/cushion_m', """
$summon cushion ~ ~ ~ {color:"$(color)",block_pos:[I;$(x),$(by),$(z)],Tags:["ky.life"]}
""")

# ---------------------------------------------------------------------------
# Survival rules: the town grows freely until its pagoda rises; after that it needs gold,
# offered in the box inside the pagoda (1 ingot = 1 blessing, 1 block = 10). A house costs one.
# ---------------------------------------------------------------------------
fn('offer/check', """
# As the offering marker, at the box
execute unless block ~ ~ ~ barrel run return 0
scoreboard players set #gi ky.var 0
scoreboard players set #gb ky.var 0
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:0b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:0b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:1b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:1b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:2b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:2b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:3b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:3b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:4b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:4b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:5b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:5b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:6b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:6b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:7b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:7b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:8b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:8b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:9b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:9b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:10b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:10b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:11b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:11b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:12b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:12b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:13b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:13b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:14b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:14b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:15b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:15b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:16b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:16b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:17b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:17b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:18b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:18b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:19b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:19b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:20b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:20b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:21b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:21b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:22b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:22b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:23b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:23b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:24b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:24b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:25b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:25b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:26b,id:"minecraft:gold_ingot"}].count
scoreboard players operation #gi ky.var += #s ky.var
execute store result score #s ky.var run data get block ~ ~ ~ Items[{Slot:26b,id:"minecraft:gold_block"}].count
scoreboard players operation #gb ky.var += #s ky.var
execute if score #gi ky.var matches 0 if score #gb ky.var matches 0 run return 0
data remove block ~ ~ ~ Items[{id:"minecraft:gold_ingot"}]
data remove block ~ ~ ~ Items[{id:"minecraft:gold_block"}]
scoreboard players operation #gift ky.var = #gi ky.var
scoreboard players operation #gb ky.var *= #10 ky.var
scoreboard players operation #gift ky.var += #gb ky.var
scoreboard players operation #fuel ky.var += #gift ky.var
scoreboard players set #warned ky.var 0
playsound minecraft:block.bell.use block @a[distance=..48] ~ ~ ~ 1 1
particle minecraft:cherry_leaves ~ ~2 ~ 2 1.5 2 0 40
particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.02 15
title @a[distance=..16] actionbar [{"text":"The gate accepts your offering  ","color":"gold"},{"text":"+","color":"yellow"},{"score":{"name":"#gift","objective":"ky.var"},"color":"yellow"},{"text":"   blessings: ","color":"gray"},{"score":{"name":"#fuel","objective":"ky.var"},"color":"yellow"}]
""")

fn('offer/gate', """
# Called each pulse: with survival rules on and a pagoda standing, growth waits for blessings
execute unless score #rules ky.var matches 1 run return 0
# (keyed to the offering box, so pagodas built before boxes existed keep growing freely)
execute unless entity @e[type=marker,tag=ky.offering] run return 0
execute if score #fuel ky.var matches 1.. run return 0
scoreboard players set #awake ky.var 0
execute unless score #warned ky.var matches 1 run tellraw @a [{"text":"The town rests. ","color":"gold","italic":true},{"text":"Offer gold in the box inside the pagoda to wake it.","color":"gray","italic":true}]
scoreboard players set #warned ky.var 1
""")

fn('pulse', """
schedule function kyoto:pulse 10t replace
execute unless score #running ky.var matches 1 run return 0
execute as @e[type=marker,tag=ky.offering] at @s run function kyoto:offer/check
scoreboard players set #awake ky.var 1
execute if score #night ky.var matches 1 run function kyoto:haunt/check
function kyoto:offer/gate
execute if score #awake ky.var matches 0 run return 0
execute store result score #tips ky.var if entity @e[type=marker,tag=ky.tip]
execute store result score #nodes ky.var if entity @e[type=marker,tag=ky.node]
execute store result score #houses ky.var if entity @e[type=marker,tag=ky.house]
execute store result score #life ky.var if entity @e[tag=ky.life]
execute as @e[type=marker,tag=ky.node] at @s run function kyoto:node/tick
function kyoto:grow/batch
execute if score #rate ky.var matches 4.. run function kyoto:grow/batch
execute if score #rate ky.var matches 8.. run function kyoto:grow/batch
execute if score #rate ky.var matches 8.. run function kyoto:grow/batch
""")

fn('grow/batch', """
execute as @e[type=marker,tag=ky.tip,sort=random,limit=2] at @s run function kyoto:tip/step
execute as @e[type=marker,tag=ky.plot,sort=random,limit=1] at @s run function kyoto:plot/try
""")

fn('haunt/check', """
# Night mode: the town only grows between dusk and dawn (you can still watch it happen)
execute store result score #time ky.var run time query daytime
execute unless score #time ky.var matches 12500..23500 run scoreboard players set #awake ky.var 0
""")

FILES['data/kyoto/function/load.mcfunction'] = FILES['data/kyoto/function/load.mcfunction'].replace(
    'execute unless score #haunted ky.var matches 0..1 run scoreboard players set #haunted ky.var 0\n',
    'execute unless score #night ky.var matches 0..1 run scoreboard players set #night ky.var 0\n'
    'execute unless score #rules ky.var matches 0..1 run scoreboard players set #rules ky.var 1\n'
    'execute unless score #fuel ky.var matches -2147483648.. run scoreboard players set #fuel ky.var 0\n')

# a house built under survival rules spends a blessing; seating comes with home and tea interiors
FILES['data/kyoto/function/plot/after_house.mcfunction'] = (
    '# Just built: spend a blessing (once the pagoda stands), then keeper, life and garden\n'
    'execute if score #rules ky.var matches 1 if entity @e[type=marker,tag=ky.offering] run scoreboard players remove #fuel ky.var 1\n'
    + FILES['data/kyoto/function/plot/after_house.mcfunction'].split('\n', 1)[1])
FILES['data/kyoto/function/plot/try.mcfunction'] = FILES['data/kyoto/function/plot/try.mcfunction'].replace(
    '# roof: tile, sometimes copper or hip-and-gable',
    'scoreboard players set #cush ky.var 0\n'
    'execute if data storage kyoto:tmp house{interior:"home"} run scoreboard players set #cush ky.var 1\n'
    'execute if data storage kyoto:tmp house{interior:"tea"} run scoreboard players set #cush ky.var 1\n'
    '# roof: tile, sometimes copper or hip-and-gable')

# The seed: a torii in the grid. Polished blackstone lintel, red concrete pillars,
# a lantern hanging under the lintel, and a cherry sapling planted between the pillars.
FILES['data/kyoto/recipe/torii_seed.json'] = json.dumps({
    'type': 'minecraft:crafting_shaped',
    'category': 'misc',
    'pattern': ['BBB', 'RLR', 'RSR'],
    'key': {'B': 'minecraft:polished_blackstone', 'R': 'minecraft:red_concrete', 'L': 'minecraft:lantern',
            'S': 'minecraft:cherry_sapling'},
    'result': {'id': 'minecraft:red_dye', 'count': 1, 'components': SEED_COMPONENTS},
}, indent=2) + '\n'

# settings: night mode instead of haunted, survival rules toggle, blessings in status
fn('set/mode_always', 'scoreboard players set #night ky.var 0\ntellraw @s {"text":"Kyoto Gate: grows all the time","color":"gold"}\n')
fn('set/mode_night', 'scoreboard players set #night ky.var 1\ntellraw @s {"text":"Kyoto Gate: grows only at night","color":"gold"}\n')
fn('set/rules_on', 'scoreboard players set #rules ky.var 1\ntellraw @s {"text":"Kyoto Gate: survival rules on (after the pagoda, growth needs gold offerings)","color":"gold"}\n')
fn('set/rules_off', 'scoreboard players set #rules ky.var 0\ntellraw @s {"text":"Kyoto Gate: endless growth (no offerings needed)","color":"gold"}\n')
FILES.pop('data/kyoto/function/set/mode_haunted.mcfunction', None)
FILES['data/kyoto/function/settings.mcfunction'] = (
    FILES['data/kyoto/function/settings.mcfunction']
    .replace('[haunted]', '[night]').replace('kyoto:set/mode_haunted', 'kyoto:set/mode_night')
    .replace('Only at night, only where nobody stands', 'Grows only between dusk and dawn')
    .replace('tellraw @s [{"text":"Size    "',
             'tellraw @s [{"text":"Rules   ","color":"gray"},%s,{"text":" "},%s]\ntellraw @s [{"text":"Size    "'
             % (_menu_btn('survival', 'set/rules_on', 'After the pagoda rises, the town needs gold offered inside it'),
                _menu_btn('endless', 'set/rules_off', 'Grows without offerings'))))
fn('status', FILES['data/kyoto/function/status.mcfunction'] +
   'tellraw @a [{"text":"Blessings left: ","color":"gray"},{"score":{"name":"#fuel","objective":"ky.var"},"color":"yellow"}]\n')



# ===========================================================================
# v8: streets leave trails; a quiet town sprouts new side streets from them (and offerings wake it)
# ===========================================================================
FILES['data/kyoto/function/load.mcfunction'] = FILES['data/kyoto/function/load.mcfunction'].replace(
    'scoreboard players set #14 ky.var 14\n', 'scoreboard players set #12 ky.var 12\nscoreboard players set #14 ky.var 14\n')

fn('tip/extras', FILES['data/kyoto/function/tip/extras.mcfunction'].replace(
    'execute if entity @s[tag=ky.senbon] run return run function kyoto:senbon/extras\n',
    'execute if entity @s[tag=ky.senbon] run return run function kyoto:senbon/extras\n'
    '# every 12 steps, leave a trail marker the town can sprout from later\n'
    'scoreboard players operation #p ky.var = @s ky.step\n'
    'scoreboard players operation #p ky.var %= #12 ky.var\n'
    'execute if score #p ky.var matches 0 run function kyoto:tip/trail\n'))

fn('tip/trail', """
scoreboard players operation #d ky.var = @s ky.dir
scoreboard players operation #c ky.var = @s ky.charge
function kyoto:util/district_of
summon marker ~ ~ ~ {Tags:["ky.trail","ky.new"]}
execute as @e[type=marker,tag=ky.trail,tag=ky.new] run function kyoto:tip/trail_init
""")

fn('tip/trail_init', """
tag @s remove ky.new
scoreboard players operation @s ky.dir = #d ky.var
scoreboard players operation @s ky.charge = #c ky.var
execute if score #district ky.var matches 1 run tag @s add ky.stream
execute if score #district ky.var matches 3 run tag @s add ky.alley
""")

fn('grow/sprout', """
# A quiet town: a side street sprouts from a random point it has already grown through
execute if score #houses ky.var >= #maxhouses ky.var run return 0
execute if score #tips ky.var >= #maxtips ky.var run return 0
execute store result score #trails ky.var if entity @e[type=marker,tag=ky.trail]
execute if score #trails ky.var matches 1.. as @e[type=marker,tag=ky.trail,sort=random,limit=1] at @s run return run function kyoto:grow/sprout_here
# towns grown before trails existed: let a gate send streets out again
execute as @e[type=marker,tag=ky.node,sort=random,limit=1] run scoreboard players set @s ky.step 0
""")

fn('grow/sprout_here', """
# As a trail marker, on the street: start a street at right angles to it, with enough life for houses
scoreboard players operation #d ky.var = @s ky.dir
execute store result score #r ky.var run random value 0..1
execute if score #r ky.var matches 0 run scoreboard players add #d ky.var 1
execute if score #r ky.var matches 1 run scoreboard players add #d ky.var 3
scoreboard players operation #d ky.var %= #4 ky.var
scoreboard players set #c ky.var 50
execute if score @s ky.charge matches 51.. run scoreboard players operation #c ky.var = @s ky.charge
function kyoto:util/district_of
summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}
execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip
scoreboard players add #tips ky.var 1
kill @s
""")

fn('pulse', FILES['data/kyoto/function/pulse.mcfunction'].replace(
    'execute as @e[type=marker,tag=ky.node] at @s run function kyoto:node/tick\n',
    'execute as @e[type=marker,tag=ky.node] at @s run function kyoto:node/tick\n'
    'execute if score #tips ky.var matches ..3 run function kyoto:grow/sprout\n'
    '# keep the trail count bounded\n'
    'execute store result score #trails ky.var if entity @e[type=marker,tag=ky.trail]\n'
    'execute if score #trails ky.var matches 301.. run kill @e[type=marker,tag=ky.trail,sort=random,limit=1]\n'))

# an accepted offering wakes the town at once
fn('offer/check', FILES['data/kyoto/function/offer/check.mcfunction'].replace(
    'scoreboard players set #warned ky.var 0\n',
    'scoreboard players set #warned ky.var 0\n'
    'execute store result score #tips ky.var if entity @e[type=marker,tag=ky.tip]\n'
    'function kyoto:grow/sprout\nfunction kyoto:grow/sprout\nfunction kyoto:grow/sprout\n'))

fn('uninstall', FILES['data/kyoto/function/uninstall.mcfunction'].replace(
    'kill @e[type=marker,tag=ky.offering]\n', 'kill @e[type=marker,tag=ky.offering]\nkill @e[type=marker,tag=ky.trail]\n'))
fn('clear', FILES['data/kyoto/function/clear.mcfunction'].replace(
    'kill @e[type=marker,tag=ky.probe]\n', 'kill @e[type=marker,tag=ky.probe]\nkill @e[type=marker,tag=ky.trail]\n'))



# ===========================================================================
# v9: more torii: more gates, torii at the mouth of new lanes, small neighbourhood shrines
# ===========================================================================
FILES['data/kyoto/function/load.mcfunction'] = FILES['data/kyoto/function/load.mcfunction'].replace(
    'scoreboard players set #maxnodes ky.var 8\n', 'scoreboard players set #maxnodes ky.var 24\n')

fn('tip/die', FILES['data/kyoto/function/tip/die.mcfunction']
   .replace('if score @s ky.step matches 35..', 'if score @s ky.step matches 25..')
   .replace('execute if score #r ky.var matches 1..30 at @s run function kyoto:tip/root',
            'execute if score #r ky.var matches 1..40 at @s run function kyoto:tip/root'))

# about one in five sprouted lanes starts under a small torii
fn('grow/sprout_here', FILES['data/kyoto/function/grow/sprout_here.mcfunction'].replace(
    'summon marker ~ ~ ~ {Tags:["ky.tip","ky.new"]}\n'
    'execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip\n',
    'summon marker ~ ~ ~ {Tags:["ky.tip","ky.new","ky.sprouted"]}\n'
    'execute as @e[type=marker,tag=ky.tip,tag=ky.new] at @s run function kyoto:node/init_tip\n'
    'execute store result score #r ky.var run random value 1..100\n'
    'execute if score #r ky.var matches 1..20 as @e[type=marker,tag=ky.sprouted] at @s positioned ^ ^ ^3 positioned over motion_blocking_no_leaves run function kyoto:senbon/torii\n'
    'tag @e[type=marker,tag=ky.sprouted] remove ky.sprouted\n'))

# about one plot in twenty becomes a small shrine with its own torii
fn('plot/try', FILES['data/kyoto/function/plot/try.mcfunction'].replace(
    'execute unless loaded ^ ^ ^12 run return 0\n',
    'execute unless loaded ^ ^ ^12 run return 0\n'
    'scoreboard players set #ok ky.var 0\n'
    'execute store result score #r ky.var run random value 1..100\n'
    'execute if score #r ky.var matches 1..5 if score @s ky.charge matches 25.. unless entity @s[tag=ky.alley] '
    'store result score #ok ky.var run function kyoto:plot/shrine\n'
    'execute if score #r ky.var matches 1..5 if score #ok ky.var matches 1 run return run kill @s\n', 1))

fn('plot/shrine', """
# As a plot: a hokora set back from the street, a torii on the approach. Returns 1 if built.
scoreboard players set #ok ky.var 0
execute store result score #blocked ky.var run function kyoto:gen/gcheck_5x5
execute if score #blocked ky.var matches 1 run return 0
fill ^-3 ^ ^ ^3 ^7 ^6 air replace #kyoto:diggable
fill ^-2 ^-2 ^1 ^2 ^-9 ^5 stone_bricks replace #kyoto:fillable
function kyoto:util/rot
function kyoto:senbon/shrine_place with storage kyoto:tmp
function kyoto:senbon/torii
execute positioned ^ ^ ^3 run summon marker ~ ~ ~ {Tags:["ky.house"]}
return 1
""")


def main():
    for rel, text in FILES.items():
        path = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
    print(f'{len(FILES)} files written')


if __name__ == '__main__':
    main()
