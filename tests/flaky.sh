#!/usr/bin/env bash

# A "flaky" program designed to fail
# every 7th time it's called. This
# is for test.py. This won't work
# for testing --pool-size multiprocessing.
times_ran=$(cat .counter)
if [[ $times_ran -gt 5 ]]; then
    echo 0 > .counter
    >&2 echo "forced error"
    exit 1 
fi
new_num=$((times_ran + 1))
echo $new_num > .counter
