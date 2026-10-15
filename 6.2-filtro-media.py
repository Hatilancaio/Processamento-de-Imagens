from PIL import Image


def filtro_media(imagem):
    largura, altura = imagem.size

    nova_imagem = Image.new(imagem.mode, (largura, altura))

    mascara = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]

    soma_coeficientes = sum(sum(linha) for linha in mascara)  # 9

    for x in range(largura):
        for y in range(altura):

            if x == 0 or y == 0 or x == largura - 1 or y == altura - 1:
                nova_imagem.putpixel((x, y), 0)
                continue

            soma = 0

            for i in range(-1, 2):
                for j in range(-1, 2):

                    pixel = imagem.getpixel((x + i, y + j))

                    coeficiente = mascara[i + 1][j + 1]

                    soma += pixel * coeficiente

            media = soma / soma_coeficientes

            media = max(0, min(255, int(media)))

            nova_imagem.putpixel((x, y), media)

    return nova_imagem


imagem = Image.open(
    "images/Fig0115(b)(100-dollars).tif"
).convert("L")

largura, altura = imagem.size

imagem_media = filtro_media(imagem)

imagem_media.save(
    "images/Fig0115-media.tif"
)

print("Filtro da Média aplicado com sucesso!")