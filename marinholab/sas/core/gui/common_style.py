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

"""Qt style sheet rules shared by the touchscreen GUI (`touchscreen_style`) and the camera viewer
(`camera_style`), which use the same indigo/violet theme. Each of them appends its own rules for
sizes, layout and widgets only it has.

Rules here mostly set colours and the typographic style. Sizes and padding are left to the
application sheets, so the same widget can be sized differently in each one. Some ids are only
used by one of the applications; they are listed here so that each palette (green, amber, red,
selected) is defined in a single place.

The rules are ordered so that ties in specificity (e.g. `#recordButton:hover` and
`#recordButton[state="recording"]`) resolve as the application sheets expect: bases, then hover,
then state palettes, then disabled.
"""

COMMON_STYLE_SHEET = """
QMainWindow, QWidget#centralwidget {
    background-color: #120d2b;
}

QLabel {
    color: #ece9ff;
}

QLabel#titleLabel {
    font-weight: 700;
    letter-spacing: 2px;
    color: #faf9ff;
}

/* Pills. The connection and result pills are muted until a state applies; the polisher and
   force-sensor pills start amber. */
QLabel#connectionLabel, QLabel#resultLabel {
    color: #aaa5d6;
    background-color: #251c4d;
    border: 2px solid #40347a;
}
QLabel#connectionLabel {
    font-weight: 600;
}
QLabel#polisherConnectionLabel, QLabel#forceSensorLabel {
    font-weight: 700;
    letter-spacing: 1px;
    border: 1px solid #92400e;
    border-radius: 12px;
}

QPushButton {
    font-weight: 600;
    color: #f4f2ff;
    background-color: #251c4d;
    border: 2px solid #40347a;
}
QPushButton:pressed {
    background-color: #4f46e5;
    border-color: #6366f1;
}
QPushButton#recordButton:hover, QPushButton#hideButton:hover {
    background-color: #352a6b;
}

/* State palettes. */
QLabel#connectionLabel[state="moving"], QLabel#resultLabel[state="unpolished"],
QLabel#polisherConnectionLabel, QLabel#forceSensorLabel {
    color: #fbbf24;
    background-color: #422006;
    border-color: #92400e;
}
QLabel#connectionLabel[state="ready"], QLabel#resultLabel[state="polished"],
QLabel#polisherConnectionLabel[state="connected"], QLabel#forceSensorLabel[state="connected"] {
    color: #4ade80;
    background-color: #052e16;
    border-color: #166534;
}
QLabel#resultLabel[state="unknown"] {
    color: #d4cff3;
    background-color: #251c4d;
    border-color: #40347a;
}
QLabel#connectionLabel[state="error"], QPushButton#recordButton[state="recording"] {
    color: #ffffff;
    background-color: #b91c1c;
    border-color: #f87171;
}
QPushButton#hideButton[state="hidden"], QPushButton[role="jogStep"][state="selected"] {
    color: #ffffff;
    background-color: #4338ca;
    border-color: #818cf8;
}
QPushButton:disabled, QPushButton#recordButton:disabled, QPushButton#hideButton:disabled {
    color: #6a62a3;
    background-color: #191340;
    border-color: #251c4d;
}

/* Sections group a caption with its content: a station in the touchscreen, a video in the
   camera viewer. They are flat, tinted areas (no raised border or bevel) so they do not read as
   buttons themselves. */
QFrame#microscopeSection, QFrame#rawSection {
    background-color: #141d4d;
    border: 1px solid #2f3fa8;
    border-radius: 28px;
}
QFrame#polisherSection, QFrame#inferenceSection {
    background-color: #27144d;
    border: 1px solid #6b34b8;
    border-radius: 28px;
}
QLabel#microscopeCaption, QLabel#polisherCaption, QLabel#rawCaption, QLabel#inferenceCaption {
    font-weight: 700;
    letter-spacing: 3px;
    background: transparent;
}
QLabel#microscopeCaption, QLabel#rawCaption {
    color: #a5b4fc;
    border-bottom: 3px solid #6366f1;
}
QLabel#polisherCaption, QLabel#inferenceCaption {
    color: #d8b4fe;
    border-bottom: 3px solid #a855f7;
}

QFrame#statusFrame {
    background-color: #251c4d;
    border: 2px solid #40347a;
    border-radius: 20px;
}
QLabel#statusLabel {
    font-weight: 600;
    color: #f4f2ff;
}
QLabel#errorLabel, QLabel#hintLabel {
    color: #aaa5d6;
}
"""
