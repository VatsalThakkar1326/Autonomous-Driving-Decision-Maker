# CAPSTONE-1
# Guide to Running the Project

This guide will help you run the code in this GitHub repository. Please follow the steps below:

go to final code folder

## Step 1: Install Dependencies

First, you need to install the necessary libraries and dependencies listed in the `requirements.txt` file. You can do this by running the following command in your terminal:

```bash
pip install -r requirements.txt
```
## Step 2: Check CUDA Compatibility
If you want to run the code quickly and efficiently, check if your system has CUDA capability. If it does, install the necessary CUDA drivers. This will allow your system to run CUDA-related libraries such as PyTorch, Tensor, and others. Make sure that all CUDA-capable libraries listed in the requirements.txt file are installed.
## Step 3: Download the Code and Model Files
Next, download all the code, model files, and the test motion data Excel file from this repository.
## Step 4: Replace Paths of the Models and Test Motion Data
You need to replace paths of all the models as described in the respective files. Do the same for the test motion data.
## Step 5: Run the Scripts
You have two options to run the project:
1.	Run Scripts Individually: You can run the following scripts one by one in VS Code:
○	Acceleration Detection
○	Decision Maker
○	Driver Behavior Detection
○	Traffic Condition Checker
○	Front Camera
2.	Run Scripts Simultaneously: If your system has sufficient processing power, you can run a user interface Python file that will run all the scripts in parallel. However, this requires a significant amount of processing power and is where CUDA compatibility can be beneficial.
Step 6: Generate Data Files
The code will generate some data files in real time. You need to replace all the necessary paths with your own hardware system to ensure everything works smoothly.
Please note that this is a general guide and might need to be adjusted based on your specific project and setup. Enjoy coding!

## Contributors: 

<span style="color:yellow">Vatsal Thakkar: Project Manager and Programming Logic Architect</span>  
<span style="color:yellow">Dhruvi Kapadia: Software Programmer and Debugger</span>  
<span style="color:yellow">Srushti Gupta: Software Programmer and Documentation Guru</span>  
<span style="color:yellow">Manav Patel: Data Engineer and Coordinator</span>  
<span style="color:yellow">Nishk Vaishnav: Data Engineer and Tester</span>  
<span style="color:yellow">Megha: Compiler</span>


