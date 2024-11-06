
# Helper function to detect Raspberry Pi
def is_raspberry_pi():
    try:
        with open("/proc/cpuinfo", "r") as file:
            cpuinfo = file.read()
            is_rasp = (
                ("Raspberry Pi" in cpuinfo)
                or ("BCM" in cpuinfo)
            )
            return is_rasp
    except FileNotFoundError:
        return False

IS_RPI = is_raspberry_pi()
ROUND_SCREEN_TIMEOUT_SECONDS = 3
GPIO_START_PIN = 18
GPIO_RESTART_PIN = 21
