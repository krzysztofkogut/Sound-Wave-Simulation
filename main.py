from sys import argv

import matplotlib
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.colors import LinearSegmentedColormap, colorConverter

from simulation_single import Simulation, minPressure, maxPressure, wall
from simulation_multi import Simulation2, wall_multi

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


if len(argv) == 1:
	print()
	print("Type -h or --help for help")
	print()

if len(argv) > 1 and (argv[1] == '-h' or argv[1] == '--help'):
	print("SYNOPSIS")
	print("	python main.py [wall_option] [single | multi]")
	print("")
	print("	[wall_option] - opcja scian, 1-9 (dla single), 1-8 (dla multi)")
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
	plt.ylabel("Położenie y[cells]")
	plt.xlabel("Położenie x[cells]")
	cbar = plt.colorbar(ca_plot_single)
	cbar.set_label("Amplitude")
	transparent = colorConverter.to_rgba('black', alpha=0)
	wall_colormap = LinearSegmentedColormap.from_list('my_colormap', [transparent, 'black'], 2)
	plt.imshow(wall, cmap=wall_colormap, interpolation='bilinear', zorder=2)

	if len(argv) > 3 and argv[3] == 'save':
		writer = FFMpegWriter(fps=30)
		frames = 100
		with writer.saving(figure, "writer_test.mp4", 200):
			for i in range(frames):
				animation_func_single(i)
				writer.grab_frame()
				print(f'\rframe: {i}/{frames}', end='')

	else:
		animation = FuncAnimation(figure, animation_func_single, interval=1)
		mng = plt.get_current_fig_manager()
		mng.window.showMaximized()
		plt.title("Beta version - Single Source, 50 cells -> 1m")


elif len(argv) > 2 and argv[2] == "multi":
	simulation_multi = Simulation2()
	figure = plt.figure()
	ca_plot_multi = plt.imshow(simulation_multi.pressure, cmap='seismic', interpolation='bilinear',
							   vmin=minPressure, vmax=maxPressure)
	plt.ylabel("Położenie y[cells]")
	plt.xlabel("Położenie x[cells]")
	cbar = plt.colorbar(ca_plot_multi)
	cbar.set_label("Amplitude")
	transparent = colorConverter.to_rgba('black', alpha=0)
	wall_colormap = LinearSegmentedColormap.from_list('my_colormap', [transparent, 'black'], 2)
	plt.imshow(wall_multi, cmap=wall_colormap, interpolation='bilinear', zorder=2)

	if len(argv) > 3 and argv[3] == 'save':
		writer = FFMpegWriter(fps=30)
		frames = 100
		with writer.saving(figure, "writer_test.mp4", 200):
			for i in range(frames):
				animation_func_multi(i)
				writer.grab_frame()
				print(f'\rframe: {i}/{frames}', end='')

	else:
		animation = FuncAnimation(figure, animation_func_multi, interval=1)
		mng = plt.get_current_fig_manager()
		mng.window.showMaximized()
		plt.title("Beta version - Multi source, 50 cells -> 1m")

plt.show()
