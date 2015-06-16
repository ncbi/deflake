#!/usr/bin/env python

import argparse
import inspect
import sys

from deflake import Deflake

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
    default_counter_token = default_args["counter_token"]

    parser = argparse.ArgumentParser(
        description="Debug flaky programs by running them until they exit with a non-zero exit status. Eg:\n$ "
                    'python deflake.py "myprogram.py"\nExits with 1 if any processes exit with non-zero exit code.')

    parser.add_argument("command", type=str, help="The command to de-flake")

    parser.add_argument("--counter-token", "-c", default=default_counter_token,
                        help="A string token which will be replaced by the value of a counter which increments for"
                             " every execution of the program.  Useful for getting programs to write to different"
                             " files if they produce an output file. Default is '%s'." % default_counter_token)

    parser.add_argument("--max-runs", "-m", type=int, default=default_max_runs,
                        help="Maximum runs before exiting. Eg. setting to 30 will run the command 30 times or until"
                        " a non-zero exit status is returned. Default is %s" % default_max_runs)

    parser.add_argument("--pool-size", "-p", type=int, default=default_pool_size,
                        help="The pool size to multi-process. Eg. set to 8 to multiprocess batches of 8 processes at"
                             " a time until max_runs is reached. Default is %s." % default_pool_size)

    parser.add_argument("--quiet", "-q",  dest="quiet", action='store_true',
                        help="When quiet mode is enabled, no output is sent to screen")

    args = vars(parser.parse_args())
    return args


def main():
    args = parse_args()
    f = Deflake(args["command"], 
        max_runs=args["max_runs"], 
        pool_size=args["pool_size"],
        counter_token=args["counter_token"],
        quiet=args["quiet"]
    )
    results = f.run()

    # 1 exit status if any processes "failed"
    a_fail = [r for r in results if "FAIL" in r]
    sys.exit(1) if len(a_fail) > 0 else sys.exit(0)
