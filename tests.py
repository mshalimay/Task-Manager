      
    
class Tasks(object):
    """A list of `Task` objects."""

    min_priority = 1
    max_priority = 3
 
    def __init__(self):
        """Read pickled tasks file into a list"""
        self.filename = ".todo.pickle"

class Task(Tasks):
    def __init__(self, priority=None, due_dt=None):
        self.priority = priority if priority else Tasks.min_priority
            
x = Tasks()


y = Task()

y.age = 1

y.age

from typing import Type
import uuid

myuuid = uuid.uuid4()
myuuid2 = uuid.uuid4()


#--

from datetime import datetime, tzinfo

x = datetime.today()
y = datetime.today()

z = (y-x).days

##--- test sort, filter


#%%
import datetime

class Task():
    def __init__(self, due_dt, priority, name):
        self.due_dt = due_dt
        self.priority = priority
        self.name = name

date1 = datetime.datetime.strptime(f"12/07/2024", "%d/%m/%Y")
date2 = datetime.datetime.strptime("01/12/2022", "%d/%m/%Y")
date3 = datetime.datetime.strptime("01/12/2023", "%m/%d/%Y")


task1 = Task(date1, 1, "walk dog")
task2 = Task(date1, 3, "study finals")
task4 = Task(date2, 2, "buy eggs")
task3 = Task(None, 3, "make eggs")
task5 = Task(None, 4, "work-out")
task6 = Task(None, 4, "eggs again")

lista = [task1, task2, task3, task4, task5, task6]

lista = sorted(lista, key = lambda task: (task.due_dt is not None, task.due_dt, task.priority), reverse=True)

date_priority = [(task.due_dt, task.priority, task.name) for task in lista]


task6.__getattribute__("due_dt")

from tabulate import tabulate

dict_attributes = {"ID":"name", "Due Date": "due_dt"}
def tabulate_tasks(dict_attributes, tasks_list):
    dict_print = {key:[] for key in dict_attributes}
    for task in tasks_list:
        for header, attribute in dict_attributes.items():
            attribute = task.__getattribute__(attribute)
            attribute = attribute if attribute else "-"
            dict_print[header].append(attribute)
    return tabulate(dict_print, headers="keys"), dict_print


x,y  = tabulate_tasks(dict_attributes, lista)

# test query
queries = ['dog', 'eggs']
filtered_list = []
for query in queries:
    for task in filter(lambda task: query in task.name, lista):
        filtered_list.append(task)

        

x= [*filtered_list]

for x_i in x:
    print(x_i.name)


#%%
def test():
    raise ValueError("testing this error")

