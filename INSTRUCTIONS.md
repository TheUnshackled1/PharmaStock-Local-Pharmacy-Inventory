# 🛠️ Windows Setup Instructions

Follow these step-by-step instructions to get **PharmaStock** up and running on a Windows environment.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:
1. **[Python 3.8+](https://www.python.org/downloads/)**
   - *Important:* Make sure to check the box **"Add Python to PATH"** during installation.
2. **[Git](https://git-scm.com/download/win)** (Optional, if you are cloning the repo).

---

## Step 1: Open the Terminal

1. Press `Win + R`, type `cmd` or `powershell`, and hit **Enter**.
2. Navigate to the folder where you want to store the project:
   ```powershell
   cd Documents
   ```

## Step 2: Clone or Extract the Project

If you are using Git:
```powershell
git clone <repository-url>
cd stock
```
*(If you downloaded a ZIP file instead, simply extract it and navigate into the `stock` folder via your terminal.)*

## Step 3: Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.
```powershell
python -m venv env
```
This command creates a folder named `env` inside your project directory.

## Step 4: Activate the Virtual Environment

Activate the environment to ensure packages are installed locally rather than globally.
```powershell
env\Scripts\activate
```
*(You should now see `(env)` at the beginning of your terminal prompt line.)*

## Step 5: Install Dependencies

Install Django, Pandas, Pillow, and all other required packages:
```powershell
pip install -r requirements.txt
```

## Step 6: Apply Database Migrations

Set up the SQLite database by running Django migrations:
```powershell
python manage.py makemigrations
python manage.py migrate
```

## Step 7: Create a Superuser (Admin)

You need an admin account to access the staff dashboard and manage inventory.
```powershell
python manage.py createsuperuser
```
*(Follow the prompts to enter a username, email, and password. Note that the password will not show as you type it.)*

## Step 8: Run the Development Server

Start the local server:
```powershell
python manage.py runserver
```

## Step 9: Access the Application

1. Open your web browser (Chrome, Edge, Firefox, etc.).
2. Go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
3. To access the admin panel, go to: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with the superuser credentials you created.

---

### Troubleshooting

- **`python is not recognized as an internal or external command`**: Python is not added to your system PATH. Reinstall Python and check the "Add to PATH" box.
- **Execution Policy Error when activating env**: If PowerShell throws an error when running `activate`, run this command as an Administrator: `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`, then try activating again.
