import json
import os
from json import JSONDecodeError

def load_characters(location='./characters'):
    for file in [file for file in os.listdir(location) if file.endswith('.json')]:
        print("Loading... {}".format(file.replace('.json', '')))

def load_data(location):
    char_list = {}
    if not os.path.exists(location):
         print("Couldn't find data file, starting from scratch...")
    else:
        try:
            with open(location, 'r') as sfv_file:
                char_list = json.loads(sfv_file.read())
            print("Loaded the following characters: {}".format(",".join(char_list.keys())))
        except JSONDecodeError:
            print("Couldn't load data file, starting from scratch...")
    return char_list

def make_selection(item_list):
    print("Available Options:")
    items = list(item_list)
    items.append('Add New Option')
    for i, item in enumerate(item_list):
        print("- {}: {}".format(i, item))
    while 1:
        selection = input("> ")
        if selection == '':
            return -1
        if selection.lower() == 'quit':
            return -2
        if selection in item_list:
            return selection
        try:
            sel = int(selection) - 1
            return items[sel]
        except (ValueError, IndexError):
            print("Not a valid option")


def new_character(char_list):
    print("Adding a new character...")
    char_name = input("Name: ")
    char_list[char_name] = {'knockdowns': [], 'moves': []}
    return char_name


def select_char(char_list, char_name):
    char_info = None
    if char_name:
        char_info = char_list.get(char_name, None)
        if char_info:
            return char_info
        print("Couldn't find selected character: {}".format(char_name))
    while not char_info:
        print("Please select from the provided list (Type 'Quit' to quit):")
        characters = list(char_list.keys())
        characters.append('Add New Character')
        for i, char in enumerate(characters):
            print("{}: {}".format(i+1, char))
        selection = input("> ")
        if selection.lower() == 'quit':
            return -1
        char_info = char_list.get(selection, None)
        if not char_info:
            try:
                sel = characters[int(selection)-1]
                if sel == 'Add New Character':
                    sel = new_character(char_list)
                char_info = char_list.get(sel, None)
            except (ValueError, IndexError):
                print("Please enter either a character name or index")
    print("Found: {}".format(char_info))
    return char_info

def select_knockdown(char_info):
    knockdowns = list(char_info['knockdowns'])
    knockdowns.append('Add New Knockdown')
    print("Select a knockdown (No entry returns to character select)")
    for i, knockdown in enumerate(knockdowns):
        print(knockdown)
    selection = input("> ")
    if selection == '':
    


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Oki calculator based off FAT SFV data")
    parser.add_argument('-c', type=str, dest='character', default=None, help='Name of the character')
    parser.add_argument('-d', type=str, dest='datafile', default='sfv_kd_data.json',
                        help='Data File location. Defaults to .\\sfv_kd_data.json')
    args = parser.parse_args()

    char_list = load_data(args.datafile)
    while 1:
        character = select_char(char_list, args.character)
        if character == -1:
            break
        while 1:
            knockdown = select_knockdown(character)

    save_data(char_list, args.datafile)
