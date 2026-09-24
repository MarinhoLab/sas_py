"""
@file __init__.py
@brief Task-space controller from ICRA 2019.

Re-exports the :class:`Controller`, an implementation of the task-space
controller described in:

  "A Unified Framework for the Teleoperation of Surgical Robots in Constrained
  Workspaces", M. M. Marinho et al., 2019 IEEE International Conference on
  Robotics and Automation (ICRA), pages 2721-2727, May 2019. IEEE.
  http://doi.org/10.1109/ICRA.2019.8794363
"""

from marinholab.sas.core.papers.icra2019.controller import Controller

__all__ = [
    "Controller",
]
