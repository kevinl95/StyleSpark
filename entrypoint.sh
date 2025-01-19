#!/bin/sh -l

echo "$(python3 analyze.py)" >>"$GITHUB_OUTPUT"

exit 0
