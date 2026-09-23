"""Type stubs for the compiled extension module ``marinholab.sas.core._core``."""
from __future__ import annotations

from typing import Optional
from datetime import datetime, timedelta

import numpy as np
from dqrobotics import DQ
from dqrobotics.robot_modeling import DQ_SerialManipulator

__all__ = [
    "Statistics",
    "ShutdownSignaler",
    "Clock",
    "RobotDriver",
    "SerialManipulatorSimulatorFriendly",
]


class Statistics:
    """Statistic types used by the Clock class."""

    Mean: "Statistics"


class ShutdownSignaler:
    """Cross-module shutdown signaling class.

    Coordinates shutdown requests between different parts of the system.
    """

    def __init__(self) -> None: ...

    def should_shutdown(self) -> bool:
        """Check whether a shutdown has been requested."""
        ...

    def shutdown(self) -> None:
        """Trigger a shutdown request."""
        ...


class Clock:
    """Timing utilities for control loops and statistics collection."""

    class TimeType:
        """Enumeration of time types recorded by Clock."""

        Computational: "Clock.TimeType"
        EffectiveSampling: "Clock.TimeType"
        Idle: "Clock.TimeType"

    def __init__(
        self, sampling_time_in_seconds: float, enable_statistics: bool = True
    ) -> None: ...

    def init(self) -> None:
        """Initialize the clock internal state and timers."""
        ...

    def update_and_sleep(self) -> None:
        """Update internal timing measurements and sleep to respect the target sampling time."""
        ...

    def get_elapsed_time_sec(self) -> float:
        """Get elapsed time since initialization in seconds."""
        ...

    def get_desired_thread_sampling_time_sec(self) -> float:
        """Get the configured sampling interval in seconds."""
        ...

    def safe_sleep_seconds(self, seconds: float, break_loop: Optional[object]) -> None:
        """Sleep for approximately the given duration while allowing early exit.

        :param seconds: Duration in seconds to sleep.
        :param break_loop: Optional pointer to an atomic boolean used to
            interrupt the sleep early.
        """
        ...

    def blocking_sleep_seconds(self, seconds: float) -> None:
        """Block the calling thread for the specified duration (no early exit)."""
        ...

    def get_overrun_count(self) -> int:
        """Return the number of times the sampling period has been missed (overrun)."""
        ...

    def get_time(self, time_type: "Clock.TimeType") -> float:
        """Get a time measurement for a given TimeType, in seconds."""
        ...

    def get_statistics(
        self, statistics: Statistics, time_type: "Clock.TimeType"
    ) -> float:
        """Get a collected statistic value.

        Raises:
            RuntimeError: If statistics collection was not enabled at
                construction or the requested statistic is not available.
        """
        ...


class RobotDriver:
    """Abstract interface for robot hardware drivers.

    Subclasses must implement the pure-virtual methods:
    ``get_joint_positions``, ``set_target_joint_positions``, ``connect``,
    ``disconnect``, ``initialize`` and ``deinitialize``.
    """

    def __init__(self, ss: ShutdownSignaler) -> None: ...

    def get_joint_positions(self) -> np.ndarray: ...
    def set_target_joint_positions(self, target: np.ndarray) -> None: ...

    def get_joint_velocities(self) -> np.ndarray: ...
    def set_target_joint_velocities(self, target: np.ndarray) -> None: ...

    def get_joint_torques(self) -> np.ndarray: ...
    def set_target_joint_torques(self, target: np.ndarray) -> None: ...

    def get_joint_limits(self) -> tuple[np.ndarray, np.ndarray]: ...
    def set_joint_limits(self, joint_limits: tuple[np.ndarray, np.ndarray]) -> None: ...

    def watchdog_start(self, period: timedelta) -> None: ...
    def watchdog_trigger(
        self,
        time_point_from_the_client: datetime,
        time_point_from_the_server: datetime,
        status: bool,
    ) -> None: ...
    def watchdog_set_maximum_acceptable_delay(self, max_acceptable_delay: float) -> None: ...
    def check_for_watchdog_exceptions(self) -> None: ...

    def connect(self) -> None: ...
    def disconnect(self) -> None: ...

    def initialize(self) -> None: ...
    def deinitialize(self) -> None: ...


class SerialManipulatorSimulatorFriendly(DQ_SerialManipulator):
    """A serial manipulator whose joints carry explicit pre/post offsets.

    Each joint contributes a dual-quaternion transformation of the form
    ``offset_before * actuation(q) * offset_after``. Supports both revolute
    (R) and prismatic (T) joints about any principal axis.

    Inherits from ``DQ_SerialManipulator`` and overrides the raw kinematic
    methods. The ``ActuationType`` enum is registered as a nested attribute
    of the class, so it is reachable as
    ``SerialManipulatorSimulatorFriendly.ActuationType.RX``.
    """

    class ActuationType:
        """The actuation type and axis of a single joint.

        - RZ: Revolution about the z-axis.
        - RY: Revolution about the y-axis.
        - RX: Revolution about the x-axis.
        - TZ: Translation along the z-axis.
        - TY: Translation along the y-axis.
        - TX: Translation along the x-axis.
        """

        RZ: "SerialManipulatorSimulatorFriendly.ActuationType"
        RY: "SerialManipulatorSimulatorFriendly.ActuationType"
        RX: "SerialManipulatorSimulatorFriendly.ActuationType"
        TZ: "SerialManipulatorSimulatorFriendly.ActuationType"
        TY: "SerialManipulatorSimulatorFriendly.ActuationType"
        TX: "SerialManipulatorSimulatorFriendly.ActuationType"

    def __init__(
        self,
        offset_before: list[DQ],
        offset_after: list[DQ],
        actuation_types: list[ActuationType],
    ) -> None:
        """Construct the manipulator.

        Args:
            offset_before: Per-joint dual-quaternion offset applied before
                actuation.
            offset_after: Per-joint dual-quaternion offset applied after
                actuation.
            actuation_types: Per-joint actuation type and axis.

        Raises:
            RuntimeError: If the three vectors do not have equal size.
        """
        ...

    def raw_fkm(self, q_vec: np.ndarray, to_ith_link: int) -> DQ:
        """Raw forward kinematics of the chain up to a given link.

        Args:
            q_vec: Joint configuration vector.
            to_ith_link: Index of the terminal link.

        Returns:
            The dual-quaternion pose of the terminal link.
        """
        ...

    def raw_pose_jacobian(self, q_vec: np.ndarray, to_ith_link: int) -> np.ndarray:
        """Raw pose Jacobian of the chain up to a given link.

        Args:
            q_vec: Joint configuration vector.
            to_ith_link: Index of the terminal link.

        Returns:
            An 8 x (to_ith_link+1) dual-quaternion pose Jacobian.
        """
        ...

    def raw_pose_jacobian_derivative(
        self, q: np.ndarray, q_dot: np.ndarray, to_ith_link: int
    ) -> np.ndarray:
        """Time derivative of the raw pose Jacobian.

        Args:
            q: Joint configuration vector.
            q_dot: Joint velocity vector.
            to_ith_link: Index of the terminal link.

        Returns:
            An 8 x (to_ith_link+1) Jacobian-derivative matrix.
        """
        ...
