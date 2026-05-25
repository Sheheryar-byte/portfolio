# Deploying to PythonAnywhere

Follow these steps to deploy your Flask application to [PythonAnywhere](https://www.pythonanywhere.com/).

## 1. Create a PythonAnywhere Account
- Sign up for a free or paid account at [pythonanywhere.com](https://www.pythonanywhere.com/pricing/).

## 2. Upload Your Code
- **Method A (GitHub - Recommended)**:
    1.  Open the **Bash Console** on PythonAnywhere.
    2.  Clone your repository:
        ```bash
        git clone https://github.com/yourusername/your-repo-name.git
        ```
- **Method B (Manual Upload)**:
    1.  Go to the **Files** tab.
    2.  Upload your project files or a `.zip` file and extract it.

## 3. Set Up a Virtual Environment
- In the Bash Console, navigate to your project folder and create a virtual environment:
    ```bash
    cd your-repo-name
    mkvirtualenv --python=/usr/bin/python3.10 my-venv  # Or your preferred version
    pip install -r requirements.txt
    ```

## 4. Configure Web App
1.  Go to the **Web** tab on the PythonAnywhere dashboard.
2.  Click **Add a new web app**.
3.  Select **Manual Configuration** (since we are using a custom folder/venv).
4.  Select your Python version (e.g., Python 3.10).
5.  After the setup, look for **Virtualenv** section and enter the path: `/home/yourusername/.virtualenvs/my-venv`.
6.  Look for **Code** section and set:
    - **Source code**: `/home/yourusername/your-repo-name`
    - **Working directory**: `/home/yourusername/your-repo-name`

## 5. Configure WSGI File
1.  In the **Web** tab, click the link to the **WSGI configuration file** (under Code section).
2.  Delete everything and replace it with:
    ```python
    import sys
    import os
    from dotenv import load_dotenv

    # Project path
    path = '/home/yourusername/your-repo-name'
    if path not in sys.path:
        sys.path.append(path)

    os.chdir(path)
    
    # Load environment variables
    load_dotenv(os.path.join(path, '.env'))

    from app import app as application
    ```
    *Replace `yourusername` and `your-repo-name` with your actual values.*

## 6. Set Environment Variables
1.  Go to the **Files** tab and create a file named `.env` in your project root.
2.  Add your email credentials:
    ```
    EMAIL_USER=your-email@gmail.com
    EMAIL_PASS=your-app-password
    ```

## 7. Reload and Visit
1.  Go back to the **Web** tab.
2.  Click the big green **Reload** button.
3.  Visit your URL: `yourusername.pythonanywhere.com`.

---

### Troubleshooting
- **Static Files**: If images are missing, configure **Static Files** in the Web tab:
    - URL: `/static/`
    - Path: `/home/yourusername/your-repo-name/static`
- **Error Logs**: If the site doesn't load, check the **Error Log** at the bottom of the Web tab.
