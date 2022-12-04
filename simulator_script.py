import glob
import os
import sys
import random
import time
import numpy as np
import cv2
import glob


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

IM_WIDTH = 1242
IM_HEIGHT = 375

def process_image(image):
    i1 = np.array(image.raw_data)
    i2 = i1.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    # print(i3/255.0)
    # cv2.imshow("", i3)
    cv2.waitKey(1)
    return image.save_to_disk('_out/%06d.png' % image.frame, cc)

actor_list = []


try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    dworld = client.get_world()
    # print(client.get_available_maps())
    # world = client.load_world("/Game/Carla/Maps/Town03") ## diff paths for diff world generation
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter("model3")[0] # found sensor locations for model 3 so why not
    spawn_points = random.choice(world.get_map().get_spawn_points())
    vehicle = world.spawn_actor(vehicle_bp, spawn_points)
    actor_list.append(vehicle)

    # vehicle.set_autopilot(True)
    # vehicle.apply_control(carla.VehicleControl(throttle = 1.0 , steer = 0.0))

    camera_bp = blueprint_library.find("sensor.camera.rgb")
    camera_bp.set_attribute("image_size_x", f"{IM_WIDTH}")
    camera_bp.set_attribute("image_size_y", f"{IM_HEIGHT}")
    camera_bp.set_attribute("fov", "110")
    camera_spawn_point = carla.Transform(carla.Location(x=2.5,z=0.7))
    sensor = world.spawn_actor(camera_bp, camera_spawn_point, attach_to=vehicle)
    actor_list.append(sensor)

    cc = carla.ColorConverter.LogarithmicDepth
    # sensor.listen(lambda image: image.save_to_disk('_out/%06d.png' % image.frame, cc))
    sensor.listen(lambda data : process_image(data))

    time.sleep(50)

    # img_array = []
    # for filename in glob.glob(r"D:/Carla/WindowsNoEditor/PythonAPI/examples/_out/*.png"):
    #     height,width,layers = cv2.imread(filename).shape
    #     #print(img)
    #     #cv2.imshow("", img)
    #     #height,width,layers = img.shape
    #     size = (width,height)
    #     img_array.append(())

    # out = cv2.VideoWriter('inputVideo.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    # for i in range(len(img_array)):
    #     out.write(img_array[i])
        
    # out.release()

    pass
finally:
    print("Simulation time limit reached")
    for actor in actor_list:
        actor.destroy()
    print("All actors cleaned up")
