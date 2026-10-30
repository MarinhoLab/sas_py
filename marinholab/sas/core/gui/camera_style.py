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

"""Qt style sheet for the camera viewer, using the same indigo/violet theme as the touchscreen GUI.
The shared rules are in `common_style`; this module adds the sizes and the camera-only widgets.

Widgets switch looks through a dynamic `state` property (set with `state.set_state`):
  - `connectionLabel`: "connecting", "ready", "error".
  - `resultLabel`: "polished", "unpolished", "unknown", or "" (no result yet).
  - `statusLabel`: "" or "error".
  - `recordButton`: "" or "recording".
  - `hideButton`: "" (inference shown) or "hidden".
"""

from .common_style import COMMON_STYLE_SHEET

STYLE_SHEET = COMMON_STYLE_SHEET + """
QLabel#titleLabel {
    font-size: 26pt;
}

QLabel#connectionLabel {
    font-size: 12pt;
    padding: 6px 18px;
    border-radius: 16px;
    min-width: 110px;
}
QLabel#resultLabel {
    font-size: 15pt;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 4px 18px;
    border-radius: 16px;
}
QPushButton#recordButton, QPushButton#hideButton {
    font-size: 13pt;
    font-weight: 700;
    padding: 6px 18px;
    border-radius: 16px;
}
QPushButton#recordButton {
    min-width: 120px;
}
QPushButton#hideButton {
    min-width: 90px;
}

QLabel#rawCaption, QLabel#inferenceCaption {
    font-size: 16pt;
    padding: 0px 4px 6px 4px;
}

QLabel#videoView {
    background-color: #0c0824;
    border: 1px solid #2a2260;
    border-radius: 18px;
    padding: 6px;
    color: #6a62a3;
    font-size: 13pt;
}
QLabel#videoView[state="error"] {
    color: #f87171;
}

QLabel#statusLabel {
    font-size: 13pt;
}
QLabel#statusLabel[state="error"] {
    color: #f87171;
}
QLabel#hintLabel {
    font-size: 11pt;
}
"""
