from PIL import Image

def itensidade_negativa(imagem):
    largura, altura = imagem.size

    nova_imagem = Image.new(imagem.mode, [largura, altura])


    for x in range (largura):
        for y in range (altura):

            pixel = imagem.getpixel([x, y])

            pixel_negativo = 255 - pixel

            nova_imagem.putpixel((x, y), pixel_negativo)

    return nova_imagem

imagem = Image.open(
    "images/transformacao_intensidade.tif"
).convert("L")

nova_imagem = itensidade_negativa(imagem)
nova_imagem.save("images/intensidade-negativa.tif")
