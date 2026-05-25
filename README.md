# Fusion Starter

A modern, responsive portfolio and blog template built with Flask, Tailwind CSS, and Python.

## Features

-   **Responsive Design**: Fully responsive layout using Tailwind CSS.
-   **Dynamic Blog System**: Write blogs in Markdown (`.md`) and they appear automatically.
-   **Contact Form**: Functional email contact form using `smtplib`.
-   **UI Animations**: Smooth transitions, fade-ins, and interactive elements.
-   **Reading Progress Bar**: Visual indicator for long-form content.

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd fusion-starter-a0f
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Create a `.env` file in the root directory:
    ```
    EMAIL_USER=your-email@gmail.com
    EMAIL_PASS=your-app-password
    ```

5.  **Run the application**:
    ```bash
    python3 app.py
    ```
    Visit `http://127.0.0.1:5000` in your browser.

## How to Add a New Blog Post

Adding a new blog post is simple:

1.  Create a new Markdown file in the `posts/` directory (e.g., `posts/my-new-blog.md`).
2.  Add the following **Frontmatter** at the top of the file:

    ```markdown
    ---
    title: My New Blog Post Title
    date: Feb 14, 2026
    category: Web Development
    summary: A short summary of the post that appears on the card.
    image: /static/images/blogs/my-image.jpg
    ---
    ```

3.  Write your content below the frontmatter using standard Markdown.
4.  Save the file. The new post will automatically appear on the home page and `/blog` page. The URL will be `/blog/my-new-blog` (based on the filename).

## Project Structure

-   `app.py`: Main Flask application.
-   `posts/`: Directory for Markdown blog posts.
-   `static/`: CSS, images, and other static assets.
-   `templates/`: HTML templates (Jinja2).
-   `requirements.txt`: Python dependencies.
