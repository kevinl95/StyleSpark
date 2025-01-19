#!/bin/sh -l

echo "$(python3 analyze.py)" >>"$GITHUB_OUTPUT"

# Check if the user wants to commit changes
if [ "$COMMIT_CHANGES" == "true" ]; then
  git config --global user.name "github-actions[bot]"
  git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
  
  # Ensure you fetch the latest changes to avoid conflicts
  git pull --rebase
  
  # Commit and push the changes
  git add README.md
  git commit -m "Update Code Style Badge [skip ci]"
  git push
fi
