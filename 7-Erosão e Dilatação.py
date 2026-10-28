from PIL import Image, ImageChops


def aplicar_morfologia(imagem, operacao):
    largura, altura = imagem.size
    nova_imagem = Image.new("L", (largura, altura))

    for x in range(largura):
        for y in range(altura):
            vizinhos = []

            for i in range(max(0, x - 1), min(largura, x + 2)):
                for j in range(max(0, y - 1), min(altura, y + 2)):
                    vizinhos.append(imagem.getpixel((i, j)))

            nova_imagem.putpixel((x, y), operacao(vizinhos))

    return nova_imagem


imagem = Image.open(
    "images/Fig0106(b)(PET_image).tif"
).convert("L")

imagem_erodida = aplicar_morfologia(imagem, min)
imagem_erodida.save("images/erosao.tif")

imagem_dilatada = aplicar_morfologia(imagem, max)
imagem_dilatada.save("images/dilatacao.tif")

imagem_aberta = aplicar_morfologia(
    aplicar_morfologia(imagem, min),
    max,
)
imagem_top_hat = ImageChops.subtract(imagem, imagem_aberta)
imagem_top_hat.save("images/tophat.tif")

print("Erosão, dilatação e Transformada Top-Hat aplicadas com sucesso!")
