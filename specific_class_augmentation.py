import os
import random
from PIL import Image, ImageEnhance

# Define paths
dataset_path = "/path/to/your/dataset"
train_images_path = os.path.join(dataset_path, "train", "images")
train_labels_path = os.path.join(dataset_path, "train", "labels")
val_images_path = os.path.join(dataset_path, "valid", "images")
val_labels_path = os.path.join(dataset_path, "valid", "labels")

# Define augmentation parameters
num_augmentations = 10  # Number of augmented images per original image

# Define the class to augment
class_to_augment = 0

augmentations = [
    ImageEnhance.Brightness,
    ImageEnhance.Contrast,
    ImageEnhance.Sharpness,
    ImageEnhance.Color,
]

def augment_images_and_labels(images_path, labels_path):
  for filename in os.listdir(images_path):
    image_path = os.path.join(images_path, filename)
    label_path = os.path.join(labels_path, filename[:-4] + ".txt")

    # Check if label file exists
    if not os.path.exists(label_path):
      continue

    # Read label to determine class ID
    class_id = None
    with open(label_path, "r") as f:
      labels = f.readlines()
      if labels:
        class_id = int(labels[0].split()[0])  # Extract class ID from first line

    # Check if the image belongs to class 2 
    if class_id == class_to_augment:
      # Augment the image
      for idx in range(num_augmentations):
        # Load image and randomly choose an augmentation
        image = Image.open(image_path)
        augmentation = random.choice(augmentations)

        # Apply augmentation and save augmented image
        augmented_image = augmentation(image).enhance(random.uniform(0.5, 1.5))
        augmented_image_path = os.path.join(images_path, f"{filename[:-4]}_{idx}.png")
        augmented_image.save(augmented_image_path)

        # Create or update label file for augmented image
        augmented_label_path = os.path.join(labels_path, f"{filename[:-4]}_{idx}.txt")
        with open(augmented_label_path, "w") as f:
          # Write all five columns to the label file
          for line in labels:
            f.write(line)

        # Print progress
        print(f"Augmented image saved: {augmented_image_path}")
        print(f"Updated label file created: {augmented_label_path}")

augment_images_and_labels(train_images_path, train_labels_path)
augment_images_and_labels(val_images_path, val_labels_path)
