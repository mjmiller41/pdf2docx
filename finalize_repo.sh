#!/bin/bash
# Final script to commit and push the project

# Initialize Git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Modern PDF to DOCX converter with PyMuPDF

- Fixed text extraction and word scrambling issues
- Implemented modular architecture
- Added comprehensive test suite
- Created documentation and summary files"

# Add remote repository
echo "Please enter your Git remote repository URL:"
read remote_url
git remote add origin $remote_url

# Push to main branch
git push -u origin main

echo "✅ Project pushed to $remote_url"
echo "🚀 Project URL: $remote_url"
