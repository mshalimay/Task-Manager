


import argparse

parser = argparse.ArgumentParser(description='Todo list')


parser.add_argument('--add', type = str, required = False, help = 'a task string to add to your list')
parser.add_argument('--due', type = str, required = False, help = 'due date in dd/mm/yyyy format')
#parser.add_argument('--priority', type = int, required = False, default = 1, help = 'priority of taks; default value is 1')
parser.add_argument('--query', type = str, required = False, nargs = "+", help = 'lists all tasks that have not been completed')
parser.add_argument('--list', action='store_true' , required = False, help = 'lists all tasks that have not been completed')
parser.add_argument('--done', type = int, required = False, 
                        help = "Mark a task as completed. Input is a whole number representing the unique ID of the task.")

parser.add_argument('--del', type = int, required = False, dest="delete",
                        help = "Delete a task. Input is a whole number representing the unique ID of the task.")



# .add mesmo; ele interpreta os "--" como flags automaticamente, retirando eles aqui dentro do py
# in fact, o programa nem funciona na cmd se não colocar aqui no python um '-' ou '--' na frente do comando add, due, etc

args = parser.parse_args()
values = list(vars(args).values())

values[1]=True
any(values)

for arg in args:
    print(arg)