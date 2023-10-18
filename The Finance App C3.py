# import libraries
import sqlite3
from datetime import datetime, date

# connect to database
db = sqlite3.connect('finances.db')

# create a cursor
cursor = db.cursor()

# create all tables
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
               expense_id INTEGER PRIMARY KEY AUTOINCREMENT , category TEXT,
               date DATE, description TEXT, amount REAL,
               user_id TEXT) 
               ''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS income (
               income_id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT,
               date DATE, description TEXT, amount REAL,
               user_id TEXT)
               ''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS budget (
               budget_id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT,
               amount REAL, user_id TEXT)
               ''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS financial_goals (
               goal_id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT,
               goal_name TEXT, target_amount REAL, 
               current_amount_saved REAL, target_date DATE)''')
db.commit()

# Create class for each table
class Expense():
    def __init__(self, category=None, amount=None, date=None, description=None,
                user_id=None):
        self.amount = amount
        self.date = date
        self.description = description
        self.category = category
        self.user_id = user_id

    def add_expense(self):
        '''This method will add an expense 
        and insert it into the expense table'''

        current_date = date.today()

        category = input("Please enter the expense category\n")
        amount = float(input("Please enter the amount of the expense\n"))
        description = input("Please enter a description for the expense\n")
        user_id = input("Please enter your user id\n")

        cursor.execute(''' INSERT INTO expenses 
                       (category, amount, date, description,  
                       user_id) 
                       VALUES  (?, ?, ?, ?, ?)''', (category, amount, current_date, description, user_id))
        
        db.commit()
        print("New expense added!")
        return
    
    def view_expenses(self):
        '''This method will select all expenses from the table
        and display using indicees '''

        cursor.execute(''' SELECT * FROM expenses''')
        expenses = cursor.fetchall()

        # check for expenses
        if expenses:
            print("All expenses")
            for expense in expenses:
                print(f"Expense ID: {expense[0]} "
                      f"Category: {expense[1]} "
                      f"Date: {expense[2]} "
                      f"Description: {expense[3]} "
                      f"Amount: {expense[4]} "
                      f"User ID: {expense[5]} "
                      )
        # error handled if not found
        else:
            print("There are no expenses!")
            return
        db.commit()             
        

    def view_expense_by_category(self):
        ''' This method will select a coloum using the promted
        category from the user, it will display using indicees'''

        category_select = input("Please enter the category of expenses you would like to view\n")
        category_select_lower = category_select.lower()
        cursor.execute(''' SELECT * FROM expenses WHERE LOWER(category) = ?''', (category_select_lower,))
        expenses = cursor.fetchall()

        # check for expenses
        if expenses:
            print(f"All expenses for category {category_select}: ")
            for expense in expenses:
                    print(f"Expense ID: {expense[0]} "
                          f"Category: {expense[1]} "
                          f"Date: {expense[2]} "
                        f"Description: {expense[3]} "
                        f"Amount: {expense[4]} "
                        f"User ID: {expense[5]} "
                        )
        # error handled if not found        
        else:
            print(f"There are no expenses found for {category_select} ")
                    
        db.commit()

    def update_expense(self):
        '''This method takes the expense id and updates the table
        using update SQL commands'''

        choice = int(input('''Please select an option: 
                       1. View all expenses before updating
                       2. View all expenses by category before updating
                       3. Continue without viewing\n'''))

        if choice == 1:
            self.view_expenses()
        elif choice == 2:
            self.view_expense_by_category()
        elif choice == 3:
            pass

        id = int(input("Please enter the expense id you like to update the amount of\n"))

        cursor.execute(''' SELECT expense_id FROM expenses WHERE expense_id  = ?''', (id,))
        existing_id = cursor.fetchone()

        # a check is done if the id does not exist
        if not existing_id:
            print("This expense id does not exist. Please enter an existing id")
            return
        new_amount = float(input("Please enter the new amount to be updated\n"))

        cursor.execute(''' UPDATE expenses
                        SET amount = ?
                        WHERE expense_id = ?''', (new_amount,id))
        
        db.commit()
        print("Amount Updated!")
        return
    
    def delete_expense(self):
        ''' This method deletes an expense from the table
        using the appropriate SQL commands, and it prompts
        the user for the expense id'''

        choice = int(input('''Please select an option: 
                       1. View all expenses before deleting
                       2. View all expenses by category before deleting
                       3. Continue without viewing\n'''))

        if choice == 1:
            self.view_expenses()
        elif choice == 2:
            self.view_expense_by_category()
        elif choice == 3:
            pass

        del_id = int(input('''Please enter the expense id you would like to delete
                           ***WARNING*** this expense will be permanantely deleted!\n'''))
        cursor.execute(''' SELECT expense_id FROM expenses WHERE expense_id = ?''', (del_id,))
        existing_id = cursor.fetchone()

        # check if the id exists and add error message
        if not existing_id:
            print("This expense id does not exist. Please enter an existing id")
            return
        
        cursor.execute(''' DELETE FROM expenses WHERE expense_id = ?''', (del_id,))
        
        db.commit()
        print("Expense Record Deleted!")
        return

# create income class
class Income():
    def __init__(self, category=None, amount=None, description=None, date=None, user_id=None):
        self.category = category
        self.amount = amount
        self.description = description
        self.date = date
        self.user_id = user_id

    def add_income(self):
        '''This method promts the user to add an income
        and inserts the info into the income table'''

        current_date = date.today()

        category = input("Please enter the income category\n")
        amount = float(input("Please enter the amount of income\n"))
        description = input("Please enter the income description\n")
        user_id = input("Please enter your user id no\n")

        cursor.execute(''' INSERT INTO income
                       (category, amount, date, description, user_id)
                       VALUES (?, ?, ?, ?, ?)''', (category, amount, current_date, 
                                                  description, user_id)) 
        db.commit()
        print("New Income Added!")
        return

    def view_incomes(self):
        '''This method selects all info from 
        the income table and displays it accordingly'''

        cursor.execute(''' SELECT * FROM income''')
        incomes = cursor.fetchall()

        if incomes:
            print("All incomes: ")
            for income in incomes:
                print(f"Income ID:  {income[0]} "
                      f"Category: {income[1]} "
                      f"Date: {income[2]} "
                      f"Description: {income[3]} "
                      f"Amount: {income[4]} "
                      f"User ID no: {income[5]}"
                    )
        else:
            print("There are no incomes recorded yet!")
            db.commit()
            return

    def view_income_by_category(self):
        '''This method displays info based on a category
        search that is promted from the user'''

        category_select = input("Please enter the category of incomes you would like to view\n").lower()
        cursor.execute(''' SELECT * FROM income WHERE LOWER(category) = ?''', (category_select,))
        incomes = cursor.fetchall()
        
        if incomes:
            print(f"All incomes for category {category_select}: ")
        
            for income in incomes:
                print(f"Income ID: {income[0]} "
                      f"Category: {income[1]} "
                    f"Date: {income[2]} "
                    f"Descriptiom: {income[3]} "
                    f"Amount: {income[4]} "
                    f"User ID: {income[5]}"
                    )
        else:
            print(f"There are no incomes found for {category_select} ")
        db.commit()
        return
    
    
    def update_income(self):
        '''This method updates the income table
        using the update and set sql commands'''

        choice = int(input('''Please select an option: 
                       1. View all incomes before updating
                       2. View all incomes by category before updating
                       3. Continue without viewing\n'''))

        if choice == 1:
            self.view_incomes()
        elif choice == 2:
            self.view_income_by_category()
        elif choice == 3:
            pass
        
        id = int(input("Please enter the income id you would like to change the amount of:\n"))

        cursor.execute(''' SELECT income_id FROM income WHERE income_id = ?''', (id,))
        current_id = cursor.fetchone()

        # check if the id exists
        if not current_id:
            print("This income id does not exist. Please enter an existing id")
            return
        new_amount = float(input("Please enter the new amount now:\n"))

        cursor.execute(''' UPDATE income
                       SET amount = ?
                       WHERE income_id = ?''', (new_amount, id))
        print("Income amount Updated!")
        db.commit()
        return

    def delete_income(self):
        '''This method deletes an income from
        the table using the delete sql commands'''

        choice = int(input('''Please select an option: 
                       1. View all incomes before deleting
                       2. View all incomes by category before deleting
                       3. Continue without viewing\n'''))

        if choice == 1:
            self.view_incomes()
        elif choice == 2:
            self.view_income_by_category()
        elif choice == 3:
            pass
        
        del_id = int(input('''Please enter the income id you would like to delete
                           ***WARNING*** this income will be permanently deleted!\n'''))
        cursor.execute(''' SELECT income_id FROM income WHERE income_id = ?''', (del_id,))
        existing_id = cursor.fetchone()
        
        # check if the id exists
        if not existing_id:
            print("This income record does not exist. Please enter an existing ID")
            return
        
        cursor.execute(''' DELETE FROM income WHERE income_id = ?''', (del_id,))

        print("Income Record Deleted")
        db.commit()
        return

# create a class for budgets
class Budget():
    def __init__(self, category=None, amount=None, user_id=None):
        self.category = category
        self.amount = amount
        self.user_id = user_id

    def set_budget(self):
        '''This method promts the user to set a budget
        and inserts into the budget table'''

        category = input("Please enter the category for which you would like to set the budget for\n")
        amount = float(input("Please enter the budget amount for this category\n"))
        user_id = input("Please enter your user id no\n")

        cursor.execute(''' INSERT INTO budget (category, amount, user_id)
                       VALUES (?, ?, ?)''', (category, amount, user_id))
        
        db.commit()
        print("Budget set successfully!")
        return

    def view_budget(self):
        '''This method displays a budget 
          record by a category  '''

        category = input("Please enter the budget category you would like to view\n").lower()
        
        cursor.execute(''' SELECT amount FROM budget WHERE LOWER(category) = ?''', (category,))
        budget_amount = cursor.fetchone()

        # check if category exists
        if budget_amount is None:
            print("This category does not exist. Please enter an existing category")

        else:
            print(f"Budget for {category}: {budget_amount[0]}")
        db.commit()
        return
    
    def calculate_budget(self):
        '''This method calculates the remaining budget for
        a category searched. It takes the sum of incomes plus
        the budget given and deducts the expenes'''

        category = input("Please enter the category to view calculated budget\n").lower()

        cursor.execute('''SELECT amount FROM budget WHERE LOWER(category) = ?''', (category,))
        budget_amount = cursor.fetchone()

        if budget_amount is None:
            print("No budget has been set for this category!")
            return
        
        cursor.execute('''SELECT SUM(amount) FROM expenses WHERE LOWER(category) = ?''', (category,))
        total_expenses = cursor.fetchone()[0] or 0

        cursor.execute('''SELECT SUM(amount) FROM income WHERE LOWER(category) = ?''', (category,))
        total_income = cursor.fetchone()[0] or 0
        
        remaining_budget = budget_amount[0] + total_income - total_expenses
       
        print(f"Budget set for {category}: {budget_amount[0]:.0f}")
        print(f"Total income for {category}: {total_income}")
        print(f"Total expenses for {category}: {total_expenses}")
        print(f"Remaining budget for {category} is : {remaining_budget}")
        
        db.commit()
        return

    def view_all_budgets(self):
        '''This method displays all the budgets set.
        It fetches all from the category column and displays the budgets'''

        cursor.execute(''' SELECT category, amount FROM budget''' )
        all_budgets = cursor.fetchall()

        # check for budgets
        if all_budgets:
            print("All Budgets: ")
            for category, amount in all_budgets:
                print(f"Category: {category} Budget Amount: {amount}")
        else:
            print("No budgets set! Please set budget from the main menu")
        db.commit()
        return

    def delete_budget(self):
        '''This method deletes a budget from
        the table using the delete sql command'''

        choice = int(input('''Please select an option: 
                       1. View all budgets before deleting
                       2. Continue without viewing\n'''))

        if choice == 1:
            self.view_all_budgets()
        elif choice == 2:
            pass

        del_budget = input(''' Please enter the budget category you would like to deleted
                           ***WARNING*** This will permanently delete this record!!!\n''').lower()
        cursor.execute('''SELECT category from budget WHERE LOWER (category) = ?''', (del_budget,))
        existing_budget = cursor.fetchone()

        if existing_budget is None:
            print("This budget category does not exist. Please enter an existing budget category!")
            return
        
        cursor.execute(''' DELETE FROM budget WHERE category = ?''', (del_budget,))

        db.commit()
        print("Budget record successfully deleted!")
        return

    def update_budget_amount(self):
        '''This method updates the table using
        the update and set sql commands'''

        choice = int(input('''Please select an option: 
                       1. View all budgets before updating
                       2. Continue without viewing\n'''))

        if choice == 1:
            self.view_all_budgets()
        elif choice == 2:
            pass

        budget_category = input("Please enter the budget category you would like to update:\n").lower()
        
        cursor.execute(''' SELECT category FROM budget WHERE LOWER(category) = ?''', (budget_category,))
        existing_budget = cursor.fetchone()
        
        # check for existing budget
        if not existing_budget:
            print("This budget category does not exist. Please enter an existing category")
            return
        
        new_amount = float(input("Please enter the new amount to be updated\n"))
        print(f"New amount to be updated: {new_amount}")
        
        cursor.execute('''UPDATE budget
                       SET amount = ?
                       WHERE LOWER(category) = ?''', (new_amount, budget_category))
        
        db.commit()
        print("Budget Successfully Updated!")
        return        


# create class for financial goal
class Financial_Goal():
    def __init__(self, category=None, goal_name=None, target_amount=None, target_date=None):
        self.category = category
        self.goal_name = goal_name
        self.target_amount = target_amount
        self.target_date = target_date
        
    def view_fin_goals(self):
        '''This methods selects all info from the 
        financial goals table and displays accordingly'''

        cursor.execute('''SELECT * FROM financial_goals''')
        fin_goals = cursor.fetchall()

        if fin_goals:
            print("All financial goals: ")

            for goal in fin_goals:
                print(f"Goal ID: {goal[0]} "
                      f"Category: {goal[1]} "
                      f"Goal Name: {goal[2]} "
                      f"Target Amount: {goal[3]} "
                      f"Current Amount: {goal[4]} "
                      f"Target Date: {goal[5]} "
                      )
                print("------------------")

        else:
            print("There are no financial goals recorded yet!")
            db.commit()

    
    def set_fin_goal(self):
        '''This method promts the user to set a financial goal
        based on a budget category. It calculates and stores the 
        remaining budget in the current amount saved column within 
        the financial goals table. This allows us to use the 
        current amount saved info in the 
        view progress towards goal method'''

        category = input("Please enter the category for the financial goal\n").lower()

        cursor.execute('''SELECT amount FROM budget WHERE LOWER(category) = ?''', (category,))
        budget_amount = cursor.fetchone()
        
        # check for an existing budget first
        if budget_amount is None:
            print(f"No budget has been set for {category}. Please set a budget first.")
            return

        cursor.execute('''SELECT SUM(amount) FROM expenses WHERE LOWER(category) = ?''', (category,))
        total_expenses = cursor.fetchone()[0] or 0

        cursor.execute('''SELECT SUM(amount) FROM income WHERE LOWER(category) = ?''', (category,))
        total_income = cursor.fetchone()[0] or 0

        remaining_budget = (budget_amount[0] + total_income) - total_expenses

        goal_name = input("Please enter the name for the financial goal\n")
        target_amount = float(input("Please enter the target amount\n"))        
        target_date = input("Please enter the target date (YYYY-MM-DD)")
        try:
            target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            print('''Incorrect date format! Please enter a valid date in the format YYYY-MM-DD.
                  Please try again''')
            return

        cursor.execute('''INSERT INTO financial_goals
                       (category, goal_name, target_amount, 
                       current_amount_saved, target_date)
                       VALUES (?, ?, ?, ?, ?)''', (category, goal_name, target_amount, 
                                                      remaining_budget, target_date))
        db.commit()
        print("Financial goal successfully added!")
        return

    
    def progress_towards_fin_goals(self):
            '''This method calculates the progress as a percentage.
            It divides the remaining budget and the target amount
            * 100 to give us the progress in a percentage '''

            category = input("Please enter the category name: ").lower()

            cursor.execute('''SELECT target_amount FROM financial_goals 
                           WHERE LOWER(category) = ?''', (category,))
            goal_info = cursor.fetchone()

            # check if category exists
            if goal_info is None:
                print("This category does not exist. Please enter an existing category")
                return 

            target_amount = goal_info[0]

            cursor.execute('''SELECT amount FROM budget WHERE LOWER(category) = ?''', (category,))
            budget_amount = cursor.fetchone()

            cursor.execute('''SELECT SUM(amount) FROM expenses WHERE LOWER(category) = ?''', (category,))
            total_expenses = cursor.fetchone()[0] or 0

            cursor.execute('''SELECT SUM(amount) FROM income WHERE LOWER(category) = ?''', (category,))
            total_income = cursor.fetchone()[0] or 0

            remaining_budget = (budget_amount[0] + total_income) - total_expenses
            progress_percentage = (remaining_budget/target_amount) * 100
            
            print(f"Progress for financial goal category {category} is {progress_percentage:.2f}%")
            return
          

    def delete_fin_goal(self):
        '''This method uses the delete sql commands 
        to delete a record from the financial goals table'''

        choice = int(input('''Please select an option: 
                       1. View all financial goals before deleting
                       2. Continue without viewing\n'''))

        if choice == 1:
            self.view_fin_goals()
        elif choice == 2:
            pass

        category = input('''Please enter the the goal category you would like to delete
                            ***WARNING*** This will permanently delete this record\n''').lower()
        cursor.execute('''SELECT category FROM financial_goals WHERE LOWER(category) = ?''', (category,))
        existing_category = cursor.fetchone()

        # check if category exist
        if not existing_category:
            print("This financial goal does not exit. Please enter an existing goal")
            return
                
        cursor.execute('''DELETE FROM financial_goals WHERE LOWER(category) = ?''', (category,))

        db.commit()
        print("Financial goal successfully deleted!")
        return

                
while True:
    try:
        
       # create objects to manage classes
       expense_obj = Expense()
       income_obj = Income()
       bud_obj = Budget()
       fin_goal_obj = Financial_Goal()

       fin_menu = int(input('''\n Please an option:
                            1. Add expense
                            2. View expenses
                            3. View expenses by category
                            4. Manage Expenses (Update/Delete)
                            5. Add income
                            6. View incomes
                            7. View income by category
                            8. Manage incomes (update\Delete)
                            9. Set budget for a category
                            10. View budget for a category
                            11. Budget calculation by category
                            12. View all budgets
                            13. Manage budgets (Update\Delete)
                            14. Set financial goals
                            15. View financial goals
                            16. View progress towards financial goal
                            17. Delete financial goal
                            18. Quit
                            '''))
        
       
       if fin_menu == 1:
           expense_obj.add_expense()
       elif fin_menu == 2:
           expense_obj.view_expenses()
       elif fin_menu == 3:
           expense_obj.view_expense_by_category()
       elif fin_menu == 4:
           exp_man = int(input(''' Please select an option: 
                               1. Update an expense
                               2. Delete and expense\n'''))
           if exp_man == 1:
               expense_obj.update_expense()
           if exp_man == 2:
               expense_obj.delete_expense()

       elif fin_menu == 5:
           income_obj.add_income()
       elif fin_menu == 6:
           income_obj.view_incomes()
       elif fin_menu == 7:
           income_obj.view_income_by_category()
       elif fin_menu == 8:
           inc_man = int(input('''Please select an option:
                               1. Update Incomes
                               2. Delete an income\n'''))
           if inc_man == 1:
               income_obj.update_income()
           if inc_man == 2:
               income_obj.delete_income()

       elif fin_menu == 9:
           bud_obj.set_budget()
       elif fin_menu == 10:
           bud_obj.view_budget()
       elif fin_menu == 11:
           bud_obj.calculate_budget()
       elif fin_menu == 12:
           bud_obj.view_all_budgets()
       elif fin_menu == 13:
            bud_menu = int(input('''Please select an option:
                                1. Update budget
                                2. Delete Budget\n'''))
            if bud_menu == 1:
               bud_obj.update_budget_amount()
            if bud_menu == 2:
               bud_obj.delete_budget()
           
       elif fin_menu == 14:
           fin_goal_obj.set_fin_goal()
       elif fin_menu == 15:
           fin_goal_obj.view_fin_goals()
       elif fin_menu == 16:
           fin_goal_obj.progress_towards_fin_goals()
       elif fin_menu == 17:
           fin_goal_obj.delete_fin_goal()

       elif fin_menu == 18:
           print("Thank You for using The Finance App :) Goodbye!")
           break 
       
       else:
        print("Incorrect option selected. Please try again!")
    
    # handle errors when incorrect values are entered
    except ValueError:
        print("Incorrect Value entered! Please start again")
db.close()
print("Database Closed!")        