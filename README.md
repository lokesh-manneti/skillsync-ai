

# SkillSync AI: Your AI-Powered Career Navigator

> **Align your skills. Accelerate your career.**

SkillSync AI is a full-stack, end-to-end AI application designed to demystify the job search. It analyzes your resume against live job descriptions to find your skill gaps, and then builds a personalized, step-by-step learning roadmap to help you land your target role.

**[Live Demo URL](https://skillsync-frontend-1078370935935.us-central1.run.app)** 

-----

## 🚀 The Problem

The job search is a "black box." We're told to "tailor your resume," but we're left guessing *how*.

  * What skills *actually* matter for a "Python Developer" today?
  * How does my resume stack up against live job postings?
  * What's the fastest way to learn the skills I'm missing?

SkillSync AI is an AI-powered mentor that gives you immediate, scannable, and actionable answers to all these questions.

-----

## ✨ Key Features

  * **Secure User Authentication**: JWT-based auth for all user-specific actions.
  * **PDF Resume Parsing**: Upload your resume, and the system extracts and saves the text.
  * **Resume History**: View all previously uploaded resumes and re-run analyses without re-uploading.
  * **Live Role Analysis**: Enter a job title (e.g., "React Developer"), and the app fetches live job postings from the Arbeitnow API to synthesize an **Ideal Candidate Profile**.
  * **AI Skill Gap Report**: Get a **match score (%)** and a detailed breakdown of which skills from the ideal profile are **Matched**, **Partial**, or **Missing** from your resume.
  * **Personalized Learning Roadmaps**: For every missing skill, the AI generates a custom, step-by-step learning plan tailored to your chosen preference (e.g., "Coding Projects," "Video Courses," "Reading / Docs").
  * **ATS-Optimized Resume**: Get an AI-generated rewrite of your resume, optimized with the keywords and skills employers are looking for, with a one-click "Copy to Clipboard."

-----

## 🛠️ Tech Stack & Architecture

This project is built as a scalable, decoupled, two-service application, fully containerized and deployed on Google Cloud.

  * **Backend**: **Python 3.12**, **FastAPI** (async), **SQLAlchemy** (async)
  * **Frontend**: **React (Vite)**, **Tailwind CSS**, `axios`, `react-router-dom`
  * **Database**: **PostgreSQL** (running on **Google Cloud SQL**)
  * **AI**: **Google Gemini 2.5 Flash** (via `google-generativeai` SDK)
  * **Deployment**:
      * Two **Docker** containers (one for backend, one for frontend)
      * **Nginx** (serving the static React app and proxying API requests)
      * **Google Artifact Registry** (for hosting Docker images)
      * **Google Cloud Run** (for serverless, scalable container hosting)
      * **Alembic** (for database migrations)

### System Flow

1.  User accesses the **React Frontend** service (Cloud Run).
2.  The React app (served by Nginx) makes API calls to `/api/...`.
3.  Nginx proxies these requests to the **FastAPI Backend** service (a separate Cloud Run instance).
4.  The Backend service (Python) securely connects to the **Cloud SQL** database using the Cloud SQL Auth proxy.
5.  The Backend service calls the **Gemini API** for all AI generation tasks.

-----

## 🚀 Getting Started (Local Setup)

You can run the entire application locally using Docker and a local Python environment.

### Prerequisites

  * [Git](https://www.google.com/search?q=https://git-scm.com/downloads)
  * [Python 3.12](https://www.python.org/downloads/)
  * [Node.js (LTS)](https://nodejs.org/)
  * [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 1\. Backend Setup

1.  **Start Postgres Database:**

    ```bash
    # Run this once to create your local database container
    docker run --name skillsync-postgres -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=skillsync -p 5432:5432 -d postgres:16
    ```

    *(If it already exists, just run `docker start skillsync-postgres`)*

2.  **Create `.env` file:** In the `backend/` folder, create a file named `.env` and paste in your secrets.

    ```ini
    DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/skillsync
    GOOGLE_API_KEY=your_gemini_api_key_here
    SECRET_KEY=your_strong_32_character_hex_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    ```

3.  **Install Dependencies & Run Migrations:**

    ```bash
    # Navigate to the backend folder
    cd backend

    # Create and activate a virtual environment
    python -m venv venv
    .\venv\Scripts\activate

    # Install all packages
    pip install -r requirements.txt

    # Run database migrations to create tables
    alembic upgrade head
    ```

4.  **Run the Backend Server:**

    ```bash
    # From the backend/ folder with venv active:
    uvicorn app.main:app --reload
    ```

    Your backend is now running on `http://127.0.0.1:8000`.

### 2\. Frontend Setup

1.  **Configure Vite Proxy:**
    In the `frontend/` folder, ensure you have a `vite.config.js` file to proxy API requests to the backend:

    ```javascript
    import { defineConfig } from 'vite'
    import react from '@vitejs/plugin-react'

    export default defineConfig({
      plugins: [react()],
      server: {
        proxy: {
          '/api': {
            target: 'http://127.0.0.1:8000',
            changeOrigin: true,
            rewrite: (path) => path.replace(/^\/api/, ''),
          }
        }
      }
    })
    ```

2.  **Install Dependencies & Run:**
    Open a **new terminal** for the frontend.

    ```bash
    # Navigate to the frontend folder
    cd frontend

    # (For Windows PowerShell, run this once to allow scripts)
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

    # Install Node modules
    npm install

    # Run the dev server
    npm run dev
    ```

    Your frontend is now running on `http://localhost:5173`.

-----

## 🧠 Future Work

This project is the foundation for a complete AI career mentor. The next planned features are:

  * **Save Analysis History**: Persist every analysis report to the database.
  * **Progress Tracking**: Allow users to see how their skill score changes over time as they learn.
  * **AI Chatbot**: Build a conversational agent (`/chat` endpoint) that uses a user's resume and their saved reports as context to answer follow-up questions.
