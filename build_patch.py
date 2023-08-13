#! /usr/bin/python3

import sys
import struct

# replace instructions that load the MQ flag in <register>
# with "mov <register>, #0x0"

patchData = {
    #<address> : <register>
    0x002C05A0 : 0, # invert first person gyro x-axis
    0x002D8D20 : 0, # invert targetted gyro x-axis
    0x002EF024 : 0, # mirror flashing dots on world map (pause/gameplay)
    0X002EF128 : 0, # mirror static dots on world map (pause screen)
    0x002F06F0 : 0, # mirror cursor on world map
    0x002F0A98 : 0, # mirror blue box on world map (pause screen)
    0x002F0F40 : 1, # mirror cloud textures on world map
    0x002F1580 : 0, # mirror boss icon on dungeon map
    0x002F16C0 : 0, # mirror chest icons on dungeon map
    0x002F1828 : 1, # mirror chest icons on dungeon minimap
    0x002F19A8 : 2, # mirror boss icon on dungeon minimap
    0x002F227C : 0, # mirror dungeon map
    0x002FFC98 : 0, # invert audio channels
    0x002FC378 : 0, # invert culling for 2D sprites (effects, projectiles,...)
    0x00344570 : 1, # invert directions in dialog (east/west)
    0x0041901C : 0, # invert stereoscopic 3D
    0x00419900 : 0, # invert culling for 3D objects
    0x0041AB10 : 0, # invert circle pad x-axis
    0x0042ADF8 : 0, # mirror yellow arrow on minimap
    0x0042AFEC : 0, # mirror red arrow on minimap
    0x0042C62C : 1, # mirror world map (gameplay)
    0x0042CEDC : 1, # mirror world map (pause screen)
    0x0042CF38 : 1, # change position of area name on world map (pause screen)
    0x0042DAF0 : 2, # mirror pause menu controls
    0x0042F7B4 : 0, # mirror overworld minimap (pause screen)
    0x004391E8 : 0, # mirror blue box on world map (gameplay)
    0x0044199C : 0, # mirror overworld minimap (gameplay)
    0x00441E14 : 0, # mirror dungeon minimap (pause/gameplay)
    0x00479088 : 0, # mirror graphics
}

def getEurAddr(usaAddr):
    if (usaAddr <= 0x419E17 or usaAddr >= 0x4A5B00):
        return usaAddr
    elif (usaAddr >= 0x41A144 and usaAddr <= 0x43668B):
        return usaAddr + 0x24
    elif (usaAddr >= 0x436690 and usaAddr <= 0x4A5ADF):
        return usaAddr + 0x20
    else:
        raise Exception("Address can't be converted")


isEur = len(sys.argv) > 1 and sys.argv[1] == "--eur"

off = lambda vaddr: struct.pack(">I",vaddr - 0x100000)[1:]
sz = lambda size: struct.pack(">H", size)

ips = b'PATCH'
cheat = '[Unmirror Master Quest]\n'
for vaddr, reg in patchData.items():
    if (isEur):
        vaddr = getEurAddr(vaddr)

    patch = b'\x00' + int(reg << 4).to_bytes(1) + b'\xA0\xE3' #instruction "mov <register>, #0x0"
    size = 4

    ips += off(vaddr)
    ips += sz(size)
    ips += patch

    addrStr = '{:08x}'.format(vaddr)
    regStr = '{:02x}'.format(reg << 4)
    cheat += (addrStr + ' E3A0' + regStr + '00\n').upper()
ips += b'EOF'

with open('code.ips', 'wb') as patchFile:
    patchFile.write(ips)

with open('cheats.txt', 'w') as cheatsFile:
    cheatsFile.write(cheat)

print(('EUR' if isEur else 'USA') + ' patch built!')
