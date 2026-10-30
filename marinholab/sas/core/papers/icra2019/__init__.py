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
