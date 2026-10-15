from argparse import ArgumentParser
from pathlib import Path
import datetime as dt
import json


date_format = '%m/%d/%y'
expenses = []
path = Path('expenses.json')
if not path.exists():
    with open(path, 'w') as file:
        json.dump(expenses, file)

def load_data(path):
    '''
        Open to the path parameter and load the data assigned to its value
    '''
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def save_data(path, data):
    '''
        Open to the path parameter and save the data assigned to the data argument
    '''
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def add_expense(data, args):
    '''
        First, we create a 'highest' variable to find track the highest value of 
        the new_expense 'expense_id' value, then we get todays date and create a
        dictionary to hold the information for our expenses. After that, we
        add the dictionary to a list stored in the data parameter and print
        that an expense has been added along with its corresponding ID.
    '''
    # Add a unique ID to each newly created task.
    highest = 0
    for expense in data:
        if expense['expense_id'] > highest:
            highest = expense['expense_id']
    new_id = highest + 1

    tday = dt.date.today().strftime(date_format)
    new_expense = {'expense_id': new_id,
                    'description': args.description,
                    'amount': args.amount,
                    'date': tday
                    }

    data.append(new_expense)
    
    print(f'Expense added successfully (ID: {new_id})')

def update_description(data, args, find_id):
    '''
        We use a for loop to find the dictionary corresponding to an expense
        by it's ID using the 'find_id' parameter (assigned to an argument that 
        returns an integer). We then set the description of the expense dictionary 
        to an argument that returns a string value. After that, we print the 
        updated description.
    '''
    for expense in data:
        if expense['expense_id'] == find_id:
            expense['description'] = args.description
    print(f'Description updated: {args.description}')

def update_amount(data, args, find_id):
    '''
        We use a for loop to find the dictionary corresponding to an expense
        by it's ID using the 'find_id' parameter (assigned to an argument that 
        returns an integer). We then set the amount of the expense dictionary 
        to an argument that returns an integer value. After that, we print the 
        updated amount.
    '''
    for expense in data:
        if expense['expense_id'] == find_id:
            expense['amount'] = args.amount
    print(f'Amount updated: {args.amount}')

def delete_expense(data, find_id):
    '''
        We use a for loop to find the dictionary corresponding to an expense
        by it's ID using the 'find_id' parameter (assigned to an argument that 
        returns an integer). We then remove the expense dictionary if 'find_id'
        equals to an ID in our list.
    '''
    for expense in data:
        if find_id == expense['expense_id']:
            data.remove(expense)
            print('Expense deleted.')
        else:
            print('This ID does not exist.')

def list_expenses(data):
    '''
        We use a for loop to find the values in our expense dictionary and
        print each value according.
    '''
    for expense in data:
        print(f'\nID:          {expense['expense_id']}')
        print(f'DATE:        {expense['date']}')
        print(f'DESCRIPTION: {expense['description']}')
        print(f'AMOUNT:      ${expense['amount']}')
        print(f'----------------------------------')

def expense_summary(data):
    '''
        We use a for loop to find our expense dictionaries, we then
        add up all of the expense amounts and assign the total to a
        variable called 'total', we then print that variable.
    '''
    total = 0

    for expense in data:
        total += expense['amount']
    
    print(f'\nTotal expenses: ${total}')

def expense_summary_by_date(data, args):
    '''
        We use a for loop to find our expense dictionaries, we then
        add up all of the expense amounts and assign the total to a
        variable called 'total', we also use a varible called 'expense_date'
        to get the date of our expense and convert it from a string back to
        a piece of data that can be used by the 'datetime.date' class.
        we then find if the value is an integer representing a specific month,
        and if it is we convert our 'expense_date' back into a strin, format
        it accordingly, and print the total expenses for that entire month.
    '''
    total = 0

    for expense in data:
        total += expense['amount']
        expense_date = dt.date.strptime(expense['date'], date_format)
    
    if expense_date.month == args.month:
        print(f'\nTotal expenses for {expense_date.strftime('%B').title()}: ${total}')
    else:
        print(f'No expenses for this month.')

def main():
    parser = ArgumentParser()
    parser.add_argument('--add', action='store_true')
    parser.add_argument('--description', type=str)
    parser.add_argument('--amount', type=int)
    parser.add_argument('--update', type=int, metavar='ID')
    parser.add_argument('--delete', type=int)
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--summary', action='store_true')
    parser.add_argument('--month', type=int)

    args = parser.parse_args()

    # Add an expense
    if args.add and args.description and args.amount:
        data = load_data(path)
        add_expense(data, args)
        save_data(path, data)

    elif args.add and args.description:
        print("Invalid parameters, Please plug the argument --amount")
    elif args.add and args.amount:
        print("Invalid parameters, Please plug the argument --description")
    elif args.add:
        print("Invalid parameters, Please plug the arguments --amount and --description")

    # Update an expense
    if args.update and args.description and args.amount:
        data = load_data(path)
        update_description(data, args, args.update)
        update_amount(data, args, args.update)
        save_data(path, data) 

    elif args.update and args.description:
        data = load_data(path)
        update_description(data, args, args.update)
        save_data(path, data)

    elif args.update and args.amount:
        data = load_data(path)
        update_amount(data, args, args.update)
        save_data(path, data)

    elif args.update:
        print("Invalid parameters, Please plug the arguments --amount and --description")

    # Delete an expense
    if args.delete:
        data = load_data(path)
        delete_expense(data, args.delete)
        save_data(path, data)        

    # List expenses
    if args.list:
        data = load_data(path)
        list_expenses(data)
        save_data(path, data)        

    if args.summary and not args.month:
        data = load_data(path)
        expense_summary(data)
        save_data(path, data)  
    elif args.summary and args.month:
        data = load_data(path)
        expense_summary_by_date(data, args)
        save_data(path, data)  
if __name__ == '__main__':
    main()