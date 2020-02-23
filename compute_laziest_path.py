import argparse
from challenge.utils import compute_laziest_path


if __name__ == '__main__':
    """ Get the shortest path for pushing a sequence of buttons

    Example:
        python compute_laziest_path.py --sequence 89602
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('--sequence',
                        type=str,
                        dest='sequence',
                        required=True,
                        help='Sequence of symbols that have to be pressed by the fingers')

    args = parser.parse_args()

    res = compute_laziest_path(args.sequence)
    print(res)
