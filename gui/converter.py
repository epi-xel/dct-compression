from PIL import Image
import scipy.fftpack as fft
import numpy as np
from joblib import Parallel, delayed

def dct2(A):
    return fft.dct(fft.dct(A, axis=0, norm='ortho'), axis=1, norm='ortho')

def idct2(A):
    return fft.idct(fft.idct(A, axis=0, norm='ortho'), axis=1, norm='ortho')

def get_intervals(pixel_map):
    min_F = 2
    max_F = int((min(pixel_map.shape[0], pixel_map.shape[1]) / 5) - 1)
    return min_F, max_F

def get_pixel_map(file):
    input_image = Image.open(file).convert('L')
    return np.array(input_image)


def convert(pixel_map, F, d):
    
    len1 = pixel_map.shape[0] - (pixel_map.shape[0] % F)
    len2 = pixel_map.shape[1] - (pixel_map.shape[1] % F)

    block_len1 = len1 // F
    block_len2 = len2 // F

    blocks = np.zeros((block_len1, block_len2, F, F), dtype=np.float32)

    for i in range(block_len1):
        for j in range(block_len2):
            blocks[i, j] = pixel_map[i * F:(i + 1) * F, j * F:(j + 1) * F]

    for i in range(block_len1):
        for j in range(block_len2):
            blocks[i, j] = dct2(blocks[i, j])

    for i in range(block_len1):
        for j in range(block_len2):
            for m in range(F):
                for n in range(F):
                    if m + n >= d:
                        blocks[i, j, m, n] = 0

    for i in range(block_len1):
        for j in range(block_len2):
            blocks[i, j] = idct2(blocks[i, j])
    
    for i in range(len(blocks)):
        for j in range(len(blocks[i])):
            for k in range(F):
                for l in range(F):
                    blocks[i][j][k][l] = int(blocks[i][j][k][l])
                    blocks[i][j][k][l] = np.clip(blocks[i][j][k][l], 0, 255)

    reassembled_len1 = block_len1 * F
    reassembled_len2 = block_len2 * F

    reassembled = np.empty((reassembled_len1, reassembled_len2), dtype=np.uint8)

    for i in range(block_len1):
        for j in range(block_len2):
            reassembled[i * F:(i + 1) * F, j * F:(j + 1) * F] = blocks[i, j]

    output_image = Image.fromarray(reassembled)
    output_image = output_image.convert("L")

    return output_image
