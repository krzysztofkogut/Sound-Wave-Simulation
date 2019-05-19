from sys import argv

import matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap, colorConverter

from simulation_single import Simulation, min_presure, max_pressure, scale, wall, size_y
from simulation_multi import Simulation2, min_presure, max_pressure, scale, wall, size_y

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

if len(argv) > 2 and argv[2] == 'single':
	with plt.style.context(('dark_background')):
		simulation_single = Simulation()
		figure = plt.figure()
		ca_plot_single = plt.imshow(simulation_single.pressure, cmap='seismic', interpolation='bilinear',
									vmin=min_presure, vmax=max_pressure)
		plt.colorbar(ca_plot_single)
		transparent = colorConverter.to_rgba('black', alpha=0)
		wall_colormap = LinearSegmentedColormap.from_list('my_colormap', [transparent, 'black'], 2)
		plt.imshow(wall, cmap=wall_colormap, interpolation='bilinear', zorder=2)

	animation = FuncAnimation(figure, animation_func_single, interval=1)
	mng = plt.get_current_fig_manager()
	mng.window.showMaximized()
	plt.title("Beta version - Single Source")

elif len(argv) > 2 and argv[2] == 'multi':
	with plt.style.context(('dark_background')):
		simulation_multi = Simulation2()
		figure = plt.figure()
		ca_plot_multi = plt.imshow(simulation_multi.pressure, cmap='seismic', interpolation='bilinear',
								   vmin=min_presure, vmax=max_pressure)
		plt.colorbar(ca_plot_multi)
		transparent = colorConverter.to_rgba('black', alpha=0)
		wall_colormap = LinearSegmentedColormap.from_list('my_colormap', [transparent, 'black'], 2)
		plt.imshow(wall, cmap=wall_colormap, interpolation='bilinear', zorder=2)

	animation = FuncAnimation(figure, animation_func_multi, interval=1)
	mng = plt.get_current_fig_manager()
	mng.window.showMaximized()
	plt.title("Beta version - Multi source")

"""
def submit(text):
    animation = FuncAnimation(figure, animation_func, interval=1)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.title(f"1 m -> {scale} cells, 1 cell -> {1 / scale}m")
    

axbox = plt.axes([0.15, 0.009, 0.5, 0.05])
text_box = TextBox(axbox, 'Evaluate', initial="test")
text_box.on_submit(submit)
"""

plt.show()
