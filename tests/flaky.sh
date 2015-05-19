times_ran=$(cat .counter)
if [[ $times_ran -gt 5 ]]; then
    echo 0 > .counter
    exit 1 
fi
new_num=$((times_ran + 1))
echo $new_num > .counter
