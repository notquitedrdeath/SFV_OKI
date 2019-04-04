import json
import os

CHAR_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class Character(object):
    def __init__(self, name='Peter',
                 health=1000, stun=1000,
                 walkspeed_forward=3, walkspeed_back=3,
                 dash_forward=17, dash_back=17,
                 jump_forward_speed=(3, 38, 4), jump_neutral_speed=(4, 38, 4), jump_back_speed=(4, 38, 4),
                 jump_forward_distance=150, jump_back_distance=150,
                 movelist=None, knockdowns=None, *args, **kwags):
        self.name = name
        self.health = health
        self.stun = stun
        self.walkspeed_forward = walkspeed_forward
        self.walkspeed_back = walkspeed_back
        self.dash_forward = dash_forward
        self.dash_back = dash_back
        # Jump speeds are a list/tuple of 3 values, Startup, Active/airtime, Landing
        self.jump_forward_speed = jump_forward_speed
        self.jump_neutral_speed = jump_neutral_speed
        self.jump_back_speed = jump_back_speed
        self.jump_forward_distance = jump_forward_distance
        self.jump_back_distance = jump_back_distance
        self.movelist = movelist or []
        self.knockdowns = knockdowns or []

    def serialise(self):
        json_dict = {}
        for item in self.__dict__:
            if not item.startswith('__') and not callable(item):
                json_dict[item] = self.__dict__[item]
        return json.dumps(json_dict, indent=4)

    def __str__(self):
        return self.serialise()

    @classmethod
    def deserialise(cls, json_str):
        return cls(**json.loads(json_str))

    def save(self, location=None):
        location = location or os.path.join(CHAR_DIRECTORY, "{}.json".format(self.name))
        with open(location, 'w') as save_file:
            save_file.write(self.serialise())

    @classmethod
    def load(cls, char_name=None, location=None):
        location = location or os.path.join(CHAR_DIRECTORY, "{}.json".format(char_name))
        with open(location, 'r') as load_file:
            character = cls.deserialise(load_file.read())
        return character

class Move(object):
    def __init__(self, name, input="s.LP",
                 startup=3, active=2, recovery=7,
                 on_block=2, on_hit=4, on_ch=None,
                 max_range=0.6, pushback_block=0.5, pushback_hit=0.4, pushback_ch=None,
                 damage=30, stun=70, cancels=None, comments=None, *args, **kwargs):
        self.name = name
        self.input = input
        self.startup = startup
        if isinstance(active, int):
            # Active can either be single value for single hit buttons (s.LP = 2 active frames)
            self.active = [(0, active)]
        else:
            # Or a series of gaps and active frames.
            # Juri's s.MK = [(0, 1), (1, 3)]
            # 0 frame gap followed by 1 active frame, 1 frame gap followed by 3 active frames
            # First value should always be 0 as initial startup is covered in startup field.
            self.active = active
        self.recovery = recovery
        self.total_frames = self.startup + self.recovery + sum([pair[0] + pair[1] for pair in self.active]) - 1
        self.on_block= on_block
        self.on_hit = on_hit
        # If there's an explicit CH value given, assume that it's a CC value, otherwise just use oH + 2
        self.on_ch = on_ch or on_hit + 2


    def move_string(self):
        move_str = (self.startup-1) * "s"
        for gap, active in self.active:
            move_str += gap * "r" + active * "A"
        move_str += self.recovery * "r"
        return move_str