"""Static checks against the real game jar, so problems show up before /reload:
  - every block id used in structures, functions and tags exists
  - every block-state property used exists for that block (from the jar's blockstate models)
  - every #minecraft: tag referenced exists
  - every function referenced exists, and macro lines ($) only appear in functions called with args

Run:  python validate.py <path to 26.3.jar>
"""
import gzip
import json
import os
import re
import struct
import sys
import zipfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kyoto_gate')
jar = zipfile.ZipFile(sys.argv[1])
names = set(jar.namelist())

blocks = {n[len('assets/minecraft/blockstates/'):-5] for n in names if n.startswith('assets/minecraft/blockstates/')}
vanilla_block_tags = {n[len('data/minecraft/tags/block/'):-5] for n in names if n.startswith('data/minecraft/tags/block/')}


def block_props(bid):
    """Property names a block's blockstate file mentions (variants keys or multipart conditions)."""
    data = json.loads(jar.read(f'assets/minecraft/blockstates/{bid}.json'))
    props = set()
    for key in data.get('variants', {}):
        for part in filter(None, key.split(',')):
            props.add(part.split('=')[0])
    def walk(cond):
        if isinstance(cond, dict):
            for k, v in cond.items():
                if k in ('OR', 'AND'):
                    for c in v:
                        walk(c)
                else:
                    props.add(k)
    for part in data.get('multipart', []):
        walk(part.get('when', {}))
    return props


errors = []
used_blocks = {}  # id -> set(props)


def note(bid, props=(), where=''):
    bid = bid.replace('minecraft:', '')
    used_blocks.setdefault(bid, set()).update(props)
    if bid not in blocks:
        errors.append(f'unknown block {bid!r} ({where})')


# ---- structures
def read_nbt(path):
    d = gzip.open(path).read()
    p = [0]
    def rd(n):
        b = d[p[0]:p[0] + n]; p[0] += n; return b
    def payload(t):
        if t == 1: return struct.unpack('>b', rd(1))[0]
        if t == 3: return struct.unpack('>i', rd(4))[0]
        if t == 8: n = struct.unpack('>H', rd(2))[0]; return rd(n).decode()
        if t == 9:
            et = rd(1)[0]; n = struct.unpack('>i', rd(4))[0]; return [payload(et) for _ in range(n)]
        if t == 10:
            out = {}
            while True:
                tt = rd(1)[0]
                if tt == 0: return out
                n = struct.unpack('>H', rd(2))[0]; k = rd(n).decode(); out[k] = payload(tt)
        raise ValueError(t)
    rd(1); rd(struct.unpack('>H', rd(2))[0])
    return payload(10)


struct_count = 0
for dirpath, _, files in os.walk(os.path.join(ROOT, 'data')):
    for f in files:
        if f.endswith('.nbt'):
            s = read_nbt(os.path.join(dirpath, f))
            struct_count += 1
            for e in s['palette']:
                note(e['id'], e.get('properties', {}).keys(), f)
            for b in s['blocks']:
                if not all(0 <= b['pos'][i] < s['size'][i] for i in range(3)):
                    errors.append(f'{f}: block outside size')

# ---- functions
functions = {}
for dirpath, _, files in os.walk(os.path.join(ROOT, 'data')):
    for f in files:
        if f.endswith('.mcfunction'):
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, os.path.join(ROOT, 'data')).replace(os.sep, '/')
            ns, _, rest = rel.partition('/function/')
            functions[f'{ns}:{rest[:-len(".mcfunction")]}'] = open(path, encoding='utf-8').read()

block_re = re.compile(r'(?:setblock \S+ \S+ \S+ |fill (?:\S+ ){6})(?:minecraft:)?([a-z_]+)(\[[^\]]*\])?')
called_with_args = set()
for name, text in functions.items():
    for line in text.splitlines():
        for m in re.finditer(r'function (#?[a-z_]+:[a-z_0-9/]+)( with| \{)?', line):
            target = m.group(1)
            if target.startswith('#'):
                continue
            if '$(' in target:
                continue
            if target not in functions:
                errors.append(f'{name}: calls missing function {target}')
            if m.group(2):
                called_with_args.add(target)
        for m in block_re.finditer(line):
            if '$(' in m.group(0) and m.group(1) == '':
                continue
            props = re.findall(r'([a-z_]+)=', m.group(2) or '')
            note(m.group(1), props, name)
        for t in re.findall(r'#minecraft:([a-z_/]+)', line):
            if t not in vanilla_block_tags and t not in ('load',):
                errors.append(f'{name}: unknown block tag #minecraft:{t}')
for name, text in functions.items():
    macro = any(l.startswith('$') for l in text.splitlines())
    if macro and name not in called_with_args:
        errors.append(f'{name}: has macro lines but is never called with arguments')
    for l in text.splitlines():
        if l.startswith('$') and '$(' not in l:
            errors.append(f'{name}: macro line without a macro argument: {l[:60]}')

# ---- tags
for dirpath, _, files in os.walk(os.path.join(ROOT, 'data')):
    for f in files:
        if f.endswith('.json') and os.sep + 'block' in dirpath:
            for v in json.load(open(os.path.join(dirpath, f)))['values']:
                if v.startswith('#minecraft:'):
                    if v[11:] not in vanilla_block_tags:
                        errors.append(f'tag {f}: unknown #{v[1:]}')
                elif v.startswith('#kyoto:'):
                    if not os.path.exists(os.path.join(dirpath, v[7:] + '.json')):
                        errors.append(f'tag {f}: missing {v}')
                else:
                    note(v, (), f'tag {f}')

# ---- block states
for bid, props in used_blocks.items():
    if bid in blocks and props:
        known = block_props(bid)
        for p in props:
            if known and p not in known:
                errors.append(f'block {bid} has no property {p!r} (known: {sorted(known)})')

print(f'{struct_count} structures, {len(functions)} functions, {len(used_blocks)} distinct blocks checked')
print('\n'.join(errors) if errors else 'no problems found')
sys.exit(1 if errors else 0)
