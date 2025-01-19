#!/bin/sh -l

# Activate Poetry's virtual environment
source /venv/bin/activate  # Ensure you activate the venv you created during the Docker build

# Ensure the directory for GitHub Actions output exists
mkdir -p $(dirname "$GITHUB_OUTPUT")
echo "$(python3 analyze.py)" >>"$GITHUB_OUTPUT"

# Check if the user wants to commit changes
if [ "$COMMIT_CHANGES" = "true" ]; then
    git config --global user.name "github-actions[bot]"
    git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
    
    # Add an exception for the directory ownership issue
    git config --global --add safe.directory /repo

    # Ensure the latest changes are fetched
    git -C /repo pull --rebase
    
    # Commit and push the changes
    git -C /repo add "$README_PATH"
    git -C /repo commit -m "Update StyleSpark Badge [skip ci]"
    git -C /repo push
fi

# Deactivate the virtual environment
deactivate
