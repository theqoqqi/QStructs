import sys
import glob
import os
import nbtlib

filename = sys.argv[1]
toBiomeName = sys.argv[2]

woodBlockIdTemplates = {
    'planks': 'minecraft:%id%_planks',
    'log': 'minecraft:%id%_log',
    'stairs': 'minecraft:%id%_stairs',
    'slab': 'minecraft:%id%_slab',
    'fence': 'minecraft:%id%_fence',
    'fence_gate': 'minecraft:%id%_fence_gate',
    'stripped_log': 'minecraft:stripped_%id%_log',
    'wood': 'minecraft:%id%_wood',
    'stripped_wood': 'minecraft:stripped_%id%_wood',
    'leaves': 'minecraft:%id%_leaves',
    'pressure_plate': 'minecraft:%id%_pressure_plate',
    'trapdoor': 'minecraft:%id%_trapdoor',
    'button': 'minecraft:%id%_button',
    'door': 'minecraft:%id%_door',
    'sign': 'minecraft:%id%_sign',
}

woodNames = {
    'plains': 'oak',
    'forest': 'oak',
    'desert': 'acacia',
    'savanna': 'acacia',
    'snowy': 'spruce',
    'taiga': 'spruce',
    'jungle': 'jungle',
    'mangrove': 'mangrove',
    'dark_forest': 'dark_oak',
    'birch_forest': 'birch',
}

defaultBricks = {
    'bricks_1': 'minecraft:stone_bricks',
    'brick_stairs_1': 'minecraft:stone_brick_stairs',
    'brick_slab_1': 'minecraft:stone_brick_slab',
    'brick_wall_1': 'minecraft:stone_brick_wall',
    'bricks_2': 'minecraft:cobblestone',
    'brick_stairs_2': 'minecraft:cobblestone_stairs',
    'brick_slab_2': 'minecraft:cobblestone_slab',
    'brick_wall_2': 'minecraft:cobblestone_wall',
}

biomes = {
    'plains': defaultBricks.copy(),
    'desert': {
        'bricks_1': 'minecraft:cut_sandstone',
        'brick_stairs_1': 'minecraft:sandstone_stairs',
        'brick_slab_1': 'minecraft:sandstone_slab',
        'brick_wall_1': 'minecraft:sandstone_wall',
        'bricks_2': 'minecraft:cut_sandstone',
        'brick_stairs_2': 'minecraft:sandstone_stairs',
        'brick_slab_2': 'minecraft:sandstone_slab',
        'brick_wall_2': 'minecraft:sandstone_wall',
        'WOOD_slab': 'minecraft:sandstone_slab',
        'WOOD_log': 'minecraft:chiseled_sandstone',
        'WOOD_planks': 'minecraft:sandstone',
        'WOOD_fence': 'minecraft:sandstone_wall',
        'WOOD_leaves': 'minecraft:sand',
    },
    'savanna': defaultBricks.copy(),
    'snowy': defaultBricks.copy(),
    'taiga': defaultBricks.copy(),
    'jungle': defaultBricks.copy(),
    'mangrove': defaultBricks.copy(),
    'dark_forest': defaultBricks.copy(),
    'birch_forest': defaultBricks.copy(),
}

for biomeName, biome in biomes.items():
    woodName = woodNames[biomeName]
    for genericId, blockIdTemplate in woodBlockIdTemplates.items():
        genericKey = 'WOOD_' + genericId
        if not genericKey in biome:
            biome[genericKey] = blockIdTemplate.replace('%id%', woodName)


if not toBiomeName in biomes:
    sys.exit(f'Biome {toBiomeName} is not defined')


def applyReplacementsInNbt(nbt, toBiomeName):
    biome = biomes[toBiomeName]
    for paletteItem in nbt['']['palette']:
        blockId = paletteItem['Name'].unpack()
        genericBlockId = findGenericBlockId(blockId)
        if genericBlockId in biome:
            paletteItem['Name'] = nbtlib.String(biome[genericBlockId])


def findGenericBlockId(blockId):
    for biomeName, map in biomes.items():
        for genericBlockId, mappedBlockId in map.items():
            if mappedBlockId == blockId:
                return genericBlockId


filenames = [filename]

if os.path.isdir(filename):
    filenames = glob.glob(f'{filename}/*.nbt')

for filename in filenames:
    nbt = nbtlib.load(filename)
    applyReplacementsInNbt(nbt, toBiomeName)
    nbt.save()

print('Structure blocks updated successfully')