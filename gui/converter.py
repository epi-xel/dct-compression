from PIL import Image
import scipy.fftpack as fft
import numpy as np


def dct2(A):
    return fft.dct(fft.dct(A, axis=0, norm='ortho'), axis=1, norm='ortho')


def idct2(A):
    return fft.idct(fft.idct(A, axis=0, norm='ortho'), axis=1, norm='ortho')


def get_intervals(pixel_map):
    min_F = 2
    max_F = int((min(pixel_map.shape[0], pixel_map.shape[1])) - 1)
    return min_F, max_F


def get_pixel_map(file):
    input_image = Image.open(file).convert('L')
    return np.array(input_image)


def divide_in_blocks(pixel_map, F):

    len1 = pixel_map.shape[0] - (pixel_map.shape[0] % F)
    len2 = pixel_map.shape[1] - (pixel_map.shape[1] % F)

    block_len1 = len1 // F
    block_len2 = len2 // F

    blocks = np.zeros((block_len1, block_len2, F, F), dtype=np.float32)

    for i in range(block_len1):
        for j in range(block_len2):
            blocks[i, j] = pixel_map[i * F:(i + 1) * F, j * F:(j + 1) * F]

    return blocks


def apply_dct(blocks):

    for i in range(len(blocks)):
        for j in range(len(blocks[i])):
            blocks[i, j] = dct2(blocks[i, j])


def delete_high_freq(blocks, d):

    for i in range(blocks.shape[0]):
        for j in range(blocks.shape[1]):
            for m in range(blocks.shape[2]):
                for n in range(blocks.shape[3]):
                    if m + n >= d:
                        blocks[i, j, m, n] = 0


def apply_idct(blocks):

    for i in range(len(blocks)):
        for j in range(len(blocks[i])):
            blocks[i, j] = idct2(blocks[i, j])


def clip(blocks):

    for i in range(blocks.shape[0]):
        for j in range(blocks.shape[1]):
            for k in range(blocks.shape[2]):
                for l in range(blocks.shape[3]):
                    blocks[i][j][k][l] = int(blocks[i][j][k][l])
                    blocks[i][j][k][l] = np.clip(blocks[i][j][k][l], 0, 255)


def reassemble(blocks):

    reassembled_len1 = blocks.shape[0] * blocks.shape[2]
    reassembled_len2 = blocks.shape[1] * blocks.shape[3]

    reassembled = np.empty((reassembled_len1, reassembled_len2), dtype=np.uint8)
    F = blocks.shape[2]

    for i in range(blocks.shape[0]):
        for j in range(blocks.shape[1]):
            reassembled[i * F:(i + 1) * F, j * F:(j + 1) * F] = blocks[i, j]

    return reassembled


def get_output_image(reassembled):

    output_image = Image.fromarray(reassembled)
    output_image = output_image.convert("L")

    return output_image


def convert(pixel_map, F, d):

    blocks = divide_in_blocks(pixel_map, F)
    apply_dct(blocks)
    delete_high_freq(blocks, d)
    apply_idct(blocks)
    clip(blocks)
    reassembled = reassemble(blocks)
    return get_output_image(reassembled)