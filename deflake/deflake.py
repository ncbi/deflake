from __future__ import print_function

"""
Classes and script for debugging a flaky program.

Type python deflake.py -h on the command-line to see usage.
"""

import subprocess


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


class Deflake(object):
    _printer = _Printer()
    _process_failed = False
    _loops = 0
    _processes_run = 0

    def __init__(self, command, max_runs=10, pool_size=1, counter_token='#count#', quiet=False):
        """
        :param command: The command to run
        :type param: str
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

        # Collect output as data
        # so we can return from run()
        self._out = []

    def _output(self, str, quiet, process_passed=True):
        """ Wrapper for _Printer.out(). Outputs
        to stdout with proper color, and saves
        output to data structure in order to return
        data from run()"""
        if not quiet:
            color = "OKGREEN" if process_passed else "FAIL"
            self._printer.out(str, color)
        self._out.append(str)

    def _get_processes(self):
        ret = []
        last_batch = self.max_runs % self.pool_size
        range_stop = last_batch if len(self._processes) >= self.max_runs/self.pool_size else self.pool_size
        for i in range(range_stop):
            cmd = self.command.replace(self.counter_token, str(self._processes_run + i + 1))
            p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            ret.append(p)
        self._processes_run += len(ret)

        # Keep track of the process pools so far since
        # this method is called by its parent method
        # recursively.
        self._processes.append(ret)
        return ret

    def _run_processes(self):
        for i, p in enumerate(self._get_processes()):
            com = p.communicate()
            result = p.returncode
            if result == 0:
                self._output("PASS", self._quiet)
            else:

                self._output("FAIL (run %s)" % (str(self._loops * self.pool_size + i + 1)), 
                    self._quiet,
                    process_passed=False)

                # Print error message if we have stderr
                try:
                    self._output(com[1], self._quiet, process_passed=False)
                except TypeError, IndexError: 
                    pass
                self._process_failed = True
                break

        self._loops = self._loops + 1
        if not self._process_failed and self._processes_run < self.max_runs:
            self._run_processes()
        return self._out

    def run(self):
        """ Runs the deflaking. 
        Method prints results to stdout and
        returns a list of output.
        """
        results = self._run_processes()

        # Take out trailing newlines from result list if necessary.
        ret = results[:-1] if results[-1] == "\n" else results 
        return ret 
