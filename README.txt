First, install the latest version of python from the link below. During installation, check the box that will add Python to your 'Path'.
	https://www.python.org/downloads/

Next, download the intsaller for the open-source, community version of PyCharm from the link below.
	https://www.jetbrains.com/pycharm/download/#section=windows

During installation, check boxes for "64-bit launcher" (to create a Desktop shortcut), and ".py" (you'll be running a python script). After clicking 'Next', continue with the default path. Launch PyCharm once it's installed, but don't create a new project yet.

Instead, select 'Get from Version Control' (or 'Get from VCS' depending on your machine). Under URL, copy and paste the following address to access the github repository: 		
	https://github.com/sudo-quinnmaloney/LFAreader

Below the URL, you can change the title of the project by changing the last portion of the location:
	'...\PycharmProjects\title_here' --> '...\PycharmProjects\LFAreader'

Below both of these boxes, if git is not installed there will be an option to install git. Select this.
Once git is installed, proceed with 'Clone' in the bottom left.

Select 'Terminal' in the bottom left of the IDE.
In the terminal, enter the command 'pip install opencv-python' to install OpenCV (the cv2 library).

Once this is done, you'll want to install the remaining packages on lines 1 through 6. You can do this easily by right clicking on the library names (each will be underlined in red as an 'unresolved reference') and opting to 'import package'.

Now simply drag and drop image directories into the project folder, and click the green play button in the top right to run the program. Turn your attention to the 'Run' terminal in the bottom half of the screen. When the program prompts you for the name of an image directory, type the name of the folder you want to process and press enter. Within the given folder, the program will create a folder of processed images, and a '.csv' file containing the data table.
