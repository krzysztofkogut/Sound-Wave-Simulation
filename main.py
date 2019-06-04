from sys import argv

import matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap, colorConverter

from simulation_single import Simulation, minPressure, maxPressure, wall
from simulation_multi import Simulation2, wall

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

def animation_func_single(i):
	simulation_single.step()
	ca_plot_single.set_data(simulation_single.pressure)
	return ca_plot_single

def animation_func_multi(i):
	simulation_multi.step()
	ca_plot_multi.set_data(simulation_multi.pressure)
	return ca_plot_multi

if len(argv) > 1 and (argv[1] == '-h' or argv[1] == '--help'):
	print("SYNOPSIS")
	print("	python main.py [wall_option] [single | multi]")
	print("")
	print("	[wall_option] - opcja scian, 1-7 (dla single), 1-8 (dla multi)")
	print("	[single] - jedno źródło ")
	print("	[multi] - dwa źródła")
	print("DESCRIPTION")
	print("	-h, --help ")
	print("		Display this help and exit")

elif len(argv) > 2 and argv[2] == 'single':
	simulation_single = Simulation()
	figure = plt.figure()
	ca_plot_single = plt.imshow(simulation_single.pressure, cmap='seismic', interpolation='bilinear',
								vmin=minPressure, vmax=maxPressure)
	plt.colorbar(ca_plot_single)
	transparent = colorConverter.to_rgba('black', alpha=0)
	wall_colormap = LinearSegmentedColormap.from_list('my_colormap', [transparent, 'black'], 2)
	plt.imshow(wall, cmap=wall_colormap, interpolation='bilinear', zorder=2)

	animation = FuncAnimation(figure, animation_func_single, interval=1)
	mng = plt.get_current_fig_manager()
	mng.window.showMaximized()
	plt.title("Beta version - Single Source")

elif len(argv) > 2 and argv[2] == 'multi':
	simulation_multi = Simulation2()
	figure = plt.figure()
	ca_plot_multi = plt.imshow(simulation_multi.pressure, cmap='seismic', interpolation='bilinear',
							   vmin=minPressure, vmax=maxPressure)
	plt.colorbar(ca_plot_multi)
	transparent = colorConverter.to_rgba('black', alpha=0)
	wall_colormap = LinearSegmentedColormap.from_list('my_colormap', [transparent, 'black'], 2)
	plt.imshow(wall, cmap=wall_colormap, interpolation='bilinear', zorder=2)

	animation = FuncAnimation(figure, animation_func_multi, interval=1)
	mng = plt.get_current_fig_manager()
	mng.window.showMaximized()
	plt.title("Beta version - Multi source")

plt.show()
