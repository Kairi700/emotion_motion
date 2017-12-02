import numpy
import cv2
import pykinect
from pykinect import nui
from pykinect.nui import JointId

import itertools

video = numpy.empty((480,640,4),numpy.uint8)
depth = numpy.empty((240,320,1),numpy.uint16)

skeletons = None

# skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

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

def draw(skeletons, video):
    # print("Draw")
    for index, data in enumerate(skeletons):
        print("Skele")
        # draw the Head
        HeadPos = data.SkeletonPositions[JointId.Head] 
        draw_skeleton_data(video, data, index, SPINE, 10)
        # pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
    
        # drawing the limbs
        draw_skeleton_data(video, data, index, LEFT_ARM)
        draw_skeleton_data(video, data, index, RIGHT_ARM)
        draw_skeleton_data(video, data, index, LEFT_LEG)
        draw_skeleton_data(video, data, index, RIGHT_LEG)

def kinect_to_cv(p):
    if p.z < 1e-7:
        return (0, 0)

    #x = p.x * 285.63 / p.z
    #y = p.y * 285.63 / p.z
    x = (p.x / p.z + 0.5) * 640.0
    y = (0.5 - p.y / p.z) * 480.0
    return (int(x), int(y))

def draw_skeleton_data(video, pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
    
    #print(start)
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = start
        curend = next

        print(curstart)

        cv2.line(video, kinect_to_cv(curstart), kinect_to_cv(curend), SKELETON_COLORS[index], width)
        # pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next

def depth_frame_ready(frame):    
    global depth
    # video = numpy.empty((480,640,4),numpy.uint8)
    frame.image.copy_bits(depth.ctypes.data)

    # cv2.imshow('KINECT Depth Stream', video)
    # print("Depth")


def video_frame_ready(frame):
    global video
    # video = numpy.empty((480,640,4),numpy.uint8)
    frame.image.copy_bits(video.ctypes.data)

    # cv2.imshow('KINECT Video Stream', video)
    # print("Video")


def post_frame(frame):
    print("Boop")
    global skeletons
    if len(frame.SkeletonData) > 0:
        skeletons = frame.SkeletonData
        # try:
        #     #pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
        #     pass
        # except:
        #     # event queue full
        #     pass


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
            cv2.imshow('KINECT Video Stream', video)

        if depth is not None:
            cv2.imshow('KINECT Depth Stream', depth)

        if cv2.waitKey(50) == 27:
            break
