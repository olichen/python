from lxml import etree
import re

dungeonList = etree.parse('./dungeon.xml')
monsterList = etree.parse('./monster.xml')
spawnList = etree.parse('./spawn.xml')
npcList = etree.parse('./npc.xml')
roomList = etree.parse('./room.xml')

def printText(text):
    print(text)
    print()

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
        printText("== "+dungeon.findtext('CustomName')+" ==")
    else:
        printText("== ????? ==")

    if dungeon.find('TextOverlay') is not None:
        printText(dungeon.find('TextOverlay').findtext('Name'))
        printText(dungeon.find('TextOverlay').findtext('Text'))
    if dungeon.find('ExpectedPlayerLevel') is not None:
        printText("Expected player level: "+dungeon.findtext('ExpectedPlayerLevel'))
    if dungeon.find('FastTravel') is not None:
        printText("You can fast travel to this location")
    if dungeon.find('ItemWorld') is not None:
        printText("This is an [[Item World]]")
    if dungeon.find('SideArea') is not None:
        printText("This is a [[Side Area]]")
    if dungeon.find('ClearReward') is not None:
        printText("Clear to receive a reward")

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
        printText(output)

def printMonsters(dungeon):
    spawnTableName = dungeon.findtext('SpawnTable')
    printMonsterTable(spawnTableName)

def printMonsterTable(spawnTableName):
    spawnTable = findSpawnTable(spawnTableName)
    if spawnTable is not None:
        printText("=== Monsters ===")
        for monster in spawnTable.findall('.//ActorRefs/*'):
            printText("* [["+findMonsterName(monster.tag)+"]] "+monster.text)

def printSideAreas(dungeon):
    currentFloor = dungeon.findtext('Level')
    if dungeon.find('AltPath') is not None:
        currentFloor = dungeon.findtext('AltPath')
    sideAreaList = findSideAreas(currentFloor)
    if sideAreaList != []:
        printText("=== Side Areas ===")
        for sideArea in sideAreaList:
            printText("* [["+sideArea.findtext('CustomName')+"]]")

def printNPCs(dungeon):
    spawnList = dungeon.findall('SpawnActor')
    output = []
    if spawnList!=[]:
        for spawn in spawnList:
            if spawn.findtext('ActorType')=='NPC':
                output.append(findNPCName(spawn.findtext('RefName')))
    if output != []:
        printText("=== NPCs ===")
        for npcName in output:
            printText("* [["+npcName+"]]")

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
        printText("=== Monsters ===")
        for monster in monsterOutput:
            printText(monster)
    if randomMonsterTable is not None:
        printMonsterTable(randomMonsterTable)
    if npcOutput != []:
        printText("=== NPCs ===")
        for npc in npcOutput:
            printText("* [["+npc+"]]")


for dungeon in dungeonList.iter("Floor"):
    printDungeonTitle(dungeon)
    printDungeonStats(dungeon)
    if dungeon.find('SpecialRoomTemplate') is not None:
        printSpecialTemplate(dungeon)
    else:
        printMonsters(dungeon)
    printSideAreas(dungeon)
    printNPCs(dungeon)
    printText("")
