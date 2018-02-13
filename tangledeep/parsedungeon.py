from lxml import etree
import re

dungeonList = etree.parse('./dungeon.xml')
monsterList = etree.parse('./monster.xml')
spawnList = etree.parse('./spawn.xml')

def findSpawnTable(spawnTableName):
    for spawn in spawnList.iter('SpawnTable'):
        if(spawn.findtext('RefName')==spawnTableName):
            return spawn

def findMonsterName(monsterName):
    for monster in monsterList.iter('Monster'):
        if(monster.findtext('RefName')==monsterName):
            return monster.findtext('Name')

def findSideAreas(floorNum):
    output = []
    for dungeon in dungeonList.iter('Floor'):
        minSpawnFloor = dungeon.findtext('MinSpawnFloor')
        maxSpawnFloor = dungeon.findtext('MaxSpawnFloor')
        if minSpawnFloor is not None and maxSpawnFloor is not None:
            if(int(minSpawnFloor) <= int(floorNum) <= int(maxSpawnFloor)):
                output.append(dungeon)
    return output

#def printDungeonStats(dungeon):

def printMonsters(spawnTableName):
    spawnTable = findSpawnTable(spawnTableName)
    if spawnTable is not None:
        print("=== Monsters ===")
        for monster in spawnTable.findall('.//ActorRefs/*'):
            print("* [["+findMonsterName(monster.tag)+"]] "+monster.text)

def printSideAreas(currentFloor):
    sideAreaList = findSideAreas(currentFloor)
    if sideAreaList != []:
        print("=== Side Areas ===")
        for sideArea in sideAreaList:
            print("* [["+sideArea.findtext('CustomName')+"]]")

output = "{{== %%CustomName%% ==\n\
{| class=\"article-table\" border=\"1\"\n\
|Maximum Secret Areas\n\
|%%MaxSecretAreas%%\n\
|-\n\
|Minimum Monsters\n\
|%%MinMonsters%%\n\
|-\n\
|Maximum Monsters\n\
|%%MaxMonsters%%\n\
|-\n\
|Maximum Champions\n\
|%%MaxChampions%%\n\
|-\n\
|Maximum Champion Mods\n\
|%%MaxChampionMods%%\n\
|}"

print(output)

for dungeon in dungeonList.iter("Floor"):

    def my_replace(elementName):
        elementName = elementName.group()[2:-2]
        if dungeon.find(elementName) is not None:
            return dungeon.find(elementName).text
        return "0"

    newoutput = output
    newoutput = re.sub(r'%%(\w+)%%', my_replace, newoutput)

    print(newoutput)

    printMonsters(dungeon.findtext('SpawnTable'))
    printSideAreas(dungeon.findtext('Level'))
