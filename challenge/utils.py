import itertools
import numpy as np
import random
from typing import *


def generate_number_sequence(k: int = 5) -> str:
    sequence = random.choices('0123456789*#', weights=None, k=k)
    return ''.join(sequence)


def dist_p2(a: np.array, b: np.array) -> float:
    """ Euclidean distance btw two points
    """
    return np.sqrt(sum((a - b) ** 2))


def create_distance_dict() -> dict:
    """ Create dictionary that maps two points to
    their Euclidean distance
    """
    str_to_point_map = {
        '1': np.array([0, 0]),
        '2': np.array([0, 1]),
        '3': np.array([0, 2]),

        '4': np.array([1, 0]),
        '5': np.array([1, 1]),
        '6': np.array([1, 2]),

        '7': np.array([2, 0]),
        '8': np.array([2, 1]),
        '9': np.array([2, 2]),

        '*': np.array([3, 0]),
        '0': np.array([3, 1]),
        '#': np.array([3, 2])
    }

    distance_dict = dict()

    for a, b in itertools.product('0123456789*#', '0123456789*#'):
        pa = str_to_point_map[a]
        pb = str_to_point_map[b]
        distance_dict[a + b] = dist_p2(pa, pb)

    return distance_dict


distance_dict = create_distance_dict()


def fingers_pos_to_fingers_pos_transition_cost(si: str, sf: str) -> float:
    """ Calculate the cost (distance) for moving your fingers from si to sf;
    only one finger should be moved.

    :param si: initial fingers positions (e.g. '*3', '12', '4#', ...)
    :param sf: final fingers positions
    :return: movement cost
    """
    if si[0] != sf[0]:
        return distance_dict[si[0] + sf[0]]
    elif si[1] != sf[1]:
        return distance_dict[si[1] + sf[1]]
    else:
        return 0.


def update_fingers_pos(x: str, finger: str, fingers_pos_i: str) -> str:
    if finger == 'L':
        fingers_pos_f = x + fingers_pos_i[1]
    else:
        fingers_pos_f = fingers_pos_i[0] + x

    return fingers_pos_f


def move_finger(x: str, state_i, finger: str) -> Union[None, Tuple[str, float, str]]:
    """ Generate a new state from the movement of a finger to a new button

    :param x: next button that has to be pressed
    :param finger: finger used to press the next_button
    :param state_i: initial state =
        (fingers_position, accumulated cost,  moved fingers sequence)
    :return: state_f =
        (fingers_position, accumulated cost,  moved fingers sequence)
    """
    fingers_pos_i, cost_i, pattern_i = state_i

    fingers_pos_f = update_fingers_pos(x, finger, fingers_pos_i)

    if fingers_pos_f[0] == fingers_pos_f[1]:
        # forbidden state
        return None

    cost_f = cost_i + fingers_pos_to_fingers_pos_transition_cost(fingers_pos_i,
                                                                 fingers_pos_f)

    pattern_f = pattern_i + finger

    return fingers_pos_f, cost_f, pattern_f


def generate_new_states(x: str, state_list: List[Tuple[str, float, str]]) \
        -> List[Tuple[str, float, str]]:
    """ Generate new states from the old states by moving
    one of your fingers to the button `x`

    :param x: next button that has to be pressed
    :param state_list: list of states; state =
        (fingers_position, accumulated cost,  moved fingers sequence)
    :return: list of states; state =
        (fingers_position, accumulated cost,  moved fingers sequence)
    """
    state_list_left = map(lambda fs: move_finger(x=x,
                                                 state_i=fs,
                                                 finger='L'),
                          state_list)

    state_list_right = map(lambda fs: move_finger(x=x,
                                                  state_i=fs,
                                                  finger='R'),
                           state_list)

    new_state_list = itertools.chain(state_list_left, state_list_right)
    new_state_list = filter(lambda y: y is not None, new_state_list)
    new_state_list = list(new_state_list)

    return new_state_list


def reduce_new_states(state_list: List[Tuple[str, float, str]]) \
        -> List[Tuple[str, float, str]]:
    """ Reduce the number of competitors / states

    From every group of competitors / states that have the same fingers_position
    keep only the one with the smallest accumulated cost (Euclidean distance).

    :param state_list: list of states; state =
        (fingers_position, accumulated cost,  moved fingers sequence)
    :return: state_list: list of states; state =
        (fingers_position, accumulated cost,  moved fingers sequence)
    """

    # sort by finger_position
    state_list = sorted(state_list, key=lambda x: x[0])

    # group by finger_position and take the element with minimal cost
    new_state_list = []
    for k, g in itertools.groupby(state_list, key=lambda x: x[0]):
        min_item = min(g, key=lambda x: x[1])
        new_state_list.append(min_item)

    return new_state_list


def reformat_best_sequence(number_sequence: str, best_state: Tuple[str, float, str]) \
        -> Tuple[float, List[Tuple[str, str]]]:
    """ Map the finger sequence to the format expected by r***yr

    :param number_sequence: string of numbers that have to be pressed
    :param best_state: state =
        (fingers_position, accumulated cost,  moved fingers sequence)
    """

    _, cost, finger_sequence = best_state  # finger_sequence = 'LRLRLRLLRRR..'

    fingers_positions = ['*#']
    for number, finger in zip(number_sequence, finger_sequence):
        state = update_fingers_pos(x=number,
                                   finger=finger,
                                   fingers_pos_i=fingers_positions[-1])

        fingers_positions.append(state)

    fingers_positions = map(lambda x: (x[0], x[1]), fingers_positions)
    fingers_positions = list(fingers_positions)

    return cost, fingers_positions


def compute_laziest_path(telephone_number: str) -> Tuple[float, List[Tuple[str, str]]]:
    fingers_pos, cost, used_fingers = '*#', 0, ''

    initial_state = (fingers_pos, cost, used_fingers)

    state_list = [initial_state]

    for number in telephone_number:
        state_list = generate_new_states(number, state_list)
        state_list = reduce_new_states(state_list)

    best_state = min(state_list, key=lambda x: x[1])

    res = reformat_best_sequence(telephone_number, best_state)

    return res
