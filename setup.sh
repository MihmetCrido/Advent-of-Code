#!/bin/bash

echo "Starting setup for Advent of Code Puzzle Downloader..."

# Step 1: Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 before proceeding."
    exit 1
else
    echo "Python 3 is installed."
fi

# Step 2: Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Installing pip3..."
    sudo apt-get install python3-pip -y || {
        echo "Failed to install pip3. Please install it manually."
        exit 1
    }
else
    echo "pip3 is installed."
fi

# Step 3: Install required Python packages
echo "Installing required Python packages: requests, beautifulsoup4, html2text..."
pip3 install requests beautifulsoup4 html2text || {
    echo "Failed to install required packages. Please check your Python setup."
    exit 1
}

# Step 4: Prompt the user for the session token
SESSION_FILE="session.json"
echo "Please enter your Advent of Code session token (leave blank to skip):"
read -r session_token

# Check if the user provided a session token
if [ -n "$session_token" ]; then
    echo "Updating session.json with the provided session token..."
    # Create or update the session.json file with the new token
    echo "{
  \"session\": \"$session_token\"
}" > "$SESSION_FILE"
    echo "Session token saved to $SESSION_FILE."
else
    echo "No session token provided. Skipping session file update."
fi

echo "Setup complete! You can now run the Advent of Code downloader script using the command:"
echo "python3 advent_of_code.py <year> [--day <day>] [--session-file <session-file>] [--clean]"
