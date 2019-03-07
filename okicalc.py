import urllib.request
import json
import os
import pprint

JSON_URL = "https://raw.githubusercontent.com/D4RKONION/fatsfvframedatajson/master/sfv.json"

class Character(object):
    def __init__(self, name):
        self.name = name
        self.knockdowns = {}

    def add_kd(self, move_name, kd, kdr, kdrb):
        # Warning! This will overwrite any existing move.
        self.knockdowns[move_name] = {'kd': kd, 'kdr': kdr, 'kdrb': kdrb}

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)



def load_data(location):
    char_list = []
    if not os.path.exists(location):
        print("Couldn't find data file, downloading and saving now...")
        with urllib.request.urlopen(JSON_URL) as sfvdata:
            json_blob = json.loads(sfvdata.read().decode())
            for char in json_blob.keys():
                c = Character(char)
                move_list = json_blob[char]['moves']
                for section in move_list:
                    for move in move_list[section]:
                        if 'kd' in move_list[section][move]:
                            name = move
                            kd = move_list[section][move]['kd']
                            kdr = move_list[section][move]['kdr']
                            kdrb = move_list[section][move]['kdrb']
                            if section != 'normal':
                                name += ' - {}'.format(section)
                            c.add_kd(name, kd, kdr, kdrb)
                char_list.append(c)
    return char_list


def select_char():
    print("Select a character from the following:")
    for i, char in enumerate(data.keys()):
        print("{}: {}".format(i+1, char))

    while 1:
        selection = input(">")
        if selection in data.keys():
            return selection
        try:
            sel = list(data.keys())[int(selection)-1]
            return sel
        except (ValueError, IndexError):
            print("Please select a valid character")

def find_kd_moves(move_list):
    for section, moves in move_list.items():
        print("Searching for moves from {}".format(section))
        for move in moves:
            s = int(moves[move]['startup'])
            a = int(moves[move]['active'])
            r = int(moves[move]['recovery'])
            print("\t- {}".format(move))
            print("\t\t- {}:{}:{} - Total {}".format(s,a,r,s+a+r-1))



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Oki calculator based off FAT SFV data")
    parser.add_argument('-c', type=str, dest='character', help='Name of the character')
    parser.add_argument('-d', type=str, dest='datafile', default='sfv_kd_data.json',
                        help='Data File location. Defaults to .\\sfv_kd_data.json')
    parser.add_argument('-u', action='store_true', dest='update', help='Attempt to update KDA data from FAT JSON file')
    args = parser.parse_args()

    char_list = load_data(args.datafile)
    for char in char_list:
        print(char)
        for move in char.knockdowns:
            print("\t- {} - {}/{}/{}".format(move, char.knockdowns[move]['kd'], char.knockdowns[move]['kdr'], char.knockdowns[move]['kdrb']))

    # character = args.character or select_char()
    # try:
    #     character_data = data[character]
    # except KeyError:
    #     print("Unknown character given")
    #
    # find_kd_moves(character_data['moves'])
