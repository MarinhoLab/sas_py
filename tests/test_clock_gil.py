"""Regression test: sleeping Clock methods must release the GIL."""
import threading
import time

from marinholab.sas.core import Clock


def _ticks_during(blocking_call):
    """Count how often a second Python thread runs while blocking_call executes."""
    ticks = 0
    stop = threading.Event()

    def ticker():
        nonlocal ticks
        while not stop.is_set():
            ticks += 1
            time.sleep(0.001)

    t = threading.Thread(target=ticker, daemon=True)
    t.start()
    time.sleep(0.005)
    start = ticks
    try:
        blocking_call()
        return ticks - start
    finally:
        stop.set()
        t.join()


def test_blocking_sleep_releases_gil():
    clock = Clock(0.01)
    clock.init()
    assert _ticks_during(lambda: clock.blocking_sleep_seconds(0.1)) > 3


def test_update_and_sleep_releases_gil():
    clock = Clock(0.1)
    clock.init()
    clock.update_and_sleep()
    assert _ticks_during(clock.update_and_sleep) > 3


def test_safe_sleep_releases_gil_and_honors_shutdown():
    from marinholab.sas.core import ShutdownSignaler

    clock = Clock(0.01)
    clock.init()
    signaler = ShutdownSignaler()
    assert _ticks_during(lambda: clock.safe_sleep_seconds(0.1, signaler)) > 3

    signaler.shutdown()
    start = time.monotonic()
    clock.safe_sleep_seconds(5.0, signaler)
    assert time.monotonic() - start < 0.5
