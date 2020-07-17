## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2
from PIL import Image
import os
import random, string

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

IMG_DIR = "imgs"
DEPTH_DIR = "depth_imgs"

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(DEPTH_DIR, exist_ok=True)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        # if not color_frame:
        #     continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # 0 - 65535 to 0 - 255
        depth_3ch = np.zeros_like(color_image)
        depth_3ch[:,:, 0] = depth_image % 256
        depth_3ch[:,:, 1] = depth_image // 256

        # Stack both images horizontally
        images = np.hstack([color_image, depth_colormap])

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        # cv2.waitKey(1)

        k = cv2.waitKey(1)

        if k == 32:  # space
            color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            fname = randomname(8)
            Image.fromarray(color_image).save(f"{IMG_DIR}/{fname}.png")
            Image.fromarray(depth_3ch).save(f"{DEPTH_DIR}/{fname}.png")
        elif k == 27:  # esc
            break

finally:

    # Stop streaming
    pipeline.stop()