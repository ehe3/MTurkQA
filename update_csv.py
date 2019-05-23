import argparse
import os
import csv
import shutil
from tempfile import NamedTemporaryFile

# fname: image file name
def get_txt_fname(fname):
    return os.path.splitext(fname)[0] + '.txt'

parser = argparse.ArgumentParser()
parser.add_argument('src', help='directory to evaluate', type=str)
parser.add_argument('csv', help='csv file to update with results', type=str)
args = parser.parse_args()

files = []
for r, d, f in os.walk(args.src):
    for img in f:
        if '.png' in img and os.path.isfile(os.path.join(args.src, get_txt_fname(img))):
            files.append(img)
files = sorted(files)
print(len(files))

fields = ['HITId', 'HITTypeId', 'Title', 'Description', 'Keywords', 'Reward', 'CreationTime', 'MaxAssignments', 'RequesterAnnotation', 'AssignmentDurationInSeconds', 'AutoApprovalDelayInSeconds', 'Expiration', 'NumberOfSimilarHITs', 'LifetimeInSeconds', 'AssignmentId', 'WorkerId', 'AssignmentStatus', 'AcceptTime', 'SubmitTime', 'AutoApprovalTime', 'ApprovalTime', 'RejectionTime', 'RequesterFeedback', 'WorkTimeInSeconds', 'LifetimeApprovalRate', 'Last30DaysApprovalRate', 'Last7DaysApprovalRate', 'Input.image_url', 'Answer.annotatedResult.inputImageProperties.height', 'Answer.annotatedResult.inputImageProperties.width', 'Answer.annotatedResult.polygons', 'Approve', 'Reject']

temp_file = NamedTemporaryFile(mode='w', delete=False)
with open(args.csv, 'r') as csv_file, temp_file:
    reader = csv.DictReader(csv_file, fieldnames=fields)
    writer = csv.DictWriter(temp_file, fieldnames=fields, quoting=csv.QUOTE_ALL)
    for row in reader:
        current_file = row['Input.image_url']
        current_status = row['AssignmentStatus']
        # update latest
        if current_status == 'Submitted':
            if current_file in files:
                row['Approve'] = 'x'
            else:
                row['Reject'] = 'Please make polygon tighter around feet'
        writer.writerow(row)

shutil.move(temp_file.name, args.csv)




