from __future__ import print_function
from pokemongo_bot.event_manager import manager
import time
try:
    #pylint: disable=import-error
    import lcd
    LCD = lcd.lcd()
    # Change this to your i2c address
    LCD.set_addr(0x23)
except ImportError:
    LCD = None


def log(string, color='white'):
    color_hex = {
        'green': '92m',
        'yellow': '93m',
        'red': '91m'
    }
    output = '[' + time.strftime("%Y-%m-%d %H:%M:%S") + '] ' + string.decode('utf-8')
    manager.fire("logging_output", output=output, color=color)
    if color in color_hex:
        output = u"\033[" + color_hex[color] + output + "\033[0m"
    print(output)
    if LCD is not None and string is not None:
        LCD.message(string)
