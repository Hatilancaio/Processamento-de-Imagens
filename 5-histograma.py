from PIL import Image

path = "images/Fig0115(b)(100-dollars).tif"  # Caminho da imagem de entrada
L = 256                   

def carregar_imagem_cinza(caminho):
    img = Image.open(caminho).convert("L")
    largura, altura = img.size
    pixels = img.load()  

    matriz = []
    for y in range(altura):
        linha = []
        for x in range(largura):
            linha.append(pixels[x, y])
        matriz.append(linha)

    
    return matriz, largura, altura

def calcular_histograma(matriz, L=256):
    #Calcula as frequencias absolutas de cada nivel de cinza (0 a L-1)
    histograma = [0] * L
    for linha in matriz:
        for pixel in linha:
            histograma[pixel] += 1
    return histograma


def normalizar_histograma(histograma, n_total_pixels):
    #calcula a frequencia relativa de cada nível de cinza
    resultado = []
    for n_k in histograma:
        resultado.append(n_k / n_total_pixels)
    return resultado


def calcular_cdf(hist_normalizado):
    """
    CDF(k) = soma de p(0) ate p(k)
    """
    cdf = []
    acumulado = 0.0
    for p_k in hist_normalizado:
        acumulado += p_k
        cdf.append(acumulado)
    return cdf

def calcular_niveis_equalizados(cdf, L=256):

    l_table = []
    for valor_cdf in cdf:
        l_table.append(round((L - 1) * valor_cdf))
    return l_table

def aplicar_equalizacao(matriz, l_table):
    
    imagem_equalizada = []
    for linha in matriz:
        nova_linha = [l_table[pixel] for pixel in linha]
        imagem_equalizada.append(nova_linha)
    return imagem_equalizada

def imprimir_tabela(histograma, hist_normalizado, cdf, lut):
    """
    Imprime, em formato de tabela texto, apenas os niveis de cinza que
    realmente ocorrem na imagem (frequencia > 0), com:
        - nivel de cinza (k)
        - frequencia absoluta (n_k)
        - frequencia normalizada (p_k)
        - frequencia acumulada (CDF)
        - novo nivel equalizado (s_k)
    """
    cabecalho = f"{'k':>5} | {'n_k':>8} | {'p_k':>10} | {'CDF':>10} | {'s_k':>5}"
    print(cabecalho)
    print("-" * len(cabecalho))
    for k in range(len(histograma)):
        if histograma[k] > 0:
            print(f"{k:>5} | {histograma[k]:>8} | {hist_normalizado[k]:>10.5f} "
                  f"| {cdf[k]:>10.5f} | {lut[k]:>5}")


def salvar_tabela_csv(caminho, histograma, hist_normalizado, cdf, lut):
    """
    Salva a tabela completa (todos os 256 niveis) em um arquivo .csv,
    usando apenas escrita de texto padrao (sem biblioteca csv/pandas).
    """
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("nivel_k,frequencia_n_k,frequencia_normalizada_p_k,"
                       "frequencia_acumulada_CDF,novo_nivel_s_k\n")
        for k in range(len(histograma)):
            arquivo.write(f"{k},{histograma[k]},{hist_normalizado[k]:.6f},"
                           f"{cdf[k]:.6f},{lut[k]}\n")

# Funcao auxiliar: converter matriz (lista de listas) de volta para imagem PIL
def matriz_para_imagem(matriz, largura, altura):
    img = Image.new("L", (largura, altura))
    pixels = img.load()
    for y in range(altura):
        for x in range(largura):
            pixels[x, y] = matriz[y][x]
    return img



def main():
    
    matriz, largura, altura = carregar_imagem_cinza(path)
    n_total_pixels = largura * altura


    histograma = calcular_histograma(matriz, L)

    hist_normalizado = normalizar_histograma(histograma, n_total_pixels)

    cdf = calcular_cdf(hist_normalizado)

    l_table = calcular_niveis_equalizados(cdf, L)

    imagem_equalizada_matriz = aplicar_equalizacao(matriz, l_table)

    print(f"Dimensoes da imagem: {largura} x {altura}  (N = {n_total_pixels} pixels)\n")
    print("Tabela do histograma (somente niveis com frequencia > 0):")
    imprimir_tabela(histograma, hist_normalizado, cdf, l_table)
    salvar_tabela_csv("tabela_histograma.csv", histograma, hist_normalizado, cdf, l_table)
    print("\nTabela completa (256 niveis) salva em 'tabela_histograma.csv'")

    # Converter a matriz equalizada de volta para imagem e salvar (PIL)
    imagem_equalizada = matriz_para_imagem(imagem_equalizada_matriz, largura, altura)
    imagem_equalizada.save("images/imagem_equalizada.png")
    


if __name__ == "__main__":
    main()