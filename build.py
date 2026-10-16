"""Generates the Kyoto Gate datapack's buildings and size-specific functions.

Writes into kyoto_gate/data/kyoto/:
  structure/torii.nbt
  structure/house/{body,front,roof,deco}_*.nbt   -- house parts, all in one shared frame
  function/gen/*.mcfunction                       -- per-size overlap checks and builders

House frame (before rotation): x = width along the street, z = depth away from it (z=0 is the
street-facing wall), y = 0 is the floor. Every part template uses the same offset (frame -1,0,-1
is template 0,0,0) and the same size, so parts placed at one position with one rotation line up.
Eaves sit at z=-1 / z=d and x=-1 / x=w: that ring is the soft margin neighbours may overlap.

Run:  python build.py
"""
import gzip
import os
import random
import shutil
import struct

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'kyoto_gate', 'data', 'kyoto')
DATA_VERSION = 5023  # Minecraft 26.3

WIDTHS = (5, 7, 9)
DEPTHS = (5, 6)
FLOORS = (1, 2)
FRONTS = ('koshi', 'koshi_r', 'shop', 'kura', 'engawa')
ROOFS = ('tile', 'copper', 'irimoya')
WINDOW_LAYOUTS = 4
GARDEN_SIZES = ((7, 6), (5, 5), (5, 4), (3, 3))   # tried largest first
GARDEN_KINDS = ('kare', 'moss', 'pond')
GARDEN_VARIANTS = 3


# ---------------------------------------------------------------------------
# NBT writer (just the tag types structure files need)
# ---------------------------------------------------------------------------
class Int(int):
    pass


def _str(s):
    b = s.encode('utf-8')
    return struct.pack('>H', len(b)) + b


def _payload(v):
    if isinstance(v, Int):
        return 3, struct.pack('>i', v)
    if isinstance(v, str):
        return 8, _str(v)
    if isinstance(v, dict):
        out = b''
        for k, item in v.items():
            t, p = _payload(item)
            out += bytes([t]) + _str(k) + p
        return 10, out + b'\x00'
    if isinstance(v, list):
        if not v:
            return 9, bytes([0]) + struct.pack('>i', 0)
        types = [_payload(x) for x in v]
        return 9, bytes([types[0][0]]) + struct.pack('>i', len(v)) + b''.join(p for _, p in types)
    raise TypeError(type(v))


def write_nbt(path, root):
    t, p = _payload(root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with gzip.open(path, 'wb') as f:
        f.write(bytes([t]) + _str('') + p)


# ---------------------------------------------------------------------------
# Template builder
# ---------------------------------------------------------------------------
class Tpl:
    def __init__(self, size, offset=(0, 0, 0)):
        self.size = size
        self.off = offset
        self.blocks = {}

    def set(self, x, y, z, block, **props):
        p = (x + self.off[0], y + self.off[1], z + self.off[2])
        if not all(0 <= p[i] < self.size[i] for i in range(3)):
            raise ValueError(f'{block} at frame {(x, y, z)} is outside the template')
        self.blocks[p] = (block, tuple(sorted((k, str(v).lower()) for k, v in props.items())))

    def fill(self, x0, y0, z0, x1, y1, z1, block, **props):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.set(x, y, z, block, **props)

    def save(self, path):
        palette, index, blocks = [], {}, []
        for pos in sorted(self.blocks, key=lambda q: (q[1], q[2], q[0])):
            key = self.blocks[pos]
            if key not in index:
                index[key] = len(palette)
                entry = {'id': 'minecraft:' + key[0]}
                if key[1]:
                    entry['properties'] = {k: v for k, v in key[1]}
                palette.append(entry)
            blocks.append({'pos': [Int(c) for c in pos], 'state': Int(index[key])})
        write_nbt(path, {
            'size': [Int(c) for c in self.size],
            'entities': [],
            'blocks': blocks,
            'palette': palette,
            'DataVersion': Int(DATA_VERSION),
        })


# ---------------------------------------------------------------------------
# House geometry
# ---------------------------------------------------------------------------
def wall_top(f):
    return 4 if f == 1 else 8


def roof_rise(d):
    return (d + 2 + 1) // 2  # rows of stairs per slope, eave row included


def roof_top(d, f):
    return wall_top(f) + 1 + roof_rise(d)


def house_size(w, d):
    # x: -1..w, y: 0..max roof, z: -1..d
    return (w + 2, roof_top(d, 2) + 2, d + 2)


OFF = (1, 0, 1)

WALL_LOW = 'dark_oak_planks'
PLASTER = 'white_terracotta'
POST = 'dark_oak_log'
BEAM = 'stripped_dark_oak_log'
FLOOR = 'spruce_planks'


def body(w, d, f):
    t = Tpl(house_size(w, d), OFF)
    yt = wall_top(f)
    t.fill(0, 0, 0, w - 1, 0, d - 1, FLOOR)
    t.fill(1, 1, 1, w - 2, yt, d - 2, 'air')  # the house clears its own inside
    for x, z in ((0, 0), (w - 1, 0), (0, d - 1), (w - 1, d - 1)):
        t.fill(x, 1, z, x, yt, z, POST, axis='y')
    # side and back walls: dark skirting, plaster, a dark band at each floor line
    for y in range(1, yt + 1):
        if y == 1:
            mat = WALL_LOW
        elif y in (5, yt):
            mat = WALL_LOW
        else:
            mat = PLASTER
        t.fill(0, y, 1, 0, y, d - 2, mat)
        t.fill(w - 1, y, 1, w - 1, y, d - 2, mat)
        t.fill(1, y, d - 1, w - 2, y, d - 1, mat)
    # a timber post in the middle of long side walls
    if d >= 6:
        mid = d // 2
        t.fill(0, 2, mid, 0, yt - 1, mid, BEAM, axis='y')
        t.fill(w - 1, 2, mid, w - 1, yt - 1, mid, BEAM, axis='y')
    # shoji window in the back wall
    cx = (w - 1) // 2
    t.fill(cx - (1 if w >= 7 else 0), 2, d - 1, cx + (1 if w >= 7 else 0), 3, d - 1, 'white_stained_glass_pane')
    if f == 2:
        t.fill(1, 5, 1, w - 2, 5, d - 2, FLOOR)
        t.fill(cx, 6, d - 1, cx, 7, d - 1, 'white_stained_glass_pane')
        # ladder up through a hole at the back-left
        t.fill(1, 1, d - 2, 1, 5, d - 2, 'ladder', facing='north')
    # a little furniture: barrel with a lantern, a pot
    t.set(w - 2, 1, d - 2, 'barrel', facing='up')
    t.set(w - 2, 2, d - 2, 'lantern', hanging='false')
    if w >= 7:
        t.set(w - 3, 1, d - 2, 'decorated_pot', facing='north')
    return t


def front(w, d, f, kind):
    t = Tpl(house_size(w, d), OFF)
    yt = wall_top(f)
    door_x = w - 2 if kind == 'koshi_r' else 1
    # ground-floor beam and upper storey are shared by every front
    t.fill(1, 4, 0, w - 2, 4, 0, WALL_LOW)
    if f == 2:
        t.fill(1, 5, 0, w - 2, 5, 0, WALL_LOW)
        t.fill(1, 6, 0, w - 2, 7, 0, PLASTER)
        t.fill(2, 6, 0, w - 3, 7, 0, 'spruce_fence')  # mushiko slat window
        t.fill(1, 8, 0, w - 2, 8, 0, WALL_LOW)
        # hisashi: the small eave between storeys
        t.fill(-1, 5, -1, w, 5, -1, 'deepslate_tile_stairs', facing='south', half='bottom')
    if kind in ('koshi', 'koshi_r'):
        t.fill(1, 1, 0, w - 2, 3, 0, 'dark_oak_fence')  # koshi lattice
        t.set(door_x, 1, 0, 'dark_oak_door', facing='north', half='lower', hinge='left', open='false')
        t.set(door_x, 2, 0, 'dark_oak_door', facing='north', half='upper', hinge='left', open='false')
        t.set(door_x, 3, 0, WALL_LOW)
    elif kind == 'shop':
        t.fill(1, 3, 0, w - 2, 3, 0, WALL_LOW)
        t.fill(2, 1, 0, w - 3, 1, 0, 'spruce_slab', type='top')  # counter
        t.set(2, 2, 0, 'flower_pot')
        t.set(w - 3, 2, 0, 'lantern', hanging='false')
        for x in range(2, w - 2):
            t.set(x, 3, -1, 'blue_wall_banner', facing='north')  # noren
    elif kind == 'none':
        pass
    elif kind == 'kura':
        t.fill(1, 1, 0, w - 2, 1, 0, WALL_LOW)
        t.fill(1, 2, 0, w - 2, 3, 0, PLASTER)
        cx = (w - 1) // 2
        t.set(cx, 1, 0, 'spruce_door', facing='north', half='lower', hinge='left', open='false')
        t.set(cx, 2, 0, 'spruce_door', facing='north', half='upper', hinge='left', open='false')
        t.set(cx, 3, 0, 'iron_bars')
    return t


def roof_cell(d, f, z):
    """The shallow roof over frame row z: (y, 'bottom' | 'top' | 'full'). The slope rises half a block
    per row (tile slabs, bottom then top), about 27 degrees: low and wide, as Kyoto roofs are."""
    zs = list(range(-1, d + 1))
    n = len(zs)
    i = zs.index(z)
    k = min(i, n - 1 - i)
    kmax = (n - 1) // 2
    y = wall_top(f) + 1 + k // 2
    if k == kmax:
        return y, 'full'
    return y, 'bottom' if k % 2 == 0 else 'top'


def roof_y(d, f, z):
    return roof_cell(d, f, z)[0]


def roof(w, d, f, mat):
    t = Tpl(house_size(w, d), OFF)
    ry = wall_top(f) + 1
    if mat == 'tile':
        full, slab, cap = 'deepslate_tiles', 'deepslate_tile_slab', 'deepslate_tile_wall'
    else:
        full, slab, cap = 'waxed_oxidized_cut_copper', 'waxed_oxidized_cut_copper_slab', 'waxed_oxidized_copper_bulb'
    # the attic is cleared by the roof itself, so nothing from the hillside stays under it
    for z in range(0, d):
        y, _ = roof_cell(d, f, z)
        if y > ry:
            t.fill(1, ry, z, w - 2, y - 1, z, 'air')
    ridge = []
    for z in range(-1, d + 1):
        y, kind = roof_cell(d, f, z)
        if kind == 'full':
            t.fill(-1, y, z, w, y, z, full)
            ridge.append((y, z))
        else:
            t.fill(-1, y, z, w, y, z, slab, type=kind)
        # gable ends: only a low sliver of plaster now
        if 0 <= z <= d - 1:
            for gx in (0, w - 1):
                for gy in range(ry, y):
                    t.set(gx, gy, z, PLASTER)
    for y, z in ridge:
        t.fill(-1, y + 1, z, w, y + 1, z, slab, type='bottom')
        if mat == 'tile':
            t.set(-1, y + 1, z, cap)
            t.set(w, y + 1, z, cap)
    return t

def deco(w, d, f):
    """Every possible small detail; placed with low integrity so each house keeps a random few."""
    t = Tpl(house_size(w, d), OFF)
    yt = wall_top(f)
    for x in range(1, w - 1, 2):
        t.set(x, 4, -1, 'lantern', hanging='true')
    t.set(-1, 2, 1, 'oak_wall_sign', facing='west')
    t.set(1, yt - 1, -1, 'spruce_trapdoor', facing='north', half='top', open='true')
    return t


def windows(w, d, f, v):
    """A random layout of windows at any height, not lined up with floors: shoji, lattice, shutters,
    barred slits, gable windows, lanterns under the side eaves, and sometimes a balcony."""
    rng = random.Random(f'win-{w}-{d}-{f}-{v}')
    t = Tpl(house_size(w, d), OFF)
    yt = wall_top(f)
    out = {'x0': 'west', 'x1': 'east', 'zb': 'south', 'zf': 'north'}

    def wall_cells():
        cells = []
        for z in range(1, d - 1):
            cells += [('x0', 0, z), ('x1', w - 1, z)]
        for x in range(1, w - 1):
            cells.append(('zb', x, d - 1))
            if f == 2:
                cells.append(('zf', x, 0))
        return cells

    cells = wall_cells()
    for _ in range(rng.randint(3, 7)):
        side, x, z = rng.choice(cells)
        lo = 6 if side == 'zf' else 2
        y = rng.randint(lo, yt - 1)
        kind = rng.choice(['shoji', 'shoji', 'lattice', 'shutter', 'bars'])
        tall = rng.random() < 0.5 and y + 1 <= yt - 1
        for yy in ([y, y + 1] if tall else [y]):
            if kind == 'shoji':
                t.set(x, yy, z, 'white_stained_glass_pane')
            elif kind == 'lattice':
                t.set(x, yy, z, 'spruce_fence')
            elif kind == 'shutter':
                t.set(x, yy, z, 'spruce_trapdoor', facing=out[side], half='bottom', open='true')
            else:
                t.set(x, yy, z, 'iron_bars')
    # small windows high in the gable ends, under the roof slope
    for _ in range(rng.randint(0, 2)):
        gx = rng.choice((0, w - 1))
        z = rng.randint(1, d - 2)
        top = roof_y(d, f, z) - 1
        if top >= yt + 1:
            t.set(gx, rng.randint(yt + 1, top), z, rng.choice(['white_stained_glass_pane', 'iron_bars']))
    # lanterns hanging under the side eaves
    for _ in range(rng.randint(0, 2)):
        gx = rng.choice((-1, w))
        z = rng.choice([z for z in range(0, d) if roof_cell(d, f, z)[1] != 'top'])
        t.set(gx, roof_y(d, f, z) - 1, z, 'lantern', hanging='true')
    # a balcony on the back or a side of two-storey houses
    if f == 2 and rng.random() < 0.6:
        if rng.random() < 0.5:
            x0 = rng.randint(1, max(1, w - 4))
            for x in range(x0, min(w - 1, x0 + 3)):
                t.set(x, 5, d, 'dark_oak_slab', type='top')
                t.set(x, 6, d, 'dark_oak_fence')
                t.set(x, 6, d - 1, 'white_stained_glass_pane')
            t.set(x0, 7, d, 'lantern', hanging='false')
        else:
            gx, side_x = (-1, 0) if rng.random() < 0.5 else (w, w - 1)
            z0 = rng.randint(1, max(1, d - 4))
            for z in range(z0, min(d - 1, z0 + 3)):
                t.set(gx, 5, z, 'dark_oak_slab', type='top')
                t.set(gx, 6, z, 'dark_oak_fence')
                t.set(side_x, 6, z, 'white_stained_glass_pane')
    return t


# ---------------------------------------------------------------------------
# Gardens: frame x 0..gw-1, z 0..gd-1, y = 0 is the garden surface at street ground level.
# The template reaches 3 below (pond) and one row past the back (waterfall rock).
# ---------------------------------------------------------------------------
GOFF = (0, 3, 0)
CURB = 'polished_tuff'


def garden_base(gw, gd):
    return Tpl((gw, 9, gd + 1), GOFF)


def put_toro(t, x, z):
    t.set(x, 1, z, 'stone_brick_wall')
    t.set(x, 2, z, 'lantern', hanging='false')
    t.set(x, 3, z, 'stone_brick_slab', type='bottom')


def put_rock(t, rng, x, z, gw, gd, tall=False):
    stone = rng.choice(['tuff', 'andesite', 'stone', 'mossy_cobblestone', 'cobblestone'])
    t.set(x, 1, z, stone)
    if tall:
        t.set(x, 2, z, rng.choice(['tuff', 'mossy_cobblestone', 'stone']))
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, nz = x + dx, z + dz
        if 0 < nx < gw - 1 and 0 < nz < gd - 1 and rng.random() < 0.7:
            t.set(nx, 0, nz, 'moss_block')
            if rng.random() < 0.5:
                t.set(nx, 1, nz, 'moss_carpet')


def interior(gw, gd):
    return [(x, z) for x in range(1, gw - 1) for z in range(1, gd - 1)] or [(gw // 2, gd // 2)]


def curb(t, gw, gd):
    if gw < 5:
        return
    for x in range(gw):
        for z in range(gd):
            if x in (0, gw - 1) or z in (0, gd - 1):
                t.set(x, 0, z, CURB)


def garden_kare(gw, gd, v):
    """Karesansui: raked pale gravel, mossy rocks, sometimes a stone lantern."""
    rng = random.Random(f'kare-{gw}-{gd}-{v}')
    t = garden_base(gw, gd)
    rake_along_x = rng.random() < 0.5
    for x in range(gw):
        for z in range(gd):
            stripe = (z if rake_along_x else x) % 2
            t.set(x, 0, z, 'calcite' if stripe == 0 else 'diorite')
    curb(t, gw, gd)
    spots = interior(gw, gd)
    rng.shuffle(spots)
    for i in range(max(1, min(len(spots), (gw * gd) // 12))):
        x, z = spots[i]
        put_rock(t, rng, x, z, gw, gd, tall=(i == 0))
    if gw >= 5 and rng.random() < 0.6:
        put_toro(t, rng.choice((1, gw - 2)), rng.choice((1, gd - 2)))
    return t


def garden_moss(gw, gd, v):
    """Moss garden: stepping stones, azaleas, a bamboo clump, pink petals."""
    rng = random.Random(f'moss-{gw}-{gd}-{v}')
    t = garden_base(gw, gd)
    for x in range(gw):
        for z in range(gd):
            t.set(x, 0, z, 'moss_block')
            if rng.random() < 0.25:
                t.set(x, 1, z, 'moss_carpet')
    curb(t, gw, gd)
    # stepping stones wander from front to back
    x = gw // 2
    for z in range(gd):
        t.set(x, 0, z, 'polished_andesite')
        if (x, z) in t.blocks:
            pass
        t.blocks.pop((x + GOFF[0], 1 + GOFF[1], z + GOFF[2]), None)
        x = max(0, min(gw - 1, x + rng.choice((-1, 0, 0, 1))))
    spots = [p for p in interior(gw, gd) if (p[0] + GOFF[0], GOFF[1], p[1] + GOFF[2]) in t.blocks
             and t.blocks[(p[0] + GOFF[0], GOFF[1], p[1] + GOFF[2])][0] == 'moss_block']
    rng.shuffle(spots)
    plants = ['flowering_azalea', 'azalea', 'pink_petals', 'pink_petals', 'fern', 'bamboo']
    for i, (x, z) in enumerate(spots[:max(1, len(spots) // 3)]):
        p = plants[i % len(plants)] if i < len(plants) else rng.choice(plants)
        if p == 'bamboo':
            for y in range(1, rng.randint(3, 5) + 1):
                t.set(x, y, z, 'bamboo')
        elif p == 'pink_petals':
            t.set(x, 1, z, 'pink_petals', facing=rng.choice(['north', 'south', 'east', 'west']), flower_amount=rng.randint(2, 4))
        else:
            t.set(x, 1, z, p)
    if gw >= 5 and rng.random() < 0.5:
        put_toro(t, rng.choice((1, gw - 2)), gd - 2)
    return t


def garden_pond(gw, gd, v):
    """A pond with lily pads, fed by a little waterfall off a rock pile at the back."""
    rng = random.Random(f'pond-{gw}-{gd}-{v}')
    t = garden_base(gw, gd)
    for x in range(gw):
        for z in range(gd):
            t.set(x, 0, z, 'moss_block')
    curb(t, gw, gd)
    for x in range(1, gw - 1):
        for z in range(1, gd - 1):
            t.set(x, -2, z, 'clay')
            t.set(x, -1, z, 'water', level=0)
            t.set(x, 0, z, 'water', level=0)
            if rng.random() < 0.3:
                t.set(x, 1, z, 'lily_pad')
    # waterfall: rock pile on the back curb, a spring on top that can only spill forward into the pond
    cx = rng.randint(1, gw - 2)
    h = rng.randint(2, 3)
    rock = lambda: rng.choice(['mossy_cobblestone', 'tuff', 'mossy_stone_bricks'])
    for x in (cx - 1, cx, cx + 1):
        for y in range(1, h + 1):
            t.set(x, y, gd - 1, rock())
    t.set(cx - 1, h + 1, gd - 1, rock())
    t.set(cx + 1, h + 1, gd - 1, rock())
    for y in range(1, h + 2):
        t.set(cx, y, gd, rock())
    t.set(cx, h + 1, gd - 1, 'water', level=0)
    t.blocks.pop((cx + GOFF[0], 1 + GOFF[1], gd - 2 + GOFF[2]), None)  # no lily pad under the fall
    # a rock or two at the edge, and a lantern
    for _ in range(rng.randint(1, 2)):
        x = rng.choice((0, gw - 1))
        z = rng.randint(1, gd - 2)
        t.set(x, 1, z, rock())
    if rng.random() < 0.6:
        put_toro(t, rng.choice((0, gw - 1)), 0)
    return t


PAGODA_TIERS = [  # (core low, core high, wall height): narrows as it rises
    (1, 7, 4), (1, 7, 3), (2, 6, 3), (2, 6, 3), (3, 5, 3),
]


def pagoda():
    """Five-storey pagoda on a 9x9 stone platform (frame x,z 0..8). Eaves reach one block past it."""
    t = Tpl((11, 38, 11), (1, 0, 1))
    t.fill(0, 0, 0, 8, 0, 8, 'stone_bricks')
    t.fill(3, 0, -1, 5, 0, -1, 'stone_brick_stairs', facing='south', half='bottom')
    cur = 1
    for n, (lo, hi, h) in enumerate(PAGODA_TIERS):
        mid = (lo + hi) // 2
        for y in range(cur, cur + h):
            for x in range(lo, hi + 1):
                for z in range(lo, hi + 1):
                    if x not in (lo, hi) and z not in (lo, hi):
                        continue
                    if x in (lo, hi) and z in (lo, hi):
                        t.set(x, y, z, POST, axis='y')
                    elif y == cur + h - 1:
                        t.set(x, y, z, BEAM, axis='x' if z in (lo, hi) else 'z')
                    elif (x == mid or z == mid) and y > cur:
                        t.set(x, y, z, PLASTER)
                    else:
                        t.set(x, y, z, WALL_LOW)
        if n == 0:
            t.set(mid, cur, lo, 'dark_oak_door', facing='north', half='lower', hinge='left', open='false')
            t.set(mid, cur + 1, lo, 'dark_oak_door', facing='north', half='upper', hinge='left', open='false')
            t.set(mid, cur, mid, 'barrel', facing='up')                  # the offering box
            t.set(mid, cur + h - 1, mid, 'bell', attachment='ceiling', facing='north')
            t.set(lo + 1, cur, hi - 1, 'lantern', hanging='false')
            t.set(hi - 1, cur, hi - 1, 'lantern', hanging='false')
        yr = cur + h
        # roof: low outer ring (stairs), middle ring (block + stair above), core cap (tiles)
        for x in range(lo - 2, hi + 3):
            for z in range(lo - 2, hi + 3):
                dist = max(lo - x, x - hi, lo - z, z - hi, 0)
                if dist == 0:
                    t.set(x, yr, z, 'deepslate_tiles')
                    t.set(x, yr + 1, z, 'deepslate_tiles')
                    continue
                corner = (x in (lo - dist, hi + dist)) and (z in (lo - dist, hi + dist))
                if z < lo and not corner:
                    face = 'south'
                elif z > hi and not corner:
                    face = 'north'
                elif x < lo and not corner:
                    face = 'east'
                elif not corner:
                    face = 'west'
                if dist == 2:
                    if corner:
                        t.set(x, yr, z, 'deepslate_tiles')
                        t.set(x, yr + 1, z, 'deepslate_tile_slab', type='bottom')  # upturned corner
                        t.set(x, yr - 1, z, 'lantern', hanging='true')
                    else:
                        t.set(x, yr, z, 'deepslate_tile_stairs', facing=face, half='bottom')
                else:  # dist == 1
                    t.set(x, yr, z, 'deepslate_tiles')
                    if corner:
                        t.set(x, yr + 1, z, 'deepslate_tiles')
                    else:
                        t.set(x, yr + 1, z, 'deepslate_tile_stairs', facing=face, half='bottom')
                    t.set(x, yr - 1, z, 'dark_oak_fence')  # brackets under the eave
        cur = yr + 2
    # sorin: the spire with its rings
    t.set(4, cur, 4, 'deepslate_tile_wall')
    for i in range(1, 4):
        t.set(4, cur + i, 4, 'iron_bars')
    for i in range(4, 8):
        t.set(4, cur + i, 4, 'iron_chain', axis='y')
    t.set(4, cur + 8, 4, 'lightning_rod', facing='up')
    return t


# ---------------------------------------------------------------------------
# More building parts: engawa front, namako storehouse band, side fronts for corner houses,
# irimoya (hip-and-gable) roof, interiors, the small senbon torii, the hilltop shrine
# ---------------------------------------------------------------------------
INTERIORS = ('home', 'kitchen', 'tea', 'store', 'shop')


def front_engawa(w, d, f):
    """Tea house front: a run of shoji with one opening, and a wooden veranda (engawa) in front."""
    t = front(w, d, f, 'none')
    for x in range(1, w - 1):
        for y in range(1, 4):
            t.set(x, y, 0, 'white_stained_glass_pane')
    cx = (w - 1) // 2
    t.blocks.pop((cx + OFF[0], 1, OFF[2]), None)
    t.blocks.pop((cx + OFF[0], 2, OFF[2]), None)
    t.set(cx, 1, 0, 'air')
    t.set(cx, 2, 0, 'air')
    for x in range(0, w):
        t.set(x, 0, -1, 'spruce_slab', type='top')
    return t


def namako(w, d):
    """Storehouse walls: a black-and-white tiled band (namako) around the base."""
    t = Tpl(house_size(w, d), OFF)
    for y in (1, 2):
        for z in range(1, d - 1):
            for x in (0, w - 1):
                t.set(x, y, z, 'deepslate_tiles' if (x + y + z) % 2 else 'white_concrete')
        for x in range(1, w - 1):
            t.set(x, y, d - 1, 'deepslate_tiles' if (x + y) % 2 else 'white_concrete')
            if y == 2:
                t.set(x, y, 0, 'deepslate_tiles' if (x + y) % 2 else 'white_concrete')
    return t


def side_front(w, d, f, side):
    """A second street front on one side wall (for houses on a corner)."""
    t = Tpl(house_size(w, d), OFF)
    x = 0 if side == 'l' else w - 1
    ox = -1 if side == 'l' else w
    face = 'west' if side == 'l' else 'east'
    for z in range(1, d - 1):
        for y in range(1, 4):
            t.set(x, y, z, 'dark_oak_fence')
        t.set(x, 4, z, WALL_LOW)
        t.set(ox, 4, z, 'deepslate_tile_stairs', facing={'west': 'east', 'east': 'west'}[face], half='bottom')
    dz = (d - 1) // 2
    t.set(x, 1, dz, 'dark_oak_door', facing=face, half='lower', hinge='left', open='false')
    t.set(x, 2, dz, 'dark_oak_door', facing=face, half='upper', hinge='left', open='false')
    t.set(x, 3, dz, WALL_LOW)
    t.set(ox, 3, dz - 1 if dz > 1 else dz + 1, 'lantern', hanging='true')
    return t


def roof_irimoya(w, d, f):
    """Hip-and-gable: a hipped skirt on all four sides, a small gable rising out of it."""
    t = Tpl(house_size(w, d), OFF)
    ry = wall_top(f) + 1
    stair, full, slab = 'deepslate_tile_stairs', 'deepslate_tiles', 'deepslate_tile_slab'

    def ring(lo_x, hi_x, lo_z, hi_z, y, corner_up):
        for x in range(lo_x, hi_x + 1):
            for z in range(lo_z, hi_z + 1):
                if x not in (lo_x, hi_x) and z not in (lo_z, hi_z):
                    continue
                corner = x in (lo_x, hi_x) and z in (lo_z, hi_z)
                if corner:
                    t.set(x, y, z, full)
                    if corner_up:
                        t.set(x, y + 1, z, slab, type='bottom')
                elif z == lo_z:
                    t.set(x, y, z, stair, facing='south', half='bottom')
                elif z == hi_z:
                    t.set(x, y, z, stair, facing='north', half='bottom')
                elif x == lo_x:
                    t.set(x, y, z, stair, facing='east', half='bottom')
                else:
                    t.set(x, y, z, stair, facing='west', half='bottom')

    t.fill(1, ry, 1, w - 2, ry + 1 + (d - 1) // 2, d - 2, 'air')
    ring(-1, w, -1, d, ry, True)
    ring(0, w - 1, 0, d - 1, ry + 1, False)
    t.fill(1, ry + 1, 1, w - 2, ry + 1, d - 2, full)
    # the gable on top, over the inner width
    zs = list(range(0, d))
    n = len(zs)
    for i, z in enumerate(zs):
        k = min(i, n - 1 - i)
        y = ry + 2 + k
        if i < n - 1 - i:
            t.fill(1, y, z, w - 2, y, z, stair, facing='south', half='bottom')
        elif i > n - 1 - i:
            t.fill(1, y, z, w - 2, y, z, stair, facing='north', half='bottom')
        else:
            t.fill(1, y, z, w - 2, y, z, full)
        for gx in (1, w - 2):
            for gy in range(ry + 2, y):
                t.set(gx, gy, z, PLASTER)
    top = ry + 2 + (n - 1) // 2
    for i, z in enumerate(zs):
        if min(i, n - 1 - i) == (n - 1) // 2:
            t.fill(1, top + 1, z, w - 2, top + 1, z, slab, type='bottom')
    return t


def house_interior(w, d, f, kind):
    """Furnishing inside the walls (x 1..w-2, z 1..d-2). The ground floor first, then upstairs."""
    t = Tpl(house_size(w, d), OFF)
    rng = random.Random(f'in-{w}-{d}-{f}-{kind}')
    x0, x1, z0, z1 = 1, w - 2, 1, d - 2
    cx, cz = (w - 1) // 2, (d - 1) // 2
    tatami = 'bamboo_planks'
    if kind in ('home', 'tea'):
        t.fill(x0, 0, z0, x1, 0, z1, tatami)
        t.set(cx, 1, cz, 'spruce_trapdoor', facing='north', half='bottom', open='false')  # low table
        # (cushions either side of the table are entities: see CUSHION_SPOTS)
        t.set(cx, 1, z1, 'spruce_slab', type='bottom')       # tokonoma
        t.set(cx, 2, z1, 'potted_azalea_bush' if kind == 'home' else 'potted_bamboo')
        if kind == 'home' and w >= 7:
            t.set(x0, 0, z0, 'campfire', lit='true', facing='north')  # irori hearth
    elif kind == 'kitchen':
        t.fill(x0, 0, z0, x1, 0, z1, 'packed_mud')  # doma, earthen floor
        t.set(x0, 1, z1, 'smoker', facing='south')
        t.set(x0 + 1, 1, z1, 'water_cauldron', level=3)
        t.set(x1, 1, z0, 'barrel', facing='up')
        t.set(cx, 1, cz, 'crafting_table')
        t.set(x1, 1, cz, 'decorated_pot', facing='west')
    elif kind == 'store':
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if (x in (x0, x1) or z == z1) and rng.random() < 0.8:
                    t.set(x, 1, z, rng.choice(['barrel', 'chest', 'hay_block', 'barrel']), **({'facing': 'up'} if False else {}))
                    if rng.random() < 0.5:
                        t.set(x, 2, z, rng.choice(['barrel', 'hay_block', 'decorated_pot']))
    elif kind == 'shop':
        t.fill(x0, 0, z0, x1, 0, z1, 'spruce_planks')
        for x in range(x0, x1 + 1):
            t.set(x, 1, z1, 'barrel', facing='up')
            t.set(x, 2, z1, rng.choice(['flower_pot', 'decorated_pot', 'lantern', 'potted_fern', 'candle']))
            t.set(x, 3, z1, 'spruce_slab', type='top')
    if f == 2:
        # upstairs: a futon, a chest, a lantern on the floor
        t.set(x1, 6, z0, 'white_bed', facing='north', part='head')
        t.set(x1, 6, z0 + 1, 'white_bed', facing='north', part='foot')
        t.set(cx, 6, z1, 'chest', facing='north')
        t.set(x0 + 1, 6, z0, 'lantern', hanging='false')
    return t


def cushion_spots(w, d):
    """Where zabuton cushions go in home and tea interiors (frame coords, y=1 is on the tatami)."""
    cx, cz = (w - 1) // 2, (d - 1) // 2
    spots = [(cx - 1, 1, cz), (cx + 1, 1, cz)]
    if w >= 7:
        spots.append((2, 1, 1))  # beside the hearth
    return spots


def torii_small():
    """The senbon torii: pillars 4 apart so a 3-wide path runs between them."""
    t = Tpl((7, 6, 1), (1, 0, 0))
    for x in (0, 4):
        t.set(x, 0, 0, 'polished_blackstone')
        t.fill(x, 1, 0, x, 4, 0, 'red_concrete')
    t.fill(-1, 3, 0, 5, 3, 0, 'red_concrete')
    t.fill(-1, 4, 0, 5, 4, 0, 'red_concrete')
    t.fill(0, 5, 0, 4, 5, 0, 'polished_blackstone_bricks')
    t.set(-1, 5, 0, 'polished_blackstone_brick_slab', type='bottom')
    t.set(5, 5, 0, 'polished_blackstone_brick_slab', type='bottom')
    return t


def hokora():
    """A small hilltop shrine at the end of a senbon torii path. Frame x 0..4, z 0..4, front at z=0."""
    t = Tpl((7, 7, 7), (1, 0, 1))
    t.fill(0, 0, 0, 4, 0, 4, 'stone_bricks')
    for x, z in ((1, 1), (3, 1), (1, 3), (3, 3)):
        t.fill(x, 1, z, x, 2, z, 'red_concrete')
    t.fill(1, 1, 3, 3, 2, 3, 'dark_oak_planks')
    t.set(1, 1, 2, 'dark_oak_planks')
    t.set(3, 1, 2, 'dark_oak_planks')
    t.set(2, 1, 2, 'spruce_slab', type='top')
    t.set(2, 2, 2, 'candle', candles=3, lit='true')
    t.set(2, 1, 1, 'barrel', facing='up')       # offering box
    for x in (0, 4):
        t.set(x, 1, 0, 'stone_brick_wall')
        t.set(x, 2, 0, 'lantern', hanging='false')
        t.set(x, 3, 0, 'stone_brick_slab', type='bottom')
    # roof
    for x in range(0, 5):
        t.set(x, 3, 0, 'deepslate_tile_stairs', facing='south', half='bottom')
        t.set(x, 3, 4, 'deepslate_tile_stairs', facing='north', half='bottom')
        t.set(x, 3, 1, 'deepslate_tiles')
        t.set(x, 3, 3, 'deepslate_tiles')
        t.set(x, 4, 1, 'deepslate_tile_stairs', facing='south', half='bottom')
        t.set(x, 4, 3, 'deepslate_tile_stairs', facing='north', half='bottom')
        t.set(x, 4, 2, 'deepslate_tiles')
        t.set(x, 5, 2, 'deepslate_tile_slab', type='bottom')
    t.set(0, 3, 0, 'polished_blackstone')
    return t


def stilts_fn(w, d):
    """Kakezukuri: timber posts down to the ground and braces under the floor (no stone fill)."""
    xs = sorted({0, (w - 1) // 2, w - 1})
    zs = sorted({0, (d - 1) // 2, d - 1})
    lines = [f'# Stilts under a {w}x{d} house built out over a drop']
    for x in xs:
        for z in zs:
            lines.append(f'fill {local(w, x, -1, z)} {local(w, x, -24, z)} dark_oak_log replace #kyoto:fillable')
    for y in (-1, -5, -9):
        lines.append(f'fill {local(w, 0, y, 0)} {local(w, w - 1, y, 0)} dark_oak_wood replace #kyoto:fillable')
        lines.append(f'fill {local(w, 0, y, d - 1)} {local(w, w - 1, y, d - 1)} dark_oak_wood replace #kyoto:fillable')
        lines.append(f'fill {local(w, 0, y, 0)} {local(w, 0, y, d - 1)} dark_oak_wood replace #kyoto:fillable')
        lines.append(f'fill {local(w, w - 1, y, 0)} {local(w, w - 1, y, d - 1)} dark_oak_wood replace #kyoto:fillable')
    return '\n'.join(lines) + '\n'


def torii():
    # 7 wide: pillars at x=1 and x=5, the path runs between them along z
    t = Tpl((7, 8, 1))
    for x in (1, 5):
        t.set(x, 0, 0, 'polished_blackstone')
        t.fill(x, 1, 0, x, 5, 0, 'red_concrete')
    t.fill(0, 3, 0, 6, 3, 0, 'red_concrete')          # nuki
    t.set(3, 4, 0, 'red_concrete')                     # gakuzuka
    t.fill(0, 5, 0, 6, 5, 0, 'red_concrete')          # shimaki
    t.fill(1, 6, 0, 5, 6, 0, 'polished_blackstone_bricks')  # kasagi
    t.set(0, 6, 0, 'polished_blackstone_brick_stairs', facing='east', half='top')
    t.set(6, 6, 0, 'polished_blackstone_brick_stairs', facing='west', half='top')
    t.set(0, 7, 0, 'polished_blackstone_brick_slab', type='bottom')
    t.set(6, 7, 0, 'polished_blackstone_brick_slab', type='bottom')
    return t


# ---------------------------------------------------------------------------
# Size-specific functions
# ---------------------------------------------------------------------------
def local(w, x, y, z):
    """Frame (x, y, z) -> local coordinates from the plot marker (street side, facing the house).
    Frame x runs to the left of the facing direction; the plot sits one block in front of z=0
    and one block above the floor."""
    left = x - (w - 1) / 2
    fmt = lambda v: ('^' if v == 0 else '^' + (str(int(v)) if float(v).is_integer() else str(v)))
    return f'{fmt(left)} {fmt(y - 1)} {fmt(z + 1)}'


def check_fn(w, d):
    xs = sorted({0, (w - 1) // 2, w - 1})
    zs = sorted({0, (d - 1) // 2, d - 1})
    lines = [
        f'# Overlap check for a {w}x{d} house. Returns 1 (blocked) if any core sample hits',
        '# another building, a path, water or ground too far from street level.',
        '# Cores are tested; eaves (the margin) are not, so neighbours may share them.',
    ]
    for x in xs:
        for z in zs:
            for y in (0, 2, 4, 7):
                lines.append(f'execute if block {local(w, x, y, z)} #kyoto:built run return 1')
            lines.append(f'execute if block {local(w, x, 0, z)} #kyoto:path run return 1')
    lines.append('# ground height under the footprint')
    for x in (0, w - 1):
        for z in (0, d - 1):
            lines.append(f'execute positioned {local(w, x, 1, z)} positioned over motion_blocking_no_leaves '
                         'run summon marker ~ ~ ~ {Tags:["ky.probe"]}')
    lines += [
        'execute store result score #py ky.var run data get entity @s Pos[1]',
        'execute as @e[type=marker,tag=ky.probe] store result score @s ky.var run data get entity @s Pos[1]',
        'execute as @e[type=marker,tag=ky.probe] run scoreboard players operation @s ky.var -= #py ky.var',
        'scoreboard players set #bad ky.var 0',
        'execute if entity @e[type=marker,tag=ky.probe,scores={ky.var=7..}] run scoreboard players set #bad ky.var 1',
        'execute if entity @e[type=marker,tag=ky.probe,scores={ky.var=..-17}] run scoreboard players set #bad ky.var 1',
        'execute as @e[type=marker,tag=ky.probe] at @s if block ~ ~-1 ~ #kyoto:water run scoreboard players set #bad ky.var 1',
        'scoreboard players set #deep ky.var 0',
        'execute if entity @e[type=marker,tag=ky.probe,scores={ky.var=..-6}] run scoreboard players set #deep ky.var 1',
        'kill @e[type=marker,tag=ky.probe]',
        'execute if score #bad ky.var matches 1 run return 1',
        '# 2 = the ground drops away under part of it: build out over the drop on stilts',
        'execute if score #deep ky.var matches 1 run return 2',
        'return 0',
    ]
    return '\n'.join(lines) + '\n'


def build_fn(w, d):
    ox = local(w, -1, 0, -1)
    top = roof_top(d, 2) + 1
    lines = [
        f'# Builds a {w}x{d} house. Macro args: f (floors), front, roof, seed, rot',
        '# 1) cut terrain out of the volume, 2) stone foundation down to the ground, 3) parts',
        f'fill {local(w, -1, 1, -1)} {local(w, w, top, d)} air replace #kyoto:diggable',
        f'execute unless score #stilt ky.var matches 1 run fill {local(w, 0, -1, 0)} {local(w, w - 1, -7, d - 1)} stone_bricks replace #kyoto:fillable',
        f'execute if score #stilt ky.var matches 1 run function kyoto:gen/stilts_w{w}_d{d}',
        f'$place template kyoto:house/body_w{w}_d{d}_f$(f) {ox} $(rot)',
        f'$place template kyoto:house/interior_w{w}_d{d}_f$(f)_$(interior) {ox} $(rot)',
        f'$place template kyoto:house/front_w{w}_d{d}_f$(f)_$(front) {ox} $(rot)',
        f'$execute if score #front ky.var matches 3 run place template kyoto:house/namako_w{w}_d{d} {ox} $(rot)',
        f'$execute if score #corner ky.var matches 1 run place template kyoto:house/sidel_w{w}_d{d}_f$(f) {ox} $(rot)',
        f'$execute if score #corner ky.var matches 2 run place template kyoto:house/sider_w{w}_d{d}_f$(f) {ox} $(rot)',
        f'$place template kyoto:house/roof_w{w}_d{d}_f$(f)_$(roof) {ox} $(rot)',
        f'$place template kyoto:house/deco_w{w}_d{d}_f$(f) {ox} $(rot) none 0.35 $(seed)',
        f'$place template kyoto:house/windows_w{w}_d{d}_f$(f)_v$(win) {ox} $(rot)',
        f'$fill {local(w, 0, 1, 0)} {local(w, w - 1, top, d - 1)} $(wall) replace white_terracotta',
        f'summon marker {local(w, (w - 1) // 2, 1, (d - 1) // 2)} {{Tags:["ky.house"]}}',
        '# pots, barrels and the like: only where there is ground to stand on',
    ]
    for x, y, z in cushion_spots(w, d):
        lines.insert(-1, f'execute if score #cush ky.var matches 1 positioned {local(w, x, y, z)} run function kyoto:life/cushion')
    cells = [(x, -1) for x in range(-1, w + 1)] + [(-1, z) for z in range(0, d)] + [(w, z) for z in range(0, d)]
    for x, z in cells:
        lines.append(f'execute positioned {local(w, x, 1, z)} run function kyoto:deco/ground')
    return '\n'.join(lines) + '\n'


def pagoda_fns():
    ox = local(9, -1, 0, -1)
    build = '\n'.join([
        '# Builds the pagoda. Macro arg: rot',
        f'fill {local(9, -1, 1, -1)} {local(9, 9, 37, 9)} air replace #kyoto:diggable',
        f'fill {local(9, 0, -1, 0)} {local(9, 8, -9, 8)} stone_bricks replace #kyoto:fillable',
        f'$place template kyoto:pagoda {ox} $(rot)',
        f'summon marker {local(9, 4, 1, 4)} {{Tags:["ky.house"]}}',
        f'summon marker {local(9, 4, 1, 4)} {{Tags:["ky.offering"]}}',
    ]) + '\n'
    try_ = '\n'.join([
        '# Try the pagoda here. Returns 1 if built.',
        'execute store result score #blocked ky.var run function kyoto:gen/check_w9_d9',
        'execute if score #blocked ky.var matches 1.. run return 0',
        '$function kyoto:gen/build_pagoda {rot:"$(rot)"}',
        'return 1',
    ]) + '\n'
    return {'check_w9_d9': check_fn(9, 9), 'build_pagoda': build, 'try_pagoda': try_}


def garden_check_fn(gw, gd):
    xs = sorted({0, (gw - 1) // 2, gw - 1})
    zs = sorted({0, (gd - 1) // 2, gd - 1})
    lines = [f'# Can a {gw}x{gd} garden go here? Returns 1 if blocked. Gardens only need the ground clear.']
    for x in xs:
        for z in zs:
            for y in (0, 1, 3):
                lines.append(f'execute if block {local(gw, x, y, z)} #kyoto:built run return 1')
            lines.append(f'execute if block {local(gw, x, 0, z)} #kyoto:path run return 1')
            lines.append(f'execute if block {local(gw, x, 1, z)} #minecraft:logs run return 1')
    for x in (0, gw - 1):
        for z in (0, gd - 1):
            lines.append(f'execute positioned {local(gw, x, 1, z)} positioned over motion_blocking_no_leaves '
                         'run summon marker ~ ~ ~ {Tags:["ky.probe"]}')
    lines += [
        'execute store result score #py ky.var run data get entity @s Pos[1]',
        'execute as @e[type=marker,tag=ky.probe] store result score @s ky.var run data get entity @s Pos[1]',
        'execute as @e[type=marker,tag=ky.probe] run scoreboard players operation @s ky.var -= #py ky.var',
        'scoreboard players set #bad ky.var 0',
        'execute if entity @e[type=marker,tag=ky.probe,scores={ky.var=4..}] run scoreboard players set #bad ky.var 1',
        'execute if entity @e[type=marker,tag=ky.probe,scores={ky.var=..-4}] run scoreboard players set #bad ky.var 1',
        'execute as @e[type=marker,tag=ky.probe] at @s if block ~ ~-1 ~ #kyoto:water run scoreboard players set #bad ky.var 1',
        'kill @e[type=marker,tag=ky.probe]',
        'execute if score #bad ky.var matches 1 run return 1',
        'return 0',
    ]
    return '\n'.join(lines) + '\n'


def garden_try_fn(gw, gd):
    kind = 'small' if gw < 5 else 'kind'
    return '\n'.join([
        f'# Try a {gw}x{gd} garden. Macro args: kind, small, v, rot. Returns 1 if placed.',
        f'execute store result score #blocked ky.var run function kyoto:gen/gcheck_{gw}x{gd}',
        'execute if score #blocked ky.var matches 1 run return 0',
        f'fill {local(gw, 0, 1, 0)} {local(gw, gw - 1, 6, gd)} air replace #kyoto:garden_clear',
        f'fill {local(gw, 0, -1, 0)} {local(gw, gw - 1, -6, gd - 1)} stone replace #kyoto:fillable',
        f'$place template kyoto:garden/{gw}x{gd}_$({kind})_$(v) {local(gw, 0, -3, 0)} $(rot)',
        'return 1',
    ]) + '\n'


def garden_dispatch():
    lines = ['# Fit the largest garden that will go here (args in storage kyoto:tmp garden). Returns 1 if placed.']
    for gw, gd in GARDEN_SIZES:
        lines.append(f'execute store result score #ok ky.var run function kyoto:gen/gtry_{gw}x{gd} with storage kyoto:tmp garden')
        if gw >= 5:
            lines.append(f'execute if score #ok ky.var matches 1 positioned {local(gw, gw // 2, 1, gd // 2)} '
                         'run function kyoto:deco/garden_tree')
        lines.append('execute if score #ok ky.var matches 1 run return 1')
    lines.append('return 0')
    return '\n'.join(lines) + '\n'


def plot_dispatch():
    lines = ['# Dispatch on #w / #hd to the size-specific try function (house args in storage kyoto:tmp house)',
             '# Returns 1 if a house was built.']
    for w in WIDTHS:
        for d in DEPTHS:
            lines.append(f'execute if score #w ky.var matches {w} if score #hd ky.var matches {d} '
                         f'run return run function kyoto:gen/try_w{w}_d{d} with storage kyoto:tmp house')
    lines.append('return 0')
    return '\n'.join(lines) + '\n'


def try_fn(w, d):
    return '\n'.join([
        f'# Try a {w}x{d} house here (macro args passed through to the builder)',
        f'execute store result score #blocked ky.var run function kyoto:gen/check_w{w}_d{d}',
        'execute if score #blocked ky.var matches 1 run return 0',
        'scoreboard players set #stilt ky.var 0',
        'execute if score #blocked ky.var matches 2 run scoreboard players set #stilt ky.var 1',
        f'$function kyoto:gen/build_w{w}_d{d} {{f:$(f),front:"$(front)",roof:"$(roof)",seed:$(seed),rot:"$(rot)",win:$(win),wall:"$(wall)",interior:"$(interior)"}}',
        'return 1',
    ]) + '\n'


# ---------------------------------------------------------------------------
def main():
    st = os.path.join(DATA, 'structure')
    gen = os.path.join(DATA, 'function', 'gen')
    for p in (os.path.join(st, 'house'), os.path.join(st, 'garden'), gen):
        shutil.rmtree(p, ignore_errors=True)
        os.makedirs(p)

    torii().save(os.path.join(st, 'torii.nbt'))
    torii_small().save(os.path.join(st, 'torii_small.nbt'))
    hokora().save(os.path.join(st, 'hokora.nbt'))
    pagoda().save(os.path.join(st, 'pagoda.nbt'))
    for name, text in pagoda_fns().items():
        with open(os.path.join(gen, name + '.mcfunction'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
    n = 1
    for w in WIDTHS:
        for d in DEPTHS:
            for f in FLOORS:
                body(w, d, f).save(os.path.join(st, 'house', f'body_w{w}_d{d}_f{f}.nbt'))
                deco(w, d, f).save(os.path.join(st, 'house', f'deco_w{w}_d{d}_f{f}.nbt'))
                n += 2
                for k in FRONTS:
                    tpl = front_engawa(w, d, f) if k == 'engawa' else front(w, d, f, k)
                    tpl.save(os.path.join(st, 'house', f'front_w{w}_d{d}_f{f}_{k}.nbt'))
                    n += 1
                for m in ROOFS:
                    tpl = roof_irimoya(w, d, f) if m == 'irimoya' else roof(w, d, f, m)
                    tpl.save(os.path.join(st, 'house', f'roof_w{w}_d{d}_f{f}_{m}.nbt'))
                    n += 1
                for k in INTERIORS:
                    house_interior(w, d, f, k).save(os.path.join(st, 'house', f'interior_w{w}_d{d}_f{f}_{k}.nbt'))
                    n += 1
                for side in ('l', 'r'):
                    side_front(w, d, f, side).save(os.path.join(st, 'house', f'side{side}_w{w}_d{d}_f{f}.nbt'))
                    n += 1
                for v in range(WINDOW_LAYOUTS):
                    windows(w, d, f, v).save(os.path.join(st, 'house', f'windows_w{w}_d{d}_f{f}_v{v}.nbt'))
                    n += 1
            namako(w, d).save(os.path.join(st, 'house', f'namako_w{w}_d{d}.nbt'))
            n += 1
            for name, text in ((f'check_w{w}_d{d}', check_fn(w, d)), (f'build_w{w}_d{d}', build_fn(w, d)),
                               (f'try_w{w}_d{d}', try_fn(w, d)), (f'stilts_w{w}_d{d}', stilts_fn(w, d))):
                with open(os.path.join(gen, name + '.mcfunction'), 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(text)
    with open(os.path.join(gen, 'plot.mcfunction'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(plot_dispatch())
    makers = {'kare': garden_kare, 'moss': garden_moss, 'pond': garden_pond}
    for gw, gd in GARDEN_SIZES:
        for kind in GARDEN_KINDS:
            if kind == 'pond' and (gw < 5 or gd < 4):
                continue
            for v in range(GARDEN_VARIANTS):
                makers[kind](gw, gd, v).save(os.path.join(st, 'garden', f'{gw}x{gd}_{kind}_{v}.nbt'))
                n += 1
        for name, text in ((f'gcheck_{gw}x{gd}', garden_check_fn(gw, gd)), (f'gtry_{gw}x{gd}', garden_try_fn(gw, gd))):
            with open(os.path.join(gen, name + '.mcfunction'), 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(text)
    with open(os.path.join(gen, 'garden.mcfunction'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(garden_dispatch())
    print(f'{n} structures, {len(os.listdir(gen))} generated functions')


if __name__ == '__main__':
    main()
