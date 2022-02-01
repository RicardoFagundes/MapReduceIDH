# -*- coding: latin-1 -*-

'''
Created on 7 de dez de 2021

@author: Nelson
'''
import sys
import boto3
import ssl
from Aluno import Aluno
import matplotlib.pyplot as plt
from AmazonS3 import AmazonS3
import pandas as pd
 
def leArquivoS3():
    s3 = boto3.resource('s3', aws_access_key_id='AKIA4OMF7P6TLKHZSAG4', aws_secret_access_key='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')
    bucket = s3.Bucket('datalake-pucminas')
    
    for obj in bucket.objects.filter(Prefix='csv/IBGE_Escolar.csv'):

        for line in obj.get()['Body'].read().decode('utf-8').splitlines():
            dados = line.split(";")

print(removerCaracteresEspeciais(dados[2]))


            
def removerCaracteresEspeciais(text) :
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')   
ssl._create_default_https_context = ssl._create_unverified_context    
leArquivoS3()