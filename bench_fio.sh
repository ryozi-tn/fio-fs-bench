#!/bin/bash

# bench_fio.sh /mnt/dummy_file.00003000

set -ue

# 変数設定
SCRIPT_HOME=$(cd "$(dirname "$0")" && pwd)
. $SCRIPT_HOME/settings.sh

export FILE_NAME="$1"
export FILE_SIZE


LOG_DIR="$SCRIPT_HOME/logs/$(date +%Y%m%d-%H%M%S)-$(basename $FILE_NAME)"

mkdir -p "$LOG_DIR"


PID_LIST=()

function teardown(){
    kill "${PID_LIST[@]}"
}

trap teardown EXIT
atop -a 1 -w "$LOG_DIR/atop.log" &
PID_LIST+=($!)

sleep 3;
for FIO_IODEPTH in 1 4 8 16; do
    for FIO_RW in write read; do
        export FIO_RW FIO_IODEPTH
        REPORT_DIR="$LOG_DIR/iodepth=$FIO_IODEPTH/rw=$FIO_RW"
        mkdir -p "$REPORT_DIR"  

        fio "$SCRIPT_HOME/bench_fio.fio" | tee "$REPORT_DIR/fio.log"
        sleep 3;
    done
done
sleep 3;

