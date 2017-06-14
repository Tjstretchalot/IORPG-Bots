import asyncio
import websockets
import json
import math

server = "ws://classfight.com:8081/Play"
moving_left = False
moving_right = False
moving_up = False
moving_down = False

def reset():
    global moving_left, moving_right, moving_up, moving_down
    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False
    

@asyncio.coroutine
def change_direction(move_left = False, move_right = False, move_up = False, move_down = False):
    global socket, moving_left, moving_right, moving_up, moving_down
    if move_left and not moving_left:
        #print("moving left")
        yield from socket.send(json.dumps([ 3, 2 ]))
        moving_left = True
    if not move_left and moving_left:
        #print("stopping move left")
        yield from socket.send(json.dumps([ 4, 2 ]))
        moving_left = False
    if move_right and not moving_right:
        #print("moving right")
        yield from socket.send(json.dumps([ 3, 1 ]))
        moving_right = True
    if not move_right and moving_right:
        #print("stopping move right") 
        yield from socket.send(json.dumps([ 4, 1 ]))
        moving_right = False
    if move_up and not moving_up:
        #print("moving up")
        yield from socket.send(json.dumps([ 3, 3 ]))
        moving_up = True
    if not move_up and moving_up:
        #print("stopping move up")
        yield from socket.send(json.dumps([ 4, 3 ]))
        moving_up = False
    if move_down and not moving_down:
        #print("moving down")
        yield from socket.send(json.dumps([ 3, 4 ]))
        moving_down = True
    if not move_down and moving_down:
        #print("stopping move down")
        yield from socket.send(json.dumps([ 4, 4 ]))
        moving_down = False

@asyncio.coroutine
def cast_spell_at_ent(spell_index, ent):
    global socket
    size = ent_size(ent)

    tarx = ent["translate"]["x"] + size / 2
    tary = ent["translate"]["y"] + size / 2

    yield from change_direction()
    yield from socket.send(json.dumps([ 5, spell_index, { "x": tarx, "y": tary } ]))

def ent_size(ent):
    hero = ent["hero"]
    if hero == 1:
        return 96
    elif hero == 2:
        return 80
    elif hero == 3:
        return 76
    else:
        raise Exception()
    
def check_distance(me, ent2):
    ptx = me["translate"]["x"]
    pty = me["translate"]["y"]
    mysize = ent_size(me)
    ptx += mysize / 2
    pty += mysize / 2
    
    rectx = ent2["translate"]["x"]
    recty = ent2["translate"]["y"]
    rectw = ent_size(ent2)
    recth = rectw

    dx = 0
    dy = 0
    if ptx < rectx:
        dx = rectx - ptx
    elif ptx > rectx + rectw:
        dx = rectx + rectw - ptx

    if pty < recty:
        dy = recty - pty
    elif pty > recty + recth:
        dy = recty + recth - pty
    
    return ( dx, dy, math.sqrt(dx * dx + dy * dy) )
