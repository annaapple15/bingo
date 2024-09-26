"""
Sean Scully, 9-17-2024
Bingo Card Generator with image resizer and randomizer, output single pdf and jpg of the bingo grid
built with deepai.org/chat

Future expansion:
Generate multiple unique cards and image grids
Add Title above and instructions below the grid (as separate images?)
Two square cards per letter-sized paper

Standardize Image Size

We'll first create a Python function to standardize the size of the JPEG images. This code will resize images to a specific width and height (say 100x100 pixels).

```python
"""
from PIL import Image
import os

def standardize_images(image_folder, output_folder, size=(100, 100)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            img_path = os.path.join(image_folder, filename)
            img = Image.open(img_path)
            img = img.resize(size, Image.LANCZOS)  # Use LANCZOS for high-quality downsampling
            output_path = os.path.join(output_folder, filename)
            img.save(output_path)
            print(f"Saved standardized image to {output_path}")
#```
"""
**Breakdown**:
- Check if the output folder exists; if not, create it.
- Loop through all JPEG files in the input folder.
- Open each image, resize it to 100x100 pixels, and save it to the output folder.
"""

"""
Generate a Bingo Card

Next, we’ll write a function that generates bingo cards using randomly selected images. Each bingo card will have a 5x5 grid (25 images).

```python
"""
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_bingo_card(image_folder, output_pdf, output_jpeg, images_per_card=25):
    # List all images in the folder
    images = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg'))]
    
    # Randomly sample images for the bingo card
    selected_images = random.sample(images, images_per_card)
    
    # Create a new blank image for the bingo grid
    grid_image_size = (500, 500)  # Size for the final grid image
    grid_img = Image.new('RGB', grid_image_size, (255, 255, 255))  # White background
    x_offset = 0
    y_offset = 0

    for i in range(5):
        for j in range(5):
            img_filename = selected_images[i * 5 + j]
            img_path = os.path.join(image_folder, img_filename)
            img = Image.open(img_path)

            # Paste the image into the appropriate position in the grid
            grid_img.paste(img, (x_offset + j * 100, y_offset + i * 100))

    # Save the bingo grid image as JPEG
    grid_img.save(output_jpeg)
    print(f"Bingo grid image created: {output_jpeg}")

    # Create a PDF
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter
    
    # Draw grid and insert images
    x_offset = 50
    y_offset = height - 50 - 100  # Adjust vertical position to avoid cutting off

    for i in range(5):
        for j in range(5):
            img_filename = selected_images[i * 5 + j]
            img_path = os.path.join(image_folder, img_filename)
            c.drawImage(img_path, x_offset + j * 100, y_offset - i * 100, width=100, height=100)

    c.save()
    print(f"Bingo card created: {output_pdf}")
#```
"""
**Breakdown**:
- Create a list of images in the folder.
- Randomly select 25 images for the card.
- Set up a PDF and define the location of the bingo card grid.
- Loop through to place images in a 5x5 grid.
- Save the PDF.

"""
def main():
    image_folder = 'images'  # Your source folder
    standardized_folder = 'standardized_images'  # The output folder for standardized images
    output_pdf = 'bingo_card.pdf'  # The output PDF for the bingo card
    output_jpeg = 'bingo_grid.jpeg'  # Output JPEG for the bingo grid

    # Standardize images
    standardize_images(image_folder, standardized_folder)

    # Create bingo card with standardized images
    create_bingo_card(standardized_folder, output_pdf, output_jpeg)
"""
   # Generate multiple bingo cards
    for card_number in range(1, 6):  # Looping to create 5 cards
        output_pdf = f'bingo_card_{card_number}.pdf'  # Unique PDF filename
        output_jpeg = f'bingo_grid_{card_number}.jpeg'  # Unique JPEG filename

            # Create bingo card with standardized images
        create_bingo_card(standardized_folder, output_pdf, output_jpeg)
"""

if __name__ == "__main__":
    main()


