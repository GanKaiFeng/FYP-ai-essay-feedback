# AI Essay Feedback System

A web application that provides AI-powered feedback for student essays, featuring separate interfaces for teachers and students.

## Features
- Homepage

- Essay list
  - Search for essays by author or content
  - Click to enter detailed view with full essay and feedback

- Teacher Upload Interface
  - Upload and manage essays
  - Add or edit essay titles and rubrics
  - View student submissions

- Student Upload Interface
  - Submit essays
  - View feedback and grades

- Language switch
  - English (default)
  - Chinese

## Tech Stack

- Frontend: TypeScript + Vite
- Backend: Python Flask
- Database: PostgreSQL

## Prerequisites

- Node.js (v22.16.0 or higher)
- Python 3.x
- npm (v10.9.2 or higher)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-essay-feedback.git
cd ai-essay-feedback
```

2. Install frontend dependencies (creates node_modules folder):
```bash
npm install
```

3. Set up Python virtual environment and install backend dependencies (creates venv folder):
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .backend\venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

1. Start the backend server:
```bash
cd backend
python app.py
```

2. In a new terminal, start the frontend development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

## Project Structure

```
ai-essay-feedback/
├── backend/           # Python Flask backend
│   ├── app.py        # Main application file
│   ├── db/           # Database files
│   └── requirements.txt
├── src/              # Frontend source code
├── public/           # Static assets
└── package.json      # Frontend dependencies
```

## NOTE:
```
Add your keys for GPT, Claude, Gemini and Supabase in the .env file.
Replace the Supabase connections in each vue file. Comment is "Supabase keys here"
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
