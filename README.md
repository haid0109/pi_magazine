# Guide to setting up sense hat emulator binary clock on ubuntu:

- Install the sense hat emulator:
    ```
    $ sudo add-apt-repository ppa://waveform/ppa
    $ sudo apt-get update
    $ sudo apt-get install python-sense-emu python3-sense-emu sense-emu-tools
    ```
- open the sense hat emulator
- install git:
    ```
    sudo apt install git
    ```
- clone the binary clock repository:
    ```
    git clone https://github.com/haid0109/pi_magazine.git
    ```
- run the application
    ```
    python3 pi_magazine/binary_clock_sh.py
    ```
- close the application by pressing `ctrl + c` in the terminal that is running the application