# `deflake.py`

Helps debug a non determinate test (or any flaky program) by running it until it exits with a non-zero exit code.

`deflake` can be run on the command-line or imported as a module. See below for more details.
At the command-line, run `python deflake.py --help` for a list of options. Default maximum runs is
10. Default pool-size is 1. 

**Note**: Setting a pool-size to > 1 can make your deflaking faster,
but it won't always work, depending on the program you are trying to deflake. If your program
writes to a file, for example, then multiple processes may try to write to that file simultanously and
render your deflaking, well, flaky. 


## Example Running as Script
`deflake.py` will exit with `1` if *any* processes return  non-zero.

```
# Defaults to running the program in 6 simultanous processes 
# up to 25 times until failure
$ python deflake.py "my_flaky_program arg1 arg2"

```

## Example as Python Class
In this case we try to deflake `ls`. `ls`
is pretty stable, so we don't expect a non-zero exit status.
We should see `PASS` 25 times (the default maximum runs) until deflake gives up.
When running as a class, the `run` method runs the processes, and returns a list
with the output from calling `run`.

```
>>> from deflake import Deflake
>>> d =Deflake("ls")
<deflake.Deflake object at 0x7fd1b40d76d0>
>>> d.run()
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
PASS
```

## Developing
To work on this package:

1. Clone the repo.
1. Test: `python tests/test.py`.
1. Fix/add stuff.
1. Test.
