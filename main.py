from finance_logic import process_new_expense, process_new_income, get_income_by_month, get_all_expenses, generate_monthly_report
from database import init_db
from rich.console import Console
from rich.panel import Panel

console = Console()

# Main function that will handle all the menu
def main_menu():
    # Start the DB
    init_db()

    while True:
        # Clearing the console at every start
        console.clear()
        
        # Title
        title = Panel("[bold cyan]FINANCIAL OR SALARY MANAGER[/bold cyan]", expand=False)
        console.print(title)

        # Menu options
        console.print("[bold white]1.[/bold white] Add new Expense")
        console.print("[bold white]2.[/bold white] Add new Income")
        console.print("[bold white]3.[/bold white] View Monthly Summary")
        console.print("[bold white]4.[/bold white] Exit")

        choice = console.input("\n[bold yellow]Select an option:[/bold yellow]")

        # Add New Expense
        if choice == '1':
            console.print("\n[blue]-- Adding new Expense --[/blue]")

            expense_name = console.input("\n[white]Please enter the expense name:[/white]")
            total_amount = float(console.input("\n[white]Please enter the total amount:[/white]"))
            currency = console.input("\n[white]Please enter the currency (ARS or USD):[/white]")
            type_currency = console.input("\n[white]Please enter the type of currency (FIXED or VARIABLE):[/white]")
            total_fees = int(console.input("\n[white]Please enter the total number of quotes:[/white]"))
            starting_month = int(console.input("\n[white]Please enter the starting month:[/white]"))
            starting_year = int(console.input("\n[white]Please enter the starting year:[/white]"))

            raw_interest = console.input("\n[white]Please enter the interest rate of the quotes (optional):[/white]")
            interest_rate = float(raw_interest) if raw_interest else 0

            process_new_expense(expense_name, total_amount, currency, type_currency, total_fees, starting_month, starting_year, interest_rate)
            console.print("\n[bold green]Expense added successfully![/bold green]")
            console.input("\nPress Enter to return to the menu...")
            
        # Add New Income   
        elif choice == '2':
            console.print("\n[blue]-- Adding new Income --[/blue]")
            amount = float(console.input("\n[white]Please enter the income amount:[/white]"))
            month = int(console.input("\n[white]Please enter the income month:[/white]"))
            year = int(console.input("\n[white]Please enter the income year:[/white]"))
            currency = console.input("\n[white]Please enter the income currency (ARS or USD):[/white]")

            process_new_income(amount, month, year, currency)
            console.print("\n[bold green]Income added successfully![/bold green]")
            console.input("\nPress Enter to return to the menu...")
        
        # Sumary of the Month
        elif choice == '3':
            console.print("\n[blue]-- Monthly Summary --[/blue]")
            target_month = int(console.input("\n[white]Please enter the target month:[/white]"))
            target_year = int(console.input("\n[white]Please enter the target year:[/white]"))

            summary = generate_monthly_report(target_month, target_year)

            if summary['colors_percentage'] > 50:
                color_percentage = "bold green"
            elif summary['colors_percentage'] >= 20:
                color_percentage = "bold yellow"
            else:
                color_percentage = "bold red"

            # Create Table and columns
            table = Table(title=f"Summary for {target_month}/{target_year}", show_header=True, header_style="bold magenta")
            table.add_column("Category", style="cyan", justify="left")
            table.add_column("Amount", style="white", justify="right")

            # Add rows and their values
            table.add_row("Total Income", f"${summary['total_income']:,.2f}")
            table.add_row("Fixed Expenses", f"${summary['fixed_expenses']:,.2f}")
            table.add_row("Variable Expenses", f"${summary['variable_expenses']:,.2f}")
            table.add_row("Total Expenses", f"${summary['total_expenses']:,.2f}")
            table.add_row("---", "---")
            table.add_row(
                "Money Left", 
                f"[{color_percentage}]${summary['money_in_hand']:,.2f} ({summary['colors_percentage']:,.1f}%)[/{color_percentage}]"
            )

            console.print("\n")
            console.print(table)
            console.input("\nPress Enter to return to the menu...")

        # Exit the APP  
        elif choice == '4':
            console.print("\n[bold green]Exiting Financial Manager. Goodbye![/bold green]")
            break
            
        else:
            console.print("\n[bold red]Invalid option. Please try again.[/bold red]")
            console.input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()