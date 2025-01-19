#!/bin/sh -l

# Activate the virtual environment
source /venv/bin/activate

# Run the analysis script and capture the output
result=$(python3 analyze.py)
echo "result=$result" >> "$GITHUB_OUTPUT"

# Check if the user wants to commit changes
if [ "$COMMIT_CHANGES" = "true" ]; then
    # Configure Git
    git config --global user.name "github-actions[bot]"
    git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"

    # Navigate to repository and ensure it's initialized
    cd /repo || exit
    git pull --rebase

    # Commit and push the changes
    git add "${README_PATH}"
    git commit -m "Update StyleSpark Badge [skip ci]"
    git push
fi

# Deactivate the virtual environment
deactivate