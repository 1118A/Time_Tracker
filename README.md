# Enterprise Time Tracker

A simple, robust Time Tracking web application built with Django. It allows employees to seamlessly clock in, clock out, and track their breaks, while providing a clear summary of their worked hours and the ability to export their logs.

## Features

- **Employee Dashboard**: A personalized dashboard for each employee based on their name.
- **Clock In / Clock Out**: Accurately track work start and end times.
- **Break Management**: Pauses and resumes time tracking for employee breaks.
- **Duration Calculation**: Automatically calculates total work time, total break time, and net working time.
- **Daily Summary**: Displays today's time logs and calculated net durations.
- **Log History**: An overview of past time logs shown in a responsive data table.
- **Export to CSV**: Easily export the time log history into a CSV file for reporting purposes.
- **Responsive Design**: The UI is optimized for both mobile and desktop screens.

## Technologies Used

- Python 3
- Django 4.2+
- SQLite (default)
- Waitress / Gunicorn & Whitenoise (for serving static files in production)
- Docker & Docker Compose

## Getting Started

### Prerequisites
- Python 3.9+
- Pip
- Virtual Environment (recommended)

### Local Development Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/1118A/Time_Tracker.git
   cd Time_Tracker/enterprise_time_tracker
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. Open your browser and navigate to `http://127.0.0.1:8000/`.

### Docker Setup

You can fully containerize the application to run using Docker Compose.

1. **Ensure Docker and Docker Compose are installed.**

2. **Build and start the container**:
   ```bash
   docker-compose up -d --build
   ```

3. Access the application on `http://localhost:8000/`.

## Screenshots / Layout

The application utilizes a responsive dashboard layout:
- Desktop: Uses a comfortable two-column grid.
- Mobile: Stacks elements neatly vertically with accessible full-width buttons.

## Data Models
- **Employee**: Tracks individual users (based purely on name for simplicity).
- **TimeLog**: Stores clock-in/clock-out times against an employee and date.
- **BreakLog**: Tracks start and end times for any breaks associated with a TimeLog.

---

**Built by [1118A](https://github.com/1118A)**
