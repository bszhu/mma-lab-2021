# TU Delft CSE2230 Muleimedia Analysis - Invention Assignment
In this assignment, we created a simple system that uses the presence of landmarks in a video to determine the geo-location at which a video was recorded. The application takes a video as an input, and outputs the location of the video. Only the 3 landmarks in Delft, the Nieuwe Kerk, the Stadhuis and the Oude Jan, are considered.

## How to install
Firstly clone the repository by the command: 
```
git clone https://github.com/bszhu/mma-lab-2021.git
```

### Anaconda environment installation
Only Linux systems are supported currently.

1. Firstly download the [Anaconda](https://docs.anaconda.com/anaconda/install/linux/) for your operating system
2. Install Anaconda from the installer
3. Open the Anaconda-Navigator
4. Go to the environment tab and import MMA2020.yml (included in this Github repository)
5. As a name fill in "mma2020" and choose the Conda environment file under "Specification file"

### Adding database
The database is of 8 GB. There are 2 options to obtain the database:
1. Download the 3 [databse](https://drive.google.com/drive/folders/1CHzgEJB7xFXBMGcqcMWasXwVzTVA5Lul) files and move them into the directory `/Code/db/`.
2. Download the set of [images](https://drive.google.com/drive/folders/1ljXDlhTVznFf0bzDC8DUygsH5fRA5F5A), place the folder of `inventionimages` in `/Images/` and run the command `python dbt.py -d invention_sift_DB sift ../Images/inventionimages/` in the directory `/Code/` to create the databse locally.

### Using the conda environment
1. Open Terminal/Powershell or your preferred shell of choice.
2. Type this in everytime before you use the application otherwise the environment won't be activated within the terminal!
```
conda activate mma2020
``` 
3. Now you are making use the environment with the correct Python version and packages. Make sure to use the command `python` and not `python3` or other variant when running the programs.
4. Check that everything is correctly installed by running the executable scripts in the `Code` folder of this repository, for example 
```
python Code/video_query.py --help
``` 
If you get an error and do not see the "help" of the program, notify the teaching team. These are the programs you will be running during the course, so if there are issues with them, they must be fixed.

## How to use
Start your terminal in the directory `/Code/`, run the command 
```
python video_geolocation_detection.py -h
``` 
to see the potential command line arguments of this application.

Then run the program with the command 
```
python video_geolocation_detection.py path-to-your-input-video
```

There are two optional arguments, `-n` the amount of sample frames (whose default value is 10) and `-t` the number of SIFT results that are taken into account in the process of estimation.

## Troubleshooting

If you encounter any packages missing make use of the following command to install these.
```
conda install [packages]
``` 

On Linux the OpenCV package might not be installed well directly. This can be resolved by activating the mma2020 environment, and then running the command 
```
conda install -c conda-forge opencv=3.4.2
```
