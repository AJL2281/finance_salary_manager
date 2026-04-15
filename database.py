import sqlite3

DB_NAME = "finance.db"

# Create the connection to the DB and attempt to establish it
def con_db():
    con = None
    try:
        con = sqlite3.connect(DB_NAME)
        print("Connection successful")
        return con

    except sqlite3.Error as e:
        # Catch any error that could occur
        print(f"Error connecting to database: {e}")
        return None

# Init and create the db tables if they don't exist
def init_db():
    con = con_db()

    if not con:
        return
    try:
        cur = con.cursor()

        # Create table Income / This table will handle the salary befero any changes
        cur.execute('''
            CREATE TABLE IF NOT EXISTS income(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL
            )
        ''')

        # Create table expenses / All changes to the salary will be handled by this table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_name TEXT NOT NULL,
                total_amount REAL NOT NULL,
                fee_amount REAL NOT NULL,
                currency TEXT NOT NULL,
                type_currency TEXT NOT NULL,
                total_fees INTEGER NOT NULL,
                starting_month INTEGER NOT NULL,
                starting_year INTEGER NOT NULL
            )
        ''')

        # Commit to the DB
        con.commit()
        print("Tables created successfully")

    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
    
    finally:
        if con:
            con.close()
            print("Connection closed")

# Insert a new expense into the DB
def add_expense(expense_name, total_amount, currency, type_currency, total_fees, starting_month, starting_year):
    # Calculate the value of the first fee in the current month
    fee_amount = total_amount / total_fees

    con = con_db()
    if not con:
        return

    try:
        cur = con.cursor()

        # SQL querie into expenses with the require data
        cur.execute('''
            INSERT INTO expenses (expense_name, total_amount, fee_amount, currency, type_currency, total_fees, starting_month, starting_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (expense_name, total_amount, fee_amount, currency, type_currency, total_fees, starting_month, starting_year))

        # Commit the values into expenses table
        con.commit()
        print(f"The expense {expense_name} has been added successfully")

    except sqlite3.Error as e:
        print(f"Error inserting data into expenses table: {e}")

    finally:
        if con:
            con.close()
            print("Connection closed")

# Insert salary or any income of the mounth and year
def add_income(amount, month, year):
    con = con_db()
    if not con:
        return

    try:    
        cur = con.cursor()

        # SQL querie into income with the require data
        cur.execute('''
            INSERT INTO income (amount, month, year)
            VALUES (?, ?, ?)
        ''', (amount, month, year))

        # Commit the values into income table
        con.commit()
        print(f"The total amount of the income was ${amount}, {month} of the {year} and it has been added successfully")

    except sqlite3.Error as e:
        print(f"Error inserting data into income table: {e}")

    finally:
        if con:
            con.close()
            print("Connection closed")

# Test Block
# if __name__ == "__main__":
    # init_db()

    # Test: adding some values to expenses table
    # add_expense("Fravega", 108922.68, "ARS", "FIJO", 12, 10, 2025)
    # add_expense("ISIV Facultad", 95000, "ARS", "FIJO", 1, 10, 2025)

    # Test: adding some values to income table
    # add_income(600000, 10, 2025)