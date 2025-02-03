import os
import sys
from themes.theme import Theme
from image_processing.fen_to_image import render_from_fen, render_from_fen_file
from image_processing.pgn_to_image import render_from_pgn_string, render_from_pgn_file, render_from_pgn_folder

def main_menu():
    theme = load_default_theme()
    while True:
        print("\n=== Chess Image Generator ===")
        print("1. Generate image from FEN string")
        print("2. Generate image from FEN file")
        print("3. Generate images from PGN string")
        print("4. Generate images from PGN file")
        print("5. Generate images from all PGN files in a folder")
        print("6. Change Theme")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            generate_from_fen_string(theme)
        elif choice == "2":
            generate_from_fen_file(theme)
        elif choice == "3":
            generate_from_pgn_string(theme)
        elif choice == "4":
            generate_from_pgn_file(theme)
        elif choice == "5":
            generate_from_pgn_folder(theme)
        elif choice == "6":
            theme = change_theme()
        elif choice == "7":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

def generate_from_fen_string(theme):
    fen = input("Enter the FEN string: ").strip()
    output_file = input("Enter the output file path (e.g., output): ").strip()

    try:
        render_from_fen(fen, theme, output_file)
        print(f"Image successfully generated and saved to {output_file}")
    except Exception as e:
        print(f"Error generating image: {e}")

def generate_from_fen_file(theme):
    fen_file = input("Enter the path to the FEN file: ").strip()
    output_file = input("Enter the output file path (e.g., output): ").strip()

    if not os.path.isfile(fen_file):
        print(f"File not found: {fen_file}")
        return
    try:
        render_from_fen_file(fen_file, theme, output_file)
        print(f"Image successfully generated and saved to {output_file}")
    except Exception as e:
        print(f"Error generating image: {e}")

def generate_from_pgn_string(theme):
    pgn_string = input("Enter the PGN string: ").strip()
    output_dir = input("Enter the output directory: ").strip()
    output_file = input("Enter the output filename: ").strip()
    final_position_only = input("Generate only the final position? (yes/no): ").strip().lower() == "yes"

    try:
        render_from_pgn_string(pgn_string, theme, output_dir, output_file, final_position_only)
        print(f"Images successfully generated and saved to {output_dir}")
    except Exception as e:
        print(f"Error generating images: {e}")

def generate_from_pgn_file(theme):
    pgn_file = input("Enter the path to the PGN file: ").strip()
    output_dir = input("Enter the output directory: ").strip()
    output_file = input("Enter the output filename: ").strip()
    final_position_only = input("Generate only the final position? (yes/no): ").strip().lower() == "yes"

    if not os.path.isfile(pgn_file):
        print(f"File not found: {pgn_file}")
        return

    try:
        render_from_pgn_file(pgn_file, theme, output_dir, output_file, final_position_only)
        print(f"Images successfully generated and saved to {output_dir}")
    except Exception as e:
        print(f"Error generating images: {e}")

def generate_from_pgn_folder(theme):
    folder_path = input("Enter the path to the folder containing PGN files: ").strip()
    output_dir = input("Enter the output directory: ").strip()
    final_position_only = input("Generate only the final position? (yes/no): ").strip().lower() == "yes"

    if not os.path.isdir(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    try:
        render_from_pgn_folder(folder_path, theme, output_dir, final_position_only)
        print(f"Images successfully generated and saved to {output_dir}")
    except Exception as e:
        print(f"Error generating images: {e}")

def load_default_theme():
    theme_file = "themes/assets/standard/config.json"  # Path to default theme JSON file
    try:
        return Theme.from_file(theme_file)
    except Exception as e:
        print(f"Error loading default theme: {e}")
        sys.exit(1)

def change_theme():
    theme_file = input("Enter the path to the new theme JSON file: ").strip()
    try:
        theme = Theme.from_file(theme_file)
        print(f"Theme successfully loaded: {theme}")
        return theme
    except Exception as e:
        print(f"Error loading theme: {e}")
        return load_default_theme()

if __name__ == "__main__":
    main_menu()
