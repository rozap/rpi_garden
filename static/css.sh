#!/bin/sh
LESS_DIRS="."
while inotifywait -e modify $LESS_DIRS; do
  lessc style.less > style.css
done

