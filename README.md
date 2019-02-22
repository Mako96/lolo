# lolo

 ## Folder structure
├── Docs
│   ├── ....
├── Data
│   ├── ....
├── App
│   ├── ....
├── API
│   ├── ....
├── AI
│   ├── ....
├── README.md

## Ionic setup
To work on ionic please install the following software:
nodejs
git
android studio : to build an app for smartphone 
and through git you can install cordova and ionic by typing the following instructions:
 
 npm install -g ionic
 npm install -g cordova 
 ****************************
 
To start working on ionic :
the app is already built, however, the insturctions for that are :  
ionic start lolo blank  // for creating an app named lolo
ionic cordova platform add android  // for adding an android platform 
*********
once you have cloned the app you can run it through these instructions :
ionic serve --lab :: provides simulations for ios and android, and inside the page there is a button called fullscreen to display it as desktop app
Or you can use this instruction to display as desktop app :: ionic serve 

For creating a new page you can type : ionic g page main
and since you have it, there are three distinct files in its folder:

in the path "lolo\src\app\"

main.page.html <-- for the structure
main.page.ts <-- for fuctionality
main.page.scss <-- to deal with the style "css"

# How to collaborate

Please if you want to collaborate create a new branch, and when you are sure
that your changes work request a merge to the master branch. This is a good
practice to avoid conflict problems.