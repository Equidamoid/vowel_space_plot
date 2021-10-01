from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import sys


def split_by_time(d):
    current = []
    ret = []
    last_t = 99999
    for i in d:
        if i[0] < last_t:
            current = []
            ret.append(current)
        current.append(i)
        last_t = i[0]

    return list(map(np.array, ret))

def main():
    data_fn = Path('example.txt')
    try:
        data_fn = Path(sys.argv[1])
    except IndexError:
        pass
    data_indexes = []
    # fields to use, <time> <Y>, <X>
    field_names = ['v_time', 'F2', 'F1']
    data = {}
    with data_fn.open() as f:
        for line in f:
            parts = line.split()
            print(parts)
            if 'F1' in line:
                fields = parts
                data_indexes = list(map(fields.index, field_names))
                continue

            key = parts[0]
            data.setdefault(key, [])
            data[key].append([float(parts[i]) for i in data_indexes])

    fig, ax = plt.subplots()
    ax.xaxis.tick_top()
    ax.yaxis.tick_right()
    plt.xlabel(f'{field_names[1]}, Hz')
    ax.xaxis.set_label_position('top')
    plt.ylabel(f'{field_names[2]}, Hz')
    ax.yaxis.set_label_position('right')
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()

    for k in list(data):
        color = next(ax._get_lines.prop_cycler)['color']
        d = np.array(data[k])
        print(d)
        s = split_by_time(d)
        for track in split_by_time(d):
            print(track)
            print(track[:, 1])
            print(track[:, 2])
            # print(np.diff(track[:, 0]))
            plt.plot(track[:, 1], track[:, 2], color = color)
            plt.text(track[-1, 1], track[-1, 2], k,
                     bbox=dict(
                         boxstyle="round",
                         ec=(1., 0.5, 0.5),
                         fc=(1., 0.8, 0.8),
            ))
    plt.show()

if __name__ == '__main__':
    main()