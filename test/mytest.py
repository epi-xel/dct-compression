from PIL import Image
import scipy.fftpack as fft
import numpy as np

F = 16
d = 1

def dct2(A):
    return fft.dct(fft.dct(A, axis=0, norm='ortho'), axis=1, norm='ortho')

def idct2(A):
    return fft.idct(fft.idct(A, axis=0, norm='ortho'), axis=1, norm='ortho')

input_image = Image.open("bmp/deer.bmp").convert('L')

pixel_map = np.array(input_image)

len1 = pixel_map.shape[0] - (pixel_map.shape[0] % F)
len2 = pixel_map.shape[1] - (pixel_map.shape[1] % F)


block_len1 = len1 // F
block_len2 = len2 // F
blocks = [[[[0 for i in range(0, F)] for j in range(0, F)] for k in range(0, block_len2)] for l in range(0, block_len1)]
i = 0
for x in range(0, len1, F):
    j = 0
    for y in range(0, len2, F):
        blocks[i][j] = pixel_map[x:x+F, y:y+F]
        j += 1
    i += 1

for i in range(len(blocks)):
    for j in range(len(blocks[i])):
        blocks[i][j] = dct2(blocks[i][j])

for block in blocks:
    for i in range(F):
        for j in range(F):
            if i + j >= d:
                block[i][j] = 0

for i in range(len(blocks)):
    for j in range(len(blocks[i])):
        blocks[i][j] = idct2(blocks[i][j])

for i in range(len(blocks)):
    for j in range(len(blocks[i])):
        for k in range(F):
            for l in range(F):
                blocks[i][j][k][l] = int(blocks[i][j][k][l])
                blocks[i][j][k][l] = np.clip(blocks[i][j][k][l], 0, 255)

reassembled = np.empty((len1, len2), dtype=np.uint8)

for i in range(0, len(blocks)):
    for j in range(0, len(blocks[i])):
        reassembled[i * F : (i + 1) * F, j * F : (j + 1) * F] = blocks[i][j]

output_image = Image.fromarray(reassembled)
output_image = output_image.convert("L")

output_image.save("bmp/deer_dct.jpg")
