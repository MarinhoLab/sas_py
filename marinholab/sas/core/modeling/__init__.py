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
