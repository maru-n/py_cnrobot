#!/usr/bin/env python

import sys
import numpy as np
import __init__ as cnr
import pdb


def convert_and_save_data(
        channel_input_filename,
        stimulus_input_filename,
        output_filename_prefix,
        time_window_list):

    print "...loading channel data."
    data_channel = load_channel_data_by_time_order(channel_input_filename)

    print "...loading stimulus data."
    data_stimulus = load_stimulus_data_by_time_order(stimulus_input_filename)

    print "...merging data."
    data = merge_channel_and_stimulus_data(data_channel, data_stimulus)

    print "...cutting data by time."
    first_stimulus_time = data_stimulus[0, 0]
    data = cut_data(data, first_stimulus_time)

    print "...sorting data by time."
    data = cnr.util.sort_data(data)

    print "...formatting time stamp."
    start_time = data[0, 0]
    data = np.array([[d[0] - start_time] + d[1:].tolist() for d in data])

    print "...saving."
    headder_comment = ("spike data: [time, channel, x, y]")
    out_filename = output_filename_prefix
    save_csv_and_npy(data, out_filename, headder_comment)

    #data = np.load("test.npy")
    for time_window in time_window_list:
        print "#time window=%f" % time_window
        convert_and_save_spike_matrix(data, time_window)


def convert_and_save_spike_matrix(data, time_window):
    print "...converting to spike num matrix."
    spikenum_matrix = cnr.util.get_time_channel_matrix(data, time_window)

    print "...saving."
    headder_comment = ("number of spikes: "
                       "row=time(per %f sec); col=channel;") % time_window
    out_filename = "%s_%f" % (output_filename_prefix, time_window)
    save_csv_and_npy(spikenum_matrix, out_filename, headder_comment)

    print "...converting to binary matrix."
    bin_matrix = convert_spikenum2binary(spikenum_matrix)

    print "...saving"
    headder_comment = ("0/1 spike: "
                       "row=time(per %f sec); col=channel;") % time_window
    out_filename = "%s_bin_%f" % (output_filename_prefix, time_window)
    save_csv_and_npy(bin_matrix, out_filename, headder_comment)


def cut_data(data, reference_time,
             time_duration_before_reference=3600.,
             time_duration_after_reference=7200.):
    data = np.array(
        filter(
            lambda d:
            reference_time - time_duration_before_reference < d[0]
            and
            reference_time + time_duration_after_reference > d[0],
            data))
    return data


def merge_channel_and_stimulus_data(data_channel, data_stimulus):
    data = np.concatenate((data_channel, data_stimulus))
    return data


def convert_spikenum2binary(spikenum_matrix):
    mtx = [[1 if v > 0 else 0 for v in row] for row in spikenum_matrix]
    mtx = np.array(mtx)
    return mtx


def save_csv_and_npy(data, filename, headder_comment):
    np.save(filename + ".npy", data)
    """
    np.savetxt(filename + ".csv", data, delimiter=",", fmt='%d',
               comments="#", header=headder_comment)
    """


def load_channel_data_by_time_order(filename):
    cd = cnr.util.load_data(filename,
                            cut_time_offset=False,
                            sort_by_time=True,
                            context_cleaned=False,
                            load_context=False)
    data_channel = cnr.util.get_channels_data(
        cd, xrange(0, cnr.util.DATA_CH_NUM))
    return data_channel


def load_stimulus_data_by_time_order(filename):
    sd = cnr.util.load_data(filename,
                            cut_time_offset=False,
                            sort_by_time=True,
                            context_cleaned=False,
                            load_context=False)

    data_stimulus = cnr.util.get_channels_data(
        sd, xrange(cnr.util.DATA_CH_NUM, cnr.util.CH_NUM))
    if len(data_stimulus) == 0:
        raise ValueError("Thid file have no stimulus data")
    return data_stimulus


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print ("usage: cnr-convert.py "
               "[channel_input_filename] [stimulus_input_filename] "
               "[output_filename_previx] [time_window(sec)]+")
        sys.exit()

    channel_input_filename = sys.argv[1]
    stimulus_input_filename = sys.argv[2]
    output_filename_prefix = sys.argv[3]
    time_window_list = [float(v) for v in sys.argv[4:]]

    convert_and_save_data(channel_input_filename,
                          stimulus_input_filename,
                          output_filename_prefix,
                          time_window_list)
