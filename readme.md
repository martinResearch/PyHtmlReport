# Project's goals

This is a small class that can help in generating Html reports for your scientific code with images, matplotlib 2D and 3D graphs, and numeric numpy arrays in Python.

it use mpl3D in order to convert 2D matplotlib figure into html

Mpl3D does not seem to support 3D plots. We could use the javascript library 
[visjs](http://visjs.org/index.html) or [3d-charts](https://plot.ly/javascript/#3d-charts)
to do 3D plots

Instead of using mpl3D for the 2D plot we could generate a json string from the matplotlib figure in a format that is used by [plotly](ttps://plot.ly/javascript/). Plotly.js has a richer set of button to navigate 2D plots. Plotly.js is the javascript part part of the larger libray plotly. It builts on top of d3.js and stack.gl, plotly.js is a high-level, declarative charting library. Plotly.js ships with 20 chart types, including 3D charts, statistical graphs, and SVG maps. 
plotly.js is open source, not the larger libray plotly.
plotly commes with a tool to convert matlplotlibe figure to a format used by plotly.js , but this tool is note free to use.

# installation

it uses [mpld3](https://github.com/mpld3/mpld3)

	sudo pip2.7 install mpld3 

# Examples


## Similar projects

* [html](https://pypi.python.org/pypi/html)

* [markup.py](http://markup.sourceforge.net/) *"Markup.py is an intuitive, light weight, easy-to-use, customizable and pythonic HTML/XML generator."* PyHtmlReport differs from markup.py in that it provides simple function to add numeric arrays matplotlib graphs etc.

* [yattag](http://www.yattag.org/). Pythonic interface to generate html. Gnertic, no specialization to display scientific results.

* [dominate](https://github.com/Knio/dominate) Pythonic interface to generate html. Gnertic, no specialization to display scientific results.


similar projets in other languages:

* Matlab : [htmlWriter](https://github.com/imisra/htmlWriter)







