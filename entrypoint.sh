#!/bin/sh -l

poetry run python3 analyze.py

# Check if the user wants to commit changes
if [ "$COMMIT_CHANGES" = "true" ]; then
    git config --global user.name "github-actions[bot]"
    git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
    
    # Add an exception for the directory ownership issue
    git config --global --add safe.directory /repo

    # Set up GitHub token for authentication
    git config --global url."https://x-access-token:${GITHUB_TOKEN}@github.com".insteadOf "https://github.com"

    # Ensure the latest changes are fetched
    git -C /repo pull --rebase
    
    # Commit and push the changes
    git -C /repo add "$README_PATH"
    git -C /repo commit -m "Update Code Style Badge [skip ci]"
    git -C /repo push
fi
