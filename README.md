# Advent of Code Puzzle Downloader

This project is a Python script designed to download puzzles from the [Advent of Code](https://adventofcode.com/) website and save them as Markdown files. It organizes the files by year and day, creating a structured directory for easy access.

## Features
- Downloads puzzles as Markdown files directly from the Advent of Code website.
- Organizes files into folders by `{year}/{day}/`.
- Uses the puzzle title to generate descriptive filenames.
- Supports downloading all puzzles from a specific year at once.
- Utilizes a session cookie for authentication to access puzzle pages.

## Requirements
- **Python 3.6+**: Make sure you have Python installed on your system.
- **Python packages**: `requests`, `beautifulsoup4`, and `html2text` are required for the script to run.

### Installing the Required Packages
If you don't have the necessary packages, you can install them using the following commands:

`pip install requests beautifulsoup4 html2text`

## Setup Instructions

### Step 1: Obtain Your Session Cookie

To download the puzzles, you'll need to log into the Advent of Code website and get your session cookie. This is required for authentication.

1. Open your browser and log in to [Advent of Code](https://adventofcode.com/).
2. Open the browser's Developer Tools (usually by pressing `F12` or `Ctrl+Shift+I`).
3. Go to the **Application** or **Storage** tab.
4. Find the cookie named `session`.
5. Copy the value of the `session` cookie.

### Step 2: Create a JSON File for the Session Cookie

Create a JSON file named `session.json` in the root directory of this project with the following content:

```json
{
  "session": "your_session_cookie_here"
}
```
Replace `your_session_cookie_here` with the actual session value you copied from the browser.

## Usage Instructions

### Running the Script

To use the script, open your terminal and navigate to the directory where the script is located. Use the following command format:

```bash
python advent_of_code.py <year> [--day <day>] [--session-file <session-file>]
``` 

#### Example Commands

1. **Download a specific day's puzzle**:

    `python advent_of_code.py 2023 --day 5`    


    This will download the puzzle for day 5 of the year 2023 and save it in the path:

    `/2023/5/<puzzle-title>.md`
    
2. **Download all puzzles for a specific year**:
        
    `python advent_of_code.py 2023`

    This command will download all 25 puzzles for the year 2023 and organize them into folders by day.
    
3. **Use a custom session file**:

    `python advent_of_code.py 2023 --session-file my_session.json`

    This command uses a custom JSON file (`my_session.json`) to load the session cookie.

## File and Directory Structure

The downloaded puzzles will be organized into a directory structure like this:

```
/2023
   ├── 1
   │   └── sonar_sweep.md
   ├── 2
   │   └── dive.md
   ├── 3
   │   └── binary_diagnostic.md
   └── 25
       └── sea_cucumber.md
```

## Things to Keep in Mind

- **Session Cookie Expiration**: Your session cookie may expire after a certain period or when you log out. If the script stops working, update your session cookie in the JSON file.
  
- **Avoid Commiting Session**: To avoid commiting session file run a command like `git update-index --assume-unchanged session.json` to avoid committing your session token.

- **File Overwrite**: If a puzzle has already been downloaded, running the script again will overwrite the existing file with the same name.

- **Markdown Conversion**: The conversion of HTML to Markdown might not always be perfect, and you might need to make small formatting adjustments
