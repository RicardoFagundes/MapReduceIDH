'''
Created on 9 de dez. de 2021

@author: Ricardo
'''
from boto.s3.connection import S3Connection


conn = S3Connection('AKIA4OMF7P6TLKHZSAG4','djv5MB2l6D1dvbX0p81UHMWc0EgkcJxpCg6xojER')



bucket = conn.get_bucket('datalake-exemplo')



for key in bucket.list():



    print (key.name.encode('utf-8'))