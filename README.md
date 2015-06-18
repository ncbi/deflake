# `deflake.py`

Helps debug a non determinate test (or any flaky program) by running it until it exits with a non-zero exit code.

`deflake` can be run on the command-line or imported as a module. See below for more details.
At the command-line, run `python deflake.py --help` for a list of options. Default maximum runs is
10. Default pool-size is 1. 

## Install

`$ pip install deflake`

## Example Running as Script
`deflake` will exit with `1` if *any* processes return  non-zero.

```
# up to 25 times until failure
$ deflake "my_flaky_program arg1 arg2"
PASS
PASS
PASS
FAIL (run 4)
$ echo $?
1
$
```

## Example as Python Class
In this case we use the Deflake class, trying to deflake `ls`. `ls`
is pretty stable, so we don't expect a non-zero exit status.
We should see `PASS` ten times (the default maximum runs) until deflake gives up.
When running as a class, the `run` method runs the processes, and returns a list
with the output from calling `run`.

```
>>> from deflake import Deflake
>>> d =Deflake("ls", quiet=True)
<deflake.Deflake object at 0x7fd1b40d76d0>
>>> results = d.run()
['PASS', 'PASS','PASS','PASS','PASS','PASS','PASS','PASS','PASS','PASS']
>>>
```

## Multiprocessing
Use the `pool-size` or `-p` option to run your program in concurrent pools of processes. The default is no multiprocessing
or a pool size of `1`. Setting a pool-size to > 1 can make your deflaking faster,
but it won't always work, depending on the program you are trying to deflake. If your program
writes to a file, for example, then multiple processes may try to write to that file simultanously and
render your deflaking, well, flaky. See below for a possible solution. 

If the program you're deflaking writes to predetermined files (for example a log file), and you want
to multiprocess using the `pool-size` option, deflake might report a failure due to multiple processes
trying to write to the same file. In this case you can use the special `#count` replacement token to change the name of the log
file each process writes to. If you need to change the default `#count` token to something else, use
the `--counter-token` or `-c` option. Whatever replacement token you use, it will be replaced
with the iterator used when looping through the processes. For example:

```
$ deflake --pool-size 4 'my_flaky_program --log-file log#count#.txt'
```

Let's say the program fails on the third run. It would output the following log files:

- log1.txt
- log2.txt
- log3.txt

## Developing
To work on this package:

1. Clone the repo.
1. `pip install -e .`
1. Test: `python tests/test.py`.
1. Fix/add stuff.
1. Test.
1. Increment version in `setup.py`
1. Submit pull request
1. Tag `$ git tag -a x.x.x -m "Description"`
1. `$ git push --tags`

To submit to pypi, make sure your .pypirc is set up:

```
[distutils]
index-servers =
    python-local-repo
    pypi

[pypi]
username:USERNAME
password:PASS
```

Also, increment the version in `setup.py`

Then:

```
python setup.py sdist upload -r pypi
```

## Known Issues
- Extra processes kicked off in Python3x
