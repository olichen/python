from lxml import etree
import re

dungeonList = etree.parse('./dungeon.xml')
monsterList = etree.parse('./monster.xml')
spawnList = etree.parse('./spawn.xml')
npcList = etree.parse('./npc.xml')
roomList = etree.parse('./room.xml')

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

def findNPCName(npcName):
    for npc in npcList.iter('NPC'):
        if(npc.findtext('RefName')==npcName):
            return npc.findtext('DisplayName')

def findSpecialTemplate(templateName):
    for room in roomList.iter('Room'):
        if(room.findtext('RefName')==templateName):
            return room

def printDungeonTitle(dungeon):
    if dungeon.findtext('CustomName'):
        print("== "+dungeon.findtext('CustomName')+" ==")
    else:
        print("== ????? ==")

    if dungeon.find('TextOverlay') is not None:
        print(dungeon.find('TextOverlay').findtext('Name'))
        print(dungeon.find('TextOverlay').findtext('Text'))
    if dungeon.find('ExpectedPlayerLevel') is not None:
        print("Expected player level: "+dungeon.findtext('ExpectedPlayerLevel'))
    if dungeon.find('FastTravel') is not None:
        print("You can fast travel to this location")
    if dungeon.find('ItemWorld') is not None:
        print("This is an [[Item World]]")
    if dungeon.find('SideArea') is not None:
        print("This is a [[Side Area]]")
    if dungeon.find('ClearReward') is not None:
        print("Clear to receive a reward")

def printDungeonStats(dungeon):
    def my_replace(elementName):
        elementName = elementName.group()[2:-2]
        if dungeon.find(elementName) is not None:
            return dungeon.find(elementName).text
        return "0"

    output = "\
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

    if dungeon.find('MaxMonsters') is not None:
        output = re.sub(r'%%(\w+)%%', my_replace, output)
        print(output)

def printMonsters(dungeon):
    spawnTableName = dungeon.findtext('SpawnTable')
    printMonsterTable(spawnTableName)

def printMonsterTable(spawnTableName):
    spawnTable = findSpawnTable(spawnTableName)
    if spawnTable is not None:
        print("=== Monsters ===")
        for monster in spawnTable.findall('.//ActorRefs/*'):
            print("* [["+findMonsterName(monster.tag)+"]] "+monster.text)

def printSideAreas(dungeon):
    currentFloor = dungeon.findtext('Level')
    sideAreaList = findSideAreas(currentFloor)
    if sideAreaList != []:
        print("=== Side Areas ===")
        for sideArea in sideAreaList:
            print("* [["+sideArea.findtext('CustomName')+"]]")

def printNPCs(dungeon):
    spawnList = dungeon.findall('SpawnActor')
    output = []
    if spawnList!=[]:
        for spawn in spawnList:
            if spawn.findtext('ActorType')=='NPC':
                output.append(findNPCName(spawn.findtext('RefName')))
    if output != []:
        print("=== NPCs ===")
        for npcName in output:
            print("* [["+npcName+"]]")

def countSpawns(room, symbol):
    occurances = 0
    for row in room.findall('Row'):
        occurances += row.text.count(symbol)
    return str(occurances)

def monsterPrintFormatter(room, char):
    if char.findtext('CharType')=='MONSTER':
        monsterName = "[["+findMonsterName(char.findtext('ActorRef'))+"]]"
    else:
        monsterName = "Random Monster(s)"
    monsterNum = countSpawns(room, char.findtext('Symbol'))+"x "
    monsterChamp = ""
    if char.find('ChampMods') is not None:
        monsterChamp = "Champion (" + char.findtext('ChampMods') + " mod(s)) "
    return "* "+monsterNum+monsterChamp+monsterName

def printSpecialTemplate(dungeon):
    room = findSpecialTemplate(dungeon.findtext('SpecialRoomTemplate'))
    charList = room.findall('CharDef')
    monsterOutput = []
    randomMonsterTable = None
    npcOutput = []
    if charList != []:
        for char in charList:
            if char.findtext('CharType')=='MONSTER':
                monsterOutput.append(monsterPrintFormatter(room, char))
            if char.findtext('CharType')=='RANDOMMONSTER':
                monsterOutput.append(monsterPrintFormatter(room, char))
                randomMonsterTable=char.findtext('ActorTable')
            if char.findtext('CharType')=='NPC':
                npcOutput.append(findNPCName(char.findtext('ActorRef')))
    if monsterOutput != []:
        print("=== Monsters ===")
        for monster in monsterOutput:
            print(monster)
    if randomMonsterTable is not None:
        printMonsterTable(randomMonsterTable)
    if npcOutput != []:
        print("=== NPCs ===")
        for npc in npcOutput:
            print("* [["+npc+"]]")


for dungeon in dungeonList.iter("Floor"):
    printDungeonTitle(dungeon)
    printDungeonStats(dungeon)
    if dungeon.find('SpecialRoomTemplate') is not None:
        printSpecialTemplate(dungeon)
    else:
        printMonsters(dungeon)
    printSideAreas(dungeon)
    printNPCs(dungeon)
    print("")
