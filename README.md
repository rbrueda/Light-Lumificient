# Light-Lumificient
Project for COMP-3710 

## About
A smart home simulator used to monitor variables like light, temperature, wind, and noise levels in order to produce the most energy-efficient results for devices.

This project is based on an original simulation built on Prolog for logic comparisons (site: https://github.com/andmon97/es-smartHome) where this simulation used user preferences to make decisions for effector agents. Our simulation builds off this repository to build a comparison with a new approach that uses two A* search algorithms (light and temperature). These algorithms manage light and temperature levels to get the minimum energy-cost path to the goal. 

For the A* algorithm concerning light, the algorithm iterates through every light fixture, dynamically adjusting their brightness levels, in order to oversee the usage of light energy and achieve light brightness goal.

For the A* algorithm concerning temperature, it manages heating, cooling, and resting actions to achieve the temperature goal.

The results are shown from the two columns on the right where the **left column represents logic** results and **right column represents A*** results

## Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone https://github.com/rbrueda/Light-Lumificient.git
    ```

2. **Navigate to the Project Directory:**
    ```bash
    cd Light-Lumificient
    ```

3. **Setup Python Virtual Environment (Optional):**
    - First, ensure virtualenv is installed:
        ```bash
        pip install virtualenv
        ```
    - Second, create a virtual environment:
        ```bash
        virtualenv venv
        ```
    - Third, activate the virtual environment:
        ```bash
        source venv/bin/activate
        ```

4. **Install Library Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Installation for Tkinter:**
    Sometimes tkinter is not detected after installing Python libraries in requirements.txt. To fix the issue, run:
    ```bash
    sudo apt-get install python3-tk
    ```

6. **Install SWI-Prolog:**
    - Find more info at: [SWI-Prolog Installation Guide](https://wwu-pi.github.io/tutorials/lectures/lsp/010_install_swi_prolog.html)
    - To install in Linux, ensure SWI-Prolog **8.4.2 or 8.4.3** for compatibility:
        - Check for available versions (Ubuntu):
            ```bash
            apt-cache madison swi-prolog
            ```
        - Install the desired version:
            ```bash
            sudo apt-get install swi-prolog=8.4.2+dfsg-2ubuntu1
            ```
    - To install with MacOS:
        - Install Homebrew if not installed:
            ```zsh
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
            ```
        - Install SWI-Prolog:
            ```zsh
            brew install swi-prolog
            ```

7. **Create API Key for OpenWeatherMap API:**
    - Create an account from: [OpenWeatherMap API](https://openweathermap.org/api)
    - Once created, go to "API key" and copy the default key
    - Create a new file in the cloned directory named "credentials.txt" and paste the API key into this file (may take a few minutes to work)

8. **Run the Program:**
    - In MacOS:
        ```zsh
        python main.py
        ```
    - In Linux:
        ```bash
        python main1.py
        ```


## Other Notes
### MacOS Issues
If you having issues with pyswip running, then you must go to your python **site-packages** folder (this should be inside your virtual environment folder, if you are running through a virtual environment, or should be found where you installed Python locally).

Once you find it, you must locate folder called pyswip (if it is not there then it is not installed). Inside this folder you should find python file **core.py**. In around line 587, if you change the line:
```python
PL_version = _lib.PL_version
```
to
```python
PL_version = _lib.PL_version_info
```
this could fix the issue.

### Windows OS Issues
If you are running natively on Windows, you may get an error message similar to below:
```
SWI-Prolog: [FATAL ERROR: at Fri Mar 29 12:59:54 2024 Could not find system resources]
```

A possible fix is to run program using a Virtual Machine with a Linux distro (like Ubuntu) or using WSL.


## Screenshots
![Screenshot from 2024-03-25 17-56-40](https://github.com/rbrueda/Light-Lumificient/assets/93105329/e9804a7a-8a21-40a1-899d-2668b6418c2b)
![Screenshot from 2024-03-25 20-15-03](https://github.com/rbrueda/Light-Lumificient/assets/93105329/28eeb301-30fb-49ef-921a-07653a0f25b3)
![Screenshot from 2024-03-27 22-05-26](https://github.com/rbrueda/Light-Lumificient/assets/93105329/c2543865-62fc-4849-afbd-58146a945463)

## Video About Project (+ Demo)
https://www.youtube.com/watch?v=VAvU_nkWC7k 

## Research Paper
https://drive.google.com/file/d/17rS3E_lTol5x54aTG_l7Y3O9ZAQxqoVM/view?usp=sharing
