import os
import sys
import cnrobot_util as cu
import csv
import shutil


def operate_output_directory(output_dirname):
    if os.path.exists(output_dirname):
        print str(output_dirname) + '" is already exist.'
        is_all_remove = raw_input('Recalclate all? [y|n]> ')
        if is_all_remove in ['y', 'Y']:
            shutil.rmtree(output_dirname)
            os.mkdir(output_dirname)


def save_all_spike_data(data):
    print "saving all spike data."
    output_file = os.path.join(output_dirname, "all_spike.csv")
    if os.path.exists(output_file):
        return

    csvfile = csv.writer(file(output_file, 'w'))
    csvfile.wrcsviterow(["# time", " channel", " x", " y"])
    csvfile.writerows(data[:, 0:4])


def usage():
    print ('Usage: '
           'python cnrobot_analyzer.py '
           '[input file name] [output directory name(optional)]')

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        usage()
        sys.exit()

    input_filename = sys.argv[1]
    if len(sys.argv) == 3:
        output_dirname = sys.argv[2]
    else:
        output_dirname = input_filename + ".data"

    operate_output_directory(output_dirname)

    print "loading data."
    data, data_input1, data_input2 = cu.load_data(input_filename,
                                                  cut_time_offset=True,
                                                  load_context=False)

    save_all_spike_data(data)
