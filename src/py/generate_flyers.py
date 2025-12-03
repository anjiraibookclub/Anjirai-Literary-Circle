import os
import json
from datetime import datetime
import re
import sys

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
BASE_FLYER_FOLDER = r"C:\Users\deeba\Website Content\images\ShortStoryFlyer"
HTML_FILE = r"C:\Users\deeba\Website Content\src\html\weeklyMeeting.html"

def natural_sort_key(filename):
    """Sort filenames naturally (1, 2, 3... 10, 11, not 1, 10, 11, 2)"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', filename)]

def extract_date_from_filename(filename):
    """Try to extract date from filename patterns like '2024-12-03.jpg' or '03-Dec-2024.jpg'"""
    # Pattern: YYYY-MM-DD
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if match:
        try:
            return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except:
            pass
    
    # Pattern: DD-Mon-YYYY or similar
    # Add more patterns as needed
    
    return None

def scan_flyers_by_year():
    """
    Scans the ShortStoryFlyer folder structure:
    - If subfolders named by year exist (2024, 2025, etc.), use those
    - Otherwise, organize all flyers in the main folder by current year
    """
    
    if not os.path.exists(BASE_FLYER_FOLDER):
        print(f"[X] Error: Folder not found: {BASE_FLYER_FOLDER}")
        return {}

    flyers_by_year = {}
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.JPG', '.JPEG', '.PNG')

    # Check if year-based subfolders exist
    year_folders = []
    for item in os.listdir(BASE_FLYER_FOLDER):
        item_path = os.path.join(BASE_FLYER_FOLDER, item)
        if os.path.isdir(item_path) and item.isdigit() and len(item) == 4:
            year_folders.append(item)

    if year_folders:
        # Use year-based folder structure
        print(f"[OK] Found year-based folders: {', '.join(sorted(year_folders))}")

        for year in year_folders:
            year_path = os.path.join(BASE_FLYER_FOLDER, year)
            flyer_files = []

            for filename in os.listdir(year_path):
                if filename.endswith(image_extensions):
                    flyer_files.append(filename)

            if flyer_files:
                flyer_files.sort(key=natural_sort_key)
                flyers_by_year[year] = process_flyers(flyer_files, year)
                print(f"  [DIR] {year}: {len(flyer_files)} flyers")
    else:
        # No year folders - use main folder and assign to current year
        print(f"[OK] No year folders found, scanning main folder...")
        current_year = str(datetime.now().year)

        flyer_files = []
        for filename in os.listdir(BASE_FLYER_FOLDER):
            if filename.endswith(image_extensions):
                flyer_files.append(filename)

        if flyer_files:
            flyer_files.sort(key=natural_sort_key)
            flyers_by_year[current_year] = process_flyers(flyer_files, current_year)
            print(f"  [DIR] {current_year}: {len(flyer_files)} flyers")
    
    return flyers_by_year

def process_flyers(flyer_files, year):
    """Process a list of flyer files into structured data"""
    from datetime import timedelta
    
    flyers = []
    
    for i, filename in enumerate(flyer_files):
        # Try to extract date from filename
        file_date = extract_date_from_filename(filename)
        
        if not file_date:
            # Generate a date (Saturdays in sequence)
            # Start from January of the year
            base_date = datetime(int(year), 1, 1)
            # Find first Saturday
            days_until_saturday = (5 - base_date.weekday()) % 7
            first_saturday = base_date + timedelta(days=days_until_saturday)
            # Add weeks for each subsequent flyer
            file_date = first_saturday + timedelta(weeks=i)
        
        # Extract number from filename if exists
        number_match = re.search(r'\d+', filename)
        session_num = number_match.group() if number_match else str(i+1)
        
        flyer = {
            'filename': filename,
            'title': f'Weekly Literary Meeting - Session {session_num}',
            'description': 'Tamil short story analysis and discussion',
            'date': file_date.strftime('%B %d, %Y')
        }
        flyers.append(flyer)
    
    return flyers

def generate_flyers_data():
    """
    Main function to scan folders and update HTML file
    """
    
    print("Scanning for flyers...")
    flyers_by_year = scan_flyers_by_year()
    
    if not flyers_by_year:
        print(f"[X] No flyers found in {BASE_FLYER_FOLDER}")
        print(f"\n[TIP] Organize your flyers in year folders:")
        print(f"   {BASE_FLYER_FOLDER}\\2024\\")
        print(f"   {BASE_FLYER_FOLDER}\\2025\\")
        return

    # Check if HTML file exists
    if not os.path.exists(HTML_FILE):
        print(f"[X] Error: HTML file not found: {HTML_FILE}")
        return
    
    # Read the HTML file
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create the JavaScript object with proper indentation
    js_lines = ['        const flyersByYear = {']
    
    years = sorted(flyers_by_year.keys())
    for year_idx, year in enumerate(years):
        flyers = flyers_by_year[year]
        js_lines.append(f'            "{year}": [')
        
        for i, flyer in enumerate(flyers):
            comma = ',' if i < len(flyers) - 1 else ''
            js_lines.append(f'                {{')
            js_lines.append(f'                    filename: {json.dumps(flyer["filename"])},')
            js_lines.append(f'                    title: {json.dumps(flyer["title"])},')
            js_lines.append(f'                    description: {json.dumps(flyer["description"])},')
            js_lines.append(f'                    date: {json.dumps(flyer["date"])}')
            js_lines.append(f'                }}{comma}')
        
        year_comma = ',' if year_idx < len(years) - 1 else ''
        js_lines.append(f'            ]{year_comma}')
    
    js_lines.append('        };')
    
    flyers_code = '\n'.join(js_lines)
    
    # Debug: Print what we're trying to inject
    print(f"\n[INFO] Generated JavaScript code ({len(js_lines)} lines):")
    print("First 10 lines:")
    for line in js_lines[:10]:
        print(line)

    # Find and replace the flyers data section - simpler pattern to match existing code
    pattern = r'(\s*const flyersByYear = \{)(.*?)(\};)'

    if not re.search(pattern, html_content, re.DOTALL):
        print("\n[X] Error: Could not find flyersByYear object in HTML file")
        print("Looking for: const flyersByYear = { ... };")

        # Try to find similar patterns
        if "flyersByYear" in html_content:
            print("\n[OK] Found 'flyersByYear' in file")
        else:
            print("\n[X] 'flyersByYear' not found in file")
        
        return
    
    replacement = f'\\1{flyers_code}\n        \\3'
    new_html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Check if pattern exists
    if re.search(pattern, html_content, re.DOTALL):
        new_html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
        
        # Verify the replacement worked
        if "flyersByYear" in new_html_content:
            # Write back to file
            with open(HTML_FILE, 'w', encoding='utf-8') as f:
                f.write(new_html_content)

            print(f"\n[OK] Successfully updated {HTML_FILE}")

            total_flyers = sum(len(flyers) for flyers in flyers_by_year.values())
            print(f"[OK] Total flyers injected: {total_flyers}")

            print(f"\nFlyers by Year:")
            for year in sorted(flyers_by_year.keys(), reverse=True):
                flyers = flyers_by_year[year]
                print(f"\n  {year} ({len(flyers)} sessions):")
                for i, flyer in enumerate(flyers, 1):
                    print(f"    {i:2d}. {flyer['filename']:25s} -> {flyer['date']}")

            print(f"\n[OK] Done! Open weeklyMeeting.html in your browser.")
            print(f"\nFolder Structure:")
            print(f"   {BASE_FLYER_FOLDER}\\")
            for year in sorted(flyers_by_year.keys()):
                print(f"   +-- {year}\\  ({len(flyers_by_year[year])} flyers)")
        else:
            print("\n[X] Error: Replacement didn't work as expected")

    else:
        print("\n[X] Error: Could not find the flyers data section in HTML file")
        print("Please make sure you're using the latest version of weeklyMeeting.html")

if __name__ == "__main__":
    print("=" * 70)
    print("  Anjirai Literary Circle - Weekly Meeting Flyers Generator")
    print("  (Year-Based Organization)")
    print("=" * 70)
    print()
    generate_flyers_data()
    print()
    print("=" * 70)
