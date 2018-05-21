from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.pyplot as plt


def setAxis(ax, major, minor):
    xmajorLocator = MultipleLocator(major)
    xminorLocator = MultipleLocator(minor)
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.xaxis.grid(True, which='minor')