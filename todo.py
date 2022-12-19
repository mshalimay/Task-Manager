import TaskManager
import myNumbers
import argparse
import random


def parse_args():
    """ Defines the the app's option and parses the user input using the 'argparse' module
    Returns: parser.parse_args(): 'Namespace' object from the argparse module, the parsed arguments given by the user"""
    parser = argparse.ArgumentParser(description='Todo list')

    # add, done, delete 
    parser.add_argument('--add', type = str, required = False, 
                help = """Adds a task to your list. Join more than one word with commas. 
                        To set due dates and a priority, add --due and --priority to your query.
                        Examples: --add "wash dishes"\n --add run\n --add "Travel US" --due 09/01/2022 --priority 3""")

    parser.add_argument('--done', type = int, required = False, 
                        help = "Mark a task as completed. Input is a whole number representing the unique ID of the task. Examples: --done 5")

    parser.add_argument('--del', type = int, required = False, dest = 'delete',
                        help = "Delete a task. Input is a whole number representing the unique ID of the task. Example: --del 10")
    
    # due, priority  
    parser.add_argument('--due', type = str, required = False, 
                        help = "Due date of your task. Input is a date the format mm/dd/yyyy. Example: --add 'Birthday Julio' --due 01/07/2022")

    parser.add_argument('--priority', type = int, required = False, 
                        help = 'Priority of your task. Input is an integer 1 and 3 (higher prioriity). Defaults to 1. Example: --add "Buy gift wife" --priority 3')

    # list, report, query
    parser.add_argument('--list', action='store_true' , required = False, 
                        help = 'Lists all the unfinished tasks.')

    parser.add_argument('--report', action='store_true' , required = False, 
                        help = 'A report of all finished and unfinished tasks.')

    parser.add_argument('--query', type = str, required = False, nargs = "+", 
                        help = 'Search your tasks by name. Accepts mutliple search arguments. Inputes are terms to search for tasks. Example: --query "wife" "run" "travel"')    

    # additional option to reset the IDs of the tasks. Useful to 'reindex' tasks after many are added/deleted (reindexing each time the app runs is also an option, but this is prefered bcs the user might want to memorize IDs)
    parser.add_argument('--resetID', action='store_true' , required = False, 
                        help = 'Resets the IDs of your tasks. Useful for restarting the indexation of your list after using it for some time.')

    return parser.parse_args()
    
def validate_args(args):
    """ Additional validation of the user's inputs.

    Args: args (argparse.Namespace): a Namepsace object containing inputs given by the user in the terminal

    Returns: error_msg (str): a string containing an appropriate error message in case the input is not valid
    """

    error_msg = ""
    # cast the user inputs to a list
    inputs = list(vars(args).values())

    # test if any input was given in the terminal. If none (eg.: --python3 todo.py), delivers an error message
    if not any(inputs):
        error_msg+="\nPlease enter an option. To get help, type --help or --h\n"
    else:
        # tests if 'due' and 'priority' commands were given along with an 'add' command. In case not, accumulates the error msg for further printing
        if args.due:
            if not args.add:
                error_msg += "\nPlease --add a task to insert a due date\n"

        if args.priority:
            if not args.add:
                error_msg += "\nPlease --add a task to insert a priority\n"

        # add more tests here as needed
    return error_msg


"""# Unfold here for debugging without the terminal
class args:
    pass

args.add = 'dog' # random.choice("abcdefghijklmnopqrstuwxyzz")+random.choice("abcdefghijklmnopqrstuwxyzz")+random.choice("abcdefghijklmnopqrstuwxyzz")+random.choice("abcdefghijklmnopqrstuwxyzz")
args.priority = random.choice([1,2,3])
args.due = "12/01/2032"
error_msg=""

args.delete = 7 #1
args.done = None #5
args.list = None #True
args.report = None# True
args.query = None #['dog', '2']
args.resetID = True"""


def main():
    """ Deploys the app"""

    # parse and validate the user inputs. 
    # If any invalid input, prints an error message in the terminal and exits the app.
    args = parse_args()
    error_msg = validate_args(args)
    if len(error_msg)>0:
        print(error_msg)
        exit()

    else:
        tasks = TaskManager.Tasks()

        # calls the appropriate method depending on the user input.
        # Each Tasks method returns an appropiate 'msg' to print in the terminal either in case of success or failure of the operation (e.g.: did not find the ID of a task, invalid dates)
          # Note 1: implementation allows for multiple inputs in the terminal (if all valid). For example, < --add "go to the beach"  --del 9 > will add and delete a task.
          # Note 2: '--add' '--priority' and '--due' date dont have to come in order.  
          # Note 3: I separated in one block for each option in case one wants to add option-specific code (example, specific error handling for '--list'). 
                    # As all methods return a standard output (a string 'msg'), can have just one block if necessary.  
          # Note 4: 'worked' is a boolean indicating if the operation was sucessful. Not used, but included because might be useful in future extensions of the app          
        if args.add:
            msg, worked = tasks.add(args.add, args.priority, args.due)
            print(msg)     

        if args.delete:
            msg, worked = tasks.delete(args.delete)
            print(msg)

        if args.done:
            msg, worked = tasks.done(args.done)
            print(msg)

        if args.list:
            msg = tasks.list_tasks()
            print(msg)

        if args.report:
            msg = tasks.report_tasks()
            print(msg)

        if args.query:
            msg, worked = tasks.query_tasks(args.query, sort_list=True)
            print(msg)

        if args.resetID:
            msg, worked = tasks.reset_IDs()
            print(msg)
        
if __name__ == "__main__":
    main()

    
    