#!/usr/bin/env python3
# Copyright (c) 2016-2026 Murilo Marques Marinho
#
#    This file is part of sas_py.
#
#    sas_py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    sas_py is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sas_py.  If not, see <https://www.gnu.org/licenses/>.
#
# ################################################################
#
#   Author: Murilo M. Marinho, email: murilomarinho@ieee.org
#
# ################################################################

"""
@file example_clock.py
@brief Example of the Clock binding.

A 10 ms sampling clock running 50 loops, printing timing measurements and
statistics.
"""

from marinholab.sas.core import Clock, Statistics


def main():
    # 10 ms clock
    clock = Clock(0.01)

    # Always initialize before the loop to reduce latency
    clock.init()

    for i in range(0, 50):
        # Starting the loop with an update reduces issues with the first loop taking too long
        clock.update_and_sleep()
        print("Loop n = {}".format(i))
        print("  Elapsed time: {}".format(clock.get_elapsed_time_sec()))
        print("  Latest computation time: {}".format(clock.get_time(Clock.TimeType.Computational)))
        print("  Latest idle time: {}".format(clock.get_time(Clock.TimeType.Idle)))
        print("  Latest effective thread sampling time: {}".format(
            clock.get_time(clock.TimeType.EffectiveSampling)
        ))
        print("  Desired thread sampling time: {}".format(
            clock.get_desired_thread_sampling_time_sec()
        ))
        print("  Overrun count: {}".format(clock.get_overrun_count()))

    # Statistics
    print("Statistics for the entire loop")
    print("  Mean computation time: {}".format(clock.get_statistics(
        Statistics.Mean, Clock.TimeType.Computational)
    ))
    print("  Mean idle time: {}".format(clock.get_statistics(
        Statistics.Mean, Clock.TimeType.Idle)
    ))
    print("  Mean effective thread sampling time: {}".format(clock.get_statistics(
        Statistics.Mean, Clock.TimeType.EffectiveSampling)
    ))


if __name__ == '__main__':
    main()
