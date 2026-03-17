# programming-projects-lab
This project is a collaboration between Frankie Antoine, Adil Ali Khan and Aryam Sharma

# How to run the build using docker
To run the app using docker, you need to build the app using the docker file and run the command provided

To build the files, go into the docker file and run:
```
docker build -t app .
```

To run the docker file, go into docker and run:
```
docker app
```

# How to create your own build using a visual environment
There are two ways to create your own build for this project.
1) Download the code directly off of github as a zip file and add it manually to your IDE
2) Clone the git repositoy through your IDE (ex. VScode)

To download it manually, click on the green code button on the section below the project name and click download zip from the drop down menu.

To Clone your own repositoy to differs from IDE to IDE but in VScode you have to go to the terminal and enter the following:
```
git clone https://github.com/AdilKhan-CS/personal-hub-CompProgProj.git
```
To run it, once the code is on your device all you have to do is go to app.py and run the code.

# Personal Hub
A centralized lifestyle dashboard designed to keep your tasks, goals, and interests organized in one place. This project will be made in Python using the tkinter library.

## Task Planning & Goals Management
- Task Agenda / To‑Do List
- Goals List

## Personalized Workspace
- Daily Quotes

- Movie Recommendation System
  - Personalized movie suggestions based on preferences.

- Sport Stat Tracker
  - Track fighters, match history, rankings, and favorites.

# Project structure
- The logic that deals with the whole project is in the app.py file
- The quotes.json and movies.json files contain the quotes and movies for the app to show

# Future Enhancements
- [ ] UI/UX improvements
- [ ] Custom themes

# How to Install
1) Go to releases and install the latest release
2) Unzip the folder and make sure you have the correct prerequisites.
3) Run ```python3 -m app.py```

# Usage & Requirements
> \>= python3.12 \
> \>= tkinter \
> \>= pytest

```
python3 -m app.py

How to run tests:
1. cd into the correct folder location
2. run pytest
```
---

# Known Limitations
- Cannot order the goals/tasks like "1) ... 2)..."
- Cannot drag goals to a specific order

## 📌 Project Status
- Can run all of the project specifications
- Refining is not complete

## 📌 Development Status
Actively under development.