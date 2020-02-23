import time
import numpy as np
import matplotlib.pyplot as plt
from challenge.utils import generate_number_sequence, compute_laziest_path


def get_avg_time(seq_length: int, n_experiments: int):
    """ Get the average time for computing the best path for
    a number string of length = seq_length

    :param seq_length: length of the randomly generated number strings
    :param n_experiments: average the computation time over this number
    :return:
    """
    start = time.time()

    for _ in range(n_experiments):
        number_sequence = generate_number_sequence(seq_length)
        _ = compute_laziest_path(number_sequence)

    end = time.time()

    avg_computation_time = (end - start) / n_experiments

    return avg_computation_time


def measure_complexity():
    n_experiments = 100
    seq_lengths = np.array([10, 100, 1000, 10000])

    ts = []
    for seq_length in seq_lengths:
        t = get_avg_time(seq_length, n_experiments)
        print('seq. length, avg. time: {0}, \t {1}'.format(seq_length, t))
        ts.append(t)
    ts = np.array(ts)

    # plot the results
    fig = plt.figure(figsize=(10, 7))
    plt.scatter(np.log10(seq_lengths), np.log10(ts))
    plt.xlabel('Log10(n)')
    plt.ylabel('Log10(t) [s]')
    plt.title('Computation time as a function of the sequence length (n)')
    fig.savefig('Computation_time.png', transparent=False, bbox_inches='tight', quality=100, dpi=300)


if __name__ == '__main__':
    """ Measure the complexity of the algorithm for 
    sequences of length 10^1, 10^2, 10^3, 10^4.
    
    Execute (3 minutes to complete):
        python measure_complexity.py
    """
    measure_complexity()
