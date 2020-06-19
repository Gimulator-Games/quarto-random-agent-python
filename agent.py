import json
import os
from random import randrange
import time

from client import Client, Key, Object

NAME = os.getenv('AGENT_NAME')
KEY_REGISTER = Key('register', NAME, 'quarto')
KEY_BOARD = Key('verdict', 'board', 'quarto')
KEY_ACTION = Key('action', NAME, 'quarto')


def callback(c, obj):
    board = json.loads(obj.Value)
    available_pieces = list()
    available_positions = list()
    if board['turn'] == NAME:
        for piece_id, _ in board['pieces']:
            is_used = False
            for position in board['positions']:
                if position['piece-id'] == piece_id:
                    is_used = True
            if is_used is False and int(piece_id) != board['picked']:
                available_pieces.append(piece_id)
        for position in board['positions']:
            if position['piece-id'] == 0:
                available_positions.append(position)

        n = randrange(len(available_pieces))
        action = {
            'picked': available_pieces[n],
            'x': available_positions[n]['x'],
            'y': available_positions[n]['y']
        }
        json_action = json.dumps(action)
        c.set(Object(KEY_ACTION, json_action, ''))


def main():
    c = Client(callback)
    c.set(Object(KEY_REGISTER, ''))
    c.watch(KEY_BOARD)


if __name__ == "__main__":
    main()
