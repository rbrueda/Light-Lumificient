# Light-Lumificient
Project for COMP-3710 

## About
A smart home simulator used to monitor variables like light, temperature, wind and noise levels in order to produce most energy-efficient results for devices.

This project is based off a original simulation built on Prolog for logic comparsions (site: https://github.com/andmon97/es-smartHome) where simulation used user preferences to make decision for effector agents. Our simulation builds off this repository to built a comparsion with a new approach that uses two A* search algoriths (light and temperature). These algorithms manage light and temperature levels to get the minimum energy-cost path to the goal. 

For the A* algorithm concerning light, the algorithm iterates through every light fixture, dynamically adjusting their brightness levels, in order to oversee the usage of light energy and achieve light brightness goal.

For the A* algorithm concerning temperature, it manages heating, cooling, and resting actions to achieve the temperature goal.

## Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/rbrueda/Light-Lumificient.git
```
2. Setup python virtual environment
- First make sure it is installed. Use:
```
pip install virtualenv
```
- Second, create a virtual environment. Use:
```bash
virtualenv venv
```
- Third, activate virtual environment. 
On Windows use:
```powershell
venv\Scripts\activate
```
On macOS or Linux use:
```bash
source venv/bin/activate
```

3. Install library dependencies
To install all required dependencies for this project, use:
```bash
pip install -r requirements.txt
```

4. Install SWI-Prolog
Find more info at: https://wwu-pi.github.io/tutorials/lectures/lsp/010_install_swi_prolog.html
To install SWI-prolog in Linux OS, use:
```bash
sudo add-apt-repository ppa:swi-prolog/stable
sudo apt-get update
sudo apt-get install swi-prolog
```

To install with Windows, install package from:
https://www.swi-prolog.org/download/stable

To install with MacOS:
(TO DO)


4. Run the program
In MacOS, run the command:
```zsh
python main.py
```

In Linux or Windows, run the command:
```bash
python main1.py
```

## Screenshots



## Video About Project (+ Demo)
(TO DO: ADD LINK HERE)

## Research Paper
(TO DO: ADD LINK HERE)
