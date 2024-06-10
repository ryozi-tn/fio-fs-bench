
#!/bin/bash
set -ue

# 変数設定
SCRIPT_HOME=$(cd "$(dirname "$0")" && pwd)
. $SCRIPT_HOME/settings.sh

INDEX=0

time while fallocate -l $FILE_SIZE "$FILE_PATH.$(printf "%08d" $INDEX)"; do
  echo -n "."
  INDEX=$((INDEX + 1))
done

echo CREATED $INDEX files.



