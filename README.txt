First, install the latest version of python from the link below. During installation, check the box that will add Python to your 'Path'.
	https://www.python.org/downloads/

Next, if you haven't already installed it, download the intsaller for the open-source, community version of PyCharm from the link below.
	https://www.jetbrains.com/pycharm/download/#section=windows

During installation, check boxes for "64-bit launcher" (to create a Desktop shortcut), and ".py" (you'll be running a python script). After clicking 'Next', continue with the default path. Launch PyCharm once it's installed, but don't create a new project yet.

Instead, select 'Get from Version Control' (or 'Get from VCS' depending on your machine). Under URL, copy and paste the following address to access the github repository: 		
	https://github.com/sudo-quinnmaloney/LFAreader

Below the URL, you can change the title of the project by changing the last portion of the location:
	'...\PycharmProjects\title_here' --> '...\PycharmProjects\LFAreader'

Below both of these boxes, if git is not installed there will be an option to install git. Select this.
Once git is installed, proceed with 'Clone' in the bottom left.

If you had PyCharm installed previously, ensure that the project is utilizing the latest version of python (v3.9). You can do this on Windows and Linux by clicking File, Settings, Project, Python Interpreter - or on macOS by clicking PyCharm, Preferences, Project, Python Interpreter - AFTER highlighting the cloned project in the project pane on the left side of the display. Once the project is using the most recent version of python, we can begin installing dependencies.

Select 'Terminal' in the bottom left of the IDE.
In the terminal, enter the command 'pip install opencv-python' to install OpenCV (the cv2 library).

Once this is done, click the green play button in the top right to run the program. If the play button is unclickable, right click on 'LFAreader.py' and click the green play button. This will underline the remaining packages on lines 1 through 6 of the code that need to be installed. You can do this easily by hovering your cursor over the underlined names of the libraries (each will be underlined in red as an 'unresolved reference') and opting to 'install package'.

Now simply drag and drop image directories into the project folder (shown in the top left of the window, a folder with the title you assigned the project earlier), and click the green play button in the top right to run the program. Turn your attention to the 'Run' terminal in the bottom half of the screen. When the program prompts you for the name of an image directory, type the name of the folder you want to process and press enter. Within the given folder, the program will create a folder of processed images, and a '.csv' file containing the data table.

The code will run in a loop, type 'quit' to escape or 'help' for all options.
