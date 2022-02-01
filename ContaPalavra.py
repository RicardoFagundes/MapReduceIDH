'''
Created on 14 de dez. de 2021

@author: Ricardo
'''
import boto3
import matplotlib.pyplot as plt
from AmazonS3 import AmazonS3


def mapS3():
    s3 = boto3.resource('s3', aws_access_key_id='AKIA4OMF7P6TLKHZSAG4', aws_secret_access_key='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')
    bucket = s3.Bucket('datalake-pucminas')
    cont = 0
    nomes = []
    for obj in bucket.objects.filter(Prefix='csv/alunos.csv'):
        for line in obj.get()['Body'].read().decode('utf-8').splitlines():
            dados = line.split(";")
            if(cont == 0):
                cont += 1
                continue;
            nome = dados[1].split(" ")
            for i in range(len(nome)):
                if(nome[i] == " " or nome[i] == "" or nome[i] == "de" or nome[i] == "da" or nome[i] == "do"):
                    continue
                nomes.append(nome[i])
    nomes.sort(key=None, reverse=False)
    mapa = {}
    for nome in nomes:
        mapa[nome] = nomes.count(nome)
    return mapa


def reduceMapa(mapa):
    chave = ""
    valor = 0
    for nome in mapa:
        if(mapa[nome] > valor):
            chave = nome
            valor = mapa[nome]
    reduce = {}
    reduce[chave] = valor
    return reduce


def gravaImagem(mapa):

    mapaPlot = {}
    cont = 0
  
    for i in sorted(mapa, key=mapa.get, reverse=True):
        if(cont > 10):
            
            break;
        cont += 1
            
        mapaPlot[i] = mapa[i]
        
    plt.barh(list(mapaPlot.keys()), mapaPlot.values())
    plt.gca().invert_yaxis()
    plt.savefig('teste.png', format='png')
    plt.show()
    plt.close()


mapa = mapS3()
reduce = reduceMapa(mapa)
gravaImagem(mapa)
AS3 = AmazonS3()
AS3.post_receipt_image('teste.png')
