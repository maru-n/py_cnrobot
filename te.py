import random
import numpy as np
from jpype import *

CH_NUM = 126


def calc_all_channel(bit_data, history=3):
    base = 2
    # calc te each channels
    te_array = np.zeros(shape=(len(bit_data), len(bit_data)))
    for di, dst in enumerate(bit_data):
        for si, src in enumerate(bit_data):
            te = calc(dst.tolist(), src.tolist(), base=base, history=history)
            te_array[si, di] = te
    return te_array


def convert_data_to_bit(rawdata, time_window=1, time_min=0, time_max=None):
    if time_max is None:
        time_max = rawdata[-1][0]
    time_bins = int((time_max - time_min) / time_window)
    bit_data = np.zeros(shape=(CH_NUM, time_bins), dtype=np.int)
    for d in rawdata:
        time = d[0]
        if time < time_min:
            continue
        if time >= time_max:
            break
        time_idx = int((time - time_min) / time_window)
        ch = int(d[1])
        bit_data[ch][time_idx] = 1
    return bit_data


def get_test_bit_data(data_length=100):
    data1 = [random.randint(0, 1) for r in xrange(data_length)]
    data2 = [random.randint(0, 1) for r in xrange(data_length)]
    data3 = [0] + data1[0:data_length-1]
    bit_data = np.array([data1, data2, data3])
    return bit_data


def calc(destArray, srcArray, base=2, history=1):
    jarLocation = "./infodynamics.jar"
    if not isJVMStarted():
        startJVM(getDefaultJVMPath(),
                 " -Xmx2048m",
                 " -Xms2048m",
                 "-Djava.class.path=" + jarLocation)

    package_name = "infodynamics.measures.discrete"
    teCalcClass = JPackage(package_name).ApparentTransferEntropyCalculator

    teCalc = teCalcClass(base, history)
    teCalc.initialise()
    teCalc.addObservations(destArray, srcArray)
    te = teCalc.computeAverageLocalOfObservations()
    #shutdownJVM()

    #del _jclass.__javaobject__

    return te
