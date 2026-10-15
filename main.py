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
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def save_data(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def add_expense(data, args):

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
    for expense in data:
        if expense['expense_id'] == find_id:
            expense['description'] = args.description
    print(f'Description updated: {args.description}')

def update_amount(data, args, find_id):
    for expense in data:
        if expense['expense_id'] == find_id:
            expense['amount'] = args.amount
    print(f'Amount updated: {args.amount}')

def delete_expense(data, find_id):
    for expense in data:
        if find_id == expense['expense_id']:
            data.remove(expense)

    print('Expense deleted.')

def list_expenses(data):
    for expense in data:
        print(f'\nID:          {expense['expense_id']}')
        print(f'DATE:        {expense['date']}')
        print(f'DESCRIPTION: {expense['description']}')
        print(f'AMOUNT:      ${expense['amount']}')
        print(f'----------------------------------')

def expense_summary(data):
    total = 0

    for expense in data:
        total += expense['amount']
    
    print(f'\nTotal expenses: ${total}')

def expense_summary_by_date(data, args):
    total = 0

    for expense in data:
        total += expense['amount']
        expense_date = dt.date.strptime(expense['date'], date_format)
    
    if expense_date.month == args.month:
        print(f'\nTotal expenses for {expense_date.strftime('%B').title()}: ${total}')

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