from PIL import Image
import os

def optimize_image(image_path, quality=80):
    try:
        img = Image.open(image_path)
        img.save(image_path, optimize=True, quality=quality)
        print(f"Optimized {image_path}")
    except Exception as e:
        print(f"Error optimizing {image_path}: {e}")

def optimize_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                optimize_image(os.path.join(root, file))

if __name__ == "__main__":
    optimize_directory("Invernadero/media")
    optimize_directory("Invernadero/Windows/static/img")