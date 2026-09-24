from PIL import Image
import math


def gradiente_sobel(imagem):
    largura, altura = imagem.size

    nova_imagem = Image.new(imagem.mode, (largura, altura))

    # Máscara Sobel para direção X
    mascara_x = [
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ]

    # Máscara Sobel para direção Y
    mascara_y = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]

    for x in range(largura):
        for y in range(altura):

            # Bordas da imagem
            if x == 0 or y == 0 or x == largura - 1 or y == altura - 1:
                nova_imagem.putpixel((x, y), 0)
                continue

            gradiente_x = 0
            gradiente_y = 0

            # Percorre a vizinhança 3x3
            for i in range(-1, 2):
                for j in range(-1, 2):

                    pixel = imagem.getpixel((x + i, y + j))

                    coeficiente_x = mascara_x[i + 1][j + 1]
                    coeficiente_y = mascara_y[i + 1][j + 1]

                    gradiente_x += pixel * coeficiente_x
                    gradiente_y += pixel * coeficiente_y

            # Magnitude do gradiente
            magnitude = math.sqrt(
                gradiente_x ** 2 +
                gradiente_y ** 2
            )

            # Mantém o resultado entre 0 e 255
            magnitude = max(0, min(255, int(magnitude)))

            nova_imagem.putpixel((x, y), magnitude)

    return nova_imagem

imagem = Image.open(
"images/Fig0115(b)(100-dollars).tif"
).convert("L")

largura, altura = imagem.size

print(f"Tamanho original: {largura}x{altura}")

imagem_sobel = gradiente_sobel(imagem)

imagem_sobel.save(
"images/Fig0115-sobel.tif"
)

print("Filtro Gradiente Sobel aplicado com sucesso!")