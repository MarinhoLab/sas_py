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

echo "=== Import + public API check ==="
python3 - <<'EOF'
import marinholab.sas.core as core
from marinholab.sas.core import Clock, Statistics, RobotDriver, ShutdownSignaler

ss = ShutdownSignaler()
assert ss.should_shutdown() is False
ss.shutdown()
assert ss.should_shutdown() is True

clock = Clock(0.001)
assert clock.get_desired_thread_sampling_time_sec() == 0.001
assert Clock.TimeType.Computational is not None

print("import + API OK")
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
