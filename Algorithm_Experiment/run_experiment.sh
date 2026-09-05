#!/bin/bash

# Check if exactly one repository URL and one status number areprovided, and exit if not
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <testing-repo-url>"
    exit 1
fi

# Assign the provided argument (repository URL) to a variable
repo_url_with_sha="$1"

# Split the input into link and sha
IFS=';' read -r TESTING_REPO_URL target_sha <<< "$repo_url_with_sha"

# Output the url
echo "Url: $TESTING_REPO_URL"
echo "Sha: $target_sha"

echo "🚀 Running experiment for: $TESTING_REPO_URL - $target_sha"

# Combine URL and SHA with semicolon
url_with_sha="${TESTING_REPO_URL};${target_sha}"

# Define the scripts to run
# scripts=("run_pymop_b.sh" "run_pymop_c.sh" "run_pymop_c+.sh" "run_pymop_d.sh")
scripts=("run_pymop_d.sh")

# Output the scripts to run
echo "Scripts: ${scripts[@]}"

# Run the original script
echo "🚀 Running run_original.sh on $TESTING_REPO_URL with SHA $target_sha..."
if timeout 1800 bash "run_original.sh" "$url_with_sha"; then
    echo "✅ Finished run_original.sh on $TESTING_REPO_URL"

    # Run pymop and dynapyt scripts sequentially
    for script in "${scripts[@]}"; do
        echo "🚀 Running $script on $TESTING_REPO_URL with SHA $target_sha..."
        if timeout 19500 bash "$script" "$url_with_sha"; then
            echo "✅ Finished $script on $TESTING_REPO_URL"
        else
            echo "❌ $script failed for $TESTING_REPO_URL. Continuing to the next script..."
        fi
    done
else
    echo "❌ run_original.sh failed, skipping remaining scripts for $TESTING_REPO_URL"
fi

echo "✅ Experiment completed for $TESTING_REPO_URL with SHA $target_sha!"
echo "------------------------------------------"


echo "🎉 All experiments completed!"