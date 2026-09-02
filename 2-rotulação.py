from PIL import Image
import numpy as np


def find_label(labels, r):
    while labels[r] != r:
        r = labels[r]
    return r


"""
Exemplo com matriz
image = [
    [0, 1, 1, 0, 0, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0],
]

for line in image:
    print(line)
"""

caminho_imagem = "images/imagem_binaria_exemplo.tif"
img = Image.open(caminho_imagem).convert("L")
matriz = np.array(img)
image = (matriz > 127).astype(int).tolist()  

labels = {}
next_label = 0




for l in range(len(image)):
    for c in range(len(image[l])):
        p = image[l][c]

        if p == 0:
            continue

        top_neighbour = image[l-1][c] if l > 0 else 0
        left_neighbour = image[l][c-1] if c > 0 else 0

        if top_neighbour == 0 and left_neighbour == 0:
            next_label += 1
            image[l][c] = next_label
            labels[next_label] = next_label

        elif top_neighbour != 0 and left_neighbour == 0:
            image[l][c] = top_neighbour

        elif top_neighbour == 0 and left_neighbour != 0:
            image[l][c] = left_neighbour

        else:
            root_top = find_label(labels, top_neighbour)
            root_left = find_label(labels, left_neighbour)

            if root_top == root_left:
                image[l][c] = root_top
            else:
                menor = min(root_top, root_left)
                maior = max(root_top, root_left)
                image[l][c] = menor
                labels[maior] = menor


for l in range(len(image)):
    for c in range(len(image[l])):
        if image[l][c] != 0:
            image[l][c] = find_label(labels, image[l][c])

# --- GERA A IMAGEM COLORIDA DE SAÍDA ---   OBS: Etapa gerada com i.a

total_componentes = len(set(find_label(labels, r) for r in labels))
rotulos_array = np.array(image) 

rng = np.random.default_rng(42) 
cores = rng.integers(50, 256, size=(total_componentes + 1, 3))
cores[0] = [0, 0, 0]  


labels_unicos = sorted(set(rotulos_array.flatten()) - {0})
remapa = {label: i + 1 for i, label in enumerate(labels_unicos)}

altura, largura = rotulos_array.shape
saida = np.zeros((altura, largura, 3), dtype=np.uint8)
for l in range(altura):
    for c in range(largura):
        if rotulos_array[l, c] != 0:
            indice_cor = remapa[rotulos_array[l, c]]
            saida[l, c] = cores[indice_cor]

img_saida = Image.fromarray(saida, mode="RGB")
img_saida.save("images/imagem_rotulada_saida.png")
print("Imagem colorida salva em images/imagem_rotulada_saida.png")