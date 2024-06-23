# AWS DeepRacer:

This repository presents my submission for the AWS DeepRacer competition in which the goal is to have self driving vehicles in a virtual environment. The competition included an initial virtual course to understand the basics of machine learning and how the competition is operated.

## How to run:

For this specific project, the code in `reward_function.py` was written inside the agent when submitted on the AWS Student Console. Once the agent was in the training phase, I analyzed it's performance when remaining on track to determine it's efficiency. The specific model for this code is recommended to be trained for at least 15 minutes before the agent is able to complete the race track.

* *Note: The agent is the car in the simulated environment.*

![Models](./.github_images/models.png)

### Code Contents:

The contents of `reward_function.py` consists of a function that returns a floating point number which allows the agent to be rewarded or punished based on the direction it takes based on it's surrounding environment.

### Code Structure:

There are 4 main parts of the code being the extraction of input data, checking that the wheels are on the road, checking that it's centered, and preventing oversteering.

#### Input Data:

In the beginning of the function, it takes out all the necessary variables from the `params` parameter that comes with the `reward_function`.

```python
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
```

#### Checking Wheels On Track:

The first section that influenced the reward function of the agent was based on if the wheels were on the track.

```python
# Give a high reward if no wheels go off the track and 
# the car is somewhere in between the track borders 
if all_wheels_on_track:
    reward *= 1.5
    if (0.5*track_width - distance_from_center) >= 0.05:
        reward *= 1.8
else:
    reward *= 0.5
```

#### Checking Centered:

If the agent was very close to the center of the track it received a higher reward because that would indicate that it's not moving off the track.

```python
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
```

* *Note: The code above is truncated, variables such as `marker_1` are predefined and calculated, this is a condensed representation. All the code is available in the `reward_function.py` file.*

#### Preventing Oversteering:

The reward function had multiple different checks to prevent oversteering, one was general and was created to prevent zig zagging, while the other was to make sure that it wasn't going off course from the track.

```python
# Penalize the reward if the difference is too large
DIRECTION_THRESHOLD = 20.0
if direction_diff > DIRECTION_THRESHOLD:
    reward *= 0.6
elif DIRECTION_THRESHOLD * 0.5 <= direction_diff and direction_diff <= DIRECTION_THRESHOLD:
    reward *= 1.2
else:
    reward *= 2.0
```

* *Note: The code above is truncated, variables such as `direction_diff` are calculated beforehand, this is a condensed representation. Additionally, reward factors were determined through trial and error by running agents with different values to determine which was most efficient. All the code is available in the `reward_function.py` file.*

## Models:

Before I submitted my final reward function for the agent, I created 16 different models before I concluded which model to use and iterated on each of them.

### Format:

The names of each model was in the format `M###` where the `###` was a 3 digit hexadecimal number. However the finalized model ended up including a `-C` for cleaned up, and a `-F` for finalized.

### Explanations:

Here are each model and an explanation of what they did.

- `M000`: The initial template provided by AWS DeepRacer for trying to remain on course.
- `M001`: Iterated on model `M000` by changing the values and using more of the code provided.
- `M002`: Modified the values in `M001` to improve performance.
- `M003`: Modified the values in `M002` and added a prevention for zig zagging.
- `M004`: Iterated on `M003` and included specific limitations for rotation.
- `M005`: Iterated on `M004` and improved values for specific limitations for rotation.
- `M006`: Iterated on `M005` but with a restructured system for calculating the reward function.
- `M007`: Revereted back from `M006` to `M005` with a different restructuring system.
  - *Note: First model to successfully complete the track properly.*
- `M008`: Iteration of `M007` with emphasis on the speed
- `M007-C`: Cleaned up model `M007` since emphasizing speed caused the agent to exit the track prematurely.
- `M009`: Iteration of `M007-C` with prevention of oversteering.
- `M00A`: Iteration of `M009` with emphasis on steering and speed.
- `M00B`: Iteration of `M00A` with different values.
- `M00C`: Iteration of `M00B` but stronger emphasis on speed
  - *Note: While this model was effective it wasn't performing as well as well as `M007-C`.*
- `M00D`: Iteration of `M007-C` but stronger emphasis on speed
- `M007-F`: The final model which is primarily the `M007-C` because `M00D` while worked wasn't as effective as `M007-C`


## Screenshots:

Here is a photo of the final model compiled and was submitted:

![Image](./.github_images/race.png)

Here is a photo of the the best submitted model:

![Image](./.github_images/time.png)

## Sources:

Here are all the sources used during this project:

- [AWS DeepRacer Home Page](https://student.deepracer.com/home): The main home page of the AWS DeepRacer project.
- [AWS DeepRacer Documentation](https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html): This was the main documentation document for how to use the input parameters and general suggestions for how to create your agent.
- [AWS DeepRacer General](https://docs.aws.amazon.com/deepracer/latest/student-userguide/what-is-scholarship.html): The document that explained how to participate in the AWS DeepRacer and how to use the tools they provided. 
