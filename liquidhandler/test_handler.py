from opentrons import protocol_api
import csv
import re

metadata = {'apiLevel': '2.2'}

def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    p300 = protocol.load_instrument('p300_single', 'right', tip_racks=[tiprack_1])

    p300.transfer(100, plate['A1'], plate['B1'])


with open('SingleHeadTransfer.csv') as csvfile:
    reader = csv.reader(csvfile)
    wells = [[0 for y in range(8)] for x in range(12)]
    regex = re.compile('[a-zA-Z][0-9]')
    for row in reader:
        well = row[0].strip()
        if not regex.match(well):
            print('Skipping well "' + well + '"')
            continue
        wellX = int(well[1:])-1
        # 32 is the difference between the unicode value of 'a' and 'A'
        wellY = (ord(well[0])-ord('A'))%32
        volume = int(row[1].strip())
        wells[wellX][wellY] = volume
    print(wells)
