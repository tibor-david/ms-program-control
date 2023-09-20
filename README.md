Program Control for Lego Mindstorms and Spike PRIME
===================================================

Presentation
------------
This repository contains all the code necessary to run a graphical interface that allows controlling the programs present on the hub and downloading new ones.

Installation
------------

### There are two methods for installing the library:

1. **Directly use pip**

   You can directly run the command: `pip install git+https://github.com/tibor-david/ms-program-control` without the need to clone the repository.

4. **Build the Library**

   This method is more intricate. If you're new to Python, consider the first installation method instead.

   1. Ensure that you have the necessary dependencies installed on your machine: wheel, setuptools, and build. On Debian/Ubuntu-based Linux systems, you can use your package manager: `apt install python3-build python3-setuptools python3-wheel`. On Windows, you can utilize pip directly: `py -m pip install --user --upgrade build pip setuptools wheel`.

   2. Execute the command `pyproject-build` at the root of the repository.

   3. This will generate a "dist" folder and a "tictactoe.egg-info" folder. Disregard the "tictactoe.egg-info" file and navigate into the "dist" folder.

   4. Inside the "dist" folder, you'll find two files: "tictactoe-x.y.z-py3-none-any.whl" and "tictactoe-x.y.z.tar.gz". If you intend to install the library on your machine or within a virtual environment, select the *.whl file. Copy the file's path and use the command `pip install <path to the file>/tictactoe-x.y.z-py3-none-any.whl` for installation.

Usage
-----

### Launching the graphical interface
To use this library, write the following in a terminal: `python3 -m msprogramcontrol`(or `python` on Windows), and it will launch the graphical interface.

### Using the GUI
This interface contains 3 buttons: a "Stop" button, a "Start" button, and an "Upload" button.

* To stop or start a program, choose the slot to be stopped or started by selecting the desired slot using the leftmost program location display.

* To upload a file to the hub, click on the "Choose a file" button, navigate to the location where the Python file you want to download to the hub is located. Now that the file is chosen, you can choose the location where the program will be downloaded using the rightmost program location display, then press the download button.

### The Terminal
Under the program management buttons, there is a terminal where program messages and errors are displayed.
