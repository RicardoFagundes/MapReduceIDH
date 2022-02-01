'''
Created on 21 de dez. de 2021

@author: Ricardo
'''
import boto3
import ssl
from Aluno import Aluno
import matplotlib.pyplot as plt
from AmazonS3 import AmazonS3



def leArquivoS3():
    s3 = boto3.resource('s3', aws_access_key_id='AKIA4OMF7P6TLKHZSAG4', aws_secret_access_key='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')
    bucket = s3.Bucket('datalake-pucminas')
    turma = []
    cont = 0

    for obj in bucket.objects.filter(Prefix='csv/alunos.csv'):
        for line in obj.get()['Body'].read().decode('utf-8').splitlines():
            dados = line.split(";")
            if(cont == 0):
                cont += 1
                continue;
            a = Aluno()
            a.matricula = dados[0]
            a.nomeAluno = dados[1]
            a.curso = dados[2]
            a.notaAv1 = float(dados[3])
            a.notaAv2 = float(dados[4])
            a.notaAv3 = float(dados[5])
            a.media = (a.notaAv1 + a.notaAv2 + a.notaAv3) / 3
            if(a.media > 6):
                a.situacao = " Aprovado"
            else:
                a.situacao = " Reprovado"
            turma.append(a)
    return turma

def gravaImagem(turma):

    dicionario = {}


    for dados in turma:

        dicionario[dados.nomeAluno] = round(float(dados.media), 2)

    cont = 0
    dicionarioPlot = {}


    for i in sorted(dicionario, key=dicionario.get, reverse=True):

        if(cont > 10):
            break;

        cont += 1

        dicionarioPlot[i] = dicionario[i]

    plt.barh(list(dicionarioPlot.keys()), dicionarioPlot.values())
    plt.gca().invert_yaxis()
    plt.savefig('teste.png', format='png')
    plt.show()
    plt.close()

    



ssl._create_default_https_context = ssl._create_unverified_context    

dados = leArquivoS3()

gravaImagem(dados)

AS3 = AmazonS3()

AS3.post_receipt_image('teste.png')