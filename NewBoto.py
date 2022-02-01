'''
Created on 9 de dez. de 2021

@author: Ricardo
'''
import s3 *
import yaml
import boto3
import pandas as pd

def leArquivo():
    s3 = boto3.resource('s3', aws_access_key_id='AKIA4OMF7P6TLKHZSAG4', aws_secret_access_key='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')
    bucket = s3.Bucket('datalake-pucminas')

    for obj in bucket.objects.filter(Prefix='json/vendas.json'):      
        file_content  = obj.get()['Body'].read().decode('utf-8')
        return file_content
        break

with open('s3.yaml', 'r') as fi:
    config = yaml.load(fi)

connection = s3.S3Connection(**config['s3'])
storage = s3.Storage(connection)

data = leArquivo()
dt = pd.read_json(data)
print(dt)

