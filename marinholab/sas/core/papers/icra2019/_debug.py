# Copyright (c) 2020-2025 Murilo Marques Marinho
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
#
# ################################################################
#
#   Author: Murilo M. Marinho, email: murilomarinho@ieee.org
#
# ################################################################

"""
Standardized debug output for the ICRA 2019 task-space controller.

Every debug line starts with a fixed-width category tag (for example
``[rcm       #0]``) followed by ``key=value`` fields with a fixed numeric
format, so the per-constraint margins printed at a control step are easy to
read and to grep. The available categories are listed in
:data:`CONSTRAINT_CATEGORIES`; the ``verbose`` argument accepted by the
public API has the type :data:`Verbose` (``True`` enables every category,
``False`` disables all of them, and a mapping selects individual
categories).
"""

import math

from termcolor import cprint

#: Constraint families that can be enabled for debug output.
CONSTRAINT_CATEGORIES: tuple[str, ...] = (
    "rcm",
)

#: ``verbose`` setting accepted by the public API: ``True`` enables every
#: category, ``False`` disables all of them, and a mapping selects
#: individual categories by name.
Verbose = bool | dict[str, bool]


def normalize_verbose(verbose: Verbose) -> dict[str, bool]:
    """Normalize a ``verbose`` setting into a per-category flag mapping.

    Args:
        verbose: ``True`` enables every category, ``False`` disables all of
            them, and a mapping selects individual categories.

    Returns:
        A mapping with one boolean entry per
        :data:`CONSTRAINT_CATEGORIES` category.

    Raises:
        ValueError: If the mapping contains an unknown category name.
        TypeError: If ``verbose`` is neither a bool nor a mapping.
    """
    if isinstance(verbose, bool):
        return {category: verbose for category in CONSTRAINT_CATEGORIES}
    if isinstance(verbose, dict):
        normalized = {category: False for category in CONSTRAINT_CATEGORIES}
        for category in CONSTRAINT_CATEGORIES:
            normalized[category] = bool(verbose.get(category, False))
        unknown = [key for key in verbose if key not in CONSTRAINT_CATEGORIES]
        if unknown:
            raise ValueError(
                f"Unknown verbose categories {unknown}. "
                f"Expected one of: {', '.join(CONSTRAINT_CATEGORIES)}."
            )
        return normalized
    raise TypeError(
        "verbose must be a bool or a dict mapping category names to booleans."
    )


def _tag(category: str, index: int) -> str:
    """Return the fixed-width debug tag for a category and entity index.

    Args:
        category: One of :data:`CONSTRAINT_CATEGORIES`.
        index: Index of the entity the message refers to (RCM constraint).

    Returns:
        A tag such as ``[rcm       #0]``.
    """
    return f"[{category:<11} #{index}]"


def _violation(description: str) -> None:
    """Print an indented red line describing a violated constraint.

    Args:
        description: Human-readable description of the violation, including
            any measured depth.
    """
    cprint(f"    VIOLATION: {description}", "red")


def debug_rcm(
    verbose: dict[str, bool],
    index: int,
    signed_error: float,
    vfi_gain: float,
) -> None:
    """Print the RCM-constraint debug block for one constraint.

    Args:
        verbose: Per-category flags from :func:`normalize_verbose`.
        index: RCM constraint index.
        signed_error: Signed line-to-point error scaled by the VFI gain
            (m^2).
        vfi_gain: VFI gain applied to the constraint; the violation depth
            is recovered as ``sqrt(-signed_error / vfi_gain)``.
    """
    if not verbose["rcm"]:
        return
    tag = _tag("rcm", index)
    print(f"{tag} signed_error={signed_error:+.6e} (m^2)")
    if signed_error < 0.0:
        if vfi_gain > 0.0:
            depth = math.sqrt(-signed_error / vfi_gain)
        else:
            depth = float("inf")
        _violation(f"RCM safe radius exceeded by {depth:.6f} m")
