
# Mergington High School Activities Website

Welcome to the Mergington High School Activities website repository! This is a simple web application that allows students to view and sign up for extracurricular activities.

## 🏫 About Mergington High School

- **School:** Mergington High School (public high school)
- **Location:** Mergington, Florida  
- **Grades:** 9-12 (approximately 100-150 students per grade)
- **School year:** August to May, 3 trimesters + optional summer cycle
- **School motto:** "Branch out and grow"

## 📋 For Teachers: Requesting Changes

**Non-technical staff can easily request changes using our issue templates!**

### How to Request Changes
1. Go to the [Issues page](https://github.com/eallenOP/skills-expand-your-team-with-copilot/issues)
2. Click "New Issue" 
3. Choose the appropriate template
4. Fill out the form with your request

### Available Templates
- **🐛 Bug Report** - Report broken features or errors
- **🏃 Add or Modify Activity** - Add new activities or change existing ones
- **💡 Feature Request** - Request new website functionality  
- **🎨 Website Design & Usability** - Improve website appearance and ease of use
- **📊 Student Data & Grades** - Features involving student information (requires special privacy protections)
- **🔒 Security & Privacy Concern** - Report security issues or privacy concerns

### Need Help?
- **Detailed guide:** [Teacher's Guide to Issue Templates](.github/ISSUE_TEMPLATE/README.md)
- **Technical support:** Contact it@mergington.edu
- **General questions:** Use GitHub Discussions

## 🚀 For Developers

The website is built with:
- **Backend:** FastAPI (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MongoDB with in-memory fallback for development

### Quick Start
```bash
cd src
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Visit `http://localhost:8000` to see the website and `http://localhost:8000/docs` for API documentation.

For detailed development instructions, see the [Development Guide](docs/how-to-develop.md).

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

