
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import random
from flask import Flask, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['F', 'L', 'R']
turns = ['L', 'R']

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

def HitAction(dir, x, y , line):
    if dir == 'E':
        for i in line:
            if i['x'] - 1 <= x < i['x'] and y == i['y']:
                return turns[random.randrange(len(turns))]
    elif dir == 'N':
        for i in line:
            if i['y'] + 1 >= y > i['y'] and x == i['x']:
                return turns[random.randrange(len(turns))]
    elif dir == 'W':
        for i in line:
            if i['x'] + 1 >= x > i['x'] and y == i['y']:
                return turns[random.randrange(len(turns))]
    elif dir == 'S':
        for i in line:
            if i['y'] - 1 <= y < i['y'] and x == i['x']:
                return turns[random.randrange(len(turns))]
    return moves[random.randrange(len(moves))]

@app.route("/", methods=['POST'])
def move():
    # request.get_data()
    data = request.json
    my_url = data['_links']['self']['href']
    st = data['arena']['state']
    my = st[my_url]
    x = my['x']
    y = my['y']
    dir = my['direction']
    wasHit = my['wasHit']
    logger.info(my)

    line = [{'x': st[i]['x'], 'y': st[i]['y'], 'direction': st[i]['direction'],} for i in st
            if abs(st[i]['x'] - x) <= 3 and abs(st[i]['y'] - y) <= 3 and st[i] != my]

    if wasHit:
        return HitAction(dir, x, y , line)
    elif dir == 'E':
        for i in line:
            if i['x'] - 3 <= x < i['x'] and y == i['y']:
                return 'T'
    elif dir == 'N':
        for i in line:
            if i['y'] + 3 >= y > i['y'] and x == i['x']:
                return 'T'
    elif dir == 'W':
        for i in line:
            if i['x'] + 3 >= x > i['x'] and y == i['y']:
                return 'T'
    elif dir == 'S':
        for i in line:
            if i['y'] - 3 <= y < i['y'] and x == i['x']:
                return 'T'

    return moves[random.randrange(len(moves))]

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
