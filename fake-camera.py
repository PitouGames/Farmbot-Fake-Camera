#!/usr/bin/env python

'''Fake a photo.'''

import os
from time import time, sleep
import cv2
import numpy as np
from random import randrange
from farmware_tools import device, get_config_value, env

def image_filename():
    'Prepare filename with timestamp.'
    return 'fake-picture-{timestamp}.jpg'.format(timestamp=int(time()))

def upload_path(filename):
    'Filename with path for uploading an image.'
    images_dir = env.Env().images_dir or '/tmp/images'
    if not os.path.isdir(images_dir):
        device.log('{} directory does not exist.'.format(images_dir), 'error')
    path = images_dir + os.sep + filename
    return path

def fake_camera_photo(x_size, y_size):
    'Fake a photo.'
    print('Generate fake image (width:{}, heigth:{})'.format(x_size, y_size))
    device.log('Generate fake image (width:{}, heigth:{})'.format(x_size, y_size), 'debug')

    image = np.zeros((y_size,x_size,3), np.uint8)
    # Fill all image pixels with a random color
    image[:,:] = (randrange(256),randrange(256),randrange(256))

    filename_path = upload_path(image_filename())
    # Save the image to file
    cv2.imwrite(filename_path, image)
    print('Image saved: {}'.format(filename_path))
    device.log('Image saved: {}'.format(filename_path), 'debug')

if __name__ == '__main__':
    X_SIZE = get_config_value('Fake-Camera', 'x_size')
    Y_SIZE = get_config_value('Fake-Camera', 'y_size')
    # Verify user inputs
    if X_SIZE < 1:
        device.log('Width must be positive (used {})! Abort fake camera farmware'.format(X_SIZE), 'error')
        sys.exit(1)
    elif Y_SIZE < 1:
        device.log('Height must be positive (used {})! Abort fake camera farmware'.format(Y_SIZE), 'error')
        sys.exit(1)
    elif X_SIZE > 4096: # Greater than 4K resolution
        device.log('Width is too big, it\'s not a good idea (used {})! Abort fake camera farmware'.format(X_SIZE), 'error')
        sys.exit(1)
    elif Y_SIZE > 4096: # Greater than 4K resolution
        device.log('Height is too big, it\'s not a good idea (used {})! Abort fake camera farmware'.format(X_SIZE), 'error')
        sys.exit(1)

    fake_camera_photo(X_SIZE, Y_SIZE)
