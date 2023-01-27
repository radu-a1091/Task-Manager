"""A program that helps a small business manage users and tasks"""
import datetime

def read_users():
    """A function that reads and returns the user data (username and password)
    in a dictionary format where username is the username is the key and
    the password is the value"""
    user_info_dict = {}
    with open("user.txt","r") as f:
        user_lines = ''
        for line in f:
            user_lines += line
        user_lines = user_lines.split("\n")
        for i in range(len(user_lines)):
            user_lines[i] = user_lines[i].split(", ")
        for i in range(len(user_lines)):
            user_info_dict[user_lines[i][0]] = user_lines[i][1]
    f.close()
    return user_info_dict

def read_tasks():
    """A fucntion that reads and returns the tasks data in a list format of dictionaries
    where each task information is added to it's corresponding key value.
    It also adds a task ID for traceability."""
    task_info = {}
    with open('tasks.txt','r') as f:
        lines = ''
        for line in f:
            lines += line
    f.close()
    lines = lines.split("\n")
    for i in range(len(lines)):
        lines[i] = lines[i].split(", ")
    tasks_all = []
    for i in range(len(lines)):
        task_info = {}
        task_info["id"] = i
        task_info["who"] = lines[i][0]
        task_info["name"] = lines[i][1]
        task_info["description"] = lines[i][2]
        task_info["added"] = lines[i][3]
        task_info["due"] = lines[i][4]
        task_info["status"] = lines[i][5]
        tasks_all.append(task_info)
    return tasks_all

def view_all():
    """A function that reads all the tasks and displays in a user friendly format
    a report with all the tasks per user."""
    tasks_all = read_tasks()
    users_all = read_users()
    for user in users_all:
        print(f"\033[1m{user.capitalize()}\'s tasks are:\033[0m")
        for i in range(len(tasks_all)):
            if tasks_all[i]['who'] == user:
                print(f"""
        Task Title:        {tasks_all[i]["name"]}
        Task Description:  {tasks_all[i]["description"]}
        Added Date:        {tasks_all[i]["added"]}
        Due Date:          {tasks_all[i]["due"]}
        Completion Status: {tasks_all[i]["status"]}\n""")

def view_mine(n):
    """A function that reads all the tasks and displays in a user friendly format
    a detailed report with all the tasks assigned to a specific user.
    It takes as input the username for which the tasks should be run."""
    task_list = read_tasks()
    all_users = read_users()
    users_with_tasks = []
    for i in range(len(task_list)):
        users_with_tasks.append(task_list[i]["who"])
    if n in all_users.keys() and n not in users_with_tasks:
        print(f"The user {n} does not have any tasks assigned.")
    else:
        for key in all_users.keys():
            if key == n:
                print(f"\033[1mYour tasks are:\033[0m")
                for i in range(len(task_list)):
                        if task_list[i]["who"] == n:
                            print(f"""
        Task ID:           {task_list[i]["id"]}
        Task Title:        {task_list[i]["name"]}
        Task Description:  {task_list[i]["description"]}
        Added Date:        {task_list[i]["added"]}
        Due Date:          {task_list[i]["due"]}
        Completion Status: {task_list[i]["status"]}\n""")
                    

def reg_user():
    """A function that adds a new user to the user database.
    Displays a successful message if the user was added to the database or
    a specific error message if there was an error."""
    all_users = read_users()
    n = input("Please enter the username you want to add: ")
    while n in all_users.keys():
        print("User already exists. Please try again. ")
        n = input("Please enter the username you want to add: ")

    p = input(f"Please enter the password for {n}: ")
    p_conf = input(f"Please confirm the password for {n}: ")
    if p == p_conf:
        with open("user.txt","a") as f:
            f.write("\n"+n+", "+p)
        f.close()
        print(f"{n} successfuly registered. ")
    else:
        print("The password doesn't match. Please try again. ")
        valid_pass = False
        while not valid_pass:
            p = input(f"Please enter the password for {n}: ")
            p_conf = input(f"Please confirm the password for {n}: ")
            if p == p_conf:
                with open("user.txt","a") as f:
                    f.write("\n"+n+", "+p)
                f.close()
                valid_pass = True
                print(f"{n} successfuly registered. ")
    
def add_task():
    """A function that adds a new task to the tasks database.
    Is taking the following user input within the function:
    the asignee, the title, the task description, the due date;
    the added date is set to the date when the task was added, current date and
    the default task status is sent to 'No'."""
    user_options = []
    for key in read_users().keys():
        user_options.append(key)
    who = input("Enter the asignee's name: ")
    valid_who = True
    if who not in user_options:
        valid_who = False
        while not valid_who:
            who = input(f"""Invalid username.
Select from below or restart the program and ask admin to create one.
{user_options}\n""")
            if who in user_options:
                valid_who = True
    title = input("What is the title of the task? ")
    desc = input("Please write a short description of the task? ")
    due = input("when is the task due? (Format: 10 Oct 2022) ")
    current_date = datetime.datetime.now()
    date_format = '%d %b %Y'
    current_date = current_date.strftime(date_format)
    to_write = f"\n{who}, {title}, {desc}, {due}, {current_date}, {due}, No"
    with open("tasks.txt","a") as f:
        f.write(to_write)
    f.close()
    print("Task successfully added")

def overwrite_tasks(new_info):
    """A function that overwrites the tasks database with new data.
    It takes the new data as parameter."""
    with open("tasks.txt","w") as f:
        pass
    f.close()
    with open("tasks.txt","w") as f:
        for i in new_info:
            f.write(i)
    f.close()

def update_sts(id):
    """A function that updates the status of a task in task database to 'Yes'.
    It takes the task ID as parameter and overwirites the data in task database."""
    tasks_all = read_tasks()
    line = tasks_all[int(id)]
    doc_line = ''
    if line['status'] == "Yes":
        print("Completed task can not be updated. ")
    else:
        line['status'] = "Yes"
        update_data = []
        for item in tasks_all:
            for key in item:
                if key != "id":
                    if key != "status":
                        doc_line += str(item[key])
                        doc_line += ", "
                    else:
                        if item == tasks_all[-1]:
                            doc_line += str(item['status'])
                        else:
                            doc_line += str(item['status'])
                            doc_line += "\n"
                        
        update_data.append(doc_line)
        overwrite_tasks(update_data)
        print("Task successfully updated.")

def update_details(id,what,param):
    """A function that update either the asignee or the due date of a task.
    It takes as parameters the taks ID, the field to update and the new field value.
    It displays an error message if the task is completed or a positive message if
    the task was successfully updated."""
    tasks_all = read_tasks()
    line = tasks_all[int(id)]
    doc_line = ''
    if line['status'] == 'Yes':
        print("Completed tasks can not be updated. ")
    else:
        if what == "2":
            line['who'] = str(param)
        else:
            line['due'] = str(param)
        update_data = []
        for item in tasks_all:
            for key in item:
                if key != "id":
                    if key != "status":
                        doc_line += str(item[key])
                        doc_line += ", "
                    else:
                        if item == tasks_all[-1]:
                            doc_line += str(item['status'])
                        else:
                            doc_line += str(item['status'])
                            doc_line += "\n"
        update_data.append(doc_line)
        overwrite_tasks(update_data)
        print("Task successfully updated.")

def task_reports():
    """A function that updates task_overview document or creates it if it does not exist
    with a user friendly view of the current task analysis."""
    tasks_all = read_tasks()
    num_tasks = 0
    num_comp_tasks = 0
    num_uncomp_tasks = 0
    num_uncomp_overdue_tasks = 0
    date_now = datetime.datetime.now()
    for dictionary in tasks_all:
        num_tasks += 1
        dictionary['due'] = datetime.datetime.strptime(dictionary['due'],'%d %b %Y')
        if dictionary['due'] < date_now and dictionary['status'] == "No":
            num_uncomp_overdue_tasks += 1
        if dictionary['status'] == "No":
            num_uncomp_tasks += 1
        if dictionary['status'] == "Yes":
            num_comp_tasks += 1
    to_write = (f"""Tasks overview report:

Total number of tasks:                          {num_tasks}
Total number of completed taks:                 {num_comp_tasks}
Total number of uncompleted tasks:              {num_uncomp_tasks}
Total number of uncompleted and overdue tasks:  {num_uncomp_overdue_tasks}
Percentage of incomplete tasks:                 {round(num_uncomp_tasks / num_tasks * 100,2)}%
Percentage of incomplete and overdue tasks:     {round(num_uncomp_overdue_tasks / num_tasks * 100,2)}%""")
    # clearing the contents of "tasks_overview.txt" file
    # if it doesn't exist, it will create it blank
    with open("task_overview.txt","w") as f:
        pass
    f.close()
    # writing "to_write"'s contents to the "task_overview.txt" 
    with open("task_overview.txt","w") as f:
        f.write(to_write)
    f.close()

def user_reports():
    """A function that updates user_overview document or is creating it if it doesn't exist
    with a user friendly view of the current task analysis per user"""
    tasks_all = read_tasks()
    users_all = read_users()
    num_tasks_all = 0
    
    users_with_tasks = []
    for i in range(len(tasks_all)):
        users_with_tasks.append(tasks_all[i]['who'])
    for i in users_with_tasks:
        num_tasks_all += 1
    unique_users = []
    for i in users_with_tasks:
        if i not in unique_users:
            unique_users.append(i)
    unique_count_dict = {}
    for i in unique_users:
        unique_count = 0
        for j in range(len(tasks_all)):
            if tasks_all[j]['who'] == i:
                unique_count += 1
        unique_count_dict[i] = unique_count
    to_write = ''
    to_write += (f"""User overview report:

Total number of registered users: {len(unique_users)}""")
    to_write += f"\nTotal number of tasks:\t\t\t  {len(tasks_all)}\n"
    to_write += "-"*60
    for user in users_all:
        if user in unique_users:
            to_write += f"\n{user.capitalize()}'s metrics:"
            to_write += f"""\n\tTotal tasks assinged:\t\t\t\t\t\t\t    {unique_count_dict[user]}
\tPercentage of assigned tasks:\t\t\t\t\t    {round(unique_count_dict[user]/len(tasks_all)*100,2)}%"""
            completed = 0
            incomplete = 0
            incomplete_overdue = 0
            date_now = datetime.datetime.now().date()
            for dictionary in tasks_all:
                try:
                    dictionary['due'] = datetime.datetime.strptime(dictionary['due'],"%d %b %Y").date()
                except:
                    pass
                if dictionary['due'] < date_now and dictionary['who'] == user and dictionary['status'] == "n":
                    incomplete_overdue += 1
                if dictionary['who'] == user and dictionary['status'] == 'No':
                    incomplete += 1
                if dictionary['who'] == user and dictionary['status'] == 'Yes':
                    completed += 1
            to_write += f"""\n\tPercentage of completed tasks assigned:\t\t\t    {round(completed / unique_count_dict[user] * 100,2)}%
\tPercentage of incompleted tasks assigned:\t\t    {round(incomplete / unique_count_dict[user] * 100,2)}%
\tPercentage of incomplete and overdue tasks assigne: {round(incomplete_overdue / unique_count_dict[user] * 100,2)}%
"""
            to_write += "-"*60
        else:
            to_write += f"\n{user.capitalize()}'s metrics:"
            to_write += f"""\n\tTotal tasks assinged:\t\t\t\t\t\t\t    0
\tPercentage of assigned tasks:\t\t\t\t\t    0.00%
\tPercentage of completed tasks assigned:\t\t\t    0.00%
\tPercentage of incompleted tasks assigned:\t\t    0.00%
\tPercentage of incomplete and overdue tasks assigne: 0.00%
"""
            to_write += "-"*60
    with open("user_overview.txt","w") as f:
        pass
    f.close()
    with open("user_overview.txt","w") as f:
        f.write(to_write)
    f.close()

user_database = read_users()
username = input("Please enter your username: ")
while username not in user_database.keys():
    username = input("Incorrect username. Please enter your correct username: ")

entred_pswd = input("Please enter your password: ")
while entred_pswd not in user_database.values():
    entred_pswd = input("Incorrect password. Please enter your password: ")

while True:
    if username == 'admin':
        menu = input('''Select one of the following Options below:
    r  - Register a user
    a  - Add a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics
    e  - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r  - Register a user
    a  - Add a task
    va - View all tasks
    vm - view my task
    e - Exit
    : ''').lower()

    if menu == 'r':
        if username == 'admin':
            reg_user()
        else:
            print("You do not have authorisation to add users.\n")
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == "vm":
        view_mine(username)
        while True:
            wants_update = input("""Would you like to do next?
 1 - update task
-1 - return to the main menu
""").lower()
            while wants_update not in ["1","-1"]:
                wants_update = input("Would you like to update a task? (Y/N) ").lower()
            if wants_update == "1":
                while True:
                    update_id = input("What is the id of the task to update? ")
                    update_what = input("""What do you want to update?
    1 - update status to "Yes"
    2 - update the asignee of the task
    3 - update the due date of the task""")
                    if update_what == "1":
                        update_sts(update_id)
                        break
                    elif update_what == "2":
                        new_assignee = input("Who is the new asignee? ")
                        update_details(update_id,update_what,new_assignee)
                        break
                    elif update_what == "3":
                        new_due_date = input("what is the new due date? (Format: 10 Oct 2022) ")
                        update_details(update_id,update_what,new_due_date)
                        break
                    else:
                        print("incorrect selection.")
            elif wants_update == "-1":
                break
            else:
                print("incorrect input. Program ending")
                break
    elif menu == "gr":
        user_reports()
        task_reports()
    elif menu == "ds":
        try:
            
            with open("task_overview.txt","r") as f:
                to_display =''
                for line in f:
                    to_display += line
            f.close()
            print(to_display)
            with open("user_overview.txt","r") as f:
                to_display =''
                for line in f:
                    to_display += line
            f.close()
            print(to_display)
        except:
            task_reports()
            user_reports()
            to_display =''
            with open("task_overview.txt","r") as f:
                to_display =''
                for line in f:
                    to_display += line
            f.close()
            print(to_display)
            with open("user_overview.txt","r") as f:
                to_display =''
                for line in f:
                    to_display += line
            f.close()
            print(to_display)
    elif menu == "e":
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")