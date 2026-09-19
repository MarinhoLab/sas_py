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
@file example_clock_sched_fifo.py
@brief Example of a real-time (SCHED_FIFO) sampling clock.

Runs a 1 ms clock under a SCHED_FIFO real-time scheduling policy when the
current user has permission; otherwise it degrades gracefully to the default
scheduling policy and still completes.
"""

import os

from marinholab.sas.core import Clock, Statistics


def main():
    # 1 ms clock
    clock = Clock(0.001)

    param = os.sched_param(os.sched_get_priority_max(os.SCHED_FIFO))
    try:
        os.sched_setscheduler(0, os.SCHED_FIFO, param)
    except PermissionError as e:
        print(e)

    # Always initialize before the loop to reduce latency
    clock.init()

    for _ in range(0, 50):
        # Starting the loop with an update reduces issues with the first loop taking too long
        clock.update_and_sleep()

    # Statistics
    print("Statistics for the entire loop")
    print(f"  Mean computation time: {clock.get_statistics(Statistics.Mean, Clock.TimeType.Computational)}")
    print(f"  Mean idle time: {clock.get_statistics(Statistics.Mean, Clock.TimeType.Idle)}")
    print(f"  Mean effective thread sampling time: {clock.get_statistics(Statistics.Mean, Clock.TimeType.EffectiveSampling)}")
    print(f"  Overrun count: {clock.get_overrun_count()}")


if __name__ == '__main__':
    main()
