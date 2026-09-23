#!/usr/bin/env bash
# Full build + test pipeline for marinholab-sas-core:
#   1. Install the package with the usual command (pip, CMake build of _core)
#   2. Verify the import path and the public API
#   3. Run all Python example scripts (Clock, SCHED_FIFO, RobotDriver subclass)
set -euo pipefail
cd "$(dirname "$0")/.."

echo "=== Version scheme (rolling YY.MM.NN) ==="

echo "=== pip install . --no-build-isolation ==="
python3 -m pip install --no-cache-dir --break-system-packages . --no-build-isolation

# Run the checks from a neutral directory so `import marinholab` resolves to
# the *installed* package in site-packages, not the source tree in /opt/sas_py
# (which would shadow it and lacks the compiled _core extension).
cd /root

echo "=== Import + public API check ==="
python3 - <<'EOF'
import numpy as np
import marinholab.sas.core as core
from marinholab.sas.core import (
    Clock,
    Statistics,
    RobotDriver,
    ShutdownSignaler,
    SerialManipulatorSimulatorFriendly,
    ActuationType,
)

ss = ShutdownSignaler()
assert ss.should_shutdown() is False
ss.shutdown()
assert ss.should_shutdown() is True

clock = Clock(0.001)
assert clock.get_desired_thread_sampling_time_sec() == 0.001
assert Clock.TimeType.Computational is not None

# Modeling: build a 3-joint RX/RY/RZ arm and check that the pose Jacobian
# agrees with the finite-difference derivative of raw_fkm.
from dqrobotics import DQ

SM = SerialManipulatorSimulatorFriendly
AT = SM.ActuationType
assert AT is ActuationType  # the enum is reachable both ways
ob = [DQ([1.0, 0.0, 0.0, 0.0])] * 3
oa = [DQ([1.0, 0.0, 0.0, 0.0])] * 3
m = SM(ob, oa, [AT.RX, AT.RY, AT.RZ])
q = np.array([0.1, -0.2, 0.3])
h = 1e-6
J = m.raw_pose_jacobian(q, 2)
assert J.shape == (8, 3), J.shape
fd = np.zeros((8, 3))
for c in range(3):
    qp = q.copy(); qp[c] += h
    qm = q.copy(); qm[c] -= h
    fd[:, c] = (np.asarray(m.raw_fkm(qp, 2).vec8()) - np.asarray(m.raw_fkm(qm, 2).vec8())) / (2 * h)
max_err = np.max(np.abs(J - fd))
assert max_err < 1e-6, f"Jacobian/FDM mismatch: {max_err}"
assert np.allclose(m.get_lower_q_limit(), -10.0)
assert np.allclose(m.get_upper_q_limit(), 10.0)

print("import + API OK (incl. modeling, FD Jacobian err=%.2e)" % max_err)
EOF

echo "=== Running example scripts ==="
sas_core_clock_example
sas_core_clock_sched_fifo_example
sas_core_robot_driver_subclass_example

echo "=== Verify installed files ==="
python3 - <<'EOF'
import marinholab.sas.core, os
d = os.path.dirname(marinholab.sas.core.__file__)
print("package dir:", d)
for f in sorted(os.listdir(d)):
    print(" ", f)
EOF

echo "=== ALL CHECKS PASSED ==="
