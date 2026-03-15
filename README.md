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
git clone https://github.com/Sebgra518/DroneDockingSim.gitDroneDockingSim
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
