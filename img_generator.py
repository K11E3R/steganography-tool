from PIL import Image, ImageDraw

def generate_image(width, height, color, file_path):
    """Solid color image Generator """
    img = Image.new('RGB', (width, height), color)
    img.save(file_path)

def generate_test_images():
    """Image Generator """
    base_image_width, base_image_height = 200, 200
    hidden_image_width, hidden_image_height = 50, 50

    generate_image(base_image_width, base_image_height, 'blue', 'img/base_image.png')

    generate_image(hidden_image_width, hidden_image_height, 'red', 'img/hidden_image.png')
    hidden_img = Image.open('img/hidden_image.png')
    draw = ImageDraw.Draw(hidden_img)
    draw.rectangle([(10, 10), (40, 40)], outline='black', width=3)
    hidden_img.save('img/hidden_image.png')

    print("Test images generating...\nbase_image.png ✅\nhidden_image.png ✅\nboth generated in the 'img' directory")

if __name__ == '__main__':
    generate_test_images()
