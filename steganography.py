import argparse
import numpy as np
from PIL import Image
import itertools
import threading
import time
import sys

stop_spinner = False

def loading_spinner():
    """Display a loading spinner."""
    spinner = itertools.cycle(['-', '\\', '|', '/'])
    while not stop_spinner:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
        time.sleep(0.1)

def show_loading_spinner():
    """Start the loading spinner in a separate thread."""
    global stop_spinner
    stop_spinner = False
    spinner_thread = threading.Thread(target=loading_spinner, daemon=True)
    spinner_thread.start()
    return spinner_thread

def stop_loading_spinner(spinner_thread):
    """Stop the loading spinner."""
    global stop_spinner
    stop_spinner = True
    spinner_thread.join()
    sys.stdout.write('Done! ✅\n')
    sys.stdout.flush()

class Steganography:
    def _merge_rgb(self, rgb1, rgb2):
        """Merge two RGB tuples by combining their lower 4 bits."""
        return tuple((c1 & 0xF0) | (c2 >> 4) for c1, c2 in zip(rgb1, rgb2))

    def _unmerge_rgb(self, rgb):
        """Extract the hidden RGB value from a merged RGB tuple."""
        return tuple(((c & 0x0F) << 4) | ((c & 0xF0) >> 4) for c in rgb)

    def merge(self, image1, image2, output):
        """Merge image2 into image1 and save to output path."""
        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 must be smaller than or equal to Image 1 in both dimensions!')

        if image1.mode != 'RGB' or image2.mode != 'RGB':
            raise ValueError('Both images must be in RGB mode!')

        print("Merging images...")
        spinner_thread = show_loading_spinner()
        try:
            img1_array = np.array(image1)
            img2_array = np.array(image2)
            height, width = img2_array.shape[:2]
            merged_array = np.copy(img1_array)

            merged_array[:height, :width] = np.array([self._merge_rgb(tuple(c1), tuple(c2))
                                                     for c1, c2 in zip(img1_array[:height, :width], img2_array)])

            new_image = Image.fromarray(merged_array, mode='RGB')
            new_image.save(output)
        finally:
            stop_loading_spinner(spinner_thread)
            print(f"Image merged and saved as '{output}'")

    def unmerge(self, image, output):
        """Unmerge an image to extract the hidden image and save to output path."""
        if image.mode != 'RGB':
            raise ValueError('The image must be in RGB mode!')

        print("Extracting hidden image...")
        spinner_thread = show_loading_spinner()
        try:
            img_array = np.array(image)
            unmerged_array = np.array([self._unmerge_rgb(tuple(c))
                                       for c in img_array])

            new_image = Image.fromarray(unmerged_array, mode='RGB')
            new_image.save(output)
        finally:
            stop_loading_spinner(spinner_thread)
            print(f"Hidden image extracted and saved as '{output}'")

def main():
    """Main function to handle command-line arguments and execute steganography tasks."""
    parser = argparse.ArgumentParser(description='Steganography Tool')
    subparser = parser.add_subparsers(dest='command')

    merge = subparser.add_parser('merge', help='Merge one image into another')
    merge.add_argument('--image1', required=True, help='Path to the base image')
    merge.add_argument('--image2', required=True, help='Path to the image to be hidden')
    merge.add_argument('--output', required=True, help='Path to save the merged image')

    unmerge = subparser.add_parser('unmerge', help='Extract hidden image from a merged image')
    unmerge.add_argument('--image', required=True, help='Path to the merged image')
    unmerge.add_argument('--output', required=True, help='Path to save the extracted image')

    args = parser.parse_args()

    try:
        stego = Steganography()
        if args.command == 'merge':
            with Image.open(args.image1) as image1, Image.open(args.image2) as image2:
                stego.merge(image1, image2, args.output)
        elif args.command == 'unmerge':
            with Image.open(args.image) as image:
                stego.unmerge(image, args.output)
        else:
            parser.print_help()
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
