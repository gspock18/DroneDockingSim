#####

**IF YOU'RE TRYING TO INSTALL GAZEBO, SKIP TO DRONEDOCKINGSIM**

Changelog - Harley Estrella April 24, 2026

1. switched all references for iris_with_standoffs in model.sdf of ardupilot_1 to iris_with_standoffs_2x_scaled
2. created a parameter file to change the strength of motors of drone
3. use a different control script to run parameters when using drone_1
4. created a dock_two_drones.py file to run script of drone2 docking on drone1
5. use script to run dock_two_drones.py

***changed from vertical to horizontal docking:

6. created folders for STL files made by Sebastian so we can reference them easier in code for gazebo/ros.
	1.1 See folders in /home/harley-estrella/DroneDockingSim/ros2_ws/src/drone_docking_sim/models: custom_parts, female_drone, male_drone

7. Added 2 files in the ardupilot_gazebo directory models as parent sdf files for drone1 and 2, respectively iris_with_standoffs_male and iris_with_standoffs_female.
8. Changed 2x drone to a regular sized drone
9. Added the connectors and attached them to both drones. Drone1 has the male, and drone2 has the female connector by changing the parent sdf files.
10. Added a new script so that they will mount horizontally and latch onto each other: dock_and_latch.py.
11. Added a wind resistance <plugin> code to two_iris.sdf to simulate wind resistance in the future. This is currently commented out and not in use.
12. Fixed plugin for the detach/topic within iris_with_standoffs_female and now it works. 

#####
Changelog - Harley Estrella May 18, 2026

1. Added slow_dock.py in DroneDockingSim/ros2_ws/Docking_Script_and_Trials folder.
2. Fixed the latch and detach bugs. Drones now attach to each other and move as one rigid body.
3. Added data collection for drone stability that is saved as a csv file in the same folder of slow_dock.py
4. Added motor control after latch to sync the two drones so that they will move in unison but still unsuccessful with implementation.
5. Moved two_drones_script.py to Docking_Script_and_Trials folder.
6. Added step in README.md for running slow_dock.py

#####
Changelog - Harley Estrella September 10, 2026

1. Added changelog and next steps to readme.

#####

**Next Steps**

1. Extract Drone_with_Dockers.zip
2. Copy the following folders to ***your_path***/DroneDockingSim/ros2_ws/src/drone_docking_sim/models
    a. custom_parts
    b. female_drone
    c. male_drone
    d. iris_with_ardupilot_0
    e. iris_with_ardupilot_1
    f. iris_with_ardupilot_2
3. Copy the following folders to ***your_path***/ardupilot_gazebo/models
    a. iris_with_standoffs_female
    b. iris_with_standoffs_male
    c. iris_with_standoffs_2x_scaled
4. Copy the following folders to ***your_path***/DroneDockingSim/ros2_ws
    a. dock_and_latch.py
    b. dock_two_drones.py 

5. Reload your Simulation. It should now have the 2 drones with connectors facing each other.
6. Run the following into a new terminal:
    a. make sure to change the tcp:127.0.0.1:xxxx to match your 2 drones address
    
    python3 dock_and_latch.py \
  --drone1 tcp:127.0.0.1:5762 \ 
  --drone2 tcp:127.0.0.1:5772 \
  --takeoff-alt 1.5 \
  --prelatch-x 0.50 \
  --final-x 0.12 \
  --xy-tol 0.03 \
  --z-tol 0.02 \
  --attach-topic /model/drone1/detachable_joint/attach

7. As of now, the drones cannot dock on each other with the script. Our next goal is to have a working script that will make them latch onto each other.you paste your iris_with_standoffs_male.sdf, I’ll place the plugin in the exact correct spot and adjust the child_model_link if your child base link is scoped differently.

############

May 18, 2026 Update

Instructions for future of project

Notes: 
We have resolved the latch and detach issue. What we need now is to change the maximum strength of the rotors in ArduPilot parent iris.
Later on we need to add weather effects to simulate different wind resistance to see the stability of the lathced drones.

1. Once you've updated your repo, run the same simulation until you've connected to both drones within Gazebo.
2. Run the following code:

    cd DroneDockingSim/ros2_ws/Docking_Script_and_Trials
    python slow_dock.py 

# DroneDockingSim

Multi-Drone ArduPilot + Gazebo Harmonic + ROS 2 Simulation

This project provides a reproducible simulation environment for controlling two ArduPilot-based quadcopters in Gazebo Harmonic using ROS 2 (Jazzy).

It includes:

- Gazebo world with two drones
- Dual ArduPilot SITL instances
- MAVLink-based Python control script
- ROS 2 launch integration

## Requirements

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic
- ArduPilot (with SITL built)
- ardupilot_gazebo plugin

## Setup

### 1) Clone the repository

```bash
git clone https://github.com/Sebgra518/DroneDockingSim.git
cd DroneDockingSim/ros2_ws
```

### 2) Source ROS 2

```bash
source /opt/ros/jazzy/setup.bash
```

### 3) Create Python Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
touch venv/COLCON_IGNORE
pip install --upgrade pip
pip install pymavlink
```

### 4) Build the Workspace

```
rm -rf build install log
export AMENT_PYTHON_EXECUTABLE=$(which python)
export PYTHON_EXECUTABLE=$(which python)

colcon build --symlink-install
source install/setup.bash
```

### 5) Configure Gazebo Model Path

```
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:$HOME/ardupilot_gazebo/models:$HOME/ardupilot_gazebo/worlds
```

## Running the Simulation

This starts:

- Gazebo
- Two ArduPilot SITL instances
- MAVProxy console

### Manual Bringup

Find the correct directory for following files in your device

- /home/***USERNAME***/DroneDockingSim/ros2_ws/src/models/iris_with_ardupilot_1
- /home/***USERNAME***/DroneDockingSim/ros2_ws/src/models/iris_with_ardupilot_2
- /home/***USERNAME***/DroneDockingSim/ros2_ws/src/worlds/two_iris.sdf

You will need the correct directory to properly load the simulation

Start up 3 Terminal Instances

***Terminal 2 and 3 should each open a MAVProxy console that displays drone data***

#### Terminal 1 (Gazebo)

```
export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/ardupilot_gazebo/build
export GZ_SIM_RESOURCE_PATH=$HOME/DroneDockingSim/ros2_ws/src/drone_docking_sim/models:$HOME/DroneDockingSim/ros2_ws/src/drone_docking_sim/worlds:$HOME/ardupilot_gazebo/models:$HOME/ardupilot_gazebo/worlds

gz sim -v4 -r ~/DroneDockingSim/ros2_ws/src/drone_docking_sim/worlds/two_iris.sdf
```

#### Terminal 2 (Drone 1)

```
cd ~/ardupilot
source ~/ardupilot_venv/bin/activate

sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON -I0 --console --map
```

#### Terminal 3 (Drone 2)

```
cd ~/ardupilot
source ~/ardupilot_venv/bin/activate

sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON -I1 --console --map
```

#### Terminal 4 (Script)

```
cd DroneDockingSim/ros2_ws/Docking_Script_and_Trials
python slow_dock.py 
```
#### ***Test Your Drones***

Type the following in Drones 1 and 2 terminals.

```
mode GUIDED
arm throttle
takeoff 5
```
_this will let your drones fly 5 meters off the ground_

```
mode rtl
LAND
```
_this will let your drones land from takeoff spot_

### Full Bringup

```
ros2 launch drone_docking_sim bringup_two_drones.launch.py
```

## Running the Python Control Script

```
cd ros2_ws
source venv/bin/activate
source /opt/ros/jazzy/setup.bash
source install/setup.bash

python -m drone_docking_sim.two_drones_script
```

The script will:

- Arm both drones
- Take off to 10 meters
- Move 10 meters north
- Land


### NEXT STEPS

```
Once your gazebo can load the 2 drones and can be controlled in the terminals head to the Drone_with_Dockers folder and open Next_Instructions.txt
```

# Troubleshooting

# NOTE: ALL COMMANDS ARE ASSUMING DEFAULT FILE LOCATIONS

### ```ros2: command not found``` OR ```Package 'drone_docking_sim' not found: "package 'drone_docking_sim' not found, searching: ['/opt/ros/jazzy']"```

Inside of your repo:

```
cd ./ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 pkg list | grep drone_docking_sim
```

### [Err] [Server.cc:86] Error Code 14: [/sdf/world[@name="two_iris_world"]/include[3]/uri:/home/sebgra518/Documents/GitHub/DroneDockingSim/ros2_ws/src/drone_docking_sim/worlds/two_iris.sdf:L24]: Msg: Unable to find uri[model://iris_with_ardupilot_1]

```
export GZ_SIM_RESOURCE_PATH=$HOME/Documents/GitHub/DroneDockingSim/ros2_ws/src/drone_docking_sim/models:$GZ_SIM_RESOURCE_PATH
export GZ_SIM_RESOURCE_PATH=$HOME/ardupilot_gazebo/models:$GZ_SIM_RESOURCE_PATH
export GZ_SIM_RESOURCE_PATH=$HOME/ardupilot_gazebo/worlds:$GZ_SIM_RESOURCE_PATH
```

### Build from Source MAVProxy:

```
sudo apt-get update
sudo apt-get install python3-pip python3-dev python3-lxml python3-tk python3-pygame python3-scipy python3-serial python3-pexpect

# Install MAVProxy via pip
pip3 install --upgrade pymavlink mavproxy   
```

### Failed to load system plugin [ArduPilotPlugin] : Could not find shared library.
```
export GZ_SIM_SYSTEM_PLUGIN_PATH=/home/sebgra518/ardupilot_gazebo/build:$GZ_SIM_SYSTEM_PLUGIN_PATH
```
