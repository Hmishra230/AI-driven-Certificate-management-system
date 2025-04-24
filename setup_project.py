import os
import subprocess

# Define the project structure
project_structure = {
    "templates": [
        "base.html",
        "navbar.html",
        "index.html",
        "signup.html",
        "login.html",
        "user_dashboard.html",
        "admin_dashboard.html",
        "generate_certificate.html",
        "certificate_preview.html",
        "user_certificates.html"
    ],
    "static": ["styles.css"],
    "files": ["app.py", "requirements.txt"]
}

# Define content for each file
file_contents = {
    "app.py": '''<Place the complete app.py content here>''',
    "requirements.txt": "Flask==2.3.2\nFlask-SQLAlchemy==3.0.5\nFlask-Login==0.6.3\nWerkzeug==2.3.6\ntransformers==4.33.2\ntorch==2.0.1\nJinja2==3.1.2\n",
    "templates": {
        "base.html": '''<Base HTML content>''',
        "navbar.html": '''<Navbar HTML content>''',
        "index.html": '''<Index HTML content>''',
        "signup.html": '''<Signup HTML content>''',
        "login.html": '''<Login HTML content>''',
        "user_dashboard.html": '''<User Dashboard HTML content>''',
        "admin_dashboard.html": '''<Admin Dashboard HTML content>''',
        "generate_certificate.html": '''<Generate Certificate HTML content>''',
        "certificate_preview.html": '''<Certificate Preview HTML content>''',
        "user_certificates.html": '''<User Certificates HTML content>'''
    },
    "static": {
        "styles.css": '''/* Add basic styles here */'''
    }
}

# Create the directory structure and ensure folders exist
def create_project_structure(base_path, structure):
    for folder, content in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        # Create files in the folder
        if isinstance(content, list):
            for item in content:
                open(os.path.join(folder_path, item), 'w').close()  # Create empty files

# Write content to the files
def write_file_content(base_path, contents):
    for file_path, content in contents.items():
        full_path = os.path.join(base_path, file_path)
        with open(full_path, "w") as file:
            file.write(content)

# Install dependencies using pip
def install_dependencies(requirements_file):
    try:
        subprocess.run(["pip", "install", "-r", requirements_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")

def main():
    base_path = os.getcwd()  # Use current working directory as base
    create_project_structure(base_path, project_structure)
    
    # Write specific file content
    write_file_content(base_path, {
        "app.py": file_contents["app.py"],
        "requirements.txt": file_contents["requirements.txt"]
    })

    # Write template content
    templates_path = os.path.join(base_path, "templates")
    for template, content in file_contents["templates"].items():
        with open(os.path.join(templates_path, template), "w") as template_file:
            template_file.write(content)
    
    # Write static content
    static_path = os.path.join(base_path, "static")
    for static_file, content in file_contents["static"].items():
        with open(os.path.join(static_path, static_file), "w") as static_file:
            static_file.write(content)

    # Install dependencies
    install_dependencies(os.path.join(base_path, "requirements.txt"))

if __name__ == "__main__":
    main()
