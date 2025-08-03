Robots for fun

# Lerobot

```
> conda activate lerobot 
> python lerobot_kbd.py
```
## Teleoperation 
```
> python -m lerobot.teleoperate \
    --robot.type=so101_follower \
    --robot.port=/dev/tty.usbmodem5A7A0157911 \
    --robot.id=sodapop \
    --teleop.type=so101_leader \
    --teleop.port=/dev/tty.usbmodem5A7A0157681 \
    --teleop.id=sodapop_leader
```

