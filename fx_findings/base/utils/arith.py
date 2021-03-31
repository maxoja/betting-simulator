import numpy as np


def avg(l):
    return sum(l)/len(l)


def avg_dict(d):
    return {key:avg(val) for key,val in d.items()}


def sorted_dict(d):
    return { k:d[k] for k in sorted(d.keys()) }


def merge_dict_of_lists(dicts):
    result = {}
    for d in dicts:
        for k, v in d.items():
            if not k in result:
                result[k] = v
            else:
                result[k] += v
    return result



def shift_right_with_nan(a):
    a = np.concatenate(([np.NaN], a))
    a = a[:-1]
    return a


def shift_left(a, val=np.NaN):
    a = np.concatenate((a,[val]))
    a = a[1:]
    return a

def remove_nan(a):
    non_nan_idx = np.isnan(a)
    return a[~non_nan_idx]