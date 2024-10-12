import os
import shutil
import random

# Directories
source_images_dir = 'annotated_images'  # Directory with all the images
source_labels_dir = 'annotated_images'  # Directory with corresponding labels

output_dir = 'squirrel_dataset'
train_images_dir = os.path.join(output_dir, 'images/train')
val_images_dir = os.path.join(output_dir, 'images/val')
train_labels_dir = os.path.join(output_dir, 'labels/train')
val_labels_dir = os.path.join(output_dir, 'labels/val')

# Fraction of data to be used for training (e.g., 0.8 for 85% training, 15% validation)
train_fraction = 0.80

# Create the output directories if they don't exist
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# Get list of all images and their corresponding label files
images = [f for f in os.listdir(source_images_dir) if f.endswith('.jpg')]
labels = [f.replace('.jpg', '.txt') for f in images]

# Shuffle images and split into training and validation sets
combined = list(zip(images, labels))
random.shuffle(combined)
split_index = int(len(combined) * train_fraction)

train_set = combined[:split_index]
val_set = combined[split_index:]

# Function to move files
def move_files(dataset, img_source_dir, label_source_dir, img_dest_dir, label_dest_dir):
    for image, label in dataset:
        shutil.copy(os.path.join(img_source_dir, image), os.path.join(img_dest_dir, image))
        shutil.copy(os.path.join(label_source_dir, label), os.path.join(label_dest_dir, label))

# Move training files
move_files(train_set, source_images_dir, source_labels_dir, train_images_dir, train_labels_dir)

# Move validation files
move_files(val_set, source_images_dir, source_labels_dir, val_images_dir, val_labels_dir)

print(f"Organized {len(train_set)} images into training and {len(val_set)} images into validation.")
