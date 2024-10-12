import os
import io
from google.cloud import vision
from PIL import Image, ImageDraw
from PIL import UnidentifiedImageError

# Set up Google Cloud Vision client with your credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_keys/caramel-feat-438322-m5-2200b6337d86.json'

client = vision.ImageAnnotatorClient()

# Function to detect objects and draw bounding boxes
def detect_objects(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Perform object detection using Google Cloud Vision API
    response = client.object_localization(image=image)
    localized_objects = response.localized_object_annotations

    print(f"Found {len(localized_objects)} objects in {image_path}")

    return localized_objects

# Function to draw bounding boxes on images and return squirrel boxes in YOLO format
def process_image(image_path, output_dir):
    try:


        localized_objects = detect_objects(image_path)

        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # Check and convert image mode if it's RGBA (or any mode other than RGB)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        image_width, image_height = image.size
        yolo_annotations = []

        for obj in localized_objects:
            if obj.name.lower() == 'squirrel':  # Change this to match detected class names
                vertices = [(vertex.x * image_width, vertex.y * image_height) for vertex in obj.bounding_poly.normalized_vertices]
                draw.line(vertices + [vertices[0]], width=5, fill='#00FF00')  # Draw bounding box on the image

                # Convert bounding box to YOLO format: class_index x_center y_center width height
                x_min = min(v[0] for v in vertices)
                x_max = max(v[0] for v in vertices)
                y_min = min(v[1] for v in vertices)
                y_max = max(v[1] for v in vertices)

                x_center = (x_min + x_max) / 2 / image_width
                y_center = (y_min + y_max) / 2 / image_height
                box_width = (x_max - x_min) / image_width
                box_height = (y_max - y_min) / image_height

                yolo_annotations.append(f"0 {x_center} {y_center} {box_width} {box_height}\n")

        # Save the annotated image
        image.save(os.path.join(output_dir, os.path.basename(image_path)))

        # Save YOLO annotations to a .txt file (same name as image)
        annotation_path = os.path.join(output_dir, os.path.basename(image_path).replace('.jpg', '.txt'))
        with open(annotation_path, 'w') as f:
            f.writelines(yolo_annotations)

        return yolo_annotations
    
    except UnidentifiedImageError:
        print(f"Skipping invalid image: {image_path}")
    except Exception as e:
        print(f"An error occurred while processing {image_path}: {e}")

# Example usage to process all images in a directory
def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for image_file in os.listdir(input_dir):
        if image_file.endswith('.jpg'):
            image_path = os.path.join(input_dir, image_file)
            print(f"Processing {image_path}")
            process_image(image_path, output_dir)

# Replace these paths with your directories
input_directory = 'squirrel_images'
output_directory = 'annotated_images'

# Process the images in the input directory
process_directory(input_directory, output_directory)
