# micropython-button-irq
A button counting library based on MicroPython IRQ.

Having good debounce.

It can be installed from [mip](https://docs.micropython.org/en/latest/reference/packages.html#installing-packages-with-mip) via:

```
>>> import mip
>>> mip.install("github:Wind-stormger/micropython-button-irq")
```

Or from mpremote via

```bash
mpremote mip install github:Wind-stormger/micropython-button-irq
```

# Use Cases

```py
from machine import Pin
from button_irq import Button
import time
button = Button(Pin(0, Pin.IN, Pin.PULL_UP), debounce_time=50, long_time=1500)
pressed = [0]
pressed_last = [0]
while True:
    pressed = button.count()
    if pressed_last[0] != pressed[0] or pressed_last[2] != pressed[2]:
        print(pressed[0], # pressed times
              pressed[1], # long pressed times
              pressed[2], # press down times
              pressed[3]) # triggered times
        pressed_last = pressed
    if pressed[1] == 3:
        button.reset() # reset all count after long pressed 3 times
    time.sleep_ms(10)

```
