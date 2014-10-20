from pylab import *


def spike_laster(data, data_input1=None, data_input2=None,
                 xmin=0, xmax=None,
                 fig_width=20, fig_height=3,
                 subplot_row=1, subplot_col=1, subplot_num=1):

    if xmax is None:
        xmax = data[-1, 0]

    figure(figsize=(fig_width, fig_height))
    subplot(subplot_row, subplot_col, subplot_num)
    xlim(xmin, xmax)
    ylim(0, 130)
    plot(data[:, 0], data[:, 1], ',', color='blue')
    if data_input1 is not None and len(data_input1) != 0:
        plot(data_input1[:, 0], data_input1[:, 1],
             '.', color='red')
    if data_input2 is not None and len(data_input2) != 0:
        plot(data_input2[:, 0], data_input2[:, 1]+3,
             '.', color='green')
        #show()


def spike_laster_all(data, data_input1=None, data_input2=None,
                     graph_length=None,
                     fig_width=20, fig_height=1):
    if graph_length is None:
        graph_length = int(data[-1, 0])

    graph_num = int(data[-1, 0]/graph_length)+1
    figure(figsize=(fig_width, fig_height*graph_num))
    for i, x in enumerate(xrange(0, int(data[-1, 0]), graph_length)):
        xmin = x
        xmax = x + graph_length
        subplot(graph_num, 1, i+1)
        xlim(xmin, xmax)
        ylim(0, 130)
        plot(data[:, 0], data[:, 1], ',', color='blue')
        if data_input1 is not None and len(data_input1) != 0:
            plot(data_input1[:, 0], data_input1[:, 1],
                 '.', color='red')
        if data_input2 is not None and len(data_input2) != 0:
            plot(data_input2[:, 0], data_input2[:, 1]+3,
                 '.', color='green')

    """
        spike_laster(data,
                     data_input1=data_input1,
                     data_input2=data_input2,
                     xmin=xmin, xmax=xmax,
                     fig_width=fig_width, fig_height=fig_height,
                     subplot_row=graph_num, subplot_col=1,
                     subplot_num=i)
    """


def te(te_data, fig_width=7, fig_height=5):
    figure(figsize=(fig_width, fig_height))
    N = te_data.shape[0]
    x = arange(N+1)
    y = arange(N+1)
    Z = te_data
    X, Y = meshgrid(x, y)
    pcolor(X, Y, Z)
    colorbar()
    xlabel("Destination channel")
    ylabel("Source channel")
    xlim(0, N)
    ylim(0, N)
    show()
