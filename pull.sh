#!/bin/bash
# pull.sh - A script to pull and merge changes from the main branch of a GitHub repo

# Check for any local changes before pulling
echo "Checking for local changes..."
git status

# Stash local changes if any, to avoid conflicts
echo "Stashing any local changes..."
git stash

# Pull the latest changes from the origin main branch
echo "Pulling latest changes from origin/main..."
git pull origin main

# Check if there were any conflicts after pulling
if [ $? -ne 0 ]; then
    echo "Merge conflict detected! Resolving conflicts manually is required."

    # Show files with conflicts
    git status

    echo "Please edit the conflicted files to resolve conflicts."
    echo "Once resolved, use 'git add <file>' for each resolved file and 'git commit' to finalize the merge."
else
    echo "Pull successful, no conflicts!"
fi

# If there were local changes, apply the stash
if git stash list | grep -q "stash@{0}"; then
    echo "Reapplying local changes..."
    git stash pop

    # Check for conflicts with stashed changes
    if [ $? -ne 0 ]; then
        echo "Conflict detected with stashed changes. Resolve manually, then commit."
    else
        echo "Local changes reapplied successfully!"
    fi
fi

echo "Pull and merge process completed!"
