from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import markdown

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for flash messages

# Email Configuration
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASS')

def load_posts():
    """Loads blog posts from the 'posts' directory."""
    posts = []
    posts_dir = 'posts'
    
    if not os.path.exists(posts_dir):
        return []

    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Parse Frontmatter manually to avoid extra dependencies
                if content.startswith('---'):
                    try:
                        _, frontmatter, body = content.split('---', 2)
                        metadata = {}
                        for line in frontmatter.strip().split('\n'):
                            if ':' in line:
                                key, value = line.split(':', 1)
                                metadata[key.strip()] = value.strip()
                        
                        # Convert markdown body to HTML
                        html_content = markdown.markdown(
                            body.strip(),
                            extensions=['fenced_code', 'tables', 'nl2br']
                        )
                        
                        posts.append({
                            'id': filename, # Use filename as ID for simplicity
                            'title': metadata.get('title', 'Untitled'),
                            'date': metadata.get('date', ''),
                            'category': metadata.get('category', 'General'),
                            'summary': metadata.get('summary', ''),
                            'image': metadata.get('image', ''),
                            'content': html_content,
                            'slug': filename.replace('.md', ''),
                            'custom_template': metadata.get('custom_template', ''),
                            'readtime': metadata.get('readtime', '5'),
                        })
                    except ValueError:
                        print(f"Error parsing frontmatter for {filename}")
                        continue

    # Sort posts by date (newest first) - simplistic string sort for now, better to parse dates if strict
    # For now, let's reverse so the file we just added is arguably at top if named right, 
    # but actually better to just rely on the order or add a reliable date sort later if needed.
    return posts

@app.route('/')
def index():
    blogs = load_posts()
    # Limit to 2 for home page if needed, or just show all
    return render_template('index.html', title='Home', blogs=blogs[:2])

@app.route('/about')
def about():
    return render_template('about.html', title="About Me")

@app.route('/service')
def service():
    return render_template('service.html', title="My Services")

@app.route('/portfolio')
def portfolio():
    projects = [
        {
            "title": "Amanat Vision Empowerment Institute",
            "category": "Full-Stack · AI Integration",
            "image": "/static/images/projects/avei.jpg",
            "description": "A full-stack web platform for Pakistan's premier eye care training institute — built with FastAPI, Next.js, Azure, and PostgreSQL. Features Gemini LLM-powered AI assistance, online admissions, CME course management, and a clinical training portal serving Pakistan's oldest eye care institution since 1958.",
            "link": "https://avei.info",
            "stack": ["FastAPI", "Next.js", "Azure", "PostgreSQL", "Gemini LLM"]
        },
        {
            "title": "Video Downloader Web App",
            "category": "Full-Stack Development",
            "image": "/static/images/projects/video_downloader.jpg",
            "description": "A high-performance web application for downloading videos from various platforms. Built with Next.js, Python/Flask backend, and FFmpeg for media processing."
        },
        {
            "title": "Real-time Video Chat",
            "category": "WebRTC & Socket.io",
            "image": "/static/images/projects/video_chat.jpg",
            "description": "A seamless video chat platform facilitating peer-to-peer communication. Leverages WebRTC for low-latency streaming and Socket.io for signaling."
        },
        {
            "title": "AI Content Generator",
            "category": "Generative AI",
            "image": "/static/images/projects/ai_content.jpg",
            "description": "An intelligent tool that generates marketing copy and blog posts using GPT-4 integration. Features a clean React interface and optimized prompt engineering."
        },
         {
            "title": "E-commerce Dashboard",
            "category": "Data Visualization",
            "image": "/static/images/projects/dashboard.jpg",
            "description": "Comprehensive admin dashboard for an e-commerce platform. Visualizes sales data, inventory levels, and user metrics using D3.js and React."
        },
         {
            "title": "Smart Home Automation",
            "category": "IoT & Mobile",
            "image": "/static/images/projects/smart_home.jpg",
            "description": "Mobile app for controlling smart home devices. Integrated with MQTT protocols and provides real-time status updates and automation scheduling."
        },
         {
            "title": "Fitness Tracking App",
            "category": "Mobile App Dev",
            "image": "/static/images/projects/fitness_app.jpg",
            "description": "Cross-platform mobile application for tracking workouts and nutrition. Features personalized plans, progress graphing, and social sharing capabilities."
        }
    ]
    return render_template('portfolio.html', title='Portfolio', projects=projects)

@app.route('/certificates')
def certificates():
    return render_template('certificates.html', title="Certificates")

@app.route('/blog')
def blog():
    blogs = load_posts()
    return render_template('blog.html', title='Blog', blogs=blogs)

@app.route('/blog/<slug>')
def post_detail(slug):
    blogs = load_posts()
    post = next((p for p in blogs if p['slug'] == slug), None)
    if post:
        template = post.get('custom_template') or 'post_detail.html'
        return render_template(template, title=post['title'], post=post)
    return "Post not found", 404

@app.route('/resume')
def resume():
    try:
        return send_from_directory('static', 'cv_sheheryar_ahmad (2).pdf', as_attachment=False)
    except FileNotFoundError:
        return "Resume not found", 404

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    
    if not email:
        flash('Please enter a valid email address.', 'error')
        return redirect(url_for('index'))

    if not EMAIL_USER or not EMAIL_PASS:
        print("Email credentials not set.")
        flash('Email service is not configured.', 'error')
        return redirect(url_for('index'))

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = email
        msg['Subject'] = "Thank you for contacting Sheheryar!"

        body = f"""
        Hi there,

        Thank you for reaching out! I have received your email ({email}) and will get back to you shortly.

        Best regards,
        Sheheryar Ahmad
        AI & Full Stack Specialist
        """
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        flash('Thank you! An automated response has been sent to your email.', 'success')
    except Exception as e:
        print(f"Error sending email: {e}")
        flash('Something went wrong. Please try again later.', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
