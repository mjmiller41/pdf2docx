#!/bin/bash
# Initialize Git repository and push to remote

# Initialize repository
git init

# Add files
git add .

# Make initial commit
git commit -m "Initial commit: Modern PDF to DOCX converter with PyMuPDF"

# Add remote repository (replace with your actual URL)
echo "Please enter your Git remote repository URL:"
read remote_url
git remote add origin $remote_url

# Push to main branch
git push -u origin main

echo "✅ Project pushed to $remote_url"
