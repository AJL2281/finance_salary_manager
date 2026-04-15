# Financial or Salary Manager

An interactive CLI APP built in Python to track personal finances.

This tool was designed to keep tract of my own personal expences so I could stop using an Excel that needs to be update it manualy every month. The project was designed to be only use in Argentina 
monetary context. The APP handles quotes with interest rate, automatically converts USD to ARS using real-time exchange rates and projects your financial health with a summary.

## Features

* **Fee Projection:** Automatically distribute and calculate future fees without the database.
* **API Integration:** Fetches the live "Dólar Tarjeta" exchange rate from DolarApi.com to log USD expenses into ARS.
* **Colorful CLI Dashboard:** Utilizes `Rich` library to provide a better looking terminal.
* **Storage:** Safely stores financial records locally using a SQLite database.

## Technologies

* **Python 3** 
* **SQLite3** (DataBase Provided)
* **Requests** (For REST API)
* **Rich** (For the interactive and styled terminal UI)

## Future Ideas

* Modified expenses and incomes that were already added.
* Fee interest that increases as time goes by.
* Add a category system for the expenses.
* Migrate to an ORM.
* Data export (Use CSV to extract SQLite tables and create an Excel file).
* A telegram bot that load the data from your own phone.
* Migrate the project from CLI to a WEB APP (It will require passing from SQLite to a different DB, for example, PostgreSQL).

---

## How to Clone and Run

Instructions to get a copy of the project and run it in your local machine.

### Pre Requirements

You will need [Python 3](https://www.python.org/downloads/) and [Git](https://git-scm.com/) installed on your system.

### Installation Steps

1. **Clone the repository:**
   * Open your terminal and run:
   ```
   git clone [https://github.com/](https://github.com/)AJL2281/finance_salary_manager.git
   ```

2. **Navigate into the project directory:**
   ```
   cd finance_salary_manager
   ```

3. **Create a Virtual Environment:**
   ```
   python3 -m venv venv
   ```

4. **Activate the Virtual Environment:**
   * On Linux/macOS:
     ```
     source venv/bin/activate
     ```

   * On Windows:
     ```
     venv\Scripts\activate
     ```

5. **Install dependencies:**
   Install the third-party libraries with the requirements.txt file:
   ```
   pip install -r requirements.txt
   ```

6. **Run the Application:**
   ```
   python3 main.py
   ```
