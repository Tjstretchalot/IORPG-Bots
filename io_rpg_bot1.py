import asyncio
import websockets
import json
import math
import shared
import traceback

@asyncio.coroutine
def hello():
    socket = yield from websockets.connect(shared.server)
    shared.socket = socket
    try:
        yield from socket.send(json.dumps([ 1, { "hero": 2, "name": "bot2" } ]))

        world = False
        got_first_data = False
        last_spotted_healer = False
        while socket.state_name == "OPEN":
            server_data_json = yield from socket.recv()
            server_data = json.loads(server_data_json)
            if server_data[0] != 2:
                break
            
            world = server_data[1]
            me = world["me"]

            if "spell_progress" in me:
                continue

            if me["health"] < 50:
                best_healer = False
                best_mana = False
                for ent in world["entities"]:
                    if ent["team"] != me["team"] or ent["hero"] != 3:
                        continue

                    if (not best_healer) or ent["mana"] > best_mana:
                        best_healer = ent
                        best_mana = ent["mana"]

                if best_healer:
                    last_spotted_healer = ent
                    dist = shared.check_distance(me, best_healer)
                    dx = dist[0]
                    dy = dist[1]
                    yield from shared.change_direction(dx < 0, dx > 0, dy < 0, dy > 0)
                    continue
                elif last_spotted_healer:
                    dist = shared.check_distance(me, last_spotted_healer)
                    dx = dist[0]
                    dy = dist[1]
                    if dx < 960 or dy < 540:
                        last_spotted_healer = False
                    else:
                        yield from shared.change_direction(dx < 0, dx > 0, dy < 0, dy > 0)
                        continue
                

            best_target = False
            best_dist = False
            for ent in world["entities"]:
                if ent["team"] == me["team"]:
                    continue
                dist_tup = shared.check_distance(me, ent)
                if (not best_target) or (dist_tup[2] < best_dist[2]):
                    best_target = ent
                    best_dist = dist_tup
                
            if best_target:
                dx = best_dist[0]
                dy = best_dist[1]
                have_enough_mana = me["mana"] >= 20

                if have_enough_mana: 
                    if best_dist[2] < 290: # 300 - 10 because distance isnt exact
                        yield from shared.cast_spell_at_ent(0, best_target)
                    else:
                        yield from shared.change_direction(dx < 0, dx > 0, dy < 0, dy > 0)
                else:
                    yield from shared.change_direction(dx > 0, dx < 0, dy > 0, dy < 0)
                continue
                    

            center_x = world["width"] / 2
            center_y = world["height"] / 2
            my_x = world["me"]["translate"]["x"]
            my_y = world["me"]["translate"]["y"]
            
            if not got_first_data:
                got_first_data = True

            yield from shared.change_direction(my_x > center_x - 20, my_x < center_x + 20, my_y > center_y - 20, my_y < center_y + 20)
    except:
        traceback.print_exc()
    finally:
        yield from socket.close()

@asyncio.coroutine
def run_bot():
    while True:
        yield from hello()
        yield from asyncio.sleep(2)
        shared.reset()
        

asyncio.ensure_future(run_bot())
asyncio.get_event_loop().run_forever()
