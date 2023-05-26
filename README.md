Program Control for Lego Mindstorms and Spike PRIME
===================================================

Presentation
------------
This repository contains all the code necessary to run a graphical interface that allows controlling the programs present on the hub and downloading new ones. This module has been tested on Windows 11 with Python 3.9.7 and Ubuntu with Python 3.10.6.

Module Configuration
--------------------

### Building the Module
1. Make sure you have installed the following dependencies on your machine: wheel, setuptools, and build. If not, on Debian/Ubuntu-based Linux systems, you can use your package manager: `apt install python3-build python3-setuptools python3-wheel`. For Windows, you can use pip directly and install these libraries at the user level: `py -m pip install --user --upgrade build pip setuptools wheel`.

2. You can now run the command `pyproject-build` at the root of the repository.

3. After that, a "dist" folder and another "programcontrol.egg-info" folder will be created. Ignore the "programcontrol.egg-info" file and go into the "dist" folder.

4. In this folder, two files have been created: "programcontrol-0.0.1-py3-none-any.whl" and "programcontrol-0.0.1.tar.gz". If you simply want to install it on your machine or in a virtual environment, choose the *.whl file. Now, copy the path of this file and simply execute the command `pip install <path to the file>/programcontrol-0.0.1-py3-none-any.whl` to install the module.

### Downloading the Module from GitHub
If you don't want to bother building the module, you can simply download the file "msprogramcontrol-1.0.0.zip" from the "Releases" section of the GitHub repository. Then, follow the last step for installation.

Usage
-----

### Launching the Graphical Interface
To use this module, write the following in a terminal: `python3 -m msprogramcontrol`(or `python` on Windows), and it will launch the graphical interface. If you want to specify a port to connect to, write `python3 -m msprogramcontrol -p <hub port>`(or `python` on Windows).

### Using the Module
This interface contains 3 buttons: a "Stop" button, a "Start" button, and an "Upload" button.

* To stop or start a program, choose the slot to be stopped or started by selecting the desired slot using the leftmost program location display.

* To upload a file to the hub, click on the "Choose a file" button, navigate to the location where the Python file you want to download to the hub is located. Now that the file is chosen, you can choose the location where the program will be downloaded using the rightmost program location display, then press the download button.

### The Terminal
Under the program management buttons, there is a terminal where program messages¹ and errors are displayed.

¹CAUTION: For a reason I cannot determine, all programs downloaded from this graphical interface that contain string prints do not appear, only those in integer or float work.. If you have a solution, please open a pull request.

Json-rpc code modified from https://github.com/nutki/spike-tools
