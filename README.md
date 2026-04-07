#  SkillSphere

##  Overview
SkillSphere is a web-based job recruitment platform that connects candidates with relevant job opportunities. It provides personalized job recommendations based on user skills using a custom-built skill matching algorithm, while also enabling recruiters to post and manage job listings.

---

##  Features
-  Secure user authentication (Login & Registration)
-  Candidate profile with skill management
-  Skill-based job recommendation system
-  Job browsing and application system
-  Recruiter dashboard for posting and managing jobs
-  Custom algorithm for matching candidate skills with job requirements

---

##  Tech Stack
- **Frontend:** HTML, CSS, Bootstrap  
- **Backend:** Django  
- **Database:** SQLite / MySQL  

---

##  How It Works
1. Candidates create an account and add their skills  
2. Recruiters post jobs with required skills  
3. The system compares candidate skills with job requirements  
4. Relevant jobs are recommended based on matching scores  

---

##  Project Structure

SkillSphere/
│
├── jobs/ # Main app (views, models, urls)
├── templates/ # HTML templates
├── static/ # CSS, JS, assets
├── manage.py # Django entry point
├── db.sqlite3 # Database (ignored in production)


---

##  Setup Instructions

### 1. Clone the repository

git clone https://github.com/yourusername/skillsphere.git

cd skillsphere


### 2. Create virtual environment (optional but recommended)

python -m venv venv
venv\Scripts\activate # Windows


### 3. Install dependencies

pip install -r requirements.txt


### 4. Run migrations

python manage.py migrate


### 5. Start the server

python manage.py runserver


### 6. Open in browser

http://127.0.0.1:8000/


---

##  Future Enhancements
-  Email notifications for job matches  
-  Resume upload & parsing  
-  Advanced recommendation system  
-  Improved UI/UX  

---


##  Author
**Govind Benzkumar**
