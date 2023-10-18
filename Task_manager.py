import os
from datetime import datetime

# def user authentification
def user_authentication():
    usernames = []       # Create list for usernames
    passwords = []       # Create list for passwords

    try:
        with open("user.txt", "r") as user_file:   # open and read file
            for line in user_file:
                user_name, pass_word = line.strip().split(", ")  # strip and split file
                usernames.append(user_name)       # append to list
                passwords.append(pass_word)       # append to list

        while True:      #  use while loop to promt user for username and password 
            user_name = input("Please enter your username: ")
            pass_word = input("Please enter your password: ")
        
            if user_name in usernames and pass_word == passwords[usernames.index(user_name)]: # check list for user and pass
                print(f"Successfully logged in. Welcome {user_name}!")
                return user_name # return logged in user
            else:
                print("Invalid username or password entered. Please try again")
    
    except FileNotFoundError: # handle error if file not found
        print("Database not found. Please ensure user.txt exists")

# def main block
def main():
    try:
        logged_in_user = user_authentication()
        print(f"Logged in as: {logged_in_user}")

        admin_menu_option_s = "" # intialise additional variable option for admin only

        if logged_in_user == "admin":   # check if logged in is admin
            admin_menu_option_s = "s - statistics" # add new option menu

        while True:
            try:
                # use f string and add placeholder for admins extra stats option
                menu = input(f'''Select one of the following options:                          
                    {admin_menu_option_s}
                    r - register a user
                    a - add task
                    va - view all tasks
                    vm - view my tasks
                    e - exit
                    : ''').lower()
                
                if menu == 'r':
                    if logged_in_user == "admin":   # check if logged is admin then allow to register
                        new_user_name = input("Kindly enter a new username: ")
                        new_password = input("Kindly enter a new password: ")
                        confirm_new_password = input("Please confirm your new password: ")

                        if new_password == confirm_new_password:   # check if new pass == to confirmed pass 
                            print("User successfully registered")

                            with open("user.txt", "a") as user_file:
                                user_file.write(f"\n{new_user_name}, {new_password}") # write to file using a in desired format

                        else:
                            print("Passwords do not match. Please try again.")
                    else:
                        print("Error! Only admin can register a new user.") # handle error with else. now only admin can register

                elif menu == "a":
                    # promt user to add name of assigned user
                    assigned_user = input("Please enter the username of the person who the task is assigned to: ")

                    with open("user.txt", "r") as user_file:  # open and read user.txt file
                        usernames = [line.strip().split(", ")[0] for line in user_file]  

                    if assigned_user not in usernames:   # handle error if user not found in usernames
                        print("User not found. Choose r to register user first")
                        continue

                    task_name = input("Please enter the title of the task: ")  # promt user for task
                    task_description = input("Please enter the description of the task: ")  # promt user for task description

                    while True:
                        try:
                            task_date = input("Please enter the due date of the task (DD-MM-YYYY): ")  # get task date
                            task_date = datetime.strptime(task_date, "%d-%m-%Y").strftime("%d-%m-%Y") # add date format
                            break
                        except ValueError: # handle error if date is added incorrectly
                            print("Invalid date format entered. Please use the format DD-MM-YYYY")

                    while True:
                        try:
                            task_status = input("Please enter the current status of the task (Yes or No): ") # get task status
                            if task_status.lower() == "yes" or task_status.lower() == "no": # convert input to lowercase
                                break         # break if added correctly
                        except ValueError:    # error handle for incorrect Yes or No input
                            print("Please enter Yes or No")

                    current_date = datetime.today().strftime("%d-%m-%Y") # get current date (datetime library imported)

                    with open("tasks.txt", "a") as tasks_file: # open file and write to file all inputs
                        tasks_file.write(f"\n{assigned_user}, {task_name}, {task_description}, {current_date}, {task_date}, {task_status}")

                    print("Task successfully added") # message added to confirm task addition

                elif menu == 'va':
                    try:
                        with open("tasks.txt", "r") as file: # read task file
                            tasks = [] # create tasks list

                            for line in file:  # iterate through file
                                task_data = line.strip().split(", ") # split and strip file to task data
                                # unpack task data 
                                assigned_user, task_name, task_description, task_assigned_date, task_date, task_status = task_data
                                 
                                # create a list with task info
                                task_info = [
                                    f"Assigned to: {assigned_user}",
                                    f"Task Title: {task_name}",
                                    f"Task Description: {task_description}",
                                    f"Task Assigned Date: {task_assigned_date}",
                                    f"Task Due Date: {task_date}",
                                    f"Task Status: {task_status}",
                                    "=" * 30          # create a line separator between tasks 
                                ]

                                print("\n".join(task_info)) # print task info and join list elements with a new line character

                    except FileNotFoundError:   # add error handling if file now found - try except block 
                        print("Task database not found. Please make sure tasks database is available")

                elif menu == 'vm':
                    with open("tasks.txt", "r") as file:  # open and read task file
                        tasks = []   # create empty list to store task data

                        for line in file: # iterate through file
                            task_data = line.strip().split(", ")  # split into elements
                            tasks.append(task_data)  # append task data to tasks list
                    
                    print("Your Tasks: ")
                    for task in tasks:  # iterate through task list
                        # unpack data
                        assigned_user, task_name, task_description, task_assigned_date, task_date, task_status = task
                        task_found = False 

                        if assigned_user == logged_in_user:  # check if the assigned user is == to logged in user
                            task_found = True
                            print(f"Assigned To: {assigned_user}")
                            print(f"Task Name: {task_name}")
                            print(f"Task Description: {task_description}")
                            print(f"Task Due Date: {task_date}")
                            print(f"Task Assigned Date: {task_assigned_date}")
                            print(f"Task Status: {task_status}")
                            print("=" * 30)
                            
                    if not task_found:
                        print("You have no tasks assigned")
                        

                elif menu == 's' and logged_in_user == "admin":   # check if logged user is the admin
                    with open("user.txt", "r") as user_file:  # open user file and read
                        total_users = len(user_file.readlines())   # read the lines of the file and use len to count them

                    with open("tasks.txt", "r") as tasks_file:
                        total_tasks = len(tasks_file.readlines())  # read the lines of the file and use leg\n to count them

                    print(f"Total number of users registered: {total_users}")  # print total users
                    print(f"Total number of tasks: {total_tasks}")      # print total tasks

                elif menu == 'e':
                    print('Goodbye!!!')
                    break

                else:
                    print("You have entered an invalid option. Please try again")

            except ValueError:    # handle error if any other character is entered (try except used)
                print("You have entered an invalid option. Please try again")

    except Exception as e:   # error handling added for user login 
        print("An error has occurred. Please try again", e)

# main function executed of code 
if __name__ == "__main__":
    main()
