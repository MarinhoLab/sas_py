"""Location of the MarinhoLab logo shipped with this package."""

from pathlib import Path

# SVG, designed for a 240x58 header slot (as used by the touchscreen GUI and the camera viewer).
LOGO_PATH = Path(__file__).resolve().parent / "assets" / "marinholab_logo.svg"
