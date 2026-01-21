#!/bin/bash

# Check if exactly one repository URL and one status number areprovided, and exit if not
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <testing-repo-url> <status-number> <libraries-enabled>"
    exit 1
fi

# Assign the provided argument (repository URL) to a variable
repo_url_with_sha="$1"

# Split the input into link and sha
IFS=';' read -r TESTING_REPO_URL target_sha <<< "$repo_url_with_sha"

# Output the url
echo "Url: $TESTING_REPO_URL"
echo "Sha: $target_sha"

# Assign the provided argument (status number and libraries enabled) to a variable
status_number="$2"
libraries_enabled="$3"

echo "🚀 Running experiment for: $TESTING_REPO_URL - $target_sha"
echo "Status number: $status_number"
echo "Libraries enabled: $libraries_enabled"

# Combine URL and SHA with semicolon
url_with_sha="${TESTING_REPO_URL};${target_sha}"

# Define the scripts to run based on the status number and libraries enabled
if [ "$status_number" = "1" ]; then
    scripts=("run_dynapyt_8.sh" "run_pymop_8.sh" "run_dylin_8.sh" "run_pymop_libs_8.sh" "run_dynapyt_libs.sh")
elif [ "$status_number" = "2" ]; then
    scripts=("run_dynapyt_12.sh" "run_pymop_12.sh" "run_dylin_12.sh" "run_pymop_libs_12.sh")
elif [ "$status_number" = "3" ]; then
    scripts=("run_dynapyt_8_with_pymop.sh" "run_pymop_8_with_pymop.sh" "run_dylin_8_with_pymop.sh" "run_pymop_libs_8_with_pymop.sh" "run_dynapyt_libs_with_pymop.sh")
elif [ "$status_number" = "4" ]; then
    scripts=("run_dynapyt_12_with_pymop.sh" "run_pymop_12_with_pymop.sh" "run_dylin_12_with_pymop.sh" "run_pymop_libs_12_with_pymop.sh")
elif [ "$status_number" = "5" ]; then
    scripts=("run_dynapyt_8_with_pymop.sh" "run_pymop_8_with_pymop.sh" "run_dylin_8_with_pymop.sh" "run_dynapyt_12_with_pymop.sh" "run_pymop_12_with_pymop.sh" "run_dylin_12_with_pymop.sh" "run_pymop_libs_8_with_pymop.sh" "run_dynapyt_libs_with_pymop.sh")
elif [ "$status_number" = "6" ]; then
    scripts=("run_pymop_8_with_pymop.sh" "run_pymop_12_with_pymop.sh" "run_pymop_libs_8_with_pymop.sh")
else
    echo "Invalid status number: $status_number"
    exit 1
fi

# If libraries are disabled, limit to first three scripts only
if [ "$libraries_enabled" = "0" ]; then
    scripts=("${scripts[@]:0:3}")
fi

# Output the scripts to run
echo "Scripts: ${scripts[@]}"

# Run the original script
echo "🚀 Running run_original.sh on $TESTING_REPO_URL with SHA $target_sha..."
if timeout 1800 bash "run_original.sh" "$url_with_sha"; then
    echo "✅ Finished run_original.sh on $TESTING_REPO_URL"

    # Run pymop and dynapyt scripts sequentially
    for script in "${scripts[@]}"; do
        echo "🚀 Running $script on $TESTING_REPO_URL with SHA $target_sha..."
        if timeout 7200 bash "$script" "$url_with_sha"; then
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