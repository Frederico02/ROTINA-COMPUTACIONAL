import numpy as np
import sys
import os.path


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

        # b) Tensões principais
        eigenvals, eigenvecs = np.linalg.eig(sigma)
        s1, s2, s3 = np.sort(eigenvals)[::-1]
        saida.write("Tensões principais:")
        saida.write("\n")
        saida.write("s1 = ")
        saida.write(str(np.round(s1, 6)))
        saida.write("\n")
        saida.write("s2 = ")
        saida.write(str(np.round(s2, 6)))
        saida.write("\n")
        saida.write("s3 = ")
        saida.write(str(np.round(s3, 6)))
        saida.write("\n")

        # c) Máxima tensão de cisalhamento
        tau_max = (s1 - s2) / 2
        saida.write("Máxima tensão de cisalhamento:  ")
        saida.write(str(np.round(tau_max, 6)))
        saida.write("\n\n")

        # d) Critério de Tresca e coeficiente de segurança
        Tresca_CS = (fy / 2) / tau_max
        saida.write("Coeficiente de segurança pelo critério de Tresca:  ")
        saida.write(str(np.round(Tresca_CS, 6)))
        saida.write("\n\n")

        # e) Critério de von Mises e coeficiente de segurança
        s_inv = np.sqrt(np.sum(np.square(np.abs(sigma - np.trace(sigma) * np.identity(3)))) * 2 / 3)
        vonMises_CS = (fy / (2 * np.sqrt(3))) / s_inv
        saida.write("Coeficiente de segurança pelo critério de von Mises:  ")
        saida.write(str(np.round(vonMises_CS, 6)))
        saida.write("\n\n")

    elif nome == 'SAIR' or nome == "sair" or nome == 'Sair':
            sys.exit(0)
    else:
        print('NÃO ENCONTRADO')
        print('POR FAVOR, INSIRA O NOME DO ARQUIVO OU DIGITE SAIR PARA ENCERRAR :')
        nome = input()





