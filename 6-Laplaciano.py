from PIL import Image


def laplaciano(imagem, mascara):
    largura, altura = imagem.size

    nova_imagem = Image.new(imagem.mode, (largura, altura))

    for x in range(largura):
        for y in range(altura):

            soma = 0

            # Não processa as bordas da imagem
            if x == 0 or y == 0 or x == largura - 1 or y == altura - 1:
                nova_imagem.putpixel((x, y), 0)
                continue

            # Vizinhança 3x3
            for i in range(-1, 2):
                for j in range(-1, 2):

                    pixel = imagem.getpixel((x + i, y + j))

                    coeficiente = mascara[i + 1][j + 1]

                    soma += pixel * coeficiente

            # Valores negativos são zerados
            soma = max(0, min(255, soma))

            nova_imagem.putpixel((x, y), soma)

    return nova_imagem


imagem = Image.open(
"images/Fig0115(b)(100-dollars).tif"
).convert("L")

largura, altura = imagem.size

mascara_1 = [
[0, 1, 0],
[1, -4, 1],
[0, 1, 0]
]

mascara_2 = [
[1, 1, 1],
[1, -8, 1],
[1, 1, 1]
]

mascara_3 = [
[0, -1, 0],
[-1, 4, -1],
[0, -1, 0]
]

mascara_4 = [
[-1, -1, -1],
[-1, 8, -1],
[-1, -1, -1]
]


laplaciano_1 = laplaciano(imagem, mascara_1)
laplaciano_1.save("images/laplaciano_mascara_1.tif")

laplaciano_2 = laplaciano(imagem, mascara_2)
laplaciano_2.save("images/laplaciano_mascara_2.tif")

laplaciano_3 = laplaciano(imagem, mascara_3)
laplaciano_3.save("images/laplaciano_mascara_3.tif")

laplaciano_4 = laplaciano(imagem, mascara_4)
laplaciano_4.save("images/laplaciano_mascara_4.tif")



print("Filtros Laplacianos aplicados com sucesso!")