#!/usr/bin/env python

"""
Classes and script for debugging a flaky program.

Type python deflake.py -h on the command-line to see usage.
"""

import argparse
import inspect
import subprocess


class _Printer(object):
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def out(self, txt, color=None):
        out = getattr(self, color) + txt + self.ENDC if color is not None else txt
        print out


class Deflake(object):
    _printer = _Printer()
    _process_failed = False
    _loops = 0
    _processes_run = 0

    def __init__(self, command, max_runs=10, pool_size=1):
        """
        :param command: The command to run
        :type param: str
        :param max_runs: The maximum runs to execute if command doesn't return non-zero exit status
        :type max_runs: int
        :param pool_size: The number of processes in each batch to multiprocess until max_runs is reached
        """

        self.command = command
        self.max_runs = max_runs
        self.pool_size = pool_size
        self._processes = []

        # Collect output as data
        # so we can return from run()
        self._out = []

    def _output(self, str, process_passed=True):
        """ Wrapper for _Printer.out(). Outputs
        to stdout with proper color, and saves
        output to data structure in order to return
        data from run()"""
        color = "OKGREEN" if process_passed else "FAIL"
        self._printer.out(str, color)
        self._out.append(str)

    def _get_processes(self):
        ret = []
        groups = str(self.max_runs/self.pool_size)
        r = self.max_runs % self.pool_size
        if len(self._processes) >= self.max_runs/self.pool_size:
            for i in range(r):
                p = subprocess.Popen(self.command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                ret.append(p)
        else:
            for i in range(self.pool_size):
                p = subprocess.Popen(self.command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
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
                self._output("PASS")
            else:
                self._output("FAIL (run %s)" % str(self._loops * self.pool_size + i + 1), 
                    process_passed=False)
                # Print out stdout and stderr from process
                self._output("\n".join(com), process_passed=False)
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


if __name__ == "__main__":

    def get_default_args(func):
        """
        returns a dictionary of arg_name:default_values for the input function
        """
        args, varargs, keywords, defaults = inspect.getargspec(func)
        return dict(zip(args[-len(defaults):], defaults))

    def parse_args():
        default_args = get_default_args(Deflake.__init__)
        default_max_runs = default_args["max_runs"]
        default_pool_size = default_args["pool_size"]

        parser = argparse.ArgumentParser(
            description="Debug flaky programs by running them until they exit with a non-zero exit status. Eg:\n$ "
                        'python deflake.py "myprogram.py"')

        parser.add_argument("command", type=str, help="The command to de-flake")
        parser.add_argument("--max-runs", "-m", type=int, default=default_max_runs , help="Maximum runs before exiting"
                                                                                         ". Eg. setting "
                                                                          "to " \
                                                                        "" \
                                                                       "30 will "
                                                               "run the command 30 times or until a non-zero exit "
                                                               "status is returned. Default is %s" % default_max_runs)

        parser.add_argument("--pool-size", "-p", type=int, default=default_pool_size, help="The pool size to multi-process. Eg. set "
                                                                           "to " \
                                                                         "8 to "
                                                                "multiprocess batches of 8 processes at a time until "
                                                                "max_runs is reached. Default is %s." % default_pool_size)
        args = vars(parser.parse_args())
        return args


    args = parse_args()
    f = Deflake(args["command"], max_runs=args["max_runs"], pool_size=args["pool_size"])
    f.run()
