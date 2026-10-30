# Copyright (c) 2012-2026 Murilo Marques Marinho
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

"""
@file __init__.py
@brief Package entry for the sas_core Python bindings.

This module re-exports the primary Python bindings provided by the
compiled extension module :mod:`marinholab.sas.core._core`.

- Clock: high-resolution timing and sleep class.
- Statistics: enumeration for statistical types.
- RobotDriver: abstract robot driver interface that can be inherited by Python classes.
- ShutdownSignaler: request and wait for orderly shutdown.
- SerialManipulatorSimulatorFriendly: serial-manipulator kinematics model
  with per-joint offsets and actuation types.

The concrete implementations live in the compiled extension module
``marinholab.sas.core._core``.

"""

# The compiled extension subclasses DQ_robotics pybind11 types, so the
# ``dqrobotics`` package (which registers them) must be imported *before*
# ``_core`` is loaded.
import dqrobotics  # noqa: F401

from marinholab.sas.core._core import (
    Clock,
    RobotDriver,
    SerialManipulatorSimulatorFriendly,
    ShutdownSignaler,
    Statistics,
)

# ``ActuationType`` is registered nested on the class (reachable as
# ``SerialManipulatorSimulatorFriendly.ActuationType``); expose it at package
# level too.
ActuationType = SerialManipulatorSimulatorFriendly.ActuationType

__all__ = [
    "Clock",
    "Statistics",
    "RobotDriver",
    "ShutdownSignaler",
    "SerialManipulatorSimulatorFriendly",
    "ActuationType",
]
