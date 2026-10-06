# Examportal

Welcome to the Examportal, an innovative, premium examination platform that revolutionizes the way students take tests and how institutions manage them. Powered by the Flask framework and utilizing a robust SQLite database, this portal provides a feature-rich, efficient, and beautifully designed interface for conducting and tracking exams.

## Features

- **Premium User Interface**: The portal offers a stunning, modern dark mode aesthetic built with glassmorphism design principles, ensuring a seamless and highly engaging testing experience.
- **Secure User Authentication**: Students can securely log in to the portal to access their tests, view historical data, and manage their personal information.
- **Student Dashboard**: A dedicated dashboard for students to track their past exam results, percentages, and history over time.
- **Advanced Question Bank**: Administrators can seamlessly create, manage, and categorize questions across multiple formats including Multiple Choice (MCQ), True/False, and Fill in the Blanks.
- **Exam Scheduling**: Administrators can enforce strict date and time constraints for when exams are active and available to students based on their academic year.
- **Timed Tests**: Exams feature a dynamic countdown timer that strictly enforces time limits and automatically submits the test when time expires.
- **Auto-Grading and Result Analytics**: The platform automatically evaluates and grades objective questions across all formats, providing instant feedback and detailed analytics immediately after submission.
- **Certificate Generation**: Upon successfully passing an exam (scoring above 50%), students are automatically issued an elegantly designed Certificate of Achievement that can be instantly downloaded or printed.

## Technology Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML5, CSS3 (Custom Glassmorphism Design System), JavaScript

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sarthaksec/Examportal.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Examportal
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database and seed it with sample data (Optional):
   ```bash
   python seed.py
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the portal in your browser at `http://localhost:5000`.

## Usage

1. Register a new account on the portal by selecting your academic year (e.g., SY or TY).
2. Log in using your credentials to access your Student Dashboard.
3. If an exam is scheduled and active for your year, click "Take Exam" to begin within the provided time frame.
4. Submit your answers before the timer runs out to receive instant auto-graded feedback.
5. If you pass the exam, return to your dashboard to generate and print your Certificate of Achievement.
6. Administrators can access the admin panel to manage questions and scheduling.

## License

This project is licensed under the MIT License.
