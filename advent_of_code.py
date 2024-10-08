import argparse
import json
import os
import re
import shutil  # Added to support directory removal
import requests
from tqdm import tqdm  # Added for the progress bar
from bs4 import BeautifulSoup
import html2text

def load_session_from_file(file_path):
    """Load the session cookie from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get('session')
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to parse the JSON file '{file_path}'.")
        return None

def slugify(title):
    """Convert a title into a filename-friendly format."""
    # Remove non-alphanumeric characters, convert spaces to underscores, and make lowercase
    return re.sub(r'\W+', '_', title.strip().lower())

def download_advent_of_code_day(day, year, session_cookie, verbose=False):
    """Download the puzzle for a specific day and year, and save it as markdown."""
    url = f"https://adventofcode.com/{year}/day/{day}"
    cookies = {'session': session_cookie}
    response = requests.get(url, cookies=cookies)

    if response.status_code != 200:
        if verbose:
            print(f"Failed to retrieve the puzzle for day {day}, year {year}: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    puzzle_content = soup.find('article', class_='day-desc')

    if puzzle_content:
        # Extract the title of the puzzle to use as the filename
        title_element = soup.find('h2')
        if title_element:
            title_text = title_element.text.split(':', 1)[-1].strip()  # Extract the title part after ":"
            filename = slugify(title_text) + ".md"
        else:
            filename = f"AdventOfCode_{year}_Day{day}.md"  # Fallback filename if title is not found
        
        markdown = html2text.html2text(str(puzzle_content))
        
        # Create the directory structure for the year and day
        directory = os.path.join(str(year), str(day))
        os.makedirs(directory, exist_ok=True)  # Create directories if they don't exist

        # Define the file path for the markdown file
        file_path = os.path.join(directory, filename)
        
        # Save the markdown to the specified file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(markdown)
        if verbose:
            print(f"Puzzle for day {day}, year {year} saved as markdown at '{file_path}'.")
    else:
        if verbose:
            print(f"Could not find the puzzle content for day {day}, year {year}.")

def clean_directories():
    """Remove all year folders and subfolders related to Advent of Code puzzles with confirmation."""
    print("WARNING: This operation will permanently delete all year folders and their subfolders in the current directory.")
    confirm = input("Are you sure you want to proceed? (y/n): ").lower()

    if confirm == 'y':
        for item in os.listdir('.'):
            if os.path.isdir(item) and item.isdigit():  # Check if the folder name is a number (representing a year)
                try:
                    shutil.rmtree(item)
                    print(f"Deleted folder '{item}' and its subfolders.")
                except Exception as e:
                    print(f"Failed to delete folder '{item}': {e}")
        print("Cleanup completed.")
    else:
        print("Cleanup operation cancelled.")

def main():
    # Setup command-line argument parsing
    parser = argparse.ArgumentParser(description="Download Advent of Code puzzle as markdown.")
    parser.add_argument('year', type=int, nargs='?', help='The year of the Advent of Code puzzles')
    parser.add_argument('--day', type=int, help='The day of the puzzle (if not specified, downloads all days)')
    parser.add_argument('--session-file', default='session.json', help='Path to the JSON file with the session cookie (default: session.json)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output for detailed logs')
    parser.add_argument('--clean', action='store_true', help='Remove all year folders and subfolders in the current directory')

    args = parser.parse_args()

    # Check if the clean command is given
    if args.clean:
        clean_directories()
        return

    # Load the session cookie from the specified file
    session_cookie = load_session_from_file(args.session_file)
    if not session_cookie:
        print("Error: Could not load the session cookie. Please check the JSON file.")
        return

    # Check if the year is specified; if not, inform the user and exit
    if not args.year:
        print("Error: Year is required unless --clean is specified.")
        return

    # Check if the day is specified; if not, download all days for that year
    if args.day:
        download_advent_of_code_day(day=args.day, year=args.year, session_cookie=session_cookie, verbose=args.verbose)
    else:
        # Use tqdm to show a progress bar while downloading all days
        for day in tqdm(range(1, 26), desc=f"Downloading puzzles for {args.year}", unit="day"):
            download_advent_of_code_day(day=day, year=args.year, session_cookie=session_cookie, verbose=args.verbose)

if __name__ == '__main__':
    main()
