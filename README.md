# marinholab-sas-core

> Python bindings for the ROS-free SmartArmStack C++ core.
>
> This repository wraps
> [MarinhoLab/sas_cpp](https://github.com/MarinhoLab/sas_cpp)
> (the pure-C++ part of
> [SmartArmStack/sas_core](https://github.com/SmartArmStack/sas_core)) with
> pybind11, exposing it to Python as the `marinholab.sas.core` package.
>
> More information about SmartArmStack is available in
> [smartarmstack.github.io](https://smartarmstack.github.io/).

## Contents

- `marinholab/sas/core/` — the Python package.
  - `_core.*` — compiled pybind11 extension (the C++ bindings live in `src/`).
  - `example_*.py` — example scripts (also installed as commands).
- `src/` — the C++ binding sources (ported from `SmartArmStack/sas_core`).
- `submodules/sas_cpp` — the C++ core (git submodule, consumed via CMake).
- `submodules/pybind11` — pybind11 (git submodule, pinned to v3.0.4).
- `docker/` — `ubuntu:noble` build environment and full test pipeline.

The C++ core depends on **Eigen3** and **dqrobotics** (the latter is located
by CMake at build time; on Debian/Ubuntu it comes from the DQ Robotics PPA).

## Installation

From source:

```bash
git clone --recursive https://github.com/MarinhoLab/sas_py.git
cd sas_py
pip install . --no-build-isolation
```

Building requires `cmake` (>= 3.16), `ninja`, a C++17 compiler, Eigen3, and
`dqrobotics`. On Debian/Ubuntu:

```bash
sudo apt install build-essential g++ cmake ninja-build python3-dev libeigen3-dev
# dqrobotics from the DQ Robotics PPA:
sudo add-apt-repository -y ppa:dqrobotics-dev/development
sudo apt install libdqrobotics
```

## Usage

```python
from marinholab.sas.core import (
    Clock,
    Statistics,
    RobotDriver,
    ShutdownSignaler,
)

# High-resolution sampling clock
clock = Clock(0.01)          # 10 ms sampling period
clock.init()
for _ in range(100):
    clock.update_and_sleep()
print(clock.get_statistics(Statistics.Mean, Clock.TimeType.Computational))

# Subclass RobotDriver to drive hardware
class MyDriver(RobotDriver):
    def __init__(self, ss):
        super().__init__(ss)
    def get_joint_positions(self):
        return np.zeros(6)
    def set_target_joint_positions(self, target):
        ...
    def connect(self):
        ...
    def disconnect(self):
        ...
    def initialize(self):
        ...
    def deinitialize(self):
        ...
```

The examples are installed as commands:

- `sas_core_clock_example` — a 10 ms `Clock` with timing statistics.
- `sas_core_clock_sched_fifo_example` — a 1 ms `Clock` under `SCHED_FIFO`.
- `sas_core_robot_driver_subclass_example` — subclass `RobotDriver` in Python
  and exercise the trampoline (connect / initialize / targets / limits).

## Versioning

The version is computed from git tags at build time by
`setuptools-git-versioning`. A monthly version tag of the form `YY.MM`
(e.g. `26.09`) plus the number of commits since that tag yields a rolling
`YY.MM.NN` version (e.g. `26.09.3`), mirroring `MarinhoLab/sas_cpp`.
An untagged checkout builds as `0.0.1` (a development version).

## Testing

A full build + test pipeline runs in an `ubuntu:noble` container:

```bash
cd docker
docker compose run --rm marinholab_sas_core
```

## License

See [`LICENSE`](LICENSE) for details (LGPLv3).