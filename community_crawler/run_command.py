#!/usr/bin/python
# -*-coding:utf-8-*-
import os
import time
import signal
import platform
import subprocess


class MyTimeoutError(Exception):
    pass


def run_command(cmd, timeout=60):
    is_linux = platform.system() == 'Linux'

    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True,
                         preexec_fn=os.setsid if is_linux else None)
    t_beginning = time.time()
    seconds_passed = 0
    while True:
        if p.poll() is not None:
            break
        seconds_passed = time.time() - t_beginning
        if timeout and seconds_passed > timeout:
            if is_linux:
                os.killpg(p.pid, signal.SIGTERM)
            else:
                p.terminate()
            raise MyTimeoutError(cmd, timeout)
        time.sleep(0.1)
    return p.stdout.read()


def test():
    cmd = "dir"
    timeout = 10
    try:
        run_command(cmd, timeout)
    except MyTimeoutError:
        print("excute command=<%s> timeout after %i' % (cmd, timeout)")
    else:
        print("other error")


if __name__ == "__main__":
    test()