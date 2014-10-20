import struct
import numpy as np

DATA_CH_NUM = 126
INPUT_CH_NUM = 2
CH_NUM = DATA_CH_NUM + INPUT_CH_NUM


def arg_param(param, arg_index):
    try:
        ret = sys.argv[arg_index]
    except Exception, e:
        ret = param
    return ret


def load_data(filename, cut_time_offset=True, sort_by_time=False,
              context_cleaned=False, load_context=False):
    f = open(filename)
    if context_cleaned:
        bin_fmt = 'Q h h h'
    else:
        bin_fmt = 'Q h h h 74h h h h'

    bin_size = struct.calcsize(bin_fmt)

    data = []

    if cut_time_offset:
        start_time = None
    else:
        start_time = 0.

    time_sorted = True
    pre_time = -1

    while True:

        bindata = f.read(bin_size)

        if len(bindata) != bin_size:
            if len(bindata) != 0:
                msg = "Error: not converted data size: %d" % (len(bindata))
                print msg
                #raise ValueError(msg)
            break

        d = list(struct.unpack(bin_fmt, bindata))

        if start_time is None:
            start_time = d[0]

        d[0] = convert_original_time_to_sec(d[0], start_time)

        if not load_context:
            d = [d[0], int(d[1]), d[2], d[3]]

        if pre_time > d[0]:
            time_sorted = False
        pre_time = d[0]
        data.append(d)

    f.close()

    data = np.array(data)

    if not time_sorted:
        if sort_by_time:
            data = sort_data(data)
        else:
            print "Warning: This data is not sorted by time."

    return data


def sort_data(data):
    result = sorted(data, key=lambda d: d[0])
    return np.array(result)


def convert_original_time_to_sec(org_time, time_offset):
    return (org_time - time_offset) / 20000.


def calc_spike_num(data, sampling_freq):
    return np.histogram(data[:, 0],
                        bins=(data[-1, 0] - data[0, 0]) * sampling_freq)


def get_spike_shape(data):
    if data.ndim == 1:
        return np.array(data[4:78])
    elif data.ndim == 2:
        return np.array(data[:, 4:78])
    else:
        raise ValueError("get_spike_shape error.")


def get_channel_data(data, ch):
    return np.array([d for d in data if d[1] == ch])


def get_channels_data(data, channels):
    return np.array([d for d in data if d[1] in channels])


def check_data_file(filename):
    print "....loading data"
    data = load_data(filename, cut_time_offset=False)
    print "....analyzing data"
    min_time = None
    pre_time = -1.0
    inversed_data = []
    for i, d in enumerate(data):
        time = d[0]
        if (min_time is None) or (time < min_time):
            min_time = time
        if pre_time > time:
            inversed_data.append(d)
        pre_time = time
    print "\n##Report##"
    print "Data point: %d" % data.shape[0]
    print "First data time: %f" % (data[0][0])
    print "Minimum time: %f" % (min_time)
    print "Inversed data point: %d" % (len(inversed_data))


def get_time_channel_matrix_regacy(data, time_window=1.0):
    matrix = [[0] * CH_NUM]
    current_window_start_time = data[0, 0]
    pre_time = -1
    for i, d in enumerate(data):
        time = d[0]
        if pre_time > time:
            raise ValueError(("This data is not sorted. "
                              "please sort before convert"))
        pre_time = time
        while current_window_start_time + time_window < time:
            matrix.append([0] * CH_NUM)
            current_window_start_time += time_window
        ch = int(d[1])
        matrix[-1][ch] += 1

    return np.array(matrix, dtype=int)


def get_time_channel_matrix(data,
                            time_window=0.01,
                            time_duration=10800,
                            dt=0.01):
    time_data_size = int(time_duration / dt)
    tc_matrix = np.zeros((time_data_size, CH_NUM), dtype=int)

    pre_time = -1
    for i, d in enumerate(data):
        time = d[0]
        if pre_time > time:
            raise ValueError(("This data is not sorted. "
                              "please sort before convert"))
        t_index_start = int((time - time_window) / dt)
        t_index_end = int(time / dt)
        for r in tc_matrix[t_index_start:t_index_end]:
            ch = int(d[1])
            r[ch] += 1

    return tc_matrix
