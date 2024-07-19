import pandas as pd
import csv
from datetime import datetime
from data_entry import *
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date', 'amount', 'category', 'description']
    date_format = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns= csv.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date" : date,
            "amount" : amount,
            "category" : category,
            'description' : description
        }
        with open(cls.CSV_FILE, 'a', newline = "") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entery added successfully")
    
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'], format=CSV.date_format)
        start_date = datetime.strptime(start_date, CSV.date_format)
        end_date = datetime.strptime(end_date, CSV.date_format)

        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in giving date range")
        else:
            print(
                f"Transactions found in given date range: {start_date.strftime(CSV.date_format)} to {end_date.strftime(CSV.date_format)}"
            )
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.date_format)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\n Summary:")
            print(f"Total Income : ${total_income:.2f}")
            print(f"Total Expense : ${total_expense:.2f}")
            print(f"Net Saving: ${(total_income - total_expense):.2f}")

            return filtered_df


def add_data():
    CSV.initialize_csv()
    date = get_date("Enter the date of transaction or enter for today's date: ", allow_default= True)
    amount =get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transaction(df):
    df.set_index('date', inplace = True)

    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income vs Expense")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("Welcome to your Daily Finance Tracker")
        print("1. Add new transaction")
        print("2. View transactions within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            add_data()
        elif choice == '2':
            start_date = get_date("Enter the start date of the range (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date of the range (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to view this date in a graph? (y/n) ").lower() == "y":
                plot_transaction(df)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid Choice. Enter 1 or 2 or 3")

if __name__ == "__main__":
    main()