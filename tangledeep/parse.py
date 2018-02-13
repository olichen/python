from lxml import etree
import re

monsterList = etree.parse('./monsters.xml')

output = "{{Monster_Template\n\
|title1 = %%Name%%\n\
|family = %%Family%%\n\
|base_level = %%ChallengeValue%%\n\
|base_health = %%HP%%\n\
|highest_stat =\n\
*Strength - %%Strength%%\n\
*Swiftness - %%Swiftness%%\n\
*Discipline - %%Discipline%%\n\
*Spirit - %%Spirit%%\n\
*Guile - %%Guile%%\n\
*Accuracy - %%Accuracy%%\n\
}}"

print(output)

for monster in monsterList.iter("Monster"):

    def my_replace(elementName):
        elementName = elementName.group()[2:-2]
        if monster.find(elementName) is not None:
            return monster.find(elementName).text
        return ""

    newoutput = output
    newoutput = re.sub(r'%%(\w+)%%', my_replace, newoutput)

    print(newoutput)
