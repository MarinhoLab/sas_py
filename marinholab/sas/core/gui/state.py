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

"""Helper for the dynamic `state` property used by the Qt style sheets in this package."""


def set_state(widget, state: str) -> None:
    """Set the `state` property and force Qt to re-evaluate the style sheet for the widget.

    `setProperty` alone does not restyle the widget; Qt's `unpolish`/`polish` pair (unrelated to
    the polisher station) is the standard way to refresh it. Does nothing if the state is unchanged.
    """
    if widget.property("state") == state:
        return
    widget.setProperty("state", state)
    widget.style().unpolish(widget)
    widget.style().polish(widget)
