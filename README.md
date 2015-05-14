# deflake

Helps debug a non determinate test (or any flakey program) by running it until it exits with a non-zero
exit code.

At the command-line, run `python deflake.py --help` for a list of options. Default maximum runs is
25. Default pool-size is 6. 

## Example

```
# Defaults to running the program in 6 simultanous processes 
# up to 25 times until failure
$ python deflake.py "my_flakey_program arg1 arg2"

