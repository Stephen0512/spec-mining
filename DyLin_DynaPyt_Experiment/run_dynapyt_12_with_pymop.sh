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

# Set the temporary directory to /tmp
TMPDIR=/tmp
echo "TMPDIR: $TMPDIR"

# Define the fixed repository URL for the DynaPyt project
DYNAPYT_REPO_URL="https://github.com/sola-st/DynaPyt.git"

# Extract the repository name from the URL
TESTING_REPO_NAME=$(basename -s .git "$TESTING_REPO_URL")

# Extract the developer ID from the URL
DEVELOPER_ID=$(echo "$TESTING_REPO_URL" | sed -E 's|https://github.com/([^/]+)/.*|\1|')

# Create combined name with developer ID and repo name
CLONE_DIR="${DEVELOPER_ID}-${TESTING_REPO_NAME}_DynaPyt_12_with_pymop"

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

# Create a virtual environment using Python's built-in venv
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Navigate to the testing project directory
cd "$TESTING_REPO_NAME" || { echo "Failed to enter directory $TESTING_REPO_NAME"; exit 1; }

# Special handling for some repositories
if [ "${DEVELOPER_ID}-${TESTING_REPO_NAME}_${target_sha}" == "alstr-todo-to-issue-action_165cd5e" ]; then
    sed -i '' \
        -e '/^ruamel\.yaml\.clib==0\.2\.6$/d' \
        -e 's/^ruamel\.yaml==0\.17\.17$/ruamel.yaml==0.18.6/' \
        requirements.txt
fi

if [ "${DEVELOPER_ID}-${TESTING_REPO_NAME}_${target_sha}" == "davidhalter-jedi_86c3a02c8cd6c0245cd8e86adf3979692dc9cab9" ]; then
    git submodule update --init --recursive
fi

if [ "${DEVELOPER_ID}-${TESTING_REPO_NAME}_${target_sha}" == "Telefonica-HomePWN_0803981" ]; then
    sed -i '87 s/^/# /; 92 s/^/# /; 97 s/^/# /' tests/test_utils.py
fi

# Install numpy
pip install numpy==2.3.5

# Install dependencies from all requirement files if they exist
for file in *.txt; do
    if [ -f "$file" ]; then
        pip install -r "$file"
    fi
done

# Install missing dependencies from the requirements directory if exists
# pushd ../../requirements &> /dev/null
# ls
# echo "PWD: $PWD"
# echo "${DEVELOPER_ID}-${TESTING_REPO_NAME}_${target_sha}"
# popd &> /dev/null
if [ -f "$PWD/../../requirements/${DEVELOPER_ID}-${TESTING_REPO_NAME}_${target_sha}/requirements.txt" ]; then
    pip install -r "$PWD/../../requirements/${DEVELOPER_ID}-${TESTING_REPO_NAME}_${target_sha}/requirements.txt"
fi

# Install the package with test dependencies using custom install script if available
if [ -f myInstall.sh ]; then
    bash ./myInstall.sh
else
    pip install .[dev,test,tests,testing]
fi

# Install required Python packages
pip install pytest
pip install pandas
pip install tensorflow

if [ -f "$PWD/../../requirements/${DEVELOPER_ID}-${TESTING_REPO_NAME}_${target_sha}/pytest.ini" ]; then
    cp "$PWD/../../requirements/${DEVELOPER_ID}-${TESTING_REPO_NAME}_${target_sha}/pytest.ini" .
fi

# ------------------------------------------------------------------------------------------------
# Install DynaPyt
# ------------------------------------------------------------------------------------------------

# Return to the parent directory
cd ..

# Clone the DynaPyt repository into the current directory
git clone "$DYNAPYT_REPO_URL" || { echo "Failed to clone $DYNAPYT_REPO_URL"; exit 1; }

# Specify the source directory containing the Python DynaPyt files
SOURCE_DIR="$PWD/../Specs_with_PyMOP/DynaPyt"

# Define the destination directory in the cloned DynaPyt repository
DESTINATION_DIR="$PWD/DynaPyt/src/dynapyt/analyses"

# Check if the source directory exists before attempting to copy files
if [ -d "$SOURCE_DIR" ]; then
    # Copy all Python files from the source directory to the destination
    cp "$SOURCE_DIR"/*.py "$DESTINATION_DIR"
else
    echo "Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# Navigate into the cloned DynaPyt repository
cd DynaPyt

# Install the required dependencies for DynaPyt and the package itself
pip install -r requirements.txt
pip install .

# Navigate back to the root project directory
cd ..

# Generate a unique session ID for the DynaPyt run (in order to run multiple analyses in one run)
export DYNAPYT_SESSION_ID=$(uuidgen)
echo "DynaPyt Session ID: $DYNAPYT_SESSION_ID"

# Copy the analyses file to temp directory with session ID
cp "$PWD/../Specs_with_PyMOP/dynapyt_analyses.txt" "$TMPDIR/dynapyt_analyses-$DYNAPYT_SESSION_ID.txt"

# Display contents of the copied file
cat "$TMPDIR/dynapyt_analyses-$DYNAPYT_SESSION_ID.txt"

# ------------------------------------------------------------------------------------------------
# Run the Instrumentation
# ------------------------------------------------------------------------------------------------

# Navigate to the testing project directory
cd "$TESTING_REPO_NAME"

# Record the start time of the instrumentation process
START_TIME=$(python3 -c 'import time; print(time.time())')

# Run DynaPyt instrumentation for analysis
python3 -m dynapyt.run_instrumentation --dir . --analysis dynapyt.analyses.Basic_Instrumentation.Basic_Instrumentation

# Record the end time and calculate the instrumentation duration
END_TIME=$(python3 -c 'import time; print(time.time())')
INSTRUMENTATION_TIME=$(python3 -c "print($END_TIME - $START_TIME)")

# ------------------------------------------------------------------------------------------------
# Run the tests
# ------------------------------------------------------------------------------------------------

# Record test start time
TEST_START_TIME=$(python3 -c 'import time; print(time.time())')

# Run tests with 1-hour timeout and save output
/usr/bin/time -v timeout -k 9 3400 pytest --continue-on-collection-errors &> ${TESTING_REPO_NAME}_Output.txt
exit_code=$?

# Process test results if no timeout occurred
if [ $exit_code -ne 124 ] && [ $exit_code -ne 137 ]; then
    # Calculate test duration
    TEST_END_TIME=$(python3 -c 'import time; print(time.time())')
    TEST_TIME=$(python3 -c "print($TEST_END_TIME - $TEST_START_TIME)")

    # Show test summary
    tail -n 3 ${TESTING_REPO_NAME}_Output.txt
else
    echo "Timeout occurred"
    TEST_TIME="Timeout"
fi

# Return to parent directory
cd ..

# Clean up virtual environment
deactivate
rm -rf venv

# Ensure results directory exists
mkdir -p $CLONE_DIR

# Save test results
RESULTS_FILE="${CLONE_DIR}/${TESTING_REPO_NAME}_results.txt"
echo "Instrumentation Start Time: ${START_TIME}" >> $RESULTS_FILE
echo "Instrumentation End Time: ${END_TIME}" >> $RESULTS_FILE
echo "Instrumentation Time: ${INSTRUMENTATION_TIME}s" >> $RESULTS_FILE

echo "Test Start Time: ${TEST_START_TIME}" >> $RESULTS_FILE
echo "Test End Time: ${TEST_END_TIME}" >> $RESULTS_FILE
echo "Test Time: ${TEST_TIME}s" >> $RESULTS_FILE

# Copy all the txt files in the TESTING_REPO_NAME directory that end with _statistics.txt to the $CLONE_DIR directory
find "${TESTING_REPO_NAME}" -name "*_statistics.txt" -exec cp {} $CLONE_DIR/ \;

# Copy the ${TESTING_REPO_NAME}_Output.txt file to the $CLONE_DIR directory
cp "${TESTING_REPO_NAME}/${TESTING_REPO_NAME}_Output.txt" $CLONE_DIR/

# Archive results
zip -r "${CLONE_DIR}.zip" $CLONE_DIR
mv "${CLONE_DIR}.zip" ..

# Return to main directory
cd ..

# Clean up project directory
rm -rf "$CLONE_DIR"