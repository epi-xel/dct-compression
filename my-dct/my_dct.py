import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.fftpack as fft
from joblib import Parallel, delayed
from time import time
import csv
import argparse
import os


def init_parser():
    
    parser = argparse.ArgumentParser(
                    prog='My DCT',
                    description='My DCT implementation, plots and results')

    parser.add_argument('-t', '--test', action='store_true', help='Run tests')
    parser.add_argument('-p', '--plot', action='store_true', help='Plot results')
    parser.add_argument('-s', '--start', type=int, help='Start matrix size. Default: 2')
    parser.add_argument('-e', '--end', type=int, help='End matrix size. Default: Start')
    parser.add_argument('-b', '--step', type=int, help='Step size for linear matrix sizes, base for exponential matrix sizes. Default: 2')
    parser.add_argument('-x', '--exp', action='store_true', help='Use exponential matrix sizes')

    return parser


def dct2(A):
    return fft.dct(fft.dct(A, axis=0, norm='ortho'), axis=1, norm='ortho')


def my_dct(v):
    N = len(v)
    a = [0] * N
    for k in range(0, N):
        for i in range(0, N):
            a[k] += np.cos(np.pi * k * ((2 * i + 1) / (2 * N))) * v[i]
        den = N / 2
        if(k == 0): den = N
        a[k] = (a[k] / np.sqrt(den))
    return a


def my_dct2(A):
    N = len(A)
    m = np.zeros((N, N))
    for i in range(0, N):
        m[i] = my_dct(A[i])
    for j in range(0, N):
        m[:, j] = my_dct(m[:, j])
    return m


def process(mat):
    print("... Computing DCT2 - Matrix size: ", len(mat))
    start = time()
    dct2(mat)
    end = time()
    time_dct2 = end - start
    start = time()
    my_dct2(mat)
    end = time()
    time_my_dct2 = end - start
    print("DONE Computed DCT2 - Matrix size: ", len(mat))
    return [len(mat), time_dct2, time_my_dct2]


def new_matrix(N):
    print("... Generating matrix - Matrix size: ", N)
    return np.random.randint(0, 255, size=(N, N))


def plot(df, name, scale='log'):

    os.makedirs('plots', exist_ok=True)

    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(15, 10))
    ax = sns.lineplot(data=df, x="N", y="DCT2 Time", legend='brief', label='DCT2')
    sns.lineplot(data=df, x="N", y="My DCT2 Time", legend='brief', label='My DCT2')
    ax.set_yscale(scale)
    plt.savefig('plots/' + name + '.png')


def wrapper(mat, seq):
    with open('data/times' + seq + '.csv', 'a') as fileObj:
        writerObj = csv.writer(fileObj)
        writerObj.writerow(process(mat))


def generate_matrices(start, end, every, exp=False):
    
    if(exp):
        # Exponential sizes
        matrices = Parallel(n_jobs=5)(delayed(new_matrix)(N) for N in (every**p for p in range(start, end)))
    else:
        # Linear sizes
        matrices = Parallel(n_jobs=5)(delayed(new_matrix)(N) for N in range(start, end, every))
        
    print("\nDone generating matrices\n")

    return matrices


def compute_times(start, end, every, exp=False):
    
    matrices = generate_matrices(start, end, every, exp)

    if(exp):
        seq = str(start) + 'to' + str(end) + 'exp' + str(every)
    else:
        seq = str(start) + 'to' + str(end) + 'step' + str(every)

    os.makedirs('data', exist_ok=True)

    with open('data/times' + seq + '.csv', 'w') as fileObj:
            writerObj = csv.writer(fileObj)
            writerObj.writerow(['N', 'DCT2 Time', 'My DCT2 Time'])

    times = Parallel(n_jobs=7)(delayed(wrapper)(m, seq) for m in matrices)

    return times


def test():

    test = [231, 32, 233, 161, 24, 71, 140, 245]
    dct_test = fft.dct(test, norm='ortho')

    print("DCT TEST")
    print(test)
    print("\nMy DCT")
    print(dct_test)
    print("\nDCT")
    print(my_dct(test))

    mat = [[231, 32, 233, 161, 24, 71, 140, 245], 
         [247, 40, 248, 245, 124, 204, 36, 107], 
         [234, 202, 245, 167, 9, 217, 239, 173], 
         [193, 190, 100, 167, 43, 180, 8, 70], 
         [11, 24, 210, 177, 81, 243, 8, 112], 
         [97, 195, 203, 47, 125, 114, 165, 181], 
         [193, 70, 174, 167, 41, 30, 127, 245], 
         [87, 149, 57, 192, 65, 129, 178, 228]]

    print("\n\nDCT2 TEST")
    print(mat) 
    print("\nMy DCT2")
    print(my_dct2(mat))
    print("\nDCT2")
    print(dct2(mat))


def main():
    
    parser = init_parser()

    start = 2
    end = 2
    step = 2
    exp = False

    if(parser.parse_args().test):
        test()
        exit(0)
    
    if(parser.parse_args().start):
        start = parser.parse_args().start
    
    if(parser.parse_args().end):
        end = parser.parse_args().end
    else:
        end = start
    
    if(parser.parse_args().step):
        step = parser.parse_args().step

    if(parser.parse_args().exp):
        exp = True

    compute_times(start, end, step, exp)

    df = pd.read_csv('data/times' + str(start) + 'to' + str(end) + 'step' + str(step) + '.csv')

    plot(df, str(start) + 'to' + str(end) + 'step' + str(step))


if __name__ == '__main__':
    main()