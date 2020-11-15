#!/usr/bin/env python3
#
# Uses excerpts of code modified from https://github.com/OlafenwaMoses/ImageAI
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
from anki_vector.util import degrees, Angle, Pose
from imageai.Prediction import ImagePrediction
import os
from PIL import Image, ImageStat
import time
from datetime import date, datetime
import sys

robot = anki_vector.Robot('0050169f')
robot.connect()
d = robot.proximity.last_sensor_reading.distance
distance = int(d.distance_mm)
distance_cms = distance / 10

#if object is within this distance, the prediction model will begin, change distance to over 400 to stop predicting objects to far away.
if (distance)<=390:
#    robot pose is recorded for future use
    pose = robot.pose
    robot.behavior.set_lift_height(0)
    robot.behavior.set_head_angle(degrees(12.0))
    robot.behavior.say_text("I found something!")
    image = robot.camera.capture_single_image()
    today = date.today()
    date = today.strftime("%A %d, %B")
    time = datetime.now().strftime(("%H:%M"))
    timeDate = (str(date) + " at " + str(time))
 
    image.raw_image.save('pictures/capture.jpeg', 'JPEG')
    new_image = Image.open('pictures/capture.jpeg')
    resize_image = new_image.resize((184, 96))

    #object prediction code below
    prediction = ImagePrediction()
    prediction.setModelTypeAsResNet()
    prediction.setModelPath("model/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
    prediction.loadModel()
    predictions, percentage_probabilities = prediction.predictImage ("pictures/capture.jpeg", result_count=1)
    for index in range(len(predictions)):
        i = 1
        s = (predictions[index])
        print(s.replace('_', ' ') , " : " , percentage_probabilities[index])
        resize_image.save('pictures/predicted/{}.jpeg'.format(s), 'JPEG')
        while os.path.exists("data/capture%s.txt" % i):
            i += 1
        f= open("data/capture%s.txt" % i, "w")
        f.write("{}".format(s))
        f.close()
        
        if (percentage_probabilities[index] >= 90):
            print("That is definitely a {}".format(s.replace('_', ' ')))
            robot.anim.play_animation_trigger('GreetAfterLongTime')
            robot.behavior.say_text("That is definitely a {}".format(s.replace('_', ' ')))

        if (percentage_probabilities[index] <= 90) and (percentage_probabilities[index] >= 60):
            print("That looks like a {}".format(s.replace('_', ' ')))
            robot.behavior.say_text("That looks like a {}".format(s.replace('_', ' ')))

        if (percentage_probabilities[index] <= 60) and (percentage_probabilities[index] >= 30):
            print("I'm not sure but that looks like a {}".format(s.replace('_', ' ')))
            robot.behavior.say_text("I'm not sure but that looks like a {}".format(s.replace('_', ' ')))

        if (percentage_probabilities[index] <= 30) and (percentage_probabilities[index] >= 0):
            print("Thats tricky, is it a {}".format(s.replace('_', ' ')))
            robot.behavior.say_text("Thats tricky, is it a {}".format(s.replace('_', ' ')))

        robot.disconnect()
        
#        creates the .txt file used for the Recollection.py script later
        data = (s.replace('_', ' ')), timeDate, pose
        f= open("data/found_items.txt","a+")
        f.write(s.replace('_', ' ') + "|")
        f.write(timeDate + "|")
        f.write(str(pose) + "\n")
        f.close()
        
else:
    print("Objects are over {} centimeters away, please move me closer". format(distance_cms))
    robot.behavior.say_text("Objects are over {} centimeters away, please move me closer". format(distance_cms))
    sys.exit()