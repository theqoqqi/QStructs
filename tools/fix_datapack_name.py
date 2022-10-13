import sys
import glob
import os
import nbtlib
from nbtlib.tag import String

filename = sys.argv[1]
fromName = 'q_structs'
toName = 'q_structs'

fileCounter = 0

def applyReplacementsInPalette(nbt, fromName, toName):
    for paletteItem in nbt['']['palette']:
        replace(paletteItem, 'Name', fromName, toName)

def applyReplacementsInBlocks(nbt, fromName, toName):
    for paletteItem in nbt['']['blocks']:
        if 'nbt' in paletteItem:
            replace(paletteItem['nbt'], 'name', fromName, toName)
            replace(paletteItem['nbt'], 'pool', fromName, toName)
            replace(paletteItem['nbt'], 'target', fromName, toName)
            replace(paletteItem['nbt'], 'final_state', fromName, toName)
            replace(paletteItem['nbt'], 'LootTable', fromName, toName)

def replace(nbt, key, fromName, toName):
    if key in nbt:
        oldValue = nbt[key].unpack()
        newValue = oldValue.replace(fromName, toName)
        nbt[key] = String(newValue)
        if oldValue != newValue:
            global fileCounter
            fileCounter += 1

filenames = [filename]

if os.path.isdir(filename):
    filenames = glob.glob(f'{filename}/**/*.nbt', recursive=True)

for filename in filenames:
    nbt = nbtlib.load(filename)
    fileCounter = 0
    applyReplacementsInPalette(nbt, fromName, toName)
    applyReplacementsInBlocks(nbt, fromName, toName)
    nbt.save()
    print(fileCounter, 'REPLACEMENTS IN FILE', filename)

print('Structure blocks updated successfully')