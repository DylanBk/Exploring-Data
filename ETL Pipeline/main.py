import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

f = 'data.csv'
db = 'db.db'


def basic_info():
    data = pd.read_csv(f)
    cols = str(data.columns).replace('Index', '').replace('(', '').replace(')', '').replace('[', '').replace('],', '').replace('dtype=\'object\'', '').replace('\'', '')

    print(f"\nColumns: \n{cols}")

def detailed_info():
    data = pd.read_csv(f)

    info = data.info()

    print(f"\nColumns and data types: \n{info}")

def sales_stats(stat):
    data = pd.read_csv(f)
    df = pd.DataFrame(data)

    if stat == "Monthly" or stat == "Quarterly":
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index("Date", inplace=True)

        if stat == "Monthly":
            sales = df['Transaction Amount'].resample('M').sum().reset_index() # gets monthly transactions
        else:
            sales = df['Transaction Amount'].resample('QE').sum().reset_index() # gets quarterly transactions

        plt.plot(sales['Date'], sales['Transaction Amount'], marker="o")
        plt.xlabel("Annum")
        plt.ylabel("Sales")
        plt.xticks(rotation=30)
        plt.title(f"{stat} Sales")

        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"£ {x/1e6:.1f}M")) # stops graph from using scientific notation e.g. 1e2

        plt.show()

        return

    sales = df.groupby(stat)['Transaction Amount'].sum().reset_index()

    plt.bar(sales[stat], sales['Transaction Amount'])
    plt.xlabel(stat)
    plt.ylabel("Sales")
    plt.xticks(rotation=30)
    plt.title(f"Sales per {stat}")

    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"£ {x/1e6:.1f}M")) # stops graph from using scientific notation e.g. 1e2

    plt.show()

    return

def statistics():
    while True:
        choice = input("""
1. Monthly Sales
2. Quarterly Sales
3. Sales per category
4. Sales per gender
5. Return
> """)

        match choice:
            case "1":
                sales_stats('Monthly')
            case "2":
                sales_stats('Quarterly')
            case "3":
                sales_stats('Category')
            case "4":
                sales_stats('Gender')
            case "5":
                break
            case default:
                print("\nInvalid input, please try again\n")

def process():
    # Extract

    print("Extracting data..")
    data = pd.read_csv(f)
    df = pd.DataFrame(data)

    # Transform

    print("\nRemoving duplicates..")
    df.drop_duplicates(inplace=True)

    print("Resolving null values..")
    df.fillna(0)

    print("Converting types..")
    pd.to_datetime(df['Birthdate'])
    pd.to_datetime(df['Date'])

    # Load

    print("\nConnecting to database..")
    conn = sqlite3.connect(db)

    print("Inserting data..")
    df.to_sql("CustomerTransactions", conn, if_exists='replace', index=False)

    print("\nProcess complete")

def menu():
    while True:
        choice = input("""
\n
1. View basic info about CSV
2. View detailed info about CSV
3. View statistics
4. Move data to database
5. Exit
> """)

        match choice:
            case "1":
                basic_info()
            case "2":
                detailed_info()
            case "3":
                statistics()
            case "4":
                process()
            case "5":
                exit()
            case default:
                print("\nInvalid input, please try again\n")

menu()