from flask import Flask, render_template, json, request, session
from flask import Response
from flask import send_file
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import tempfile, os




application = Flask(__name__)

# Constants for IBM COS values
COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "_bAzHuCAN1yPz4Rcg5CZY1Tbp0UOpshuMhpoNkIvJAa3" # eg "W00YiRnLW4a3fTjMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/oidc/token"
COS_RESOURCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/693fe8ead49b44b192004113d21b15c2:fce26086-5b77-42cc-b1aa-d388aa2853d7::" # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003abfb5d29761c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

ibm_boto3.set_stream_logger('')

# Create resource
cos = ibm_boto3.resource(service_name='s3',
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_RESOURCE_CRN,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)
bucket_name = 'gamification-cos-standard-tkq'

@application.route("/",methods = ['GET', 'POST'])
def get_bucket_contents():
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        print("in try",)
        files = cos.Bucket(bucket_name).objects.all()
        print("files :",files)
 
       
        for file in files:
           print("in for",)
           print("Item: {0} ({1} bytes).".format(file.key, file.size))
        item_id = '1002'
        f = item_id + '.jpg'
        #isr = cos.get_object(Bucket=bucket_name, Key=f)
        isr = cos.Object(bucket_name, f).get()
        imgjpg = isr['Body'].read()
        print("read")
        #response = make_response(imgjpg)
        response.headers['Content-Type'] = "image/jpg"
        return img, {'Content-Type': 'image/jpg'}
        #img = open(jpg, 'rb').read()
        #URL = "http://cosimg-ikea-d-o-d.gamification-d3c0cb24e2b77f6869027abe3de4bca3-0001.sng01.containers.appdomain.cloud"
        #response = requests.post(URL, data=img, headers=headers)
        #return send_file(jpg, mimetype='image/jpeg')       
        
        
        
                
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

if __name__ == "__main__":
    application.run()
    

# for bucket in cos.buckets.all():
#    print(bucket.name)

#print("gallery")

