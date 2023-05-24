from PIL import Image
import scipy.fftpack as fft
import numpy as np

def dct2(A):
    return fft.dct(fft.dct(A, axis=0, norm='ortho'), axis=1, norm='ortho')

def idct2(A):
    return fft.idct(fft.idct(A, axis=0, norm='ortho'), axis=1, norm='ortho')

def get_intervals(pixel_map):
    min_F = 2
    max_F = int((min(pixel_map.shape[0], pixel_map.shape[1]) / 2) - 1)
    return min_F, max_F

def get_pixel_map(file):
    input_image = Image.open(file).convert('L')
    return np.array(input_image)


def convert(pixel_map, F, d):
    
    len1 = pixel_map.shape[0] - (pixel_map.shape[0] % F)
    len2 = pixel_map.shape[1] - (pixel_map.shape[1] % F)

    blocks = [pixel_map[x:x+F, y:y+F] for x in range(0, len1, F) for y in range(0, len2, F)]

    dct_blocks = []

    for block in blocks:
        dct_blocks.append(dct2(block))

    for block in dct_blocks:
        for i in range(F):
            for j in range(F):
                if i + j >= d:
                    block[i][j] = 0

    idct_blocks = []

    for block in dct_blocks:
        idct_blocks.append(idct2(block))

    for block in idct_blocks:
        for i in range(F):
            for j in range(F):
                block[i][j] = int(block[i][j])
                if block[i][j] < 0:
                    block[i][j] = 0
                if block[i][j] > 255:
                    block[i][j] = 255

    reassembled = np.empty((len1, len2), dtype=np.uint8)

    block_index = 0
    for i in range(0, len1, F):
        for j in range(0, len2, F):
            reassembled[i:i+F, j:j+F] = idct_blocks[block_index]
            block_index += 1

    output_image = Image.fromarray(reassembled)
    output_image = output_image.convert("L")

    return output_image