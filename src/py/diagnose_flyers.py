import os
import sys

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
BASE_FLYER_FOLDER = r"C:\Users\deeba\Website Content\images\ShortStoryFlyer"

print("=" * 70)
print("  Anjirai Literary Circle - Flyer Diagnostic Tool")
print("=" * 70)
print()

# Check base folder
if not os.path.exists(BASE_FLYER_FOLDER):
    print(f"[X] Base folder not found: {BASE_FLYER_FOLDER}")
    exit(1)

print(f"[OK] Base folder exists: {BASE_FLYER_FOLDER}")
print()

# List all items in base folder
print("Contents of base folder:")
items = os.listdir(BASE_FLYER_FOLDER)
for item in sorted(items):
    item_path = os.path.join(BASE_FLYER_FOLDER, item)
    if os.path.isdir(item_path):
        print(f"  [DIR] {item}/")
    else:
        print(f"  [FILE] {item}")

print()

# Check for year folders
year_folders = []
for item in items:
    item_path = os.path.join(BASE_FLYER_FOLDER, item)
    if os.path.isdir(item_path) and item.isdigit() and len(item) == 4:
        year_folders.append(item)

if year_folders:
    print(f"[OK] Found {len(year_folders)} year folder(s): {', '.join(sorted(year_folders))}")
    print()

    # Check contents of each year folder
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.JPG', '.JPEG', '.PNG', '.GIF', '.WEBP')

    for year in sorted(year_folders):
        year_path = os.path.join(BASE_FLYER_FOLDER, year)
        print(f"{year}/ folder contents:")

        year_items = os.listdir(year_path)
        image_files = [f for f in year_items if f.endswith(image_extensions)]
        other_files = [f for f in year_items if not f.endswith(image_extensions)]

        if image_files:
            print(f"  [OK] {len(image_files)} image file(s):")
            for img in sorted(image_files):
                file_path = os.path.join(year_path, img)
                size = os.path.getsize(file_path)
                size_kb = size / 1024
                print(f"    [IMG] {img:30s} ({size_kb:.1f} KB)")
        else:
            print(f"  [X] No image files found!")

        if other_files:
            print(f"  [WARNING] {len(other_files)} other file(s):")
            for f in sorted(other_files):
                print(f"    [FILE] {f}")

        print()
else:
    print("[X] No year folders found (folders named 2024, 2025, etc.)")
    print()
    print("[TIP] Expected structure:")
    print(f"   {BASE_FLYER_FOLDER}\\")
    print("   +-- 2024\\")
    print("   |   +-- 1.jpg")
    print("   |   +-- 2.jpg")
    print("   |   +-- ...")
    print("   +-- 2025\\")
    print("       +-- 1.jpg")
    print("       +-- ...")
    print()

    # Check for images in base folder
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.JPG', '.JPEG', '.PNG')
    image_files = [f for f in items if f.endswith(image_extensions)]

    if image_files:
        print(f"[WARNING] Found {len(image_files)} image(s) in base folder (not in year folders):")
        for img in sorted(image_files)[:10]:
            print(f"   [IMG] {img}")
        if len(image_files) > 10:
            print(f"   ... and {len(image_files) - 10} more")

print()
print("=" * 70)
print()
print("Next steps:")
print("1. Make sure images are in year folders (2024, 2025, etc.)")
print("2. Run: python generate_flyers.py")
print("3. Refresh your browser")
print()
