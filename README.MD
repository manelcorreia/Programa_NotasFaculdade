# Programa_NotasFaculdade
A desktop application built with **Python**, **MySQL**, and **CustomTkinter** to help university students manage their academic performance.
The system allows users to **register and log in**, store their course grades, and automatically calculate final results based on continuous assessment or exams.
---
## Features
- User registration and login system 
- MySQL database integration with dynamic user tables
- **Course Catalog**: Select from pre-defined courses with automatic year, semester and ECTS allocation
- **Degree Progress**: Visual progress bar tracking completed ECTS credits (0 to 180)
- **Weighted Average Calculation**: Automatically calculates the student's current average grade based on ECTS credits and approved courses
- Academic grade management per user
- Automatic calculation of final grades
- Approval / rejection logic based on academic rules 
- Modern desktop GUI using CustomTkinter 
- Secure configuration using environment variables (`.env´) 
---
## Grade Calculation Logic
- **Continuous assessment ('eFolioA + eFolioB >= 3.5')**
  -> Student proceeds to *eFolio Global* -> Approved if 'eFolio Global >= 5.5'
- **Continuous assessment < 3.5** 
  -> Student proceeds to *Exam* -> Approved if 'Exam >= 9.5'
- The final grade and approval status are calculated automatically.
- **Weighted Average**: Calculated using the formula `Sum(Final Grade * ECTS) / Total Approved ECTS`.
---
## Tech Stack
- **Python 3**
- **MySQL**
- **CustomTkinter**
- **python-dotenv**
- **mysql-connector-python**
---
## Installation
```md
### Clone the repository 
```bash
git clone https://github.com/manelcorreia/Programa_NotasFaculdade.git 
cd Programa_NotasFaculdade
```
# create and activate a virtual environment
```bash
python -m venv venv 
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate
```
# install dependencies
```bash
pip install -r requirements.txt
```
# database setup
Create the main database in your local MySQL server before running the app:
```sql
CREATE DATABASE IF NOT EXISTS faculdade;
```
# create a .env file in the project root with
```env
DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=faculdade
```

# run the application
```bash
python main.py
```