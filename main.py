import numpy as np
import sys
import os.path
import math

# Definir constantes
E = 21000 #kN/cm2
v = 0.30
fy = 12.0

#Inserindo Matricula
N = int(input("POR FAVOR, INSIRA O ÚLTIMO DIGITO DA SUA MATRÍCULA:  "))


nome = input('POR FAVOR, INSIRA O NOME DO ARQUIVO OU DIGITE SAIR PARA ENCERRAR:  ')

ArquivoExiste = True

while ArquivoExiste:
    # carregar o arquivo
    if os.path.isfile(nome+'.DAT'):
        sigma = np.loadtxt(nome+'.DAT')

        # Criando arquivo de saida
        saida=open(nome+'.OUT','w+')
        saida.write('         **** ROTINA COMPUTACIONAL – EXERCÍCIO  RESOLVIDO COM O PROGRAMA ****\n\n')

        saida.write("ÚLTIMO DIGITO MATRÍCULA:   ")
        saida.write(str(N))
        saida.write("\n\n")

        ArquivoExiste = False

        # soma os valores em posições ímpares
        for i in range(sigma.shape[0]):
            for j in range(sigma.shape[1]):
                if (i + j) % 2 == 0:
                    sigma[i, j] += N



        # a) Tensor de deformação
        epsilon = (1 / E) * ((1 - v) * sigma + v * np.trace(sigma) * np.identity(3))
        saida.write("Tensor de deformação:  ")
        saida.write("\n")
        saida.write(str(np.round(epsilon, 6)))
        saida.write("\n\n")

        #I1
        soma_diagonal = np.trace(sigma)
        saida.write("I1: ")
        saida.write(str(soma_diagonal))
        saida.write("\n")

        # I2
        termo1 = sigma[0, 0] * sigma[1, 1] - sigma[0, 1] ** 2
        termo2 = sigma[1, 1] * sigma[2, 2] - sigma[1, 2] ** 2
        termo3 = sigma[2, 2] * sigma[0, 0] - sigma[0, 2] ** 2
        resultado_i2 = termo1 + termo2 + termo3
        saida.write("I2: ")
        saida.write(str(resultado_i2))
        saida.write("\n")

        # I3
        det_sigma = np.linalg.det(sigma)
        saida.write("I3: ")
        saida.write(str(det_sigma))
        saida.write("\n\n")

        #Tensão Octa
        P = soma_diagonal/3
        saida.write("Tensão Octa: ")
        saida.write(str(P))
        saida.write("\n\n")

        # J2
        J_dois = ((1/3)*((pow(soma_diagonal,2))-(3*resultado_i2)))
        saida.write("J2: ")
        saida.write(str(J_dois))
        saida.write("\n")

        # J3
        J_tres = math.ceil(((1/27)*((2*(pow(soma_diagonal,3))-(9*(soma_diagonal*resultado_i2))+27*(det_sigma)))))
        saida.write("J3: ")
        saida.write(str(J_tres))
        saida.write("\n\n")

        # Cos
        cos = (((3*(math.sqrt(3)))/2)*(J_tres/(pow(J_dois, (3/2)))))
        saida.write("Cos: ")
        saida.write(str(cos))
        saida.write("\n")

        # Arcoseno
        arcoseno_radianos = math.acos(cos)
        arcoseno_graus = math.degrees(arcoseno_radianos)
        saida.write("Arcoseno: ")
        saida.write(str(arcoseno_graus))
        saida.write("\n")

        #Teta
        teta = math.ceil(arcoseno_graus/3)
        saida.write("Teta: ")
        saida.write(str(teta))
        saida.write("\n\n")


        # b) Tensões principais
        eigenvals, eigenvecs = np.linalg.eig(sigma)
        s1, s2, s3 = np.sort(eigenvals)[::-1]
        saida.write("Tensões principais:")
        saida.write("\n")
        saida.write("s1 = ")
        saida.write(str(np.round(s1, teta)))
        saida.write("\n")
        saida.write("s2 = ")
        saida.write(str(np.round(s2, teta)))
        saida.write("\n")
        saida.write("s3 = ")
        saida.write(str(np.round(s3, teta)))
        saida.write("\n\n")

        # c) Máxima tensão de cisalhamento
        tau_max = (s1 - s2) / 2
        saida.write("Máxima tensão de cisalhamento:  ")
        saida.write(str(np.round(tau_max, teta)))
        saida.write("\n\n")

        # d) Tresca
        tresca = (s1 - s3)
        saida.write("Tresca:  ")
        saida.write(str(tresca))
        saida.write("\n")

        #  Critério de Tresca e coeficiente de segurança
        Tresca_CS = (fy / tresca)
        saida.write("Coeficiente de segurança pelo critério de Tresca:  ")
        saida.write(str(np.round(Tresca_CS, teta)))
        saida.write("\n")
        if tresca > fy: saida.write("Escoamento\n\n")
        else: saida.write("Estável\n\n")

        # e) Von Mises
        von_Mises = math.sqrt((3*J_dois))
        saida.write("Von Mises:  ")
        saida.write(str(von_Mises))
        saida.write("\n")

        # Critério de von Mises e coeficiente de segurança
        vonMises_CS = (fy / von_Mises)
        saida.write("Coeficiente de segurança pelo critério de von Mises:  ")
        saida.write(str(np.round(vonMises_CS, teta)))
        saida.write("\n")
        if von_Mises > fy: saida.write("Escoamento\n\n")
        else: saida.write("Estável\n\n")

    elif nome == 'SAIR' or nome == "sair" or nome == 'Sair':
            sys.exit(0)
    else:
        print('NÃO ENCONTRADO')
        print('POR FAVOR, INSIRA O NOME DO ARQUIVO OU DIGITE SAIR PARA ENCERRAR :')
        nome = input()



