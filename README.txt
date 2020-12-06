First, download the Anaconda Graphical Installer for Python 3.7
Accept default settings, and select 'Install only for me' when given the option.
 and follow installation instructions:
	https://www.anaconda.com/products/individual




Next, follow these instructions to download the OpenCV Python library:
	https://medium.com/@pranav.keyboard/installing-opencv-for-python-on-windows-using-anaconda-or-winpython-f24dd5c895eb


If you chose “All users” while installing then you have to launch the prompt by Right-clicking and choosing “Run as Administrator” to execute with administrator privileges. This is critical.

Run the following commands in the given order. These create a virtual environment for the program to run on, and installs a necessary library.

>conda create — name LFAreader
>activate LFAreader
>conda install -c conda-forge opencv

