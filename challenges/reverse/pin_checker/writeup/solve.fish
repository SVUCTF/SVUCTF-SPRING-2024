#!/usr/bin/env fish

function check
    set pin $argv[1]
    set result (echo $pin | perf stat -x , -e instructions:u ../attachments/pin_checker 2>&1 >/dev/null)
    echo $result | cut -d ',' -f1
end

function find_len
    set pin ""
    set max_count 0
    set length 0

    for i in (seq 30)
        set pin $pin"0"
        set count (check $pin)
        if test -n "$count" -a "$count" -gt $max_count
            set max_count $count
            set length $i
        end
    end
    echo $length
end

function find_pin
    set length $argv[1]
    set pin ""

    for i in (seq $length)
        set char ""
        set max_count 0

        for code in (seq 0 9)
            set padded_pin (string pad -r -w $length -c '0' $pin$code)
            set count (check $padded_pin)

            if test -n "$count" -a "$count" -gt $max_count
                set max_count $count
                set char $code
            end
        end
        set pin $pin$char
    end
    echo $pin
end

set length (find_len)
set pin (find_pin $length)
echo "PIN: "$pin
