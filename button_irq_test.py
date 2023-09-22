# MIT License (MIT)
# Copyright (c) 2023 Wind-stormger
# https://opensource.org/licenses/MIT

# A button counting library based on MicroPython IRQ.
# This test script will output the IRQ trigger position,
# so you can see the details of the button bounce.
# https://github.com/Wind-stormger/micropython-button-irq

import time
from machine import Pin
import micropython
micropython.alloc_emergency_exception_buf(100)


class Button(object):

    def __init__(self, pin=None, debounce_time=50, long_time=1500):
        if isinstance(pin, int):
            self.pin = Pin(pin, Pin.IN)
        else:
            self.pin = pin
        self.debounce_time = debounce_time
        self.long_time = long_time
        self.trig_locks = 0
        self.__trig_timeticks_0 = 0
        self.__trig_timeticks_1 = 0
        self.count_0 = 0  # pressed times
        self.count_1 = 0  # long pressed times
        self.count_2 = 0  # press down times
        self.count_3 = 0  # triggered times
        self.enable_irq(self.pin_irq)

    def enable_irq(self, callback=None):
        self.pin.irq(handler=callback,
                     trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)

    def disable_irq(self, callback=None):
        self.pin.irq(handler=None)

    def reset(self):
        self.disable_irq()
        self.count_0 = 0
        self.count_1 = 0
        self.count_2 = 0
        self.count_3 = 0
        self.enable_irq(self.pin_irq)

    def pin_irq(self, pin):
        self.count_3 = self.count_3 + 1
        print(1)
        if self.pin.value() == 0 and self.trig_locks == 0:
            print(2)
            self.trig_locks = 1
            self.count_2 = self.count_2 + 1
            self.__trig_timeticks_0 = time.ticks_ms()
        elif self.pin.value() == 1 and self.trig_locks == 1:
            print(3)
            self.__trig_timeticks_1 = time.ticks_diff(
                time.ticks_ms(), self.__trig_timeticks_0)
            if self.__trig_timeticks_1 >= self.debounce_time:
                print(4)
                self.trig_locks = 0
                self.count_0 = self.count_0 + 1
            if self.__trig_timeticks_1 >= self.long_time:
                self.count_1 = self.count_1 + 1
        elif self.pin.value() == 0:
            print(5)
        elif self.pin.value() == 1:
            print(6)

    def count(self):
        count = [self.count_0, self.count_1, self.count_2, self.count_3]
        return count


# def main():
#     import gc
#     from machine import Pin
#     button = Button(Pin(35, Pin.IN, Pin.PULL_UP))
#     pressed = []
#     pressed_last = [0]
#     while True:
#         pressed = button.count()
#         if pressed_last[0] != pressed[0]:
#             print("RAM used = {RAM_used}KB".format(
#                 RAM_used=gc.mem_alloc()/1024))
#             print(pressed)
#             pressed_last = pressed
#         time.sleep_ms(10)


# main()
