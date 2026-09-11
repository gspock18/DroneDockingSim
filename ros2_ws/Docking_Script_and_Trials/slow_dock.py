# #!/usr/bin/env python3

# from pymavlink import mavutil
# import time
# import math

# DRONE_MALE = "tcp:127.0.0.1:5762"    # ardupilot_0 / male
# DRONE_FEMALE = "tcp:127.0.0.1:5772"  # ardupilot_2 / female

# ALTITUDE = 2.0
# APPROACH_SPEED = 0.15  # m/s, slow approach
# APPROACH_TIME = 18     # seconds


# def connect(name, address):
#     print(f"Connecting to {name} at {address}...")
#     master = mavutil.mavlink_connection(address)
#     master.wait_heartbeat()
#     print(f"{name} connected: system {master.target_system}")
#     return master


# def set_mode(master, mode):
#     mode_id = master.mode_mapping()[mode]
#     master.mav.set_mode_send(
#         master.target_system,
#         mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
#         mode_id
#     )
#     time.sleep(1)


# def arm_and_takeoff(master, name, altitude):
#     print(f"{name}: setting GUIDED mode")
#     set_mode(master, "GUIDED")

#     print(f"{name}: arming")
#     master.arducopter_arm()
#     master.motors_armed_wait()

#     print(f"{name}: taking off to {altitude} m")
#     master.mav.command_long_send(
#         master.target_system,
#         master.target_component,
#         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
#         0,
#         0, 0, 0, 0,
#         0, 0,
#         altitude
#     )

#     time.sleep(8)


# def send_body_velocity(master, vx, vy, vz):
#     """
#     Body frame:
#     +X = forward
#     +Y = right
#     +Z = down
#     """
#     master.mav.set_position_target_local_ned_send(
#         0,
#         master.target_system,
#         master.target_component,
#         mavutil.mavlink.MAV_FRAME_BODY_NED,
#         0b0000111111000111,
#         0, 0, 0,
#         vx, vy, vz,
#         0, 0, 0,
#         0, 0
#     )


# def stop(master):
#     send_body_velocity(master, 0, 0, 0)


# def main():
#     male = connect("male drone / ardupilot_0", DRONE_MALE)
#     female = connect("female drone / ardupilot_2", DRONE_FEMALE)

#     arm_and_takeoff(male, "male drone", ALTITUDE)
#     arm_and_takeoff(female, "female drone", ALTITUDE)

#     print("Both drones should now be near 2 m altitude.")
#     print("Beginning slow approach...")

#     start = time.time()

#     while time.time() - start < APPROACH_TIME:
#         # Male moves forward
#         send_body_velocity(male, APPROACH_SPEED, 0, 0)

#         # Female moves forward too.
#         # If female is facing the male, this brings them together.
#         send_body_velocity(female, APPROACH_SPEED, 0, 0)

#         time.sleep(0.2)

#     print("Stopping both drones.")
#     stop(male)
#     stop(female)

#     print("Done.")


# if __name__ == "__main__":
#     main()


######################################################################


# #!/usr/bin/env python3

# from pymavlink import mavutil
# import subprocess
# import time

# MALE_ENDPOINT   = "tcp:127.0.0.1:5762"   # ardupilot_0 / male
# FEMALE_ENDPOINT = "tcp:127.0.0.1:5772"   # ardupilot_2 / female

# WORLD_CONTROL_SERVICE = "/world/two_iris/control"

# ALTITUDE = 2.0
# TRAVEL_DISTANCE = 1.25        # meters forward before stopping
# HEARTBEAT_TIMEOUT = 4.0


# def connect(name, endpoint):
#     print(f"Connecting to {name}...")
#     m = mavutil.mavlink_connection(endpoint)
#     m.wait_heartbeat(timeout=10)
#     m.last_seen = time.time()
#     print(f"{name} connected.")
#     return m


# def set_mode(master, mode):
#     mode_id = master.mode_mapping()[mode]
#     master.mav.set_mode_send(
#         master.target_system,
#         mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
#         mode_id
#     )
#     time.sleep(1)


# def arm_and_takeoff(master, name, alt):
#     set_mode(master, "GUIDED")
#     master.arducopter_arm()
#     master.motors_armed_wait()

#     print(f"{name}: taking off to {alt} m")
#     master.mav.command_long_send(
#         master.target_system,
#         master.target_component,
#         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
#         0, 0, 0, 0, 0, 0, 0, alt
#     )
#     time.sleep(8)


# def send_body_velocity(master, vx, vy, vz):
#     # BODY_NED: +X forward, +Y right, +Z down
#     master.mav.set_position_target_local_ned_send(
#         0,
#         master.target_system,
#         master.target_component,
#         mavutil.mavlink.MAV_FRAME_BODY_NED,
#         0b0000111111000111,
#         0, 0, 0,
#         vx, vy, vz,
#         0, 0, 0,
#         0, 0
#     )


# def hover(master):
#     send_body_velocity(master, 0, 0, 0)


# def alive(master):
#     try:
#         msg = master.recv_match(type="HEARTBEAT", blocking=False)
#         if msg:
#             master.last_seen = time.time()
#         return (time.time() - master.last_seen) < HEARTBEAT_TIMEOUT
#     except:
#         return False


# def reset_world():
#     subprocess.run([
#         "gz", "service",
#         "-s", WORLD_CONTROL_SERVICE,
#         "--reqtype", "gz.msgs.WorldControl",
#         "--reptype", "gz.msgs.Boolean",
#         "--timeout", "3000",
#         "--req", "reset: {all: true}"
#     ])


# def ask_speed(prompt):
#     while True:
#         try:
#             v = float(input(prompt))
#             if v <= 0:
#                 print("Enter a positive speed.")
#                 continue
#             return v
#         except:
#             print("Enter a number like 0.10")


# def move_exact_distance(master, speed, distance):
#     travel_time = distance / speed
#     start = time.time()

#     while time.time() - start < travel_time:
#         if not alive(master):
#             return False
#         send_body_velocity(master, speed, 0, 0)
#         time.sleep(0.1)

#     hover(master)
#     return True


# def main():
#     male_speed = ask_speed("Male drone speed m/s: ")
#     female_speed = ask_speed("Female drone speed m/s: ")

#     male = connect("Male Drone", MALE_ENDPOINT)
#     female = connect("Female Drone", FEMALE_ENDPOINT)

#     arm_and_takeoff(male, "Male Drone", ALTITUDE)
#     arm_and_takeoff(female, "Female Drone", ALTITUDE)

#     print("Moving each drone forward %s m..." % (TRAVEL_DISTANCE))

#     ok1 = move_exact_distance(male, male_speed, TRAVEL_DISTANCE)
#     ok2 = move_exact_distance(female, female_speed, TRAVEL_DISTANCE)

#     if not ok1 or not ok2:
#         print("Heartbeat lost. Resetting world.")
#         reset_world()
#         return

#     print("Both drones reached target. Hovering now.")

#     while True:
#         if not alive(male) and not alive(female):
#             print("Both drones off. Resetting world.")
#             reset_world()
#             return

#         hover(male)
#         hover(female)
#         time.sleep(0.5)


# if __name__ == "__main__":
#     main()

###################################################################

# #!/usr/bin/env python3


# from pymavlink import mavutil
# import subprocess
# import time
# import csv
# import os
# from datetime import datetime
# import matplotlib.pyplot as plt
# from collections import deque

# MALE_ENDPOINT = "tcp:127.0.0.1:5762"     # ardupilot_0 / male
# FEMALE_ENDPOINT = "tcp:127.0.0.1:5772"   # ardupilot_2 / female

# WORLD_CONTROL_SERVICE = "/world/two_iris/control"

# ALTITUDE = 2.0
# FORWARD_DISTANCE = 1.3
# CLOSING_DISTANCE = 0.1
# HEARTBEAT_TIMEOUT = 4.0

# LOG_FILE = "hover_results.csv"
# HOVER_HOLD_TIME = 10

# LIVE_PLOT_WINDOW = 20
# TARGET_ALTITUDE = 2.0
# ALT_TOLERANCE = 0.25


# def connect(name, endpoint):
#     print(f"Connecting to {name}...")
#     m = mavutil.mavlink_connection(endpoint)
#     m.wait_heartbeat(timeout=10)
#     m.last_seen = time.time()
#     print(f"{name} connected.")
#     return m


# def set_mode(master, mode):
#     mode_id = master.mode_mapping()[mode]
#     master.mav.set_mode_send(
#         master.target_system,
#         mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
#         mode_id
#     )
#     time.sleep(1)


# def arm_and_takeoff(master, name, alt):
#     set_mode(master, "GUIDED")
#     master.arducopter_arm()
#     master.motors_armed_wait()

#     print(f"{name}: taking off to {alt} m")
#     master.mav.command_long_send(
#         master.target_system,
#         master.target_component,
#         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
#         0, 0, 0, 0, 0, 0, 0, alt
#     )
#     time.sleep(8)


# def send_body_velocity(master, vx, vy, vz):
#     # BODY_NED: +X forward, +Y right, +Z down
#     master.mav.set_position_target_local_ned_send(
#         0,
#         master.target_system,
#         master.target_component,
#         mavutil.mavlink.MAV_FRAME_BODY_NED,
#         0b0000111111000111,
#         0, 0, 0,
#         vx, vy, vz,
#         0, 0, 0,
#         0, 0
#     )


# def hover(master):
#     send_body_velocity(master, 0, 0, 0)


# def alive(master):
#     try:
#         msg = master.recv_match(type="HEARTBEAT", blocking=False)
#         if msg:
#             master.last_seen = time.time()
#         return (time.time() - master.last_seen) < HEARTBEAT_TIMEOUT
#     except Exception:
#         return False


# def reset_world():
#     subprocess.run([
#         "gz", "service",
#         "-s", WORLD_CONTROL_SERVICE,
#         "--reqtype", "gz.msgs.WorldControl",
#         "--reptype", "gz.msgs.Boolean",
#         "--timeout", "5000",
#         "--req", "reset: {all: true}"
#     ])


# def ask_speed(prompt):
#     while True:
#         try:
#             v = float(input(prompt))
#             if v <= 0:
#                 print("Enter a positive speed.")
#                 continue
#             return v
#         except Exception:
#             print("Enter a number like 0.10")


# def log_result(male_speed, female_speed, success, reason, hover_time):
#     file_exists = os.path.isfile(LOG_FILE)

#     with open(LOG_FILE, "a", newline="") as f:
#         writer = csv.writer(f)

#         if not file_exists:
#             writer.writerow([
#                 "timestamp",
#                 "male_speed",
#                 "female_speed",
#                 "success",
#                 "reason",
#                 "hover_time_sec"
#             ])

#         writer.writerow([
#             datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             male_speed,
#             female_speed,
#             success,
#             reason,
#             round(hover_time, 2)
#         ])


# def get_altitude(master):
#     msg = master.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
#     if msg:
#         return msg.relative_alt / 1000.0
#     return None


# def setup_live_plot():
#     plt.ion()

#     fig, ax = plt.subplots(figsize=(9, 5))

#     ax.set_title("Live Two-Drone Hover Stability")
#     ax.set_xlabel("Time (s)")
#     ax.set_ylabel("Altitude (m)")
#     ax.set_ylim(0, 3)

#     male_line, = ax.plot([], [], label="Male Drone")
#     female_line, = ax.plot([], [], label="Female Drone")

#     ax.axhline(TARGET_ALTITUDE, linestyle="--", label="Target Altitude")
#     ax.axhline(TARGET_ALTITUDE + ALT_TOLERANCE, linestyle=":")
#     ax.axhline(TARGET_ALTITUDE - ALT_TOLERANCE, linestyle=":")

#     ax.legend()
#     plt.show(block=False)

#     return fig, ax, male_line, female_line


# def update_live_plot(fig, ax, male_line, female_line, times, male_alts, female_alts):
#     male_line.set_data(times, male_alts)
#     female_line.set_data(times, female_alts)

#     if len(times) > 0:
#         ax.set_xlim(max(0, times[-1] - LIVE_PLOT_WINDOW), times[-1] + 1)

#     fig.canvas.draw()
#     fig.canvas.flush_events()


# def move_both_distance(male, female, male_speed, female_speed, distance, male_dir=1, female_dir=1):
#     male_time = distance / male_speed
#     female_time = distance / female_speed
#     total_time = max(male_time, female_time)

#     start = time.time()

#     while time.time() - start < total_time:
#         elapsed = time.time() - start

#         if not alive(male) or not alive(female):
#             hover(male)
#             hover(female)
#             return False

#         if elapsed < male_time:
#             send_body_velocity(male, male_dir * male_speed, 0, 0)
#         else:
#             hover(male)

#         if elapsed < female_time:
#             send_body_velocity(female, female_dir * female_speed, 0, 0)
#         else:
#             hover(female)

#         time.sleep(0.1)

#     hover(male)
#     hover(female)
#     return True


# def monitor_hover_with_live_plot(male, female, male_speed, female_speed):
#     print("Final hover position reached. Monitoring hover stability with live plot...")

#     fig, ax, male_line, female_line = setup_live_plot()

#     times = deque(maxlen=300)
#     male_alts = deque(maxlen=300)
#     female_alts = deque(maxlen=300)

#     hover_start = time.time()

#     while True:
#         elapsed = time.time() - hover_start

#         if not alive(male) or not alive(female):
#             hover_time = time.time() - hover_start
#             print("Drone lost heartbeat.")
#             log_result(male_speed, female_speed, False, "heartbeat_lost", hover_time)
#             plt.close(fig)
#             reset_world()
#             return False

#         hover(male)
#         hover(female)

#         male_alt = get_altitude(male)
#         female_alt = get_altitude(female)

#         if male_alt is not None and female_alt is not None:
#             times.append(elapsed)
#             male_alts.append(male_alt)
#             female_alts.append(female_alt)

#             update_live_plot(
#                 fig,
#                 ax,
#                 male_line,
#                 female_line,
#                 list(times),
#                 list(male_alts),
#                 list(female_alts)
#             )

#             male_ok = abs(male_alt - TARGET_ALTITUDE) <= ALT_TOLERANCE
#             female_ok = abs(female_alt - TARGET_ALTITUDE) <= ALT_TOLERANCE

#             if not male_ok or not female_ok:
#                 print(
#                     f"Altitude warning | Male: {male_alt:.2f} m | Female: {female_alt:.2f} m"
#                 )

#         if elapsed >= HOVER_HOLD_TIME:
#             print("SUCCESS: Hover stable for 10 seconds.")
#             log_result(male_speed, female_speed, True, "stable_hover", elapsed)
#             plt.close(fig)
#             return True

#         time.sleep(0.2)


# def run_one_cycle(male_speed, female_speed):
#     male = connect("Male Drone", MALE_ENDPOINT)
#     female = connect("Female Drone", FEMALE_ENDPOINT)

#     arm_and_takeoff(male, "Male Drone", ALTITUDE)
#     arm_and_takeoff(female, "Female Drone", ALTITUDE)

#     print(f"Phase 1: Move both drones forward {FORWARD_DISTANCE} m")
#     ok = move_both_distance(
#         male,
#         female,
#         male_speed,
#         female_speed,
#         FORWARD_DISTANCE,
#         male_dir=1,
#         female_dir=1
#     )

#     if not ok:
#         print("Heartbeat lost during Phase 1. Resetting world.")
#         log_result(male_speed, female_speed, False, "heartbeat_lost_phase_1", 0)
#         reset_world()
#         return False

#     time.sleep(1)

#     print(f"Phase 2: Move {CLOSING_DISTANCE} m toward each other")
#     ok = move_both_distance(
#         male,
#         female,
#         male_speed,
#         female_speed,
#         CLOSING_DISTANCE,
#         male_dir=1,
#         female_dir=-1
#     )

#     if not ok:
#         print("Heartbeat lost during Phase 2. Resetting world.")
#         log_result(male_speed, female_speed, False, "heartbeat_lost_phase_2", 0)
#         reset_world()
#         return False

#     return monitor_hover_with_live_plot(male, female, male_speed, female_speed)


# def main():
#     male_speed = ask_speed("Male drone speed m/s: ")
#     female_speed = ask_speed("Female drone speed m/s: ")

#     cycle = 1

#     while True:
#         print(f"\n========== RUN {cycle} ==========")

#         success = run_one_cycle(male_speed, female_speed)

#         if success:
#             print(f"Run {cycle}: SUCCESS")
#         else:
#             print(f"Run {cycle}: FAILED")

#         print("Resetting world to original drone positions...")
#         reset_world()

#         print("Waiting for world reset to settle...")
#         time.sleep(8)

#         cycle += 1


# if __name__ == "__main__":
#     main()

###################################################################

#!/usr/bin/env python3

from pymavlink import mavutil
import subprocess
import time
import math
import csv
import matplotlib.pyplot as plt

MALE_ENDPOINT   = "tcp:127.0.0.1:5762"   # ardupilot_0 / male
FEMALE_ENDPOINT = "tcp:127.0.0.1:5772"   # ardupilot_2 / female

DETACH_TOPIC = "/drone_dock/detach"
ATTACH_TOPIC = "/drone_dock/attach"

ALTITUDE = 2.0
TRAVEL_DISTANCE = 1.25
FINAL_DISTANCE = 1.0

HEARTBEAT_TIMEOUT = 4.0
POST_ATTACH_RECORD_TIME = 180.0
LOG_RATE = 10.0

CSV_FILE = "docking_trial_log.csv"
PLOT_FILE = "docking_trial_plot.png"


############################# ADDED CODES ###############################

def send_world_velocity(master, vx, vy, vz):
    # LOCAL_NED: same world direction for both drones
    master.mav.set_position_target_local_ned_send(
        0,
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0, 0, 0,
        vx, vy, vz,
        0, 0, 0,
        0, 0
    )

######################### ADDED CODES FINISH ############################

def connect(name, endpoint):
    print(f"Connecting to {name}...")
    m = mavutil.mavlink_connection(endpoint)
    m.wait_heartbeat(timeout=10)
    m.last_seen = time.time()
    print(f"{name} connected.")
    return m


def request_position_stream(master):
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
        0,
        mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED,
        100000,  # 10 Hz
        0, 0, 0, 0, 0
    )
    time.sleep(0.5)


def set_mode(master, mode):
    mode_id = master.mode_mapping()[mode]
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id
    )
    time.sleep(1)


def arm_and_takeoff(master, name, alt):
    set_mode(master, "GUIDED")
    master.arducopter_arm()
    master.motors_armed_wait()

    print(f"{name}: taking off to {alt} m")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0, 0, 0, 0, 0, 0, 0, alt
    )
    time.sleep(8)


def send_body_velocity(master, vx, vy, vz):
    master.mav.set_position_target_local_ned_send(
        0,
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_BODY_NED,
        0b0000111111000111,
        0, 0, 0,
        vx, vy, vz,
        0, 0, 0,
        0, 0
    )


def hover(master):
    send_body_velocity(master, 0, 0, 0)


def alive(master):
    try:
        msg = master.recv_match(type="HEARTBEAT", blocking=False)
        if msg:
            master.last_seen = time.time()
        return (time.time() - master.last_seen) < HEARTBEAT_TIMEOUT
    except:
        return False


def get_position(master):
    while master.recv_match(type="LOCAL_POSITION_NED", blocking=False):
        pass

    msg = master.recv_match(type="LOCAL_POSITION_NED", blocking=True, timeout=2)

    if msg is None:
        return None

    return (msg.x, msg.y, msg.z)


def distance_3d(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2 +
        (p1[2] - p2[2]) ** 2
    )


def midpoint(p1, p2):
    return (
        (p1[0] + p2[0]) / 2,
        (p1[1] + p2[1]) / 2,
        (p1[2] + p2[2]) / 2
    )


def gz_empty_topic(topic):
    print(f"Publishing to {topic}")

    result = subprocess.run(
        ["gz", "topic", "-t", topic, "-m", "gz.msgs.Empty", "-p", ""],
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)


def ask_speed(prompt):
    while True:
        try:
            v = float(input(prompt))
            if v <= 0:
                print("Enter a positive speed.")
                continue
            return v
        except:
            print("Enter a number like 0.10")


def move_both_for_distance(male, female, male_speed, female_speed, distance):
    male_time = distance / male_speed
    female_time = distance / female_speed
    total_time = max(male_time, female_time)

    start = time.time()

    while time.time() - start < total_time:
        elapsed = time.time() - start

        if not alive(male) or not alive(female):
            return False

        if elapsed < male_time:
            send_body_velocity(male, male_speed, 0, 0)
        else:
            hover(male)

        if elapsed < female_time:
            send_body_velocity(female, female_speed, 0, 0)
        else:
            hover(female)

        time.sleep(0.1)

    hover(male)
    hover(female)
    return True


def move_until_close(male, female, male_speed, female_speed, target_distance):
    print(f"Moving toward each other until distance is about {target_distance} m...")

    MAX_CLOSE_TIME = 8.0
    last_print = 0
    start = time.time()

    while time.time() - start < MAX_CLOSE_TIME:
        if not alive(male) or not alive(female):
            return False

        male_pos = get_position(male)
        female_pos = get_position(female)

        if male_pos is not None and female_pos is not None:
            d = distance_3d(male_pos, female_pos)

            now = time.time()
            if now - last_print >= 1.0:
                print(f"Center-to-center distance: {d:.3f} m")
                last_print = now

            if d <= target_distance:
                print(f"Target center distance reached: {d:.3f} m")
                hover(male)
                hover(female)
                return True

        send_body_velocity(male, male_speed, 0, 0)
        send_body_velocity(female, -female_speed, 0, 0)
        time.sleep(0.1)

    print("Close approach time reached. Attempting attach now.")
    hover(male)
    hover(female)
    return True


def record_after_attach(male, female, attach_male_pos, attach_female_pos, attach_point):
    print(f"Recording post-attach movement for {POST_ATTACH_RECORD_TIME} seconds...")

    rows = []
    start = time.time()
    last_time = start
    last_attach_point = attach_point

    while time.time() - start < POST_ATTACH_RECORD_TIME:
        now = time.time()
        t = now - start

        male_pos = get_position(male)
        female_pos = get_position(female)

        if male_pos is None or female_pos is None:
            print("Could not read position during recording.")
            continue

        current_attach_point = midpoint(male_pos, female_pos)
        drift_from_original = distance_3d(current_attach_point, attach_point)

        dt = now - last_time
        speed_from_last = 0.0

        if dt > 0:
            speed_from_last = distance_3d(current_attach_point, last_attach_point) / dt

        rows.append({
            "time_s": t,

            "male_x": male_pos[0],
            "male_y": male_pos[1],
            "male_z": male_pos[2],

            "female_x": female_pos[0],
            "female_y": female_pos[1],
            "female_z": female_pos[2],

            "attach_point_x": current_attach_point[0],
            "attach_point_y": current_attach_point[1],
            "attach_point_z": current_attach_point[2],

            "drift_from_original_m": drift_from_original,
            "attach_point_speed_mps": speed_from_last
        })

        last_time = now
        last_attach_point = current_attach_point

        send_world_velocity(male, 0, 0, 0)
        send_world_velocity(female, 0, 0, 0)

        time.sleep(1.0 / LOG_RATE)

    return rows


def save_csv(rows):
    if not rows:
        print("No rows recorded.")
        return

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved CSV: {CSV_FILE}")


def make_plot(rows, attach_male_pos, attach_female_pos, attach_point):
    if not rows:
        print("No rows to plot.")
        return

    male_x = [r["male_x"] for r in rows]
    male_y = [r["male_y"] for r in rows]

    female_x = [r["female_x"] for r in rows]
    female_y = [r["female_y"] for r in rows]

    attach_x = [r["attach_point_x"] for r in rows]
    attach_y = [r["attach_point_y"] for r in rows]

    plt.figure(figsize=(8, 6))

    plt.plot(male_x, male_y, label="Male drone movement")
    plt.plot(female_x, female_y, label="Female drone movement")
    plt.plot(attach_x, attach_y, label="Attachment midpoint movement")

    plt.scatter([attach_male_pos[0]], [attach_male_pos[1]], marker="o", label="Male attach position")
    plt.scatter([attach_female_pos[0]], [attach_female_pos[1]], marker="o", label="Female attach position")
    plt.scatter([attach_point[0]], [attach_point[1]], marker="x", label="Original attach midpoint")

    plt.xlabel("Local X position, m")
    plt.ylabel("Local Y position, m")
    plt.title("Drone Movement After Attachment")
    plt.legend()
    plt.grid(True)
    plt.axis("equal")

    plt.savefig(PLOT_FILE, dpi=200)
    print(f"Saved plot: {PLOT_FILE}")


def main():
    male_speed = ask_speed("Male drone speed m/s: ")
    female_speed = ask_speed("Female drone speed m/s: ")

    male = connect("Male Drone", MALE_ENDPOINT)
    female = connect("Female Drone", FEMALE_ENDPOINT)

    request_position_stream(male)
    request_position_stream(female)

    print("Detaching drones before takeoff...")
    gz_empty_topic(DETACH_TOPIC)
    time.sleep(1)

    arm_and_takeoff(male, "Male Drone", ALTITUDE)
    arm_and_takeoff(female, "Female Drone", ALTITUDE)

    print(f"Moving each drone forward {TRAVEL_DISTANCE} m...")
    ok = move_both_for_distance(
        male,
        female,
        male_speed,
        female_speed,
        TRAVEL_DISTANCE
    )

    if not ok:
        print("Heartbeat lost. Ending trial.")
        return

    print("Moving drones toward each other...")
    ok = move_until_close(
        male,
        female,
        male_speed,
        female_speed,
        FINAL_DISTANCE
    )

    if not ok:
        print("Heartbeat lost. Ending trial.")
        return

    hover(male)
    hover(female)

    print("Drones are close. Hovering before attach...")
    time.sleep(2)

    male_attach_pos = get_position(male)
    female_attach_pos = get_position(female)

    if male_attach_pos is None or female_attach_pos is None:
        print("Could not read attach positions.")
        return

    attach_point = midpoint(male_attach_pos, female_attach_pos)

    print("Attach position recorded.")
    print(f"Male attach position:   {male_attach_pos}")
    print(f"Female attach position: {female_attach_pos}")
    print(f"Attachment midpoint:    {attach_point}")

    print("Sending attach command...")
    gz_empty_topic(ATTACH_TOPIC)
    time.sleep(1)

    print("Stopping body-frame motion and syncing both drones in world-frame hover...")

    for _ in range(20):
        send_world_velocity(male, 0, 0, 0)
        send_world_velocity(female, 0, 0, 0)
        time.sleep(0.1)

    rows = record_after_attach(
        male,
        female,
        male_attach_pos,
        female_attach_pos,
        attach_point
    )

    save_csv(rows)
    make_plot(rows, male_attach_pos, female_attach_pos, attach_point)

    if rows:
        max_drift = max(r["drift_from_original_m"] for r in rows)
        avg_speed = sum(r["attach_point_speed_mps"] for r in rows) / len(rows)

        print("")
        print("Trial summary:")
        print(f"Max drift from original attach point: {max_drift:.4f} m")
        print(f"Average attach point movement speed: {avg_speed:.4f} m/s")
        print(f"Recorded duration: {POST_ATTACH_RECORD_TIME} s")

    print("Done. Drones are hovering.")

    while True:
        if not alive(male) and not alive(female):
            print("Both drones off. Ending script.")
            return

        hover(male)
        hover(female)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
