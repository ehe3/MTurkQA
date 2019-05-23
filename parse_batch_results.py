import argparse
import os
import csv  
import json

# csv_path: mturk csv output to parse
def parse_csv(csv_path):
    annotations = {}
    with open(csv_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            current_img, current_annotation, current_status = None, None, None
            for (k, v) in row.items():
                if k == 'Input.image_url': current_img = v
                if k == 'Answer.annotatedResult.polygons': current_annotation = v
                if k == 'AssignmentStatus': current_status = v
            if current_status == 'Submitted':
                annotations[current_img] = current_annotation
    
    return annotations

# fname: png file name
# annotation_data: annotation content from csv file in unprocessed json format
def build_json_string(fname, annotation_data):
    annotations_raw = json.loads(annotation_data) 
    annotations_processed = []
    for annotation in annotations_raw:
        annotation_vertices = []
        for v in annotation['vertices']:
            annotation_vertices.append([v['x'], v['y']])

        individual_annotation = {}
        individual_annotation['label'] = annotation['label']
        individual_annotation['line_color'] = None
        individual_annotation['fill_color'] = None
        individual_annotation['points'] = annotation_vertices
        individual_annotation['shape_type'] = 'polygon'
        annotations_processed.append(individual_annotation)
        
    data = {}
    data['version'] = '3.9.0'
    data['flags'] = {}
    data['shapes'] = annotations_processed
    data['lineColor'] = [0, 255, 0, 128]
    data['fillColor'] = [51, 153, 255, 64]
    data['imagePath'] = fname
    data['imageData'] = None
    data['imageHeight'] = 480
    data['imageWidth'] = 640
    return json.dumps(data)

# dst: output file name
# content: string to write out to file
def write_json_to_file(dst, content):
    if os.path.isfile(dst):
        os.remove(dst)
    f = open(dst, 'w+')
    f.write(content)
    f.close()

# fname: image file name
def get_json_fname(fname):
    return os.path.splitext(fname)[0] + '.json'
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv', help='csv file to parse', type=str)
    parser.add_argument('dst', help='destination folder for json outputs', type=str)
    args = parser.parse_args()

    annotations = parse_csv(args.csv)
    for fname, annotation_raw in annotations.items():
        annotation = build_json_string(fname, annotation_raw)
        write_json_to_file(os.path.join(args.dst, get_json_fname(fname)), annotation)

    
