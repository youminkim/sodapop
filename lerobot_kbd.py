from lerobot.robots.so101_follower import SO101Follower, SO101FollowerConfig
import sys
import tty
import termios
import time
import signal

# change this to the port of your robot. Find it by running `python -m lerobot.find_port`
PORT = "/dev/tty.usbmodem5A7A0157681"
ID = "sodapop"

def get_key() -> str:
    """Read one character from stdin (no Enter needed)."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        
        # Handle arrow keys (3-character sequences)
        if ch == '\x1b':
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                if ch3 == 'A':
                    return 'UP'
                elif ch3 == 'B':
                    return 'DOWN'
                elif ch3 == 'C':
                    return 'RIGHT'
                elif ch3 == 'D':
                    return 'LEFT'
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def signal_handler(sig, frame):
    """Handle CTRL-C gracefully"""
    print("\nExiting...")
    sys.exit(0)

# Set up signal handler for graceful exit
signal.signal(signal.SIGINT, signal_handler)

# connect to the robot
robot_cfg = SO101FollowerConfig(port=PORT,id=ID)
robot = SO101Follower(robot_cfg)
robot.connect()

# positions 
neutral = {k: 0.0 for k in robot.action_features}
folding = {'shoulder_pan.pos': 0, 'shoulder_lift.pos': -90.0, 'elbow_flex.pos': 90.0, 'wrist_flex.pos': -90.0, 'wrist_roll.pos': 0.0, 'gripper.pos': 0}

# Make it neutral position 
sent = robot.send_action(neutral)

print("Robot control started:")
print("  A/D - Shoulder pan left/right")
print("  W/S - Shoulder lift up/down")
print("  Arrow Up/Down - Elbow flex")
print("  Q/E - Wrist flex")
print("  Arrow Left/Right - Wrist roll")
print("  SPACE - Gripper toggle")
print("Press 'k' or CTRL+C to quit.")

# Once keys are pressed, send the action
position = neutral.copy()
increment = 3

try:
    while True:
        key = get_key()
        
        # Quit conditions
        if key == 'k' or key == '\x03':  # 'k' or CTRL-C
            print("\nQuitting...")
            break
            
        if key == 'a':
            position['shoulder_pan.pos'] -= increment
        elif key == 'd':
            position['shoulder_pan.pos'] += increment
        elif key == 'w':    
            position['shoulder_lift.pos'] -= increment
        elif key == 's':
            position['shoulder_lift.pos'] += increment
        elif key == 'UP': # arrow up
            position['elbow_flex.pos'] -= increment
        elif key == 'DOWN': # arrow down
            position['elbow_flex.pos'] += increment
        elif key == 'q': # q 
            position['wrist_flex.pos'] -= increment
        elif key == 'e': # e
            position['wrist_flex.pos'] += increment
        elif key == 'LEFT': # arrow left
            position['wrist_roll.pos'] -= increment
        elif key == 'RIGHT': # arrow right
            position['wrist_roll.pos'] += increment
        elif key == ' ':
            position['gripper.pos'] = 90 if position['gripper.pos'] == 0 else 0
        elif key == 'n':
            position = neutral.copy()

        print(position)
        
        sent = robot.send_action(position)
        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("\nInterrupt received, exiting...")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Cleanup
    try:
        # go to folding position 
        print("Moving to folding position...")
        robot.send_action(folding)

        # give some time to the robot to move
        time.sleep(1)

        robot.disconnect()
        print("Disconnected from robot.")
    except:
        pass







