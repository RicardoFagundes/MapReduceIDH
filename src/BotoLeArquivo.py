'''
Created on 9 de dez. de 2021

@author: Ricardo
'''

import boto3

def leArquivo():
    s3 = boto3.resource('s3', aws_access_key_id='AKIA4OMF7P6TLKHZSAG4', aws_secret_access_key='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')
    bucket = s3.Bucket('datalake-pucminas')

    for obj in bucket.objects.filter(Prefix='csv/aluno.csv'):      
        for line in obj.get()['Body'].read().decode('utf-8').splitlines():
     
            print (line)
leArquivo()