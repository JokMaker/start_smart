# StartSmart 🚀

**Empowering African Youth Through Job Creation & Entrepreneurship**

A comprehensive web platform connecting students with job opportunities, startup ventures, and mentorship programs across Africa.

## ✨ Features

### 🎯 Core Functionality
- **Multi-User System**: Students, Mentors, and Recruiters with role-based access
- **Job Board**: Browse, search, and apply for opportunities with advanced filtering
- **Startup Hub**: Showcase ventures and connect with co-founders
- **Mentorship Network**: Connect students with industry professionals
- **Resource Center**: Access educational materials and career guidance

### 🔐 Security & Authentication
- Secure user registration and login system
- Password hashing with Werkzeug security
- Session-based authentication
- Input validation and sanitization

### 📱 User Experience
- Responsive design for mobile and desktop
- Intuitive dashboard for each user type
- Real-time search and filtering
- Clean, modern interface with Bootstrap

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Flask (Python) |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **Database** | SQLite |
| **Security** | Werkzeug password hashing |
| **Styling** | Custom CSS + Bootstrap |

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/JokMaker/start_smart.git
cd start_smart
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database (First Time Only)
```bash
python -c "from app import init_db; init_db()"
```

### 4. Run Application
```bash
python app.py
```

### 5. Access Platform
Open your browser and navigate to:
```
http://localhost:5000
```

## 🌐 Live Demo

**Public URL:** [Add your deployed URL here]

## 📋 Documentation

**SRS Document:** [https://docs.google.com/document/d/1Vlsymv0g8lc0wPMPNhg_SzNuSNfJymLiKWNp06GSoX0/edit?tab=t.0]

## 👥 User Types & Capabilities

### 🎓 Students
- Browse and search job opportunities
- Apply for positions with one-click
- Join startup ventures
- Access mentorship programs
- View educational resources

### 👨‍🏫 Mentors
- Provide guidance to students
- Share industry expertise
- Manage mentorship requests
- Upload educational resources

### 🏢 Recruiters
- Post job opportunities
- Manage job listings
- Review applications
- Access candidate profiles

## 📁 Project Structure

```
start_smart/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── startsmart.db         # SQLite database (auto-created)
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/               # JavaScript files
│   │   ├── animations.js
│   │   ├── job-posting.js
│   │   └── search.js
│   └── uploads/          # File uploads
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── jobs.html         # Job board
│   ├── startups.html     # Startup hub
│   ├── dashboard.html    # User dashboard
│   └── ...              # Other pages
└── README.md            # This file
```

## 🗄️ Database Schema

### Users Table
- User authentication and profile information
- Role-based access control (student/mentor/recruiter)

### Jobs Table
- Job postings with detailed information
- Search and filtering capabilities

### Startups Table
- Startup venture listings
- Founder and team information

### Applications Table
- Job application tracking
- Application status management

### Mentorship Table
- Mentor-mentee connections
- Session management

## 🔧 Configuration

### Environment Setup
The application uses default configurations suitable for development. For production:

1. Change the secret key in `app.py`:
```python
app.secret_key = 'enter your secret key in the file concern with api'
```

2. Configure database settings for production use

### File Upload Settings
- Maximum file size: 16MB
- Upload directory: `static/uploads/`

## 🚀 Deployment

### Deploy to Heroku
1. Install Heroku CLI
2. Create `Procfile`:
```
web: python app.py
```
3. Create `runtime.txt`:
```
python-3.11.0
```
4. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Deploy to Railway
1. Connect GitHub repository to Railway
2. Set environment variables if needed
3. Deploy automatically

## 🔍 Troubleshooting

### Common Issues
1. **Database not found**: Run the database initialization command
2. **Port already in use**: Change port in `app.py` or kill existing process
3. **Module not found**: Ensure all dependencies are installed with `pip install -r requirements.txt`

### Database Reset
If you need to reset the database:
```bash
del startsmart.db
python -c "from app import init_db; init_db()"
```

## 🚦 Getting Started Guide

### For Students
1. Register with student account
2. Complete your profile
3. Browse available jobs and startups
4. Apply for opportunities
5. Connect with mentors

### For Recruiters
1. Register with recruiter account
2. Access the job posting interface
3. Create detailed job listings
4. Review and manage applications

### For Mentors
1. Register with mentor account
2. Set up your expertise areas
3. Respond to mentorship requests
4. Share resources and guidance

## 🎨 Customization

### Styling
- Modify `static/css/style.css` for custom styling
- Bootstrap classes available throughout templates

### Features
- Add new routes in `app.py`
- Create corresponding templates in `templates/`
- Update database schema as needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team

## 🌟 Acknowledgments

Built with the vision of empowering African youth through technology and entrepreneurship.

---

**StartSmart** - *Where Careers Begin and Dreams Take Flight* ✈️