# Programa_NotasFaculdade
A desktop application built with **Python**, **MySQL**, and **CustomTkinter** to help university students manage their academic performance.
The system allows users to **register and log in**, store their course grades, and automatically calculate final results based on continuous assessment or exams.
---
## Features
- User registration and login system 
- MySQL database integration
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
---
## Tech Stack
- **Python 3**
- **MySQL**
- **CustomTkinter**
- **python-dotenv**
- **mysql-connector-python**
---
## How to Run
### Clone the repository 
```bash
git clone https://github.com/manelcorreia/Programa_NotasFaculdade.git
cd Programa_NotasFaculdade