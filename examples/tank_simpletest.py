"""
A simple test of the Tank drivetrain class.

This iterates through a list of drivetrain commands
and tallies up the ellapsed time taken to acheive each set of commands
as well as the ellapsed time taken for each motor to acheive each individual command
"""
# pylint: disable=invalid-name
import time
import board
from drivetrain.drivetrain import Tank, BiMotor

mymotors = [BiMotor([board.D22, board.D13], ramp_time=2000),
            BiMotor([board.D17, board.D18], ramp_time=2000)]
d = Tank(mymotors, max_speed=100)
testInput = [[100, 0],
             [-100, 0],
             [0, 0],
             [0, 100],
             [0, -100],
             [0, 0]]
for test in testInput:
    # use the list `end` to keep track of each motor's ellapsed time
    end = []
    for m in mymotors:
        # end timer for motor[i] = end[i]
        end.append(None)
    d.go(test * 655.35)  # send input commands
    # unanimous start of all timmers
    start = time.monotonic()
    t = start
    # do a no delay wait for at least 3 seconds
    while d.is_cellerating or t < start + 3:
        t = time.monotonic()
        for j, m in enumerate(mymotors):
            if not m.is_cellerating and end[j] is None:
                end[j] = time.monotonic()
        # avoid infinite looping via a hard timeout of 6 seconds
        if t > start + 6: # something went wrong; abort!
            break

    # notice the motor values are different from the drivetrain's commands' value
    # ratio of drivetrain commands to motor value == [-100, 100] : [-65535, 65535]
    print(f'test commands {repr(test)} took {time.monotonic() - start} seconds\n')
    for j, m in enumerate(mymotors):
        if end[j] is not None:
            print(f'motor {j} acheived {m.value} in {end[j]-start} seconds')
        else:
            print(f"motor {j} didn't finish cellerating and a has value of {m.value}")
