from PIL import Image


def reducao_vizinhoMaisProximo(imagem, nova_largura:int, nova_altura:int):
    largura, altura = imagem.size

    nova_imagem = Image.new(imagem.mode, (nova_largura, nova_altura))

    fator_x = int(largura/nova_largura)
    faotor_y = int(altura/nova_altura)

    for x in range (nova_largura):
        for y in range (nova_altura):
            x_original = (x * fator_x)
            y_original = (y * faotor_y)

            pixel = imagem.getpixel((x_original, y_original))
            nova_imagem.putpixel((x, y), pixel)

    return nova_imagem

#----------------------------------------------------------#

def ampliacao_vizinhoMaisProximo(imagem, nova_largura:int, nova_altura:int):
    largura, altura = imagem.size

    nova_imagem = Image.new(imagem.mode,(nova_largura, nova_altura))
    

    for x in range(nova_largura):
        for y in range(nova_altura):
            x_original = min(int(x * largura / nova_largura), largura - 1)
            y_original = min(int(y * altura / nova_altura), altura - 1)

            pixel = imagem.getpixel((x_original, y_original))
            nova_imagem.putpixel((x,y), pixel)

    return nova_imagem

#---------------------------------------------------------------------#

def bilinear(imagem, nova_largura:int, nova_altura:int):
    largura, altura = imagem.size

    nova_imagem = Image.new(imagem.mode, (nova_largura, nova_altura))

    fator_x = largura/nova_largura
    fator_y = altura/nova_altura

    for x in range(nova_largura):

        for y in range(nova_altura):

            x_original = (x + 0.5) * (fator_x) - 0.5
            y_original = (y + 0.5) * (fator_y) - 0.5

            i = int(x_original)
            j = int(y_original)

            dx = x_original - i
            dy = y_original - j

            i = max(0, min(i, largura - 1))
            j = max(0, min(j, altura - 1))
            i2 = min(i + 1, largura - 1)
            j2 = min(j + 1, altura - 1)

            vizinho_1 = imagem.getpixel((i, j))
            vizinho_2 = imagem.getpixel((i, j2))
            vizinho_3 = imagem.getpixel((i2, j))
            vizinho_4 = imagem.getpixel((i2, j2))

            pixel = (
                vizinho_1 * (1 - dx) * (1 - dy) +
                vizinho_3 * dx * (1 - dy) +
                vizinho_2 * (1 - dx) * dy +
                vizinho_4 * dx * dy
            )

            nova_imagem.putpixel((x, y), int(pixel))

    return nova_imagem






imagem = Image.open(
    "images/Fig0115(b)(100-dollars).tif"
).convert("L")

largura, altura = imagem.size

print(f"Tamanho original: {largura}x{altura}")


imagem_reduzida_vizinho = reducao_vizinhoMaisProximo(
    imagem,
    nova_largura=largura // 2,
    nova_altura=altura // 2
)
imagem_reduzida_vizinho.save("images/Fig0115-reduzida-vizinho.tif")


imagem_ampliada_vizinho = ampliacao_vizinhoMaisProximo(
    imagem,
    nova_largura=largura * 2,
    nova_altura=altura * 2
)
imagem_ampliada_vizinho.save("images/Fig0115-ampliada-vizinho.tif")

imagem_bilinear = bilinear(
    imagem,
    nova_largura=largura // 2,
    nova_altura=altura // 2
)
imagem_bilinear.save("images/Fig0115-bilinear.tif")



    
        
    