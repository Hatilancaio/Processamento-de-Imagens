from PIL import Image
import numpy as np



def imagem_para_matriz(caminho_imagem):
    img = Image.open(caminho_imagem).convert("L")
    matriz = np.array(img)
    matriz = matriz.tolist()  
    return matriz

def matriz_para_imagem(matriz, caminho_saida):
    array = np.array(matriz, dtype=np.uint8)
    img = Image.fromarray(array)
    img.save(caminho_saida)


def subtrair_imagens(caminho1, caminho2):
    matriz1 = imagem_para_matriz(caminho1)
    matriz2 = imagem_para_matriz(caminho2)

    resultado = []
    for i in range(len(matriz1)):
        linha_resultado = []
        for j in range(len(matriz1[0])):
            valor = matriz1[i][j] - matriz2[i][j] if matriz1[i][j] - matriz2[i][j] >= 0 else 0
            linha_resultado.append(valor)
        resultado.append(linha_resultado)

    matriz_para_imagem(resultado, "images/subtracao_resultado.tif") 

def somar_imagens(caminho1, caminho2):
    matriz1 = imagem_para_matriz(caminho1)
    matriz2 = imagem_para_matriz(caminho2)

    resultado = []
    for i in range(len(matriz1)):
        linha_resultado = []
        for j in range(len(matriz1[0])):
            valor = matriz1[i][j] + matriz2[i][j] if matriz1[i][j] + matriz2[i][j] <= 255 else 255
            linha_resultado.append(valor)
        resultado.append(linha_resultado)

    matriz_para_imagem(resultado, "images/soma_resultado.tif") 

import numpy as np

def transladar(caminho, dx, dy):
    matriz = imagem_para_matriz(caminho)
    resultado = []
    for i in range(len(matriz)):
        linha_resultado = []
        for j in range(len(matriz[0])):
            novo_i = i + dy
            novo_j = j + dx
            if 0 <= novo_i < len(matriz) and 0 <= novo_j < len(matriz[0]):
                linha_resultado.append(matriz[novo_i][novo_j])
            else:
                linha_resultado.append(0)
        resultado.append(linha_resultado)
    matriz_para_imagem(resultado, "images/translacao_resultado.tif")
    


############################################################################################    


imagem1_path = "images/imagem1.tif"
imagem2_path = "images/imagem2.tif"


subtrair_imagens(imagem1_path, imagem2_path)
somar_imagens(imagem1_path, imagem2_path)
transladar(imagem1_path, dx=100, dy=50)  