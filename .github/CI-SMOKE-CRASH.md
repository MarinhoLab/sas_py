# `Build and Publish`: x86_64 Smoke test segfaults, PyPI is frozen

`publish` needs every `build` leg, and since 2026-10-21 every `ubuntu-latest` (x86_64) leg dies in
the **Smoke test** step with `Process completed with exit code 139` (SIGSEGV) and no trace. The
Linux arms are pinned to `ubuntu-24.04` and pass, so the crash looks x86_64-specific; `ubuntu-latest`
began migrating to Ubuntu 26.04 on 2026-10-19.

Consequence: PyPI is still at **26.9.15 (2026-10-02)**. The `marinholab.sas.core.gui` subpackage
(camera + touchscreen style sheets, `set_state`, logo — `66e22ca`..`79d4bdc`, 2026-10-21) is
therefore uninstallable from PyPI, which breaks `camera/cv_inference_gui.py` and
`sas_touchscreen_gui` on any machine that installs the distribution rather than the `sas-full`
image. Nothing in the Smoke test touched `gui`, so the gap was invisible.

Reproduced as passing (x86_64 under qemu, `dqrobotics 26.4.0a7`, `numpy 2.5.4`): the published
cp312/cp314 wheels on `ubuntu:24.04` and `ubuntu:26.04`; `main` built from source on 26.04 with
system CMake; `main` built CI-style with `python -m build --wheel` (pip CMake 4.x); the same wheel
after `auditwheel repair --plat auto` (auditwheel 6.8.2, bundles nothing); both import orders; and
`nm -D` shows `_core` exports no `dq::` symbols, ruling out interposition with dqrobotics' copy.

So the fault is only reachable on GitHub runners and needs a native backtrace: run the smoke script
under `-X faulthandler`, and on exit 134/139 re-run it under `gdb -batch -ex run -ex "thread apply
all bt"`. See the PR description for the proposed workflow.
