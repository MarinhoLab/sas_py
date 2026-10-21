"""
Copyright (C) 2020-2026 Murilo Marques Marinho (www.murilomarinho.info)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not,
see <https://www.gnu.org/licenses/>.
"""

from .common_style import COMMON_STYLE_SHEET

# Qt style sheet for the touchscreen GUI: a dark indigo/violet, high-contrast theme with large
# touch targets.
#
# Some widgets are styled according to a dynamic `state` property, set in main_window.py:
#   - target buttons: "" (idle), "active" (robot moving towards it), "reached" (robot converged),
#     "short" (the motion timed out before converging).
#   - `connectionLabel`: "connecting", "ready", or "moving".
#   - `progressBar`: "moving", "reached", or "short".
#   - `errorLabel`, `jogHintLabel`, `polisherHintLabel`: "warning".
#   - `polisherConnectionLabel`: "" (not connected) or "connected".
#   - `polisherPanel`: "" or "on".
STYLE_SHEET = COMMON_STYLE_SHEET + """
QLabel#titleLabel {
    font-size: 28pt;
}

QLabel#connectionLabel {
    font-size: 13pt;
    padding: 8px 20px;
    border-radius: 18px;
    min-width: 120px;
}
QLabel#jogHintLabel[state="warning"], QLabel#polisherHintLabel[state="warning"],
QLabel#forceHintLabel[state="warning"], QLabel#errorLabel[state="warning"],
QLabel#forceValueLabel[state="high"] {
    color: #fbbf24;
}

QPushButton {
    font-size: 22pt;
    border-radius: 20px;
    padding: 16px;
}
QPushButton[state="active"], QPushButton[state="active"]:disabled {
    color: #ffffff;
    background-color: #b45309;
    border-color: #f59e0b;
}
QPushButton[state="reached"] {
    color: #ffffff;
    background-color: #15803d;
    border-color: #22c55e;
}
QPushButton[state="reached"]:pressed {
    background-color: #4f46e5;
    border-color: #6366f1;
}
QPushButton[state="short"] {
    color: #fde68a;
    background-color: #451a03;
    border-color: #d97706;
}
QPushButton[state="short"]:disabled {
    color: #b45309;
    background-color: #2a1305;
    border-color: #78350f;
}
QPushButton[state="reached"]:disabled {
    color: #86efac;
    background-color: #14321f;
    border-color: #166534;
}

QLabel#microscopeCaption, QLabel#polisherCaption {
    font-size: 20pt;
    padding: 0px 4px 8px 4px;
}
QLabel#statusLabel {
    font-size: 17pt;
}
QLabel#errorLabel {
    font-size: 13pt;
}

/* Rules shared by the polisher and force panels and the jog pad. */
QFrame#polisherPanel, QFrame#forcePanel {
    background-color: #1d1042;
    border: 1px solid #6b34b8;
    border-radius: 20px;
}
QLabel#jogTitleLabel, QLabel#polisherControlTitleLabel, QLabel#forceTitleLabel {
    font-weight: 700;
    letter-spacing: 2px;
    background: transparent;
}
QLabel#jogOffsetLabel, QLabel#jogStepLabel, QLabel#jogHintLabel,
QLabel#jogTranslateLabel, QLabel#jogRotateLabel,
QLabel#polisherPowerLabel, QLabel#polisherSpeedLabel, QLabel#polisherHintLabel,
QLabel#forceValueLabel, QLabel#forceHintLabel {
    color: #aaa5d6;
    background: transparent;
}
QPushButton[role="jog"], QPushButton[role="jogStep"],
QPushButton#polisherSpeedDownButton, QPushButton#polisherSpeedUpButton,
QPushButton#forceResetPeakButton {
    border-radius: 14px;
}

/* Fine-adjustment pad, inside the microscope section. */
QFrame#jogPanel {
    background-color: #150f3a;
    border: 1px solid #2f3fa8;
    border-radius: 20px;
}
QFrame#jogPanel[state="enabled"] {
    border-color: #6366f1;
}
QLabel#jogTitleLabel {
    font-size: 15pt;
    color: #a5b4fc;
}
QLabel#jogOffsetLabel, QLabel#jogStepLabel, QLabel#jogHintLabel,
QLabel#jogTranslateLabel, QLabel#jogRotateLabel {
    font-size: 12pt;
}
QLabel#jogTranslateXLabel, QLabel#jogTranslateYLabel, QLabel#jogTranslateZLabel,
QLabel#jogRotateXLabel, QLabel#jogRotateYLabel, QLabel#jogRotateZLabel {
    font-size: 16pt;
    font-weight: 700;
    color: #d4cff3;
    min-width: 28px;
    background: transparent;
}
QPushButton[role="jog"] {
    font-size: 24pt;
    padding: 4px;
}
QPushButton[role="jogStep"] {
    font-size: 12pt;
    font-weight: 600;
    color: #d4cff3;
    background-color: #191340;
    border: 2px solid #2f3fa8;
    padding: 8px 12px;
    min-height: 28px;
}
QPushButton[role="jogStep"][state="selected"] {
    color: #ffffff;
    background-color: #4338ca;
    border-color: #818cf8;
}

/* Polisher control panel, inside the polisher section (see polisher_panel.py). */
QFrame#polisherPanel[state="on"] {
    border-color: #a855f7;
}
QLabel#polisherControlTitleLabel {
    font-size: 15pt;
    color: #d8b4fe;
}
QLabel#polisherConnectionLabel {
    font-size: 11pt;
    padding: 4px 12px;
}
QLabel#polisherPowerLabel, QLabel#polisherSpeedLabel, QLabel#polisherHintLabel {
    font-size: 12pt;
}
QPushButton#polisherPowerButton {
    font-size: 24pt;
    font-weight: 700;
    letter-spacing: 2px;
}
QPushButton#polisherPowerButton:checked {
    color: #ffffff;
    background-color: #7e22ce;
    border-color: #c084fc;
}
QPushButton#polisherSpeedDownButton, QPushButton#polisherSpeedUpButton {
    font-size: 22pt;
    padding: 2px;
}

/* Force column on the right (see force_panel.py). ForceBar paints itself; only the labels
   around it are styled. */
QLabel#forceTitleLabel {
    font-size: 14pt;
    color: #d8b4fe;
}
QLabel#forceValueLabel {
    font-size: 17pt;
    font-weight: 700;
}
QLabel#forceValueLabel[state="ok"] {
    color: #d8b4fe;
}
QLabel#forceSensorLabel {
    font-size: 10pt;
    padding: 4px 10px;
}
QLabel#forceHintLabel {
    font-size: 11pt;
}
QPushButton#forceResetPeakButton {
    font-size: 12pt;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 4px;
}

QProgressBar {
    background-color: #120d2b;
    border: none;
    border-radius: 6px;
    min-height: 12px;
    max-height: 12px;
}
QProgressBar::chunk {
    border-radius: 6px;
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #a855f7);
}
QProgressBar[state="moving"]::chunk {
    background-color: #f59e0b;
}
QProgressBar[state="reached"]::chunk {
    background-color: #22c55e;
}
QProgressBar[state="short"]::chunk {
    background-color: #d97706;
}
"""

