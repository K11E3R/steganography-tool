# Steganography Tool

## Overview

This tool provides functionality to hide and extract images within other images using steganographic techniques. It uses Least Significant Bit (LSB) modification to embed and extract hidden images while maintaining the visual integrity of the carrier image.

## Features

- **Merge Images**: Embed one image into another.
- **Extract Hidden Image**: Retrieve a hidden image from a merged image.

## Installation

To get started with the Steganography Tool, you'll need Python and some libraries. Follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/K11E3R/steganography-tool.git
   cd steganography-tool
   ```

2. **Create a Virtual Environment (optional but recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   Use the provided `requirements.txt` to install the necessary Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

The tool is designed to be used from the command line. Below are instructions for each command.

#### Merging Images

To merge one image into another, use:

```bash
python steganography.py merge --image1 img/base_image.png --image2 img/image_to_hide.png --output path/to/output_image.png
```

- `--image1`: Path to the base image where the second image will be hidden.
- `--image2`: Path to the image to be hidden.
- `--output`: Path to save the merged image.

#### Extracting Hidden Image

To extract the hidden image from a merged image, use:

```bash
python steganography.py unmerge --image path/to/merged_image.png --output path/to/extracted_image.png
```

- `--image`: Path to the merged image from which the hidden image will be extracted.
- `--output`: Path to save the extracted image.

## Code Explanation

### Loading Spinner

A loading spinner is used to indicate progress during long operations.

- **`loading_spinner()`**: Runs a spinner in a loop to show activity.
- **`show_loading_spinner()`**: Starts the spinner in a separate thread.
- **`stop_loading_spinner(spinner_thread)`**: Stops the spinner and prints "Done!".

### Steganography Class

This class handles the embedding and extraction of images.

- **`_merge_rgb(self, rgb1, rgb2)`**: Combines two RGB color values by merging the lower 4 bits of `rgb2` with the higher 4 bits of `rgb1`.

  ```python
  def _merge_rgb(self, rgb1, rgb2):
      return tuple((c1 & 0xF0) | (c2 >> 4) for c1, c2 in zip(rgb1, rgb2))
  ```

- **`_unmerge_rgb(self, rgb)`**: Extracts the hidden color values from a merged RGB tuple.

  ```python
  def _unmerge_rgb(self, rgb):
      return tuple(((c & 0x0F) << 4) | ((c & 0xF0) >> 4) for c in rgb)
  ```

- **`merge(self, image1, image2, output)`**: Embeds `image2` into `image1` and saves the result.

  ```python
  def merge(self, image1, image2, output):
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
  ```

- **`unmerge(self, image, output)`**: Extracts the hidden image from `image` and saves it.

  ```python
  def unmerge(self, image, output):
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
  ```

### Main Function

The `main()` function handles command-line arguments and calls the appropriate steganography methods.

```python
def main():
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
```

## Technical Details

### Steganographic Technique

- **Merging Logic**: The tool hides an image (`image2`) within another image (`image1`) by combining their RGB values. Specifically, the lower 4 bits of `image2` are merged with the higher 4 bits of `image1`.

- **Unmerging Logic**: Extracts the hidden image by reversing the merging process, recovering the lower 4 bits from the combined RGB values.

### Capacity and Limits

- **Capacity**: The amount of data you can hide depends on the carrier image’s resolution and bit depth. For a 24-bit RGB image, each pixel can theoretically store up to 3 bits of hidden data per color channel.
  
- **Quality Considerations**: Hiding more data can reduce the quality of the carrier image. The hidden image's size and the amount of data being hidden affect the visual integrity of the carrier image.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. **Fork the Repository**: Create a copy of the repository under your GitHub account.
2. **Create a Feature Branch**: Create a new branch for your feature or bug fix.
3. **Make Your Changes**: Implement your changes and test thoroughly.
4. **Submit a Pull Request**: Push your changes to your fork and submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
