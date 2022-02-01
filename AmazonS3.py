'''
Created on 8 de dez de 2021

@author: Nelson
'''
import os
import base64
import random
import boto3
import ssl

class AmazonS3:
    bucket = None
    bucket_name = None
    aws_secret_access_key = None
    aws_access_key_id = None 
    region_name = None
    resource = None
    file_name = None
        
    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context    
        self.bucket = ""
        self.bucket_name = 'datalake-pucminas'
        self.aws_access_key_id = 'AKIA4OMF7P6TLKHZSAG4'
        self.aws_secret_access_key = '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'
        self.region_name = 'sa-east-1'
        self.resource = 's3'
        self.file_name = None
        
    def _connect_s3(self):
            try:    
                session = boto3.Session(
                    aws_access_key_id = self.aws_access_key_id,
                    aws_secret_access_key = self.aws_secret_access_key,
                    region_name = self.region_name
                )
                s3 = session.resource(self.resource)
                self.bucket = s3.Bucket(self.bucket_name)
            except Exception as e:
                print(e)
            #raise NotFound("Resource Amazon Bucket not found!\n{}".format(table_name, str(e)))
            
    def _convert_b64_to_image(self, image=None):
        with open(image, "rb") as imageFile:
            file = base64.b64encode(imageFile.read())
            print(file)
            ramdom_img_id  = random.randint(1, 999999999999)
        self.file_name  = "{}.png".format(ramdom_img_id)
        image_64_decode = base64.decodebytes(file)
        image_result = open(self.file_name, 'wb')
        image_result.write(image_64_decode)
        
        
    def _put_object_bucket(self, request_ticket_receipt_id=None,     amazon_path=None):
        path = os.path.dirname(os.path.realpath(__file__))
        full_path = os.path.join(path, self.file_name)
        if not amazon_path:
            amazon_path  = "imagens/"
            self.file_name = full_path[len(path)+1:]
            amazon_destiny = amazon_path + self.file_name
        try:
            with open(full_path, 'rb') as data:
                self.bucket.put_object(Key=amazon_destiny, Body=data)
        except Exception as e:
            print(e)
            #raise NotFound("Resource Amazon Bucket not found!\n{}".format(table_name, str(e)))
        os.remove(self.file_name)
        url = 'https://{}.s3.amazonaws.com/{}'.format(
            self.bucket_name, 
            amazon_destiny
        )
        print(url)
        return url
    
    
    def post_receipt_image(self, image=None):
        self._connect_s3()
        self._convert_b64_to_image(image)
        amazon_url = self._put_object_bucket()
        return amazon_url
    
   