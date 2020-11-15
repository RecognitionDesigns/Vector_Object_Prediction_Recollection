#!/usr/bin/env python3
#
# Copyright (c) 2020 Recognition Designs Ltd, Colin Twigg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# for use with DDL/Anki's Vector Robot: https://www.anki.com/en-us/vector

import anki_vector
import time
import os.path
import os
import sys
from PIL import Image

def image_screen():
    i = 1
    while True:
        check_file_exists = ('data/capture%s.txt' % i)
        if os.path.isfile(check_file_exists) == True:
            capture = open("data/capture%s.txt" % i, "r")
            if capture.mode == 'r':
                capture_image = capture.read()
                print("Displaying {} photo on Vectors face...".format(capture_image))

            current_directory = os.path.dirname(os.path.realpath(__file__))
            image_path = os.path.join(current_directory, 'pictures/predicted', '{}.jpeg'.format(capture_image))
            image_file = Image.open(image_path)

            screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
            robot.screen.set_screen_with_image_data(screen_data, 20.0)
            time.sleep(9)
            i += 1
        
        else:
            sys.exit()
locate = {}
i = 1

with open("data/found_items.txt", 'r') as f:
    for line in f:
        listDetails = line.strip().split("|")
        locate[i] = {"I saw": listDetails[0]}
        locate[i].update({"on ": listDetails[1]})
#        pose data not used yet, still some work to do to incorparate this into the iterations
#        locate[i].update({"Position from base found": listDetails[2]})
        i+=1
    
#option to print out the lines from the found_items.txt file  
#print(locate)

with anki_vector.AsyncRobot('0050169f') as robot:
    robot.behavior.set_head_angle(anki_vector.util.degrees(33.0))
    robot.behavior.say_text(str(locate).replace("'", " "))
    image_screen()