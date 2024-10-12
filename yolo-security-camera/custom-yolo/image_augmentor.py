import os
import cv2
import random
import albumentations as A
from albumentations.pytorch import ToTensorV2

# Directories for original and augmented datasets
input_images_dir = 'squirrel_dataset/images/train'
input_labels_dir = 'squirrel_dataset/labels/train'
output_images_dir = 'squirrel_dataset/images/train'
output_labels_dir = 'squirrel_dataset/labels/train'

# Make sure output directories exist
os.makedirs(output_images_dir, exist_ok=True)
os.makedirs(output_labels_dir, exist_ok=True)

# Function to create a dynamic augmentation pipeline with adjustable crop sizes
def get_augmentation_pipeline(img_height, img_width):
    crop_height = min(450, img_height)  # Ensure the crop height is within the image height
    crop_width = min(450, img_width)  # Ensure the crop width is within the image width

    return A.Compose([
        A.HorizontalFlip(p=0.5),  # Flip horizontally with 50% probability
        A.Rotate(limit=30, p=0.5),  # Rotate within [-30, 30] degrees with 50% probability
        A.RandomCrop(width=crop_width, height=crop_height, p=0.5),  # Dynamically adjust the crop size
        A.GaussNoise(p=0.2),  # Add random noise to 20% of images
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels'], min_visibility=0.3))

# Function to read bounding boxes from a YOLO-format label file
def read_bboxes(label_path):
    bboxes = []
    class_labels = []
    with open(label_path, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split()
            class_id = int(parts[0])
            bbox = [float(p) for p in parts[1:]]
            bboxes.append(bbox)
            class_labels.append(class_id)
    return bboxes, class_labels

# Function to write bounding boxes to a YOLO-format label file
def write_bboxes(label_path, bboxes, class_labels):
    with open(label_path, 'w') as f:
        for bbox, class_id in zip(bboxes, class_labels):
            bbox_str = ' '.join([str(x) for x in bbox])
            f.write(f"{class_id} {bbox_str}\n")

# Function to augment images and adjust bounding boxes
def augment_images():
    for image_file in os.listdir(input_images_dir):
        if image_file.endswith('.jpg'):
            img_path = os.path.join(input_images_dir, image_file)
            label_path = os.path.join(input_labels_dir, image_file.replace('.jpg', '.txt'))

            # Load image and bounding boxes
            img = cv2.imread(img_path)
            img_height, img_width = img.shape[:2]  # Get image dimensions
            bboxes, class_labels = read_bboxes(label_path)

            # Apply augmentations dynamically based on image size
            transform = get_augmentation_pipeline(img_height, img_width)
            augmented = transform(image=img, bboxes=bboxes, class_labels=class_labels)

            # Save augmented image and updated bounding boxes
            aug_img_path = os.path.join(output_images_dir, 'aug_' + image_file)
            aug_label_path = os.path.join(output_labels_dir, 'aug_' + image_file.replace('.jpg', '.txt'))

            # Save augmented image
            cv2.imwrite(aug_img_path, augmented['image'])

            # Save adjusted bounding boxes
            write_bboxes(aug_label_path, augmented['bboxes'], augmented['class_labels'])

    print(f"Augmented images saved to {output_images_dir}")
    print(f"Augmented labels saved to {output_labels_dir}")

# Run the augmentation process
augment_images()