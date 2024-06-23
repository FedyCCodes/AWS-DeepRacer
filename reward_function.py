# Place import statement outside of function (supported libraries: math, random, numpy, scipy, and shapely)
# Example imports of available libraries
#
# import math
# import random
# import numpy
# import scipy
# import shapely

import math

def reward_function(params):
    
    '''
    {
        "all_wheels_on_track": Boolean,        # flag to indicate if the agent is on the track
        "x": float,                            # agent's x-coordinate in meters
        "y": float,                            # agent's y-coordinate in meters
        "closest_objects": [int, int],         # zero-based indices of the two closest objects to the agent's current position of (x, y).
        "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
        "distance_from_center": float,         # distance in meters from the track center 
        "is_crashed": Boolean,                 # Boolean flag to indicate whether the agent has crashed.
        "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not. 
        "is_offtrack": Boolean,                # Boolean flag to indicate whether the agent has gone off track.
        "is_reversed": Boolean,                # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
        "heading": float,                      # agent's yaw in degrees
        "objects_distance": [float, ],         # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
        "objects_heading": [float, ],          # list of the objects' headings in degrees between -180 and 180.
        "objects_left_of_center": [Boolean, ], # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
        "objects_location": [(float, float),], # list of object locations [(x,y), ...].
        "objects_speed": [float, ],            # list of the objects' speeds in meters per second.
        "progress": float,                     # percentage of track completed
        "speed": float,                        # agent's speed in meters per second (m/s)
        "steering_angle": float,               # agent's steering angle in degrees
        "steps": int,                          # number steps completed
        "track_length": float,                 # track length in meters.
        "track_width": float,                  # width of the track
        "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center
    
    }
    '''
    
    ###################
    ##### Initial #####
    ###################
    
    '''
    Example of using waypoints and heading to make the car point in the right direction
    '''

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    abs_steering = abs(params['steering_angle']) # Only need the absolute steering angle
    steering = params['steering_angle']
    all_wheels_on_track = params['all_wheels_on_track']
    is_left_of_center = params['is_left_of_center']
    
    reward = 1
    
    
    ###################
    ##### Wheels  #####
    ###################
    
    '''
    All Wheels on Track:
    '''
    
    # Give a high reward if no wheels go off the track and 
    # the car is somewhere in between the track borders 
    if all_wheels_on_track:
        reward *= 1.5
        if (0.5*track_width - distance_from_center) >= 0.05:
            reward *= 1.8
    else:
        reward *= 0.5
    
    
    ###################
    ##### Center  #####
    ###################
    
    '''
    Track Center Section:
    '''
    
    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.05 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.6 * track_width
    marker_4 = 0.9 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward *= 5.0
    elif distance_from_center <= marker_2:
        reward *= 2.0
    elif distance_from_center <= marker_3:
        reward *= 1.0
    elif distance_from_center <= marker_4:
        reward *= 0.4
    elif distance_from_center > marker_4:
        reward *= 1e-10
        # if it's way off then it goes
    
    ###################
    #### Oversteer ####
    ###################
    
    '''
    Checking Oversteering to direction
    '''
    
    
    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 20.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.6
    elif DIRECTION_THRESHOLD * 0.5 <= direction_diff and direction_diff <= DIRECTION_THRESHOLD:
        reward *= 1.2
    else:
        reward *= 2.0
    
    ###################
    #### Steering  ####
    ###################
    
    '''
    Steering Reward Section:
    '''
    
    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 30 
    
    # Penalize reward if the car is steering too much
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.6
    else:
        reward *= 1.2
    
    ###################
    ##### Return  #####
    ###################
    
    '''
    Returning The Reward:
    '''
    
    return float(reward)