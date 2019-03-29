# lolo

# MVP

## Functionalities of the MVP

* Login/register (no password needed)
* Selection of the topics the user wants to learn about (animals, food, clothes, colours)
* Learning phase: The user learns random words from his preferred topics. The result of the a learning phase is stored in the db (see Docs/dataStructure.md for more info)
* Test phase: The user is tested on the words from his preferred topics that he has already learned. The result of the a testing phase is stored in the db (see Docs/dataStructure.md for more info) 

## Work done and ideas for future improvement

This file explains who did what and contained some ideas for future improvement:
https://docs.google.com/document/d/1yOlnkmRApAuh_QsqT5Mi0zi1IAXekeSKP3sz8Myt6Ag/edit?usp=sharing

 ## Folder structure
 ```
├── Docs
│   ├── ....
├── Data
│   ├── ....
├── App
│   ├── ....
├── API
│   ├── ....
├── README.md
```
* Docs contains a document explaining the structure of the data stored in the mongo database 
* Data contains all the vocabulary in csv files (the vocabulary is already inserted in the DB)
* App contains all the Ionic files
* API contains all the backend components (the api, and the DBcontroller)
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

## Run the app on your mobile phone

You need SDK android installed, SDK Java 1.8

You can install android sdk easily by installing android-studio, and update your .bashrc file with :

> export JAVA_HOME=your path to java

> export PATH=$JAVA_HOME/bin:$PATH

> export ANDROID_SDK_ROOT= your path to the sdk

> export PATH=$PATH:$ANDROID_SDK_ROOT/tools/bin

> export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools

> export PATH=$PATH:$ANDROID_SDK_ROOT/emulator

connect your android phone to your computer

> ionic cordova run android -l --device

if you dont have an android phone, download an emulator using android studio then

> ionic cordova emulate android -l

## Generate splash and icons
To automatically generate the icons and splash screens run:

> ionic cordova resources

A ionic account is needed.

# How to collaborate

Please if you want to collaborate create a new branch, and when you are sure
that your changes work request a merge to the master branch. This is a good
practice to avoid conflict problems.