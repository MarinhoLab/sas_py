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
    Statistics,
    RobotDriver,
    ShutdownSignaler,
    SerialManipulatorSimulatorFriendly,
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
