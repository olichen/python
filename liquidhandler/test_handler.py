from opentrons import protocol_api
import csv
import re

metadata = {
    'protocolName': 'Single head transfer',
    'author': 'oliver chen <olichen@ucdavis.edu',
    'description': 'Read in volumes from a CSV file and transfer volumes',
    'apiLevel': '2.2'
}

def run(protocol: protocol_api.ProtocolContext):

    volumes = readCSV('SingleHeadTransfer.csv')

    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    plate1 = protocol.load_labware('corning_96_wellplate_360ul_flat', 2)
    plate2 = protocol.load_labware('corning_96_wellplate_360ul_flat', 3)

    p300 = protocol.load_instrument('p300_single', 'right', tip_racks=[tiprack_1])

    for x in range(12):
        for y in range(8):
            well = chr(ord('A')+y) + str(x+1)
            p300.transfer(volumes[x][y], plate1[well], plate2[well])


def readCSV(csvname):
    volumes = [[0 for y in range(8)] for x in range(12)]

    # read in the CSV file
    with open(csvname) as csvfile:
        reader = csv.reader(csvfile)
        wellFormat = re.compile('[a-zA-Z][0-9]')

        for row in reader:
            well = row[0].strip()
            # check to make sure well is correctly formatted
            if not wellFormat.match(well):
                print('Skipping cell "' + well + '"')
                continue
    
            wellX = int(well[1:])-1
            # 32 is the difference between the unicode value of 'a' and 'A'
            wellY = (ord(well[0])-ord('A'))%32
            volume = int(row[1].strip())
            volumes[wellX][wellY] = volume

    return volumes
