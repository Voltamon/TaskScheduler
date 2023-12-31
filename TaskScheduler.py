import json
from datetime import datetime

#A package to schedule your tasks effectively (Taskito)
class TaskScheduler():
    def __init__(self):
        pass
    
    #method to load the tasks from Schedule.json
    def load_tasks(self):
        sch_file = open('Schedule.json', 'r')
        schedule = json.load(sch_file)
        return schedule
    
    #method to update tasks from Schedule.json
    def save_tasks(self, schedule):
        sch_file = open('Schedule.json', 'w')
        sch = json.dumps(schedule)
        sch_file.write(sch)
    
    #method to add a task to Schedule.json
    def add_task(self, task, time):
        tasks = self.load_tasks()
        
        if not time in tasks:
            tasks[time] = [(task, False)]
        else:
            tasks[time].append((task, False))
        self.save_tasks(tasks)
        self.main()
    
    #method to remove a task from Schedule.json
    def remove_task(self, task, time):
        try: 
            tasks = self.load_tasks()
            
            if time in tasks:
                if task in tasks[time]:
                    self.set_task_status(task, time, False)
                    tasks[time].remove((task, False))
                    print()
                    print(f'Task {task} Removed')
                    self.save_tasks(tasks)
                else:
                    raise Exception
            else:
                raise Exception
        except Exception:
            print()
            print("No such Task Found in the list")
        self.main()

    #method to remove tasks older than today
    def update_tasks(self):
        tasks = self.load_tasks()
        old_tasks = []

        for i in tasks.keys():
            if self.checkDate(i):
                old_tasks.append(i)
            
            if tasks[i] == list():
                old_tasks.append(i)
            
        for i in old_tasks:
            del tasks[i]
            
        self.save_tasks(tasks)
    
    #method to check if the date is older than today's date
    def checkDate(self, date):
        current_date = str(datetime.now().date())
        current_year = int(current_date[0:4])
        current_month = int(current_date[5:7])
        current_day = int(current_date[8:10])

        date_to_check = date
        check_year = int(date_to_check[0:4])
        check_month = int(date_to_check[5:7])
        check_day = int(date_to_check[8:10])

        if check_year < current_year:
            return True
        else:
            if check_month < current_month:
                return True
            else:
                if check_day < current_day:
                    return True
                else:
                    return False
    
    #method to check if the time is in the right format
    def checkTime(self, time):
        try:
            time = datetime.strptime(time, '%H:%M:%S')
            today = datetime.now().date()
            time = datetime.combine(today,time.time())
        except ValueError:
            return [False]
        
        return [True, str(time)]
    
    #method to set the status of the task
    def set_task_status(self, task, time, status):
        tasks = self.load_tasks()
        flag = False
        print()
        
        try:
            if time in tasks.keys():
                ls_task = tasks[time]
                
                for i in ls_task:
                    if task == i[0]:
                        i[1] = status
                        flag = True
            else:
                raise Exception
            
            if flag:
                tasks[time] = ls_task
                self.save_tasks(tasks)
            else:
                raise Exception
        except Exception:
            print()
            print("No such Task Found in the list")
            print()
            
        self.display()
    
    #method to see a list of all your task in sequence:
    def display(self):
        tasks = self.load_tasks()
        tasks = {k: tasks[k] for k in sorted(tasks)}
        
        for i, j in tasks.items():
            
            if j[0][1]:
                tick = u'[\u2713]'
            else:
                tick = '[ ]'
            
            print(f'{i[11:]} | {tick} {j[0][0]}')
            for k in range(1, len(j)):
                if j[k][1]:
                    tick = u'[\u2713]'
                else:
                    tick = '[ ]'
                print(f'         | {tick} {j[k][0]}')
            print()

        self.menu(1)
        
        try:
            print()
            ch = int(input("Enter your choice : "))
            print()
            
            if ch == 1:
                task = input("Enter task : ")
                time = input("Enter time (in UTC) [HH:MM:SS] : ")
                time = time.replace(" ", "")
            
                if self.checkTime(time)[0]:
                    self.set_task_status(task, self.checkTime(time)[1], True)
                else:
                    raise TimeoutError
            elif ch == 2:
                task = input("Enter task : ")
                time = input("Enter time (in UTC) [HH:MM:SS] : ")
                time = time.replace(" ", "")
            
                if self.checkTime(time)[0]:
                    self.set_task_status(task, self.checkTime(time)[1], False)
                else:
                    raise TimeoutError
            elif ch == 3:
                pass
            else:
                raise ValueError
        except ValueError:
            print()
            print("Invalid Input, Try Again")
            print()
        except TimeoutError:
            print()
            print("Invalid Time Format, Try Again")
            print()
        
        self.main()
    
    #method to display the menu/s
    def menu(self, ch):
        if ch == 0:
            print()
            print(" ~~~Taskito~~~   ")
            print()
            
            print("1> Add Task")
            print("2> Remove Task")
            print("3> View Tasks")
            print("4> Exit")
            print()
        else:
            print("1> Mark Done")
            print("2> Mark Undone")
            print("3> Return to Main Menu")
            print()
    
    #main function of the class to call all other methods
    def main(self):
        self.menu(0)
        self.update_tasks()
        
        try:
            print()
            ch = int(input("Enter your choice : "))
            print()
            
            if ch == 1:
                task = input("Enter task : ")
                time = input("Enter time (in UTC) [HH:MM:SS] : ")
                time = time.replace(" ", "")
                
                if self.checkTime(time)[0]:
                    self.add_task(task, self.checkTime(time)[1])
                else:
                    raise TimeoutError
            elif ch == 2:
                task = input("Enter task : ")
                time = input("Enter time (in UTC) [HH:MM:SS] : ")
                time = time.replace(" ", "")
                
                if self.checkTime(time)[0]:
                    self.remove_task(task, self.checkTime(time)[1])
                else:
                    raise TimeoutError
            elif ch == 3:
                self.display()
            elif ch == 4:
                exit()
            else:
                raise ValueError
        except ValueError:
            print()
            print("Invalid Input, Try Again")
            self.main()
        except TimeoutError:
            print()
            print("Invalid Time Format, Try Again")
            self.main()
        
if __name__ == "__main__":
    TaskScheduler().main()
    