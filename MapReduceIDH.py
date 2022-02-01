'''
Created on 21 de dez. de 2021

@author: Ricardo
'''


import boto3
import ssl
from Aluno import Aluno
import matplotlib.pyplot as plt
from AmazonS3 import AmazonS3
from unicodedata import normalize
from IBGE_escolar import IBGE_escolar
 
def leArquivoS3():
    s3 = boto3.resource('s3', aws_access_key_id='AKIA4OMF7P6TLKHZSAG4', aws_secret_access_key='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')
    bucket = s3.Bucket('datalake-pucminas')
    listaIBGE = []
    cont = 0
    for obj in bucket.objects.filter(Prefix='csv/IBGE_Escolar.csv'): 
        for line in obj.get()['Body'].read().decode('utf-8').splitlines():
            if(cont == 0):
                cont += 1
                continue
            
            dados = line.split(";")
            ibge = IBGE_escolar()  
            ibge.codigo_ibge = dados[0]
            ibge.nome_regiao = dados[1]
            ibge.cidade = removerCaracteresEspeciais(dados[2])
            ibge.ensino_incompleto_amarela = int(dados[3])
            ibge.ensino_incompleto_branca = int(dados[4])
            ibge.ensino_incompleto_indigena = int(dados[5])
            ibge.ensino_incompleto_parda = int(dados[6])
            ibge.ensino_incompleto_preta = int(dados[7])
            ibge.ensino_completo_amarela = int(dados[8])
            ibge.ensino_completo_branca = int(dados[9])
            ibge.ensino_completo_indigena = int(dados[10])
            ibge.ensino_completo_parda = int(dados[11])
            ibge.ensino_completo_preta = int(dados[12])
            ibge.chave = ibge.codigo_ibge + "_" + ibge.cidade
            listaIBGE.append(ibge)
            
        return listaIBGE
    

def mapIBGE(listaIBGE, etinia):
    listaIBGE.sort(key=lambda ibge: ibge.chave)    
    mapa = {}
    for ibge in listaIBGE:
        # amarela
        if(etinia == 1): 
            mapa[ibge.chave] = ibge.ensino_incompleto_amarela
    
    return mapa


def reduceMapa(mapa):
    chave = ""
    valor = 0
    
    for microregiao in mapa:
        if(mapa[microregiao] > valor):
            chave = microregiao
            valor = mapa[microregiao]
            
    
    reduce = {}
    reduce[chave] = valor
    return reduce
            
def removerCaracteresEspeciais (text):
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

            
ssl._create_default_https_context = ssl._create_unverified_context    
dados = leArquivoS3()

mapa = mapIBGE(dados, 1)
print(reduceMapa(mapa))