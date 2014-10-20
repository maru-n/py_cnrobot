#import pyximport; pyximport.install()
import random
import struct
import numpy as np


CH_NUM = 126

def load_data_legacy(filename, cut_time_offset=True,
                     context_cleaned=False, load_context=False):
    f = open(filename)
    if context_cleaned:
        bin_fmt = 'Q h h h'
    else:
        bin_fmt = 'Q h h h 74h h h h'

    bin_size = struct.calcsize(bin_fmt)

    data = []
    data_input1 = []
    data_input2 = []

    start_time = -1

    while True:

        bindata = f.read(bin_size)

        if len(bindata) != bin_size:
            if len(bindata) != 0:
                print "Error: not converted data size: " + str(len(data))
            break

        d = list(struct.unpack(bin_fmt, bindata))

        if start_time == -1:
            start_time = d[0]
            continue
        if start_time == d[0]:
            continue

        if cut_time_offset:
            d[0] = (d[0] - start_time) / 20000.
        else:
            d[0] = d[0] / 20000.

        if not load_context:
            d = [d[0], int(d[1]), d[2], d[3]]

        if int(d[1]) == CH_NUM - 2:
            data_input1.append(d)
        elif int(d[1]) == CH_NUM - 1:
            data_input2.append(d)
        else:
            data.append(d)

    f.close()

    return np.array(data), np.array(data_input1), np.array(data_input2)


def load_data_legacy_legacy(filename, cut_time_offset=True):
    f = open(filename)

    bin_fmt = 'Q h h h 74h h h h'
    bin_size = struct.calcsize(bin_fmt)

    data = []

    start_time = -1

    while True:
        bindata = f.read(bin_size)

        if len(bindata) != bin_size:
            if len(bindata) != 0:
                print "Error: not converted data saze: "+str(len(data))
            break

        d = list(struct.unpack(bin_fmt, bindata))

        if start_time == -1:
            start_time = d[0]
            continue

        if start_time == d[0]:
            continue

        #convert time range for msec
        if cut_time_offset:
            d[0] = (d[0] - start_time) / 20000.
        else:
            d[0] = d[0] / 20000.
        data.append(d)

    f.close()
    data = np.array(data)
    return data


def plot_spike_laster()


def calc_te_in_channel(filename, time_window=1, history=3, time_min=0, time_max=None, output_filename=None):
    """
    rawdata = load_data(filename, cut_time_offset = True)
    bit_data = convert_raw_to_bit(rawdata, time_window=time_window, time_min=time_min, time_max=time_max)
    """

    #for debug
    num = 100
    data1 = [random.randint(0, 1) for r in xrange(num)]
    data2 = [random.randint(0, 1) for r in xrange(num)]
    data3 = [0] + data1[0:num-1]
    bit_data = np.array([data1, data2, data3])

    # calc te each channels
    if output_filename != None:
        outf = open(output_filename, 'w')
    te_array = np.zeros(shape=(len(bit_data),len(bit_data)))
    for di, dst in enumerate(bit_data):
        for si, src in enumerate(bit_data):
            te = calc_te(dst.tolist(), src.tolist(), base=2, history=history)
            if output_filename != None:
                outf.write(str(te))
                outf.write(' ')
            te_array[di,si] = te
        if output_filename != None:
            outf.write('\n')
    return te_array

def convert_raw_to_bit(rawdata, time_window=1, time_min=0, time_max=None):
    if time_max == None:
        time_max = rawdata[-1][0]
    time_bins = int(( time_max - time_min ) / time_window)
    bit_data = np.zeros(shape=(CH_NUM,time_bins), dtype=np.int)
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

def get_channel_pos_from_configfile(filename, channel):
    config = np.loadtxt(filename)
    for c in config:
        if int(c[0]) == channel:
            return c[2],c[3]

    return None

"""
def convert_channel_form(data):
    channel_num = 126
    data = [[]]*ch_num
    for i in range(channel_num):
        data.append(np.array(get_channel_data(i)))
"""

def get_channel_data(data, ch):
    return np.array([ d for d in data if d[1]==ch])

def get_spike_shape(data):
    if data.ndim == 1:
        return np.array(data[4:78])
    elif data.ndim == 2:
        return np.array(data[:,4:78])
    else:
        raise CNRobotUtilError()

def get_channels_data(data, channels):
    return np.array([ d for d in data if d[1] in channels])

def calc_te(destArray, srcArray, base=2, history=1):
    #global teCalc
    # Create a TE calculator and run it:
    #teCalcClass = JPackage("infodynamics.measures.discrete").ApparentTransferEntropyCalculator
    teCalc = teCalcClass(base, history)
    teCalc.initialise()
    teCalc.addObservations(destArray, srcArray)
    te = teCalc.computeAverageLocalOfObservations()
    #shutdownJVM()
    del teCalc

    return te

class CNRobotUtilError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
       return str(self.msg)

from jpype import *
import sys

jarLocation = "./infodynamics.jar"
if not isJVMStarted():
    startJVM(getDefaultJVMPath(),
        " -Xmx2048m",
        " -Xms2048m",
        "-Djava.class.path=" + jarLocation)

teCalcClass = JPackage("infodynamics.measures.discrete").ApparentTransferEntropyCalculator



