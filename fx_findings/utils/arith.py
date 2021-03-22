def avg(l):
    return sum(l)/len(l)


def avg_dict(d):
    return {key:avg(val) for key,val in d.items()}