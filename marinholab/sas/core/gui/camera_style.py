"""Qt style sheet for the camera viewer, using the same indigo/violet theme as the touchscreen GUI
(see `touchscreen_style`).

Widgets switch looks through a dynamic `state` property (set with `state.set_state`):
  - `connectionLabel`: "connecting", "ready", "error".
  - `resultLabel`: "polished", "unpolished", "unknown", or "" (no result yet).
  - `statusLabel`: "" or "error".
  - `recordButton`: "" or "recording".
  - `hideButton`: "" (inference shown) or "hidden".
"""

STYLE_SHEET = """
QWidget#centralwidget {
    background-color: #120d2b;
}

QLabel {
    color: #ece9ff;
}

QLabel#titleLabel {
    font-size: 26pt;
    font-weight: 700;
    letter-spacing: 2px;
    color: #faf9ff;
}

/* Pills (connection and result) and buttons (record and hide) share their base look. */
QLabel#connectionLabel, QLabel#resultLabel {
    border-radius: 16px;
    color: #aaa5d6;
    background-color: #251c4d;
    border: 2px solid #40347a;
}
QLabel#connectionLabel {
    font-size: 12pt;
    font-weight: 600;
    padding: 6px 18px;
    min-width: 110px;
}
QLabel#resultLabel {
    font-size: 15pt;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 4px 18px;
}
QPushButton#recordButton, QPushButton#hideButton {
    font-size: 13pt;
    font-weight: 700;
    padding: 6px 18px;
    border-radius: 16px;
    color: #f4f2ff;
    background-color: #251c4d;
    border: 2px solid #40347a;
}
QPushButton#recordButton {
    min-width: 120px;
}
QPushButton#hideButton {
    min-width: 90px;
}
QPushButton#recordButton:hover, QPushButton#hideButton:hover {
    background-color: #352a6b;
}

/* Shared state colours. */
QLabel#connectionLabel[state="ready"], QLabel#resultLabel[state="polished"] {
    color: #4ade80;
    background-color: #052e16;
    border-color: #166534;
}
QLabel#resultLabel[state="unpolished"] {
    color: #fbbf24;
    background-color: #422006;
    border-color: #92400e;
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
QPushButton#hideButton[state="hidden"] {
    color: #ffffff;
    background-color: #4338ca;
    border-color: #818cf8;
}
QPushButton#recordButton:disabled {
    color: #6a62a3;
    background-color: #191340;
    border-color: #251c4d;
}

/* Sections group a caption with its video, tinted like the touchscreen's station sections. */
QFrame#rawSection {
    background-color: #141d4d;
    border: 1px solid #2f3fa8;
    border-radius: 28px;
}
QFrame#inferenceSection {
    background-color: #27144d;
    border: 1px solid #6b34b8;
    border-radius: 28px;
}

QLabel#rawCaption, QLabel#inferenceCaption {
    font-size: 16pt;
    font-weight: 700;
    letter-spacing: 3px;
    padding: 0px 4px 6px 4px;
    background: transparent;
}
QLabel#rawCaption {
    color: #a5b4fc;
    border-bottom: 3px solid #6366f1;
}
QLabel#inferenceCaption {
    color: #d8b4fe;
    border-bottom: 3px solid #a855f7;
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

QFrame#statusFrame {
    background-color: #251c4d;
    border: 2px solid #40347a;
    border-radius: 20px;
}
QLabel#statusLabel {
    font-size: 13pt;
    font-weight: 600;
    color: #f4f2ff;
}
QLabel#statusLabel[state="error"] {
    color: #f87171;
}
QLabel#hintLabel {
    font-size: 11pt;
    color: #aaa5d6;
}
"""
