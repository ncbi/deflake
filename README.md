# deflake

Helps debug a non determinate test (or any flakey program) by running it until it exits with a non-zero
exit code.

At the command-line, run `python deflake.py --help` for a list of options. Default maximum runs is
25. Default pool-size is 6. 

## Example Running as Script

```
# Defaults to running the program in 6 simultanous processes 
# up to 25 times until failure
$ python deflake.py "my_flakey_program arg1 arg2"

```

## Example as Python Class
In this case we try to deflake `ls`. This program
is pretty stable, so we don't expect a non-zero exit status.
We should see `PASS` 25 times (the default maximum runs) until deflake gives up.

```
>>> from deflake import DeFlake
>>> DeFlake
<class 'deflake.DeFlake'>
>>> DeFlake("ls")
<deflake.DeFlake object at 0x7fd1b40d7810>
>>> d =DeFlake("ls")
<deflake.DeFlake object at 0x7fd1b40d76d0>
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
