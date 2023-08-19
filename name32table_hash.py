all_strings=[]

def name32hash(name):
    if name.startswith(b'0x'):
        return int(name[2:].decode("utf8"),16)
    sum = 0
    for i in range(len(name)):
        sum = ((sum*0x1003F)&0xFFFFFFFF) + name[i]
        sum = sum&0xFFFFFFFF
    return sum

# Expects a raw string table dump from game memory - strings separated by '\0' character (i.e. hex 00)
with open('name32 table.bin', 'rb') as f:
    data = f.read()
cur_stroffs=0
for i in range(0,len(data)):
    if data[i] == 0:
        all_strings.append(data[cur_stroffs:i])
        cur_stroffs = i+1
name_by_hash={}
for name in all_strings:
    namehash = name32hash(name)
    if namehash in name_by_hash:
        namelist = name_by_hash[namehash]
    else:
        namelist = set()
        name_by_hash[namehash] = namelist
    namelist.add(name)
for namehash in name_by_hash:
    names = name_by_hash[namehash]
    if len(names) > 1:
        print("#Collision with 0x%08x: %s" % (namehash, str(names)))
print(', '.join(["%s: 0x%08x"%(name,name32hash(name)) for name in all_strings]))