import os
import xml.etree.ElementTree as ET

def convert_annotation(xml_file_path, classes_dict, image_width, image_height):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    labels = []

    for obj in root.findall('object'):
        class_name = obj.find('name').text
        if class_name not in classes_dict:
            continue  # Skip objects that are not in the class mapping

        class_id = classes_dict[class_name]
        bbox = obj.find('bndbox')
        xmin = float(bbox.find('xmin').text)
        ymin = float(bbox.find('ymin').text)
        xmax = float(bbox.find('xmax').text)
        ymax = float(bbox.find('ymax').text)

        # Calculate YOLOv5 format coordinates (normalized)
        x_center = (xmin + xmax) / 2.0 / image_width
        y_center = (ymin + ymax) / 2.0 / image_height
        box_width = (xmax - xmin) / image_width
        box_height = (ymax - ymin) / image_height

        # Append label in YOLOv5 format to the list
        labels.append(f"{class_id} {x_center} {y_center} {box_width} {box_height}")

    return labels

def main(annotations_dir, output_dir, classes_dict):
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over XML files in annotations directory
    for filename in os.listdir(annotations_dir):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(annotations_dir, filename)

            # Extract image width and height from XML
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            size = root.find('size')
            image_width = float(size.find('width').text)
            image_height = float(size.find('height').text)

            # Convert annotation to YOLOv5 format
            labels = convert_annotation(xml_file_path, classes_dict, image_width, image_height)

            # Write labels to output file
            output_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.txt')
            with open(output_file_path, 'w') as f:
                f.write('\n'.join(labels))

if __name__ == '__main__':
    # Define your class mapping (class_name: class_id)
    classes_dict = {
        'Guide_Sign': 0,
        'Regulatory_Sign': 1,
        'Warning_Sign': 2
    }

    # Path to annotations directory containing XML files
    annotations_dir = 'Test/Annotations'

    # Output directory for YOLOv5 format labels
    output_dir = '/home/akram/Documents/master/project/dataaset2/dataset/Test/labels'

    # Convert annotations to YOLOv5 labels format
    main(annotations_dir, output_dir, classes_dict)
