import numpy as np
import cv2
import pykinect
from pykinect import nui
from pykinect.nui import JointId

import itertools

#TODO Modularize system into distinct classes and files

DEBUG_MODE = True;

VIDEO_WIDTH = 480
VIDEO_HEIGHT = 640

DEPTH_WIDTH = 240
DEPTH_HEIGHT = 320

video = np.empty((VIDEO_WIDTH,VIDEO_HEIGHT,4),np.uint8)
depth = np.empty((DEPTH_WIDTH,DEPTH_HEIGHT,1),np.uint16)

skeletons = None
skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

SKELETON_COLORS = [(255,0,0),
                   (0,0,255),
                   (0,255,0), 
                   (255,65,0), 
                   (255,0,255), 
                   (255,255,0), 
                   (255,0,125)]

LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)

CURRENT_LEFT_ARM = (0, 0, 0, 0, 0)
CURRENT_RIGHT_ARM = (0, 0, 0, 0, 0)
CURRENT_LEFT_LEG = (0, 0, 0, 0, 0)
CURRENT_RIGHT_LEG = (0, 0, 0, 0, 0)
CURRENT_SPINE = (0, 0, 0, 0)

RAISED_ARM_ANGLE = 45

##### Poor coding practice, fix later

def recordLeftArmPos(data): 
    global CURRENT_LEFT_ARM
    CURRENT_LEFT_ARM = (data.SkeletonPositions[JointId.ShoulderCenter], 
            data.SkeletonPositions[JointId.ShoulderLeft], 
            data.SkeletonPositions[JointId.ElbowLeft], 
            data.SkeletonPositions[JointId.WristLeft], 
            data.SkeletonPositions[JointId.HandLeft])

def recordRightArmPos(data): 
    global CURRENT_RIGHT_ARM
    CURRENT_RIGHT_ARM = (data.SkeletonPositions[JointId.ShoulderCenter], 
             data.SkeletonPositions[JointId.ShoulderRight], 
             data.SkeletonPositions[JointId.ElbowRight], 
             data.SkeletonPositions[JointId.WristRight], 
             data.SkeletonPositions[JointId.HandRight])

def recordLeftLegPos(data): 
    global CURRENT_LEFT_LEG
    CURRENT_LEFT_LEG = (data.SkeletonPositions[JointId.HipCenter], 
            data.SkeletonPositions[JointId.HipLeft], 
            data.SkeletonPositions[JointId.KneeLeft], 
            data.SkeletonPositions[JointId.AnkleLeft], 
            data.SkeletonPositions[JointId.FootLeft])

def recordRightLegPos(data): 
    global CURRENT_RIGHT_LEG
    CURRENT_RIGHT_LEG = (data.SkeletonPositions[JointId.HipCenter], 
             data.SkeletonPositions[JointId.HipRight], 
             data.SkeletonPositions[JointId.KneeRight], 
             data.SkeletonPositions[JointId.AnkleRight], 
             data.SkeletonPositions[JointId.FootRight])

def recordSpinePos(data): 
    global CURRENT_SPINE
    CURRENT_SPINE = (data.SkeletonPositions[JointId.HipCenter], 
         data.SkeletonPositions[JointId.Spine], 
         data.SkeletonPositions[JointId.ShoulderCenter], 
         data.SkeletonPositions[JointId.Head])

##################################################### Change everything above

def getLeftArmPos():
    return CURRENT_LEFT_ARM 

def getRightArmPos():
    return CURRENT_RIGHT_ARM 

def getLeftLegPos():
    return CURRENT_LEFT_LEG 

def getRightLegPos():
    return CURRENT_RIGHT_LEG 

def getSpinePos():
    return CURRENT_SPINE 


def debugPrint(statement):
    if DEBUG_MODE:
        print(str(statement))

def draw(skeletons, video):
    # print("Draw")
    for index, data in enumerate(skeletons):
        # print("Skele")
        # draw the Head
        HeadPos = data.SkeletonPositions[JointId.Head] 
        draw_skeleton_data(video, data, index, SPINE, 10)
    
        # drawing the limbs
        draw_skeleton_data(video, data, index, LEFT_ARM)
        # with open("position.txt", "a") as f:
        #     f.write("-------------------- LEFT ARM --------------------")
        #     f.write(str(data.SkeletonPositions[JointId.ShoulderCenter]))
        #     f.write(str(data.SkeletonPositions[JointId.ShoulderLeft]))
        #     f.write(str(data.SkeletonPositions[JointId.ElbowLeft]))
        #     f.write(str(data.SkeletonPositions[JointId.WristLeft]))
        #     f.write(str(data.SkeletonPositions[JointId.HandLeft]))
        #     f.write("--------------------------------")
        #     f.close()

        # print("-------------------- LEFT ARM --------------------")
        # print("ShoulderCenter")
        # print(data.SkeletonPositions[JointId.ShoulderCenter])
        # print("ShoulderLeft")
        # print(data.SkeletonPositions[JointId.ShoulderLeft])
        # print("ElbowLeft")
        # print(data.SkeletonPositions[JointId.ElbowLeft])
        # print("WristLeft")
        # print(data.SkeletonPositions[JointId.WristLeft])
        # print("HandLeft")
        # print(data.SkeletonPositions[JointId.HandLeft])
        # print("--------------------------------")
        draw_skeleton_data(video, data, index, RIGHT_ARM)
        draw_skeleton_data(video, data, index, LEFT_LEG)
        draw_skeleton_data(video, data, index, RIGHT_LEG)

        recordLeftArmPos(data)
        recordRightArmPos(data)
        recordLeftLegPos(data)
        recordRightLegPos(data)
        recordSpinePos(data)

def kinect_to_cv(p):
    if p.z < 1e-7:
        return (0, 0)
    x = (p.x / p.z + 0.5) * 640.0
    y = (0.5 - p.y / p.z) * 480.0
    return (int(x), int(y))

def draw_skeleton_data(video, pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
    
    #print(start)
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]

        ##################################
        
        curstart = start
        curend = next

        # debugPrint(curstart)

        cv2.line(video, kinect_to_cv(curstart), kinect_to_cv(curend), SKELETON_COLORS[index], width)


        ##################################

        #TODO Use depth to make body frame tracking more accurate
        # Figure out why positions keep coming back as 0


        # curstart = skeleton_to_depth_image(start, VIDEO_WIDTH, VIDEO_HEIGHT)
        # curend = skeleton_to_depth_image(next, VIDEO_WIDTH, VIDEO_HEIGHT)

        # print(curstart)

        # cv2.line(video, (int(curstart[0]), int(curstart[1])), (int(curend[0]), int(curend[1])), SKELETON_COLORS[index], width)

        ##################################
        
        start = next

def depth_frame_ready(frame):    
    global depth
    frame.image.copy_bits(depth.ctypes.data)
    # print("Depth")


def video_frame_ready(frame):
    global video
    frame.image.copy_bits(video.ctypes.data)
    # print("Video")


def post_frame(frame):
    global skeletons
    if len(frame.SkeletonData) > 0:
        skeletons = frame.SkeletonData

def getAngleBetweenVectors(vec_1=(0,0), vec_2=(0,0)):
    numer = np.dot(vec_1, vec_2)
    denom = np.dot(np.linalg.norm(vec_1), np.linalg.norm(vec_2))

    if denom==0:
        return 90

    return np.arccos(numer/denom)*(180/np.pi)

def isIntersect(vec_1=(0,0), vec_2=(0,0)):
    # if(np.intersect1d(vec_1,vec_2)):
    #     return True
    return False

def leftArmCheck():
    left_arm = getLeftArmPos()
    shoulder = left_arm[1]
    wrist = left_arm[3]

    print(shoulder)
    print(wrist)

    arm_vec = (shoulder.x-wrist.x, shoulder.y-wrist.y)

    print(arm_vec)

    angle = getAngleBetweenVectors(arm_vec,(VIDEO_WIDTH,0))
    print(angle)

    # return (getAngleBetweenVectors())


# LEFT_ARM = (JointId.ShoulderCenter, 
#             JointId.ShoulderLeft, 
#             JointId.ElbowLeft, 
#             JointId.WristLeft, 
#             JointId.HandLeft)
# RIGHT_ARM = (JointId.ShoulderCenter, 
#              JointId.ShoulderRight, 
#              JointId.ElbowRight, 
#              JointId.WristRight, 
#              JointId.HandRight)


def rightArmCheck():
    right_arm = getRightArmPos()
    shoulder = right_arm[1]
    wrist = right_arm[3]

    angle = getAngleBetweenVectors((shoulder,wrist),(0,VIDEO_WIDTH))
    print(angle)

def crossArmCheck():
    pass

def findPatterns():
    leftArmCheck()
    # rightArmCheck()
    # crossArmCheck()

    # pass


if __name__ == '__main__':
    kinect = nui.Runtime()
    kinect.skeleton_engine.enabled = True

    kinect.skeleton_frame_ready += post_frame
    
    kinect.depth_frame_ready += depth_frame_ready
    kinect.video_frame_ready += video_frame_ready

    kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
    kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution320x240, nui.ImageType.Depth)

    while True:
        if video is not None:
            if skeletons is not None:
                draw(skeletons, video)
                #Detect arm patterns
                findPatterns()
            cv2.imshow('KINECT Video Stream', video)

        if depth is not None:
            cv2.imshow('KINECT Depth Stream', depth)

        if cv2.waitKey(50) == 27:
            break
