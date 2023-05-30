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


def delete_freq(block, d):

    for i in range(block.shape[0]):
        for j in range(block.shape[1]):
            if i + j >= d:
                block[i, j] = 0
    
    return block


def clip(block):

    for i in range(block.shape[0]):
        for j in range(block.shape[1]):
            block[i, j] = int(block[i, j])
            block[i, j] = np.clip(block[i, j], 0, 255)
    
    return block


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
    
    for i in range(blocks.shape[0]):
        for j in range(blocks.shape[1]):
            blocks[i, j] = dct2(blocks[i, j])
            blocks[i, j] = delete_freq(blocks[i, j], d)
            blocks[i, j] = idct2(blocks[i, j])
            blocks[i, j] = clip(blocks[i, j])
    
    reassembled = reassemble(blocks)
    return get_output_image(reassembled)