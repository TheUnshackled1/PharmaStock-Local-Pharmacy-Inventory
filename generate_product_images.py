
import os
import django
from PIL import Image, ImageDraw, ImageFont

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocktime.settings')
django.setup()

from inventory.models import Product
from django.core.files import File

def generate_product_images():
    # Ensure the output directory exists
    output_dir = os.path.join('static', 'images', 'products')
    os.makedirs(output_dir, exist_ok=True)

    # Use a truetype font if available, otherwise default
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    for product in Product.objects.all():
        # Create a simple image
        image = Image.new('RGB', (100, 100), color = 'gray')
        draw = ImageDraw.Draw(image)

        # Draw product name on the image
        text = product.name
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((100 - text_width) / 2, (100 - text_height) / 2)
        draw.text(position, text, fill='white', font=font)

        # Save the image to a file
        image_path = os.path.join(output_dir, f'{product.name.replace(" ", "_")}.png')
        image.save(image_path)

        # Update the product's image field
        with open(image_path, 'rb') as f:
            product.image.save(os.path.basename(image_path), File(f), save=True)

if __name__ == '__main__':
    generate_product_images()
