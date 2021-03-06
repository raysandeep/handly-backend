import json
import os

import boto3
from botocore.exceptions import NoCredentialsError
import requests
from django.conf import settings
from celery.task import task
from Algo.document_parser import main
from .models import OutputFiles, HandwritingInputLogger
from firebase_admin import messaging

s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET)


def upload_to_aws(local_file, bucket, s3_file):
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def sendNotif(notif, message, title):
    message = messaging.Message(
        data={
            'message': message,
        },
        notification=messaging.Notification(
            title=title,
            body=message,
        ),
        token=notif,
    )
    response = messaging.send(message)
    print('Successfully sent notification:', response)


# start after 1 sec
@task(name="process_flashdeals",serializer='json')
def output_file_proccessor(id, file_url, player_id):
    output_file_name = os.path.join(settings.MEDIA_ROOT, id + ".pdf")
    pic_loc = settings.PICKLE_LOC
    input_loc = os.path.join(settings.MEDIA_ROOT,file_url.split('/media/')[1])
    print(input_loc, pic_loc, output_file_name)
    status, resp = main(input_loc, output_file_name, pic_loc)
    print(resp)
    handwriter = HandwritingInputLogger.objects.filter(id=id)[0]
    handwriter.status = True
    name = handwriter.name
    if status:
        data = {
            'input_details': handwriter,
            'url': '/media/' + resp.split('/media/')[1]
        }
        output = OutputFiles(**data)
        uploaded = upload_to_aws(output_file_name, 'dsc-handly', id + ".pdf")
        print(uploaded)
        output.save()
        handwriter.save()
        output = OutputFiles.objects.filter(input_details__id=id)
        if player_id != '':
            sendNotif(player_id,name+" is ready!","Handwritten Document Ready!")
            print("done")
    else:
        handwriter.error_status = True
        handwriter.error_logger = resp
        handwriter.save()
        if player_id != '':
            sendNotif(player_id,name+" failed to processed as it contained some invalid characters or images. Please check and retry!","Handwritten Document Failed!")
        # send push
    
    print(status)

# @task(name="process_notif",serializer='json')
# def send_push(player_id, output, status, name):
#     if status:
#         header = {
#             "Content-Type": "application/json; charset=utf-8",
#             "Authorization": settings.ONE_SIGNAL_AUTH_KEY
#         }
#         payload = {"app_id": settings.ONE_SIGNAL_ID,
#                    "include_player_ids": [player_id],
#                    "headings": {"en": "Handwritten Document Ready!"},
#                    "contents": {"en": name+" is ready!"},
#                    "data": {"status": "Success", "payload": output}
#                    }
#         print(payload)
#         req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
#         print(req.status_code, req.json())
#     else:
#         header = {
#             "Content-Type": "application/json; charset=utf-8",
#             "Authorization": settings.ONE_SIGNAL_AUTH_KEY
#         }
#         payload = {"app_id": settings.ONE_SIGNAL_ID,
#                    "include_player_ids": [player_id],
#                     "headings": {"en": "Handwritten Document Failed!"},
#                     "contents": {"en": name+" failed to processed as it contained some invalid characters or images. Please check and retry!"},
                   
#                    "data": {"status": "Failed", "payload": output}
#                    }
#         print(payload)
#         req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
#         print(req.status_code, req.json())




