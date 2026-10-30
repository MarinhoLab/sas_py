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
@brief Kinematic modeling bindings.

This subpackage mirrors the C++ namespace ``marinholab::sas::core::modeling``
and re-exports the modeling classes bound by the compiled extension module
:mod:`marinholab.sas.core._core`.

- SerialManipulatorSimulatorFriendly: serial-manipulator kinematics model with
  configurable per-joint offsets and actuation types.
- ActuationType: per-joint actuation type and axis (also reachable as
  ``SerialManipulatorSimulatorFriendly.ActuationType``).

"""

# The compiled extension subclasses DQ_robotics pybind11 types; import
# ``dqrobotics`` first so its types are registered before ``_core`` loads.
import dqrobotics  # noqa: F401

from marinholab.sas.core._core import SerialManipulatorSimulatorFriendly

# ``ActuationType`` is registered nested on the class (reachable as
# ``SerialManipulatorSimulatorFriendly.ActuationType``); expose it here too.
ActuationType = SerialManipulatorSimulatorFriendly.ActuationType

__all__ = [
    "SerialManipulatorSimulatorFriendly",
    "ActuationType",
]
