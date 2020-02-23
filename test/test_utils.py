from challenge.utils import *


def test_distance():
    a = np.array([0, 0])
    b = np.array([1, 1])
    assert dist_p2(a, b) == np.sqrt(2.)

    a = np.array([1, 1])
    b = np.array([2, 2])
    assert dist_p2(a, b) == np.sqrt(2.)

    a = np.array([1, 1])
    b = np.array([1, 4])
    assert dist_p2(a, b) == 3.

    a = np.array([1, 1])
    b = np.array([4, 5])
    assert dist_p2(a, b) == 5.


def test_transition_cost():
    assert fingers_pos_to_fingers_pos_transition_cost('*#', '2#') == np.sqrt(10.)
    assert fingers_pos_to_fingers_pos_transition_cost('*#', '*#') == 0.


def test_state_transition():
    state_i = ('*#', 0., '')
    assert move_finger('9', state_i, 'L') == ('9#', np.sqrt(5.), 'L')
    assert move_finger('9', state_i, 'R') == ('*9', 1., 'R')
    assert move_finger('*', state_i, 'R') is None


def test_reduce_new_states():
    states_list = [
        ('06', 4.414213562373095, 'RRRL'),
        ('0#', 5.650281539872885, 'LLLL'),
        ('08', 6.8863495173726745, 'RLLL'),
        ('09', 6.06449510224598, 'LRLL'),
        ('06', 4.414213562373095, 'LRRL'),
        ('06', 5.82842712474619, 'LLRL'),
        ('*0', 5.650281539872885, 'RRRR'),
        ('60', 4.414213562373095, 'LLLR'),
        ('60', 5.650281539872885, 'RLLR'),
        ('60', 5.242640687119285, 'LRLR'),
        ('80', 5.650281539872885, 'LRRR'),
        ('90', 6.650281539872885, 'LLRR')
    ]

    states_list = reduce_new_states(states_list)

    print(states_list)

    assert states_list == [
        ('06', 4.414213562373095, 'RRRL'),
        ('0#', 5.650281539872885, 'LLLL'),
        ('08', 6.8863495173726745, 'RLLL'),
        ('09', 6.06449510224598, 'LRLL'),
        ('*0', 5.650281539872885, 'RRRR'),
        ('60', 4.414213562373095, 'LLLR'),
        ('80', 5.650281539872885, 'LRRR'),
        ('90', 6.650281539872885, 'LLRR')
    ]


def test_reformat_best_sequence():
    number_sequence = '19602'
    best_state = ('02', 8.23606797749979, 'RRRLR')

    res = reformat_best_sequence(number_sequence=number_sequence, best_state=best_state)
    assert res == (8.23606797749979,
                   [('*', '#'), ('*', '1'), ('*', '9'), ('*', '6'), ('0', '6'), ('0', '2')])


def test_compute_laziest_path():
    number_sequence = '19602'
    res = compute_laziest_path(number_sequence)

    assert res == (8.23606797749979,
                   [('*', '#'), ('1', '#'), ('1', '9'), ('1', '6'), ('1', '0'), ('2', '0')])
