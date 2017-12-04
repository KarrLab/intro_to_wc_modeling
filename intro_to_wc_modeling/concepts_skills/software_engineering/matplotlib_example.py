""" matplotlib example

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-07-11
:Copyright: 2017, Karr Lab
:License: MIT
"""

import matplotlib
import numpy
import os

# set backend
matplotlib.use('Agg')  # for non-interactive usage, e.g. on servers
# matplotlib.use('TkAgg') # for GUI display

from matplotlib import pyplot


def main():
    # create a figure with 2x1 subplots
    fig, axes = pyplot.subplots(nrows=2, ncols=1)

    # plot data on the subplots
    axis = axes[0]
    x = numpy.linspace(0., numpy.pi * 2., 100)
    y0 = numpy.sin(x)
    y1 = numpy.cos(x)
    line0, = axes[0].plot(x, y0, label='sin(x)')
    line1, = axes[1].plot(x, y1, label='cos(x)')

    # set line color, style
    line0.set_color((1, 0, 0))  # set color to red
    line0.set_linewidth(2.)

    line1.set_color((0, 1, 0))  # set color to green
    line1.set_linewidth(2.)

    # set axes limits
    axes[0].set_xlim([0, numpy.pi * 2])
    axes[0].set_ylim([-1, 1])

    axes[1].set_xlim([0, numpy.pi * 2])
    axes[1].set_ylim([-1, 1])

    # set axes ticks
    axes[0].set_xticks([0, numpy.pi / 2, numpy.pi, numpy.pi * 3 / 2, numpy.pi * 2])
    axes[0].set_yticks([-1, -0.5, 0, 0.5, 1])

    axes[1].set_xticks([0, numpy.pi / 2, numpy.pi, numpy.pi * 3 / 2, numpy.pi * 2])
    axes[1].set_yticks([-1, -0.5, 0, 0.5, 1])

    # add title and axis labels
    axes[0].set_title(r'$\sin{x}$')
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('Y')

    axes[1].set_title(r'$\cos{x}$')
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('Y')

    # add annotations
    line0.set_markevery([50])
    line0.set_marker('o')
    axes[0].text(numpy.pi, 0, r'$(\pi, 0)$')

    # turn off axis border
    axes[0].spines['top'].set_visible(False)
    axes[0].spines['right'].set_visible(False)

    axes[1].spines['top'].set_visible(False)
    axes[1].spines['right'].set_visible(False)

    # turn on grid
    axes[0].grid(True)
    axes[1].grid(True)

    # add legend
    axes[0].legend()
    axes[1].legend()

    # display figure
    # fig.show()

    # save figure
    png_filename = os.path.join(os.path.dirname(__file__), '../../../docs/concepts_skills/software_engineering/matplotlib-example.png')
    fig.savefig(png_filename, transparent=True, bbox_inches='tight')  # save in png format

    pdf_filename = os.path.join(os.path.dirname(__file__), '../../../docs/concepts_skills/software_engineering/matplotlib-example.pdf')
    fig.savefig(pdf_filename, transparent=True, bbox_inches='tight')  # save in pdf format

    os.remove(pdf_filename)
