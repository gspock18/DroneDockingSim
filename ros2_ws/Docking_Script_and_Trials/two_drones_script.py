#!/usr/bin/env python3
from pymavlink import mavutil
import time

def connect(port: int):
    """
    Connect to an ArduPilot SITL instance via TCP on localhost.
    Ports are commonly 5760, 5770 for -I0/-I1 (offset by 10).
    """
    master = mavutil.mavlink_connection(f"tcp:127.0.0.1:{port}")
    master.wait_heartbeat(timeout=30)
    print(f"Connected: sysid={master.target_system} compid={master.target_component} port={port}")
    return master

def set_mode(master, mode: str):
    # For ArduCopter, GUIDED and LAND are common.
    master.set_mode_apm(mode)
    time.sleep(0.5)

def arm(master):
    master.arducopter_arm()
    master.motors_armed_wait(timeout=30)
    print(f"Armed sysid={master.target_system}")

def takeoff(master, altitude_m: float):
    # MAV_CMD_NAV_TAKEOFF: param7 is altitude
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0, 0, 0, 0,   # params 1-4 unused
        0, 0, altitude_m  # lat, lon unused in GUIDED takeoff; altitude in meters
    )

def goto_local_ned(master, north_m: float, east_m: float, down_m: float):
    """
    Position target in LOCAL_NED frame:
      +north, +east, +down
    Up 10m => down = -10
    """
    type_mask = 0b0000111111000111  # ignore velocities/accels/yaw; use position
    master.mav.set_position_target_local_ned_send(
        0,  # time_boot_ms (0 is fine)
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        type_mask,
        north_m, east_m, down_m,
        0, 0, 0,  # vx, vy, vz (ignored)
        0, 0, 0,  # ax, ay, az (ignored)
        0, 0      # yaw, yaw_rate (ignored)
    )

def land(master):
    set_mode(master, "LAND")
    print(f"Landing sysid={master.target_system}")

def main():
    print("Running two drones script")

    # Adjust ports if your SITL uses different ones
    drone1 = connect(5760)  # -I0
    drone2 = connect(5770)  # -I1

    # Put both into GUIDED, arm, takeoff to 10m
    for d in (drone1, drone2):
        set_mode(d, "GUIDED")
        arm(d)
        takeoff(d, 10.0)

    # Give them time to climb
    time.sleep(8)

    # Move north 10m while holding altitude (~10m => down=-10 in NED)
    goto_local_ned(drone1, 10.0, 0.0, -10.0)
    goto_local_ned(drone2, 10.0, 0.0, -10.0)

    time.sleep(8)

    # Land both
    land(drone1)
    land(drone2)

if __name__ == "__main__":
    main()