/*
# Copyright (c) 2016-2026 Murilo Marques Marinho
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
# ################################################################*/

/**
 * @file sas_modeling_py.cpp
 * @brief Python bindings for the kinematic modeling classes.
 */

#include <memory>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include <marinholab/sas/core/modeling/serial_manipulator_simulator_friendly.hpp>

namespace py = pybind11;

using SM = marinholab::sas::core::modeling::SerialManipulatorSimulatorFriendly;
using DQ = DQ_robotics::DQ;
using SMBase = DQ_robotics::DQ_SerialManipulator;

namespace marinholab::sas::core
{

void init_sas_modeling_py(py::module_& m)
{
    py::class_<SM, std::shared_ptr<SM>, SMBase> cls(
        m, "SerialManipulatorSimulatorFriendly",
        R"pbdoc(@brief A serial manipulator whose joints carry explicit pre/post offsets.

Each joint contributes a dual-quaternion transformation of the form
``offset_before * actuation(q) * offset_after``, which lets the model
represent sensor frames and joint offsets that a plain
``DQ_SerialManipulator`` would not. Supports both revolute (R) and
prismatic (T) joints about any principal axis.)pbdoc");

    cls.def(py::init<std::vector<DQ>, std::vector<DQ>, std::vector<SM::ActuationType>>(),
            py::arg("offset_before"), py::arg("offset_after"), py::arg("actuation_types"),
            R"pbdoc(@brief Construct the manipulator.

@param offset_before Per-joint dual-quaternion offset applied before actuation.
@param offset_after Per-joint dual-quaternion offset applied after actuation.
@param actuation_types Per-joint actuation type and axis.

@throws RuntimeError if the three vectors do not have equal size.)pbdoc")
        .def("raw_fkm",
             (DQ (SM::*)(const VectorXd&, const int&) const) & SM::raw_fkm,
             py::arg("q_vec"), py::arg("to_ith_link"),
             R"pbdoc(@brief Raw forward kinematics of the chain up to a given link.

@param q_vec Joint configuration vector.
@param to_ith_link Index of the terminal link.
@return The dual-quaternion pose of the terminal link.)pbdoc")
        .def("raw_pose_jacobian",
             (MatrixXd (SM::*)(const VectorXd&, const int&) const) & SM::raw_pose_jacobian,
             py::arg("q_vec"), py::arg("to_ith_link"),
             R"pbdoc(@brief Raw pose Jacobian of the chain up to a given link.

@param q_vec Joint configuration vector.
@param to_ith_link Index of the terminal link.
@return An 8 x (to_ith_link+1) dual-quaternion pose Jacobian.)pbdoc")
        .def("raw_pose_jacobian_derivative",
             (MatrixXd (SM::*)(const VectorXd&, const VectorXd&, const int&) const)
                 & SM::raw_pose_jacobian_derivative,
             py::arg("q"), py::arg("q_dot"), py::arg("to_ith_link"),
             R"pbdoc(@brief Time derivative of the raw pose Jacobian.

@param q Joint configuration vector.
@param q_dot Joint velocity vector.
@param to_ith_link Index of the terminal link.
@return An 8 x (to_ith_link+1) Jacobian-derivative matrix.)pbdoc");

    // Registered on the class (not the module) so it is reachable as
    // SerialManipulatorSimulatorFriendly.ActuationType.<...>.
    py::enum_<SM::ActuationType>(
        cls, "ActuationType",
        R"pbdoc(@brief The actuation type and axis of a single joint.

Values:
- RZ: Revolution about the z-axis.
- RY: Revolution about the y-axis.
- RX: Revolution about the x-axis.
- TZ: Translation along the z-axis.
- TY: Translation along the y-axis.
- TX: Translation along the x-axis.)pbdoc")
        .value("RZ", SM::ActuationType::RZ, "Revolution about the z-axis")
        .value("RY", SM::ActuationType::RY, "Revolution about the y-axis")
        .value("RX", SM::ActuationType::RX, "Revolution about the x-axis")
        .value("TZ", SM::ActuationType::TZ, "Translation along the z-axis")
        .value("TY", SM::ActuationType::TY, "Translation along the y-axis")
        .value("TX", SM::ActuationType::TX, "Translation along the x-axis")
        .export_values();
}

}
