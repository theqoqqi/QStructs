import sys
import glob
import os
import nbtlib

filename = sys.argv[1]
fileCounter = 0

def findAirBlocksInPalette(nbt):
    return [i for i in range(len(nbt['']['palette'])) if nbt['']['palette'][i]['Name'] == 'minecraft:air']

def removeBlocksInFundament(nbt, stateIds):
    blocksToRemove = []
    for block in nbt['']['blocks']:
        if block['pos'][1] == 0 and block['state'] in stateIds:
            global fileCounter
            blocksToRemove.append(block)
            fileCounter = fileCounter + 1
    for block in blocksToRemove:
        nbt['']['blocks'].remove(block)

filenames = [filename]

if os.path.isdir(filename):
    filenames = glob.glob(f'{filename}/**/*.nbt', recursive=True)

for filename in filenames:
    nbt = nbtlib.load(filename)
    fileCounter = 0
    airIds = findAirBlocksInPalette(nbt)
    removeBlocksInFundament(nbt, airIds)
    nbt.save()
    print(fileCounter, 'REPLACEMENTS IN FILE', filename)

print('Structure blocks updated successfully')