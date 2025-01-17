# ImageProcessorS18 &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/facebook/react/blob/master/LICENSE) &middot; [![Build Status](https://travis-ci.org/kjans123/ImageProcessorS18.svg?branch=master)](https://travis-ci.org/kjans123/ImageProcessorS18) &middot; [![Documentation Status](https://readthedocs.org/projects/imageprocessors18-cps/badge/?version=latest)](http://imageprocessors18-cps.readthedocs.io/en/latest/?badge=latest)

### ONLINE Read-The-Docs README: [Read-The-Docs](http://imageprocessors18-cps.readthedocs.io/en/latest/)
### ONLINE RFC Document: [RFC](https://docs.google.com/document/d/1zIfm1slOxkt7Gfgiu5WG25OfD-nz8LZkS0AF_JTfVUc/edit?usp=sharing)
### ONLINE Demo: [Video Demonstration](https://youtu.be/i2oXpjaGT1w)
### APP Link: [Deployed App](http://cps_imageprocessors18.surge.sh/)

### Description

The Crunchwrap Pizza Image Processor can be used to take in one or more .jpg images or a .zip archive of .jpg images in order for the user to run histogram equalization, log compression, constrast stretching, or reverse video operations on the image(s) they upload. This repository includes starter code for a ReactJSX app frontend that allows image upload, download, and display; starter code for a Mongo Database to store user information; and server code that processes the selected images and returns them to the frontend.

<img src="https://user-images.githubusercontent.com/24235476/39473111-2f73adf8-4d1b-11e8-8d19-27a584e2de02.png" width="700"/>
<img src="https://user-images.githubusercontent.com/24235476/39543161-7cfde392-4e18-11e8-9f1d-13e687621a8d.png" width="700"/>
<div align="center"><table align="center">
  <tr><th>User Input</th><th>Output</th></tr>
<tr><td><img src="https://user-images.githubusercontent.com/24235476/39538195-fba57750-4e09-11e8-8fbd-b58212e37637.png" width="300"/></td><td><img src="https://user-images.githubusercontent.com/24235476/39538174-ef37ca9a-4e09-11e8-86a5-6020e3c53d75.png" width="300"/></td></tr>
</table></div>


## Initial Setup
First you will need to clone this repository to your local machine. Install all of the required python dependencies using:
```
pip install -r requirements.txt
```
and make sure to activate your virtual environment before continuing. ```source venv/bin/activate ```

   ***NOTE: if Tkinter throws a Not Found error, you will need to use this command: ``` apt-get install python-tk```. This may happen if the server is being run on a VCM being accessed through a command line window.***
    
## Database
To get started running the database (if you want to run your own database), use the below command in the same directory as the ProcessServer.py file ```(~/ImageProcessorS18/server)```
```
sudo docker run -v $PWD/db:/data/db -p 27017:27017 mongo
```
and on line 33 in the ProcessServer.py file edit
```
connect("mongodb://vcm-3594.vm.duke.edu:27017/image_process_app")
```
with the name you want assigned to your database:
```
connect("mongodb://vcm-3594.vm.duke.edu:27017/<your_database_name_here>")
```

## Server
In order to run the server, make sure that you are within the server folder before starting
```
cd ~/ImageProcessorS18/server
```
You can run the server on your local computer using gunicorn:
```
gunicorn --bind 0.0.0.0:5000 ProcessServer:app
```
## App
Use this [link](http://cps_imageprocessors18.surge.sh/) to simply utilize the already deployed version of the app. However, if you wish to make edits and run the app locally, follow the next steps:


To run the app locally first make sure you are within the ```frontend``` folder
```
cd frontend
```
Make sure you have Node.JS installed on your machine. Use this [link](https://nodejs.org/en/) to install it if you haven't already. Then, run
```
npm install
```
this will install all necessary dependencies. Run
```
npm start
```
to launch the app and use it within your browser. 

***NOTE: Make sure that the server and database are running, as well, and that you have edited lines 156 and 196 in the App.js file to reflect where you're running your server.***

### License

ImageProcessorS18 is [MIT licensed](./LICENSE).
