import pickle
import os
from datetime import datetime
from tabulate import tabulate
from itertools import chain

import myDates

      
    
class Tasks(object):
    """A list of `Task` objects for the 'todo' app.

    Attributes:
     - min_priority, max_priority (int): the minimum and maximum values allowed for the 'priority' attribute of 'Task' objects.
     - default_priority (int): the default value the 'priority' attribute of 'Task' objects
     - filename (str): filename of the pickle file containing 'Tasks' object data

     - dt_format (str): the date format adopted for the app. Applies to all dates in the app. If '%m/%d/%Y' is chosen, user inputs like 31/12/2022 or 31/dec/2022 will throw an error.
     - print_tz (bool): a boolean indicating to print timezones in reports. Useful to improve readibility when timezones are long words.
     - tasks (list): a list of Task objects

     - tasks_ID (list): a list containing only the ID of the Task objects. It is always synchronized with the 'tasks' list. 
                        Useful for indexing regardless of the order of the objects in the 'tasks' list.  
     - age_updated(bool): Indicates if the 'age' attribute of the 'Task' objects for the app's current run.  
     - min_ID, max_ID (int): minimum and maximum IDs in the 'tasks' list in the app's current run. Useful for error-handling print statements.  
     
    """

    min_priority, max_priority = (1, 3)
    default_priority = 1
    filename = ".todo.pickle"
    dt_format = '%m/%d/%Y'
    print_tz = True
    
    def __init__(self):
        """  Read pickled tasks file and ID data into lists; initializes auxiliary variables"""

        # tests if a pickle file containing 'Tasks' data already exists; if not, initialize a 'Tasks' object from scrap.
        if os.path.isfile(self.filename):
            with open(self.filename, 'rb') as file:
                Tasks_data = pickle.load(file)
                self.tasks = Tasks_data["tasks"]
                self.tasks_ID = Tasks_data["tasks_ID"]
                self.min_ID = min(self.tasks_ID)
                self.max_ID = max(self.tasks_ID)
        else:
            self.tasks = []
            self.tasks_ID = []
            self.min_ID = 0
            self.max_ID = 0

        self.age_updated = False
        
#===========================================================================
#SECTION File processing methods
#===========================================================================
    def pickle_tasks(self):
        """Pickle relevant data for the 'Tasks' object into a file.
        Currently saves: (i) list of Task objects, (ii) list of Task IDs
        Path to save is given by 'self.filename'. """

        with open(self.filename, 'wb') as file:
            Tasks_data = {"tasks":self.tasks, "tasks_ID":self.tasks_ID}
            pickle.dump(Tasks_data, file)


#\SECTION

#===========================================================================
#SECTION Validate input methods
#===========================================================================

    def valid_priority(self, priority):
        """ Checks if the 'priority' input given by the user is in the accepted range     

        Args: priority (int): priority input from the terminal. Obs.: 'argparse' ensures the input is an integer.

        Returns: (bool): 'True' if the input is valid, 'False' if not.
        """
        if priority >= self.min_priority and priority <= self.max_priority:
            return True
        else:
            return False

    def valid_ID(self, task_ID):
        """ Checks if the 'ID' input given by the user is in the list of Task objects. 

        Args: task_ID (int): ID input from the terminal. Obs.: 'argparse' ensures the input is an integer.
        Returns: 
            (bool): 'True' if the input is valid, 'False' if not.
            (str) | None: An error message to print in the terminal. | None if the input is valid
        """
        if task_ID < self.min_ID or task_ID > self.max_ID:
            return False, f"\nPlease input a task task_ID between {self.min_ID} and {self.max_ID}\nTip: To retrieve information about tasks (including ID numbers), use --query to retrieve search tasks by name.\n"

        if task_ID not in self.tasks_ID:
            return False, f"\nTask ID not found.\nTip: To retrieve information about tasks (including ID numbers), --query allows to retrieve information about tasks (including IDs) by name.\n"

        return True, None
#\SECTION


#===========================================================================
#SECTION Methods that modify the list of Task objects (add, remove, done)
#===========================================================================
    
    def add(self, name, priority = None, due_dt = None):
        """ Implements the command-line '--add' option. 
        If sucessful, adds a 'Task' object and its ID to 'self.tasks' and 'self.tasks_ID' lists.
  
        Args:
          name(str): name of the task entered by the user in the terminal.
          priority(int): priority of the task entered by the user in the terminal. If None, defaults to self.default_priority
          due_dt (datetime, optional): due date of the task entered by the user in the terminal. Defaults to None.
  
        Returns:
          msg (str): A message to print in the terminal indicating sucess or failure of the command.
          worked(bool): 'True' if a task was added, 'False' if an error ocurred 
        """
          
        msg = ""
        worked = False

        # checks if 'priority' input is valid; accumulate an error msg if not
        if priority:
            if not self.valid_priority(priority):
                msg += f"\nFor 'priority' please a whole number between {self.min_priority} and {self.max_priority}\n"

        # checks if 'due date' input is valid; accumulate an error msg if not
        if due_dt:
            if not myDates.valid_date(due_dt, remove_whitespace=True, dt_format=self.dt_format):
                msg += f"\nFor 'due date' please input a date in the format mm/dd/yyyy. Examples: 12/31/2022, 12/1/2022, 01/1/2022, 1/1/2022\n"

        # if no error, adds the task to the list
        if len(msg)==0:
           # attributes a new ID to the new 'Task' and updates max_ID
           self.max_ID += 1
           task_id = self.max_ID

           # includes the new 'Task' object and its ID in the 'Tasks' lists
           self.tasks.append(Task(name, priority, due_dt, task_id))
           self.tasks_ID.append(task_id)

           # msg and boolean indicating success; saves updated 'Tasks' data to the disk.
           msg+= f"\nCreated task {task_id}\n"
           worked = True
           self.pickle_tasks()
        return msg, worked


    def done(self, task_ID:int):
        """ Implements the command-line '--done' option. 
        If sucessful, 'completed_dt' (datetime) attribute with the user's current local time is added to the specified 'Task' object.  

        Args:
            task_ID (int): unique identifier of the 'Task' object entered by the user in the terminal.
        Returns:
            msg (str): A message to print in the terminal indicating sucess or failure of the command.
            worked(bool): 'True' if a task was marked as completed, 'False' if an error ocurred
        """
        msg=""
        worked=False

        # checks if 'ID' input is valid; accumulate an error msg if not
        valid_id, error_msg = self.valid_ID(task_ID)
        if not valid_id:
            msg += error_msg
        else:
            # retrieves 'Task' object from 'self.tasks' through the position of it's unique ID in 'self.tasks_ID'.
                # obs: 'self.tasks_ID' contains 'Task' objects IDs in the same order they appear in the 'self.tasks list'.
                #      'Task' objects may be in any order in the 'self.tasks list' (regardless of their ID numbers).
            curr_task = self.tasks[self.tasks_ID.index(task_ID)]

            # if the task was already complete, print a message for the user
            if curr_task.completed_dt:
                msg+= f"\nTask {task_ID}, '{curr_task.name}', was completed in: {curr_task.completed_dt_str}\n"
            else:
                # updates the 'completed_dt' datetime attribute of the specified 'Task' object with the current day and time.
                # in adding the datetime, ensures the date and time are in the user's local timezone.  
                curr_task.completed_dt = myDates.date_localtz(datetime.now())

                # msg and boolean indicating success; saves updated 'Tasks' data to the disk.
                msg += f"\nCompleted task {task_ID}, '{curr_task.name}'\n"
                worked = True
                
                self.pickle_tasks()
            
        return msg, worked

    def delete(self, task_ID):
        """ Implements the command-line '--del' option. 
        If sucessful, the specified 'Task' object and its ID are removed from 'self.tasks' and 'self.tasks_ID' lists.

        Args:
            task_ID (int): unique identifier of the 'Task' object entered by the user in the terminal.
        Returns:
            msg (str): A message to print in the terminal indicating sucess or failure of the command.
            worked(bool): 'True' if a task was deleted, 'False' if an error ocurred
        """

        msg=""
        worked=False

        # checks if 'ID' input is valid; accumulate an error msg if not
        valid_id, error_msg = self.valid_ID(task_ID)
        if not valid_id:
            msg += error_msg

        else:
            # retrieves and delete 'Task' object from 'self.tasks' through the position of it's unique ID in 'self.tasks_ID'.
                # obs: 'self.tasks_ID' contains 'Task' objects IDs in the same order they appear in the 'self.tasks list'.
                #      'Task' objects may be in any order in the 'self.tasks list' (regardless of their ID numbers).
            del self.tasks[self.tasks_ID.index(task_ID)]
            self.tasks_ID.remove(task_ID)

            # msg and boolean indicating success; saves updated 'Tasks' data to the disk.
            msg+= f"Deleted task {task_ID}"
            worked = True
            self.pickle_tasks()
        return msg, worked

#\SECTION

#===========================================================================
#SECTION methods for printing/reporting to the user
#===========================================================================
     
    def list_tasks(self):
        """ Implements the command-line '--del' option.
        Lists all unfinished tasks data. Sort by priority (higher-low) then by due date (closer to furthest in time).

        Returns:
            (str): A formatted table containing data for the unfinished tasks. Obs.: if no unfinished tasks, table still returned only with headers.
        """

        # updates the 'age' attribute of each 'Task' object ('age' of Task = timedelta(now, Task.created_dt))
        if not self.age_updated:
            self.set_age()
            self.age_updated = True
            
        # sort tasks: 'priority' higher-low ; 'due date' closer to furthest. If no 'due date', goes to the end of the list.
        sorted_tasks = self.sort_tasks(self.tasks, due_dt_order = 'ascending', priority_order = 'descending')

        # filter out completed tasks from the list
        sorted_tasks = filter(lambda task: task.completed_dt is None, sorted_tasks)

        # Printing of the list of tasks: a dictionary is passed to 'self.tabulate_tasks()' that implements
        # the formatting of the table and returns a string ready to be printed in the terminal

        # Dictionary with headers of the table and the 'Task' attributes to print to the user;
           # 'key'  of the dictionary are the headers of the table as they will be printed to the user. 
           # 'value' of the dictionary are the python attributes to be retrieved from 'Task' objects. 
           # Example: {'Priority will be printed like this: Task.priority'}
          
        header_attributes = {'ID': 'task_ID', 'Age': 'age', 'Due Date': 'due_dt_str', 'Priority': 'priority', 
                            'Task':'name'}

        # returns the output table as a string to be printed in the terminal 
        return self.tabulate_tasks(header_attributes, sorted_tasks)

    def report_tasks(self):
        """ Implements the command-line '--del' option.
        Lists all tasks data. Sort by priority (higher-low) then by due date (closer to furthest in time).

        Returns:
            (str): A formatted table containing data for all tasks. Obs.: if no data, table still returned only with headers.
        """

        # updates the 'age' attribute of each 'Task' object ('age' of Task = timedelta(now, Task.created_dt))
        if not self.age_updated:
            self.set_age()
            self.age_updated = True

        # sort tasks: 'priority' higher-low ; 'due date' closer to furthest. If no 'due date', goes to the end of the list.
        sorted_tasks = self.sort_tasks(self.tasks,  due_dt_order = 'ascending', priority_order = 'descending')

        # Printing of the task's report: a dictionary is passed to 'self.tabulate_tasks()' that implements
        # the formatting of the table and returns a string ready to be printed in the terminal.

        # Dictionary with headers of the table and the 'Task' attributes to print to the user
           # 'key'  of the dictionary are the headers of the table as they will be printed to the user. 
           # 'value' of the dictionary are the python attributes to be retrieved from 'Task' objects. 
           # Example: {'Priority will be printed like this: Task.priority'}

        header_attributes = {'ID': 'task_ID', 'Age': 'age', 'Due Date': 'due_dt_str', 'Priority': 'priority', 
                            'Task':'name', 'Created Date':'created_dt_str', 'Completed Date': 'completed_dt_str'}

        # returns the output table as a string to be printed in the terminal.
        return self.tabulate_tasks(header_attributes, sorted_tasks)


    def query_tasks(self, queries, sort_list=False):
        """ Implements the command-line '--query' option. 
        Search for unfinished tasks that match the search terms and list their data.

        Args:
           queries (list): a list containing the search ters entered by the user in the terminal
           sort_list (bool): Sort the resulting list of tasks? If True, sort by priority (higher-low) then by due date (closer to furthest in time).      
        Returns:
            msg (str): A formatted table containing data for all tasks found. If no task was found, an error message
        """

        # updates the 'age' attribute of each 'Task' object ('age' of Task = timedelta(now, Task.created_dt))
        if not self.age_updated:
            self.set_age()
            self.age_updated = True
            
        if sort_list:
            # sort tasks: 'priority' higher-low ; 'due date' closer to furthest. If no 'due date', goes to the end of the list.
            sorted_tasks = self.sort_tasks(self.tasks, due_dt_order = 'ascending', priority_order = 'descending')
        else:
            sorted_tasks = self.task

        # loop: search for each term in the list of Tasks, returning the Task object if term found and Task not complete
        filtered_tasks = [] 
        for query in queries:
            filtered_list = list(filter(lambda task: query in task.name and task.completed_dt is None, sorted_tasks))
            filtered_tasks.append(filtered_list)
     
        # flatten the list of filtered 'Task' objects and keep only the unique matches
        filtered_tasks = set(list(chain(*filtered_tasks)))
        

        if len(filtered_tasks)>0:
            # Printing of the task's report: a dictionary is passed to 'self.tabulate_tasks()' that implements
            # the formatting of the table and returns a string ready to be printed in the terminal.

            # Dictionary with headers of the table and the 'Task' attributes to print to the user
                # 'key'  of the dictionary are the headers of the table as they will be printed to the user. 
                # 'value' of the dictionary are the python attributes to be retrieved from 'Task' objects. 
                # Example: {'Priority will be printed like this: Task.priority'}
            header_attributes = {'ID': 'task_ID', 'Age': 'age', 'Due Date': 'due_dt_str', 'Priority': 'priority', 
                            'Task':'name'}

            # string with table of tasks to print in the terminal and boolean indicating success.
            msg = self.tabulate_tasks(header_attributes, filtered_tasks)
            worked = True
        else:
            # string and boolean indicating failure.
            msg = "\nCould not find any tasks with your queries. Please try again\n"
            worked = False
        return msg, worked

#\SECTION        
#===========================================================================
#SECTION auxiliary methods to process and extract data from the Tasks list
#===========================================================================
    def set_age(self):
        """ Sets the 'age' attribute of the Tasks objects. Task.age = timedelta(now, Task.created_dt)
        """
        # user's current LOCAL time
        today = myDates.date_localtz(datetime.now())

        # for each Task object, calculates updates the 'age' attribute. 
        # time deltas are computed in UTC terms to prevent problems with timing conventions.
        for task in self.tasks:
            age = myDates.date_diff_absolute(today, task.created_dt).days
            task.age = f"{age}d"
        self.age_updated = True

    def sort_tasks(self, tasks_list, due_dt_order = 'ascending', priority_order = 'descending'):
        """ Sorts a list of 'Task' objects.

        Args:
            tasks_list (list): list containing 'Task' objects
            due_dt_order (str|None, optional): order by 'due_dt' attribute? 'Ascending' goes from earlier due date to latest. Defaults to 'ascending'.
            priority_order (str|None, optional): order by 'priority' attribute? 'Descending' order goes from higher to lower priority (where priority 3 is higher than 1). Defaults to 'descending'.

        Raises:
            ValueError: error in case of non-allowed ordering arguments

        Returns:
            list: A sorted list of Task objects.
        """

        # checks if the ordering inputs are valid
        allowed_order = ('ascending', 'descending', None)
        if any([due_dt_order not in allowed_order, priority_order not in allowed_order]):
            raise ValueError("\norder inputs must be either 'ascending' or 'descending'\n")

        # The sorting is made by passing a tuple of Task attributes to the 'sorted' method. 
        # Exampl: ascending 'due_dt_order' and descending 'priority_order'
            #   'task.due_dt is None': returns True if a Task has no due date, putting any of them at the end of the list (1>0, ascending order)
            #   'task.due_dt': datetime attribute, ordered ascending (earlier to latest)
            #   '-task.priority': reverse the value of the 'priority' attribute, so when ordered ascending, 3 comes first than 1 (same as descending priority)
            # To remember: tuples are ordered from 'left' to 'right' each at a time; this guarantees the method works

        if due_dt_order=='ascending':
            if priority_order == 'descending':
                return sorted(tasks_list, key = lambda task: (task.due_dt is None, task.due_dt, -task.priority))
            if priority_order == 'ascending':
                return sorted(tasks_list, key = lambda task: (task.due_dt is None, task.due_dt, task.priority))
            else: # just order by due_date
                return sorted(tasks_list, key = lambda task: (task.due_dt is None, task.due_dt))

        if due_dt_order=='descending':
            if priority_order == 'descending':
                return sorted(tasks_list, key = lambda task: (task.due_dt is not None, task.due_dt, task.priority), reverse=True)
            if priority_order == 'ascending':
                return sorted(tasks_list, key = lambda task: (task.due_dt is not None, task.due_dt, -task.priority), reverse=True)
            else: # just order by due_date
                return sorted(tasks_list, key = lambda task: (task.due_dt is not None, task.due_dt), reverse=True)

        # just order by priority 
        if priority_order=='descending':
            return sorted(tasks_list, key = lambda task: (task.due_dt is None, -task.priority))

        if priority_order=='ascending':
            return sorted(tasks_list, key = lambda task: (task.due_dt is None, -task.priority))

        # do not order at all (all ordering inputs == None)
        return tasks_list

    def reset_IDs(self):
        """ Reset the task_ID attribute of the all the Task objects to integers between [1, len(self.tasks)]. 
        Updates 'self.tasks_ID', 'self.tasks' accordingly. 
        Obs.: Useful to 'reindex' tasks after many are added/deleted. Prefered overreindexing each time the app runs, as user might have IDs memorized.
        """

        self.tasks_ID = [None]*len(self.tasks)
        for i, task in enumerate(self.tasks):
            task.task_ID = i+1
            self.tasks_ID[i] = i+1
            self.pickle_tasks()
        return "IDs successfully reseted", True


#===========================================================================
#SECTION auxiliar methods to format printing
#===========================================================================

    def due_dt_to_str(self,date):
        """ Convert a Task 'due_dt' datetime attribute to a string to be printed in the terminal
        """
        if date is None:
            return "-"
        else:
            return date.strftime(self.dt_format)


    def created_dt_to_str(self, date):
        """ Convert a Task 'created_dt' attribute from datetime to string to be printed in the terminal
        """
        if date is None:
            return "-"
        else:
            # choose wether to include the user's timezone when printing to the terminal
            if self.print_tz:
                return date.strftime(f"%a %b %d %H:%M:%S {date.tzname()} %Y")
            else:
                return date.strftime(f"%a %b %d %H:%M:%S %Y")

    def completed_dt_to_str(self,date):
        """ Convert a Task 'created_dt' attribute from datetime to string to be printed in the terminal
        """
        if date is None:
            return "-"      
        else:
            # choose wether to include the user's timezone when printing to the terminal
            if self.print_tz:
                return date.strftime(f"%a %b %d %H:%M:%S {date.tzname()} %Y")
            else:
                return date.strftime(f"%a %b %d %H:%M:%S %Y")


    def tabulate_tasks(self, header_attributes:dict, tasks_list):
        """ Tabulates a list of tasks to print to the terminal.
        Args:
            header_attributes (dict): dictionary, where:
                'key's are table's headers as they will be printed in the terminal  
                'value's are the Task attributes to be retrieved and filled in the table

            tasks_list (list): a list of 'Task' objects

        Returns:
            str: A table ready to be printed to the terminal.

        Examples:
            tabulate_tasks(header_attributes: {'ID':'task_ID', 'Age':'age', 'Due date': due_dt, 'Priority':'priority', 'Task':name}, ...)

                  ID   Age  Due Date   Priority   Task
                  --   ---  --------   --------   ----
                  1    3d   4/17/2018   1         Walk dog
                  3    1d   -           2         Buy eggs
                  4    30d  -           1         Make eggs
                    
        """
        dict_print = {header:[] for header in header_attributes}

        # loop: for each Task object, retrieves the desired 'attribute' and puts below the appropriate 'header' column in the table
        for task in tasks_list:
            for header, attribute in header_attributes.items():
                task_attribute = task.__getattribute__(attribute)
                dict_print[header].append(task_attribute)

        # returns the formatted table as string ready to be printed to the terminal; numbers are centered; extra lines "\n" for redability 
        return "\n" + tabulate(dict_print, headers="keys", numalign="center") + "\n"

    

    
#\SECTION

#===========================================================================
#SECTION Task subclass and its methods
#===========================================================================    

class Task(Tasks):
    """Representation of a task

    Attributes:
      name (str, optional): Task name as entered with '--add'.
  
      priority (int, optional): Task priority as entered with the '--priority'. Can be any integer between Tasks.min_priority and Tasks.max_priority.
                                  Priority is in descending order: 3 higher priority than 1. Defaults to 'Tasks.default_priority'.
      due_dt (datetime, optional): Due date as entered with '--due'. Format in day/month/year follows 'Tasks.dt_format'.  Defaults to None. 
  
      created_dt (datetime): Automatially assigned the first time the Task is created. Format in 'day/month/year' follows 'Tasks.dt_format'.
  
      completed_dt (datetime, optional): Due date as entered with '--done'. Format in day/month/year follows 'Tasks.dt_format'. Deafults to None.
  
      task_ID (int): Uniqued ID identifying the task. Automatically assigned when by the parent Tasks class when the Task is created.
    """
    def __init__(self, name, priority, due_dt, task_ID):
        self.name = name
        self.task_ID = task_ID
        self.priority = priority if priority else Tasks.default_priority

        # assigns the created date in the user's LOCAL current time
        self.created_dt = myDates.date_localtz(datetime.now())        

        # if a due date is passed, parses it using 'Tasks.dt_format' and assigns in the user's LOCAL current time
        self.due_dt = myDates.date_localtz(datetime.strptime(due_dt, Tasks.dt_format)) if due_dt else None
        self.completed_dt = None

    # get methods for the dates attributes in string format.
    # update each time attribute is called to be in line with the app's current configurations.
    @property 
    def created_dt_str(self):
        return Tasks.created_dt_to_str(Tasks,self.created_dt)

    @property
    def due_dt_str(self):
        return Tasks.due_dt_to_str(Tasks, self.due_dt)

    @property 
    def completed_dt_str(self):
        return Tasks.completed_dt_to_str(Tasks,self.completed_dt)
    



