from database import con_db, init_db, add_expense, add_income
from api_clients import get_dollar_type_card

# Process a new expense and load it
def process_new_expense(expense_name, total_amount, currency, type_currency, total_fees, 
    starting_month, starting_year, interest_rate=0):

        # Calculate interest
        if interest_rate > 0:
            multiplier = 1 + (interest_rate / 100)
            price_interest = total_amount * multiplier
        else:
            price_interest = total_amount
        
        # Handle currency conversion (USD to ARS)
        if currency.upper() == "USD":
            sell_value = get_dollar_type_card()

            if not sell_value:
                print("Error: Could not retrieve the dollar value, the expense will not be save.")
                return False

            final_total_ars = price_interest * sell_value
            print(f"Calculated USD expense: ${price_interest} USD at ${sell_value} ARS = ${final_total_ars:,.2f} ARS")
        else:
            final_total_ars = price_interest

        add_expense(
            expense_name=expense_name,
            total_amount=final_total_ars,
            currency="ARS",
            type_currency=type_currency.upper(),
            total_fees=total_fees,
            starting_month=starting_month,
            starting_year=starting_year
        )

        return True

# Process a new income and load it
def process_new_income(amount, month, year, currency="ARS"):

        # If the income is in dollars then it will pass it to ARS
        if currency.upper() == "USD":
            sell_value = get_dollar_type_card()

            if not sell_value:
                print("Error: Could not retrieve the dollar value, the income will not be saved.")
                return False

            final_total_ars = amount * sell_value
            print(f"Calculated USD income: ${amount} USD at ${sell_value} ARS = ${final_total_ars:,.2f} ARS")
            
        else:
            final_total_ars = amount

        add_income(
            amount=final_total_ars,
            month=month,
            year=year
        )
        
        print(f"Income of ${final_total_ars:,.2f} registered for {month}/{year}.")
        return True


# Get the incomes from a specific month
def get_income_by_month(month, year):
    c = con_db()
    if not c:
        return 0

    try:
        cur = con.cursor()
        cur.execute('''
            SELECT SUM(amount) FROM income WHERE month = ? AND year = ?
        ''', (month, year))
        result = cur.fetchone()
        return result[0] if result else 0

    except sqlite3.Error as e:
        print(f"Error getting income: {e}")
        return 0

    finally:
        if c:
            c.close()

# Get all the expenses
def get_all_expenses():
    c = con_db()
    if not c:
        return []

    try:
        cur = con.cursor()
        cur.execute('''
            SELECT expense_name, total_amount, fee_amount, total_fees, starting_month, starting_year FROM expenses
        ''')
        expenses = cur.fetchall()
        return expenses

    except sqlite3.Error as e:
        print(f"Error getting expenses: {e}")
        return []

    finally:
        if con:
            con.close()

# Generate a monthly report
def generate_monthly_report(target_month, target_year):
    total_income = get_income_by_month(target_month, target_year)
    expenses = get_all_expenses()

    total_fixed_expenses = 0
    total_var_expenses = 0
    active_expenses = []

    # Find the target month
    target_abs_month = (target_year * 12) + target_month

    for expense in expenses:
        expense_name, total_amount, type_currency, total_fees, starting_month, starting_year = expense

        # Finding our edges
        start_abs_mouth = (starting_year * 12) + starting_month
        end_abs_month = (target_year * 12) + target_month

        if start_abs_mouth <= target_abs_month <= end_abs_month:
            actual_quote = (target_abs_month - start_abs_mouth) + 1

            if type_currency == "FIXED":
                total_fixed_expenses += total_amount
            if type_currency == "VARIABLE":
                total_var_expenses += total_amount
            
            active_expenses.append({
                "expense_name": expense_name,
                "total_amount": total_amount,
                "type_currency": type_currency,
                "actual_quote": actual_quote,
                "total_fees": total_fees  
            })
    
    total_expenses = total_fixed_expenses + total_variable_expenses
    money_in_hand = total_income - total_expenses

    # Adding a percentage rate for giving colors to the summary results
    colors_percentage = (money_in_hand / total_income * 100) if total_income > 0 else 0

    return {
        "month": target_month,
        "year": target_year,
        "total_income": total_income,
        "fixed_expenses": total_fixed_expenses,
        "variable_expenses": total_variable_expenses,
        "total_expenses": total_expenses,
        "money_in_hand": money_in_hand,
        "colors_percentage": colors_percentage,
        "expenses_list": active_expenses
    }

# Testing Block
#if __name__ == "__main__":
 #   print("Init DB")
 #   init_db()

#     print("Testing Logic")
#     print("Adding an expense")
#     process_new_expense(
#         expense_name="Fravega",
#         total_amount=100000,
#         currency="ARS",
#         type_currency="FIJO",
#         total_fees=12,
#         starting_month=10,
#         starting_year=2025,
#         interest_rate=15
#     )

#     print("Trying USD currency")
#     process_new_expense(
#         expense_name="Monitor Zowie",
#         total_amount=500,
#         currency="USD",
#         type_currency="VARIABLE",
#         total_fees=1,
#         starting_month=10,
#         starting_year=2025,
#         interest_rate=0
#     )

#   print("\n--- Testing Income Logic ---")
#   process_new_income(
#       amount=498087.06, 
#       month=10, 
#       year=2025, 
#       currency="ARS"
#   )