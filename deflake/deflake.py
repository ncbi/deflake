from __future__ import print_function
import signal

"""
Classes and script for debugging a flaky program.

Type python deflake.py -h on the command-line to see usage.
"""

import subprocess
from multiprocessing import Pool


class _Printer(object):
    """ "Private" class for printing pass and error
    messages to screen."""
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def out(self, txt, color=None):
        out = getattr(self, color) + txt + self.ENDC if color is not None else txt
        print(out)


def _init_worker():
    """
    Makes worker processes ignore ctrl+c so Deflake.run can catch it
    see http://stackoverflow.com/a/1408476/725604
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def run_cmd(command, procnum, counter_token):
    """
    Worker process which executes the command to be deflaked
    Must be defined outside class to avoid pickling mess (seriously)
    :param command: command to be deflaked
    :type command: str
    :param procnum: process number to be used as a replacement for the counter_token
    :type procnum: int
    :param counter_token: counter_token to be replaced by the process number
    :type counter_token: str
    :return: PASS or FAIL message (FAIL message includes stderr)
    """
    cmd = command.replace(counter_token, str(procnum))
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    com = p.communicate()
    result = p.returncode
    if result == 0:
        return "PASS"
    else:
        res = "FAIL (run %s)\n" % procnum
        # Print error message if we have stderr
        try:
            res += com[1]
        except (TypeError, IndexError):
            pass
        return res


class Deflake(object):
    _printer = _Printer()
    _process_failed = False
    _loops = 0
    _processes_run = 0

    def __init__(self, command, max_runs=10, pool_size=1, counter_token='#count#', quiet=False):
        """
        :param command: The command to run
        :type command: str
        :param max_runs: The maximum runs to execute if command doesn't return non-zero exit status
        :type max_runs: int
        :param pool_size: The number of processes in each batch to multiprocess until max_runs is reached
        :type pool_size: int
        :param counter_token: A string token which will be replaced by the value of a counter which increments for
        every process started
        :type counter_token: string
        :param quiet: Quiet mode. No printing to stdout
        """

        self.command = command
        self.max_runs = max_runs
        self.pool_size = pool_size
        self.counter_token = counter_token
        self._processes = []
        self._quiet = quiet

        self.pool = Pool(processes=self.pool_size, initializer=_init_worker)

        # Collect output as data
        # so we can return from run()
        self._out = []

    def _output(self, outstr, quiet, process_passed=True):
        """ Wrapper for _Printer.out(). Outputs
        to stdout with proper color, and saves
        output to data structure in order to return
        data from run()"""
        if not quiet:
            color = "OKGREEN" if process_passed else "FAIL"
            self._printer.out(outstr, color)
        self._out.append(outstr)

    def check_result(self, result):
        if result == 'PASS':
            self._output(result, self._quiet)
        else:
            self._output(result, self._quiet, process_passed=False)
            self.pool.terminate()

    def run(self):
        """ Runs the deflaking.
        Method prints results to stdout and
        returns a list of output.
        """
        try:
            for i in range(self.max_runs):
                try:
                    self.pool.apply_async(run_cmd,
                                          args=(self.command, i + 1, self.counter_token),
                                          callback=self.check_result).get(9999999)
                except AssertionError:
                    break
            self.pool.close()
        except KeyboardInterrupt:
            print("\nYou cancelled the job!")
            self.pool.terminate()
        finally:
            self.pool.join()
        return self._out
