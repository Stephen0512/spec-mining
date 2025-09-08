#!/bin/bash

# Check if exactly one repository URL is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <testing-repo-url>"
    exit 1
fi

# Assign the provided repository URL with SHA to a variable
repo_url_with_sha="$1"

# Split the input into repository URL and SHA
IFS=';' read -r TESTING_REPO_URL target_sha <<< "$repo_url_with_sha"

# Output the URL and SHA
echo "Url: $TESTING_REPO_URL"
echo "Sha: $target_sha"

# Fixed repository URL for the mop-with-dynapt project
PYMOP_REPO_URL="https://$GH_ACCESS_TOKEN@github.com/SoftEngResearch/mop-with-dynapt.git"
# PYMOP_REPO_URL="git@github.com:SoftEngResearch/mop-with-dynapt.git"

# Extract the repository name from the URL
TESTING_REPO_NAME=$(basename -s .git "$TESTING_REPO_URL")

# Extract the developer ID from the URL
DEVELOPER_ID=$(echo "$TESTING_REPO_URL" | sed -E 's|https://github.com/([^/]+)/.*|\1|')

# Create combined name with developer ID and repo name
CLONE_DIR="${DEVELOPER_ID}-${TESTING_REPO_NAME}_PyMOP"

# Create the directory if it does not exist
mkdir -p "$CLONE_DIR"

# Navigate to the project directory
cd "$CLONE_DIR" || { echo "Failed to enter directory $CLONE_DIR"; exit 1; }

# ------------------------------------------------------------------------------------------------
# Install the testing repository
# ------------------------------------------------------------------------------------------------

# Clone the testing repository and checkout specific SHA if provided
if [ -n "$target_sha" ]; then
    git clone "$TESTING_REPO_URL" && cd "$(basename "$TESTING_REPO_URL" .git)" && git checkout "$target_sha" && cd .. || { echo "Failed to clone/checkout $TESTING_REPO_URL at $target_sha"; exit 1; }
else
    git clone "$TESTING_REPO_URL" || { echo "Failed to clone $TESTING_REPO_URL"; exit 1; }
fi

# Navigate to the testing project directory
cd "$TESTING_REPO_NAME" || { echo "Failed to enter directory $TESTING_REPO_NAME"; exit 1; }

# Create a virtual environment in the project directory using Python's built-in venv
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies from all requirement files if they exist
for file in *.txt; do
    if [ -f "$file" ]; then
        pip install -r "$file"
    fi
done

# Install the package with test dependencies using custom install script if available
if [ -f myInstall.sh ]; then
    bash ./myInstall.sh
else
    pip install .[dev,test,tests,testing]
fi

# Install required Python packages
pip install pytest
pip install numpy
pip install pandas

# ------------------------------------------------------------------------------------------------
# Install PyMOP
# ------------------------------------------------------------------------------------------------

# Return to the parent directory
cd ..

# Clone the mop-with-dynapt repository
git clone "$PYMOP_REPO_URL" || { echo "Failed to clone $PYMOP_REPO_URL"; exit 1; }

# Navigate to the mop-with-dynapt directory
cd mop-with-dynapt

# TODO: Currently using a temp version of PyMOP
git checkout fix-pymop-broken-2

# Install the project in editable mode with dev dependencies
pip install . || { echo "Failed to install mop-with-dynapt"; exit 1; }

# ------------------------------------------------------------------------------------------------
# Run the tests
# ------------------------------------------------------------------------------------------------

# Navigate back to the root project directory
cd ..

# Navigate into the testing repository
cd $TESTING_REPO_NAME

# Record the start time of the test execution
TEST_START_TIME=$(python3 -c 'import time; print(time.time())')

# Run tests with 1-hour timeout and save output
timeout -k 9 3000 bash -c 'PYMOP_SPEC_FOLDER="$PWD"/../../Specs/PyMOP PYMOP_ALGO=D PYMOP_STATISTICS=yes PYMOP_STATISTICS_FILE=D.json PYMOP_INSTRUMENTATION_STRATEGY=ast PYTHONPATH="$PWD"/../mop-with-dynapt/pythonmop/pymop-startup-helper/ pytest --continue-on-collection-errors' > ${TESTING_REPO_NAME}_Output.txt
exit_code=$?

# Process test results if no timeout occurred
if [ $exit_code -ne 124 ] && [ $exit_code -ne 137 ]; then
    # Record the end time and calculate the test execution duration
    TEST_END_TIME=$(python3 -c 'import time; print(time.time())')
    TEST_TIME=$(python3 -c "print($TEST_END_TIME - $TEST_START_TIME)")

    # Display the last few lines of the test output for quick status check
    tail -n 3 ${TESTING_REPO_NAME}_Output.txt
else
    echo "Timeout occurred"
    TEST_TIME="Timeout"
fi

# Clean up virtual environment
deactivate
rm -rf venv

# Return to parent directory
cd ..

# Ensure results directory exists
mkdir -p $CLONE_DIR

# Save test results
RESULTS_FILE="${CLONE_DIR}/${TESTING_REPO_NAME}_results.txt"
echo "Test Start Time: ${TEST_START_TIME}" >> $RESULTS_FILE
echo "Test End Time: ${TEST_END_TIME}" >> $RESULTS_FILE
echo "Test Time: ${TEST_TIME}s" >> $RESULTS_FILE

# Copy the necessary files to the $CLONE_DIR directory
cp "${TESTING_REPO_NAME}/${TESTING_REPO_NAME}_Output.txt" $CLONE_DIR/
cp $TESTING_REPO_NAME/D-full.json $CLONE_DIR/D-full.json
cp $TESTING_REPO_NAME/D-time.json $CLONE_DIR/D-time.json
cp $TESTING_REPO_NAME/D-violations.json $CLONE_DIR/D-violations.json

# Archive results
zip -r "${CLONE_DIR}.zip" $CLONE_DIR
mv "${CLONE_DIR}.zip" ..

# Return to main directory
cd ..

# Clean up project directory
rm -rf "$CLONE_DIR"
