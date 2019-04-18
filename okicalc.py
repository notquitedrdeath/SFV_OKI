import os
from characters.character import Character, Move, Knockdown

CHAR_DIR = os.path.join('.', 'characters')


def load_characters(location=CHAR_DIR):
    char_list = {}
    for f in [f for f in os.listdir(location) if f.endswith('.json')]:
        print("Loading... {}".format(f.replace('.json', '')))
        c = Character.load(f.replace('.json', ''))
        print("Loaded {}".format(c.name))
        char_list[c.name] = c
    return char_list

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
        for i, char in enumerate(characters):
            print("{}: {}".format(i+1, char))
        selection = input("> ")
        if selection.lower() == 'quit':
            return -1
        char_info = char_list.get(selection, None)
        if not char_info:
            try:
                sel = characters[int(selection)-1]
                char_info = char_list.get(sel, None)
            except (ValueError, IndexError):
                print("Please enter either a character name or index")
    print("Found: {}".format(char_info))
    return char_info


def select_knockdown(kd_list, kd=None):
    knockdown = None
    kd_dict = {kd.name: kd for kd in kd_list}
    if kd:
        knockdown = kd_dict.get(kd, None)
        if not knockdown:
            print("Couldn't find selected knockdown")
    while not knockdown:
        print("Select a Knockdown from the list (Type 'return' to return to Character Select)")
        print(kd_dict)
        kds = list(kd_dict.keys())
        for i, k in enumerate(kds):
            print("{}: {}".format(i+1, k))
        selection = input("> ")
        if selection.lower() == 'return':
            return -1
        knockdown = kd_dict.get(selection, None)
        if not knockdown:
            try:
                sel = kds[int(selection)-1]
                knockdown = kd_dict.get(sel, None)
            except (ValueError, IndexError):
                print("Please enter either a character name or index")
    print("Found: {}".format(knockdown))
    return knockdown


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Oki calculator based off FAT SFV data")
    parser.add_argument('-c', type=str, dest='character', default=None, help='Name of the character')
    parser.add_argument('-d', type=str, dest='char_dir', default=CHAR_DIR)
    args = parser.parse_args()

    char_list = load_characters(args.char_dir)
    while 1:
        character = select_char(char_list, args.character)
        if character == -1:
            break
        while 1:
            knockdown = select_knockdown(character.knockdowns)
            if knockdown == -1:
                break
            print("Looking at {}".format(knockdown))
            print("."*knockdown.advantage_norise)