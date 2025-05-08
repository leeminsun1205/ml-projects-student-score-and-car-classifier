import os
import argparse

def reindex_images(directory, prefix, digits, extension):
    # Get the list of files in the directory
    files = sorted([f for f in os.listdir(directory) if f.endswith(extension)])
    
    # Loop through the files and rename them
    for index, filename in enumerate(files, start=1):
        old_path = os.path.join(directory, filename)
        new_filename = f"{prefix}{index:0{digits}d}.{extension}"  # Parameterized digits and extension
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)
    
    print("Reindexing complete!")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Reindex image files in a directory.")
    parser.add_argument("-d", "--directory", required=True, help="Directory containing the images.")
    parser.add_argument("-p", "--prefix", default="image", help="Prefix for the new filenames.")
    parser.add_argument("-n", "--digits", type=int, default=3, help="Number of digits in numbering (default: 3).")
    parser.add_argument("-e", "--extension", default="jpg", help="File extension to target (default: jpg).")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the function with the provided arguments
    reindex_images(args.directory, args.prefix, args.digits, args.extension)
