__author__ = 'Djamel'

import wiringpi as wp
import datetime
import sys


def printResult(sender, group, on, recipient):
    print "sender :", sender
    if on:
        print "on"
    else:
        print "off"
    print "recipient ", recipient


def pulse_in(gpio, state, timeout):
    tn = datetime.datetime.now()
    t0 = datetime.datetime.now()
    micros = 0

    while wp.digitalRead(gpio) != state:
        tn = datetime.datetime.now()
        if tn.second > t0.second:
            micros = 1000000L
        else:
            micros = 0
        micros += tn.microsecond - t0.microsecond
        if micros > timeout:
            return 0

    t1 = datetime.datetime.now()

    while wp.digitalRead(gpio) == state:
        tn = datetime.datetime.now()
        if tn.second > t0.second:
            micros = 1000000L
        else:
            micros = 0
        micros = micros + (tn.microsecond - t0.microsecond)
        if micros > timeout:
            return 0

    if tn.second > t1.second:
        micros = 1000000L
    else:
        micros = 0
    micros = micros + (tn.microsecond - t1.microsecond)

    return micros

#def start_receiver(gpio):
gpio = int(sys.argv[1])
wp.wiringPiSetup()
wp.pinMode(gpio, 0)

i = 0
t = 0

prev_bit = 0
bit = 0

sender = 0
group = False
on = False
recipient = 0

while True:
    while t < 9480 or t > 10350:
        t = pulse_in(gpio, wp.LOW, 1000000)
    print "first step"

    while t < 2550 and t > 2750:
        t = pulse_in(gpio, wp.LOW, 1000000)

    print "second step"

    while i < 64:
        print "data !"
        t = pulse_in(gpio, wp.LOW, 1000000)
        if t > 200 and t < 365:
            bit = 0

        elif t > 1000 and t < 1360:
            bit = 1
        else:
            i = 0
            break

        if i % 2 == 1:
            if (prev_bit ^ bit) ==  0:
                i = 0
                break
            if i < 53:
                sender <<= 1
                sender |= prev_bit
            elif i == 53:
                group = prev_bit
            elif i == 55:
                on = prev_bit
            else:
                recipient <<= 1
                recipient |= prev_bit
        prev_bit = bit
        i += 1
    if i > 0:
        printResult(sender, group, on, recipient)
        break