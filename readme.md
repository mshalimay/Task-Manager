# Command Line Task Manager

This is an OOP task manager accessible via the CMD created as project for MPCS50101-Summer2022.

# Description
To use the app, run the file `todo.py` from the command line with the desired flag representing an action. To see available options, run `todo.py --h` (or see below)

- With the app one can create a list of tasks with their respectives due dates and priorities. The task list will be saved in the disk as a `pickle` file
- The app keeps track of the creation date, number of days since creation and which tasks are finished or not
- It is possible to query for tasks using the name of the task, list unfinished tasks or make a report of all tasks (finished and unfinished)


# Options
 -  `-h`, `--help`            show this help message and exit
 
  - `--add` Adds a task to your list. Join more than one word with commas. To set due dates and a priority, add --due and --priority to your query. 
    - Examples: --add "wash dishes" 
    - --add run 
    - --add "Travel US" --due 09/01/2022 --priority 3
  
  - `--done` Mark a task as completed. Input is a whole number representing the unique ID of the task. 
    - Examples: --done 5
  
  - `--del` Delete a task. Input is a whole number representing the unique ID of the task. 
    - Example: --del 10
  
  - `--due` Due date of your task. Input is a date the format mm/dd/yyyy. 
    - Example: --add 'Birthday Julio' --due 01/07/2022
  
  - `--priority` Priority of your task. Input is an integer between 1 and 3 (higher priority). Defaults to 1. 
    - Example: --add "Buy gift wife" --priority 3
  
  - `--list` Lists all the unfinished tasks.
  
  - `--report` A report of all finished and unfinished tasks.
  
  - `--query` Search tasks by name. Accepts mutliple search arguments. Inputs are terms to search for tasks. 
    - Example: --query "wife" "run" "travel"
  
  - `--resetID` Resets the tasks IDs. Useful for restarting the indexation of your list after using the app for some time.

# Python modules description

## todo.py
- This module parse and validate command line instructions and deploys the app

## TaskManager.py
- This module contains:
    - the `Tasks` class definition
    - the `Task` subclasss definition 
    - All methods used in the task manager app

## myDates.py
- Auxiliary module to deal with datetime arithmetics, conversion and validation
- Obs.: this module might be used for other apps; it is not specific to this app

## myNumbers.py
- Auxiliary module to parse string input from the command line to numbers
- Obs.: this module might be used for other apps; it is not specific to this app

## myErrors.py
- Auxiliary module with customized error classes

## test_argparse.py, test_myDate.py, tests
- Modules for: test behavior of the `argparse` library, `myDate` unit testing and testing general behavior of the app, respectively.

