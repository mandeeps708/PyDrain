# PyDrain
Creating drawing of Drain using coordinates from CSV file. Calculates the cutting and filling area. 

Pre-requisite
-------------

- dxfwrite:

    `pip install dxfwrite`

Execution:
----------

- Clone repo:

    `git clone https://github.com/mandeeps708/PyDrain`
    
- Changing CSV input:
    Go to the PyDrain and locate coord.csv file. It is the input to the pyDrain.py program. The first 10 lines (contains coordinates) for creating the base. The next three lines are for creating the working space that includes coordinates and the angle or the third line.

- Execute:

    `cd PyDrain`

    `python pyDrain.py`

Then open the dxf file created in the current directory with some CAD software.
