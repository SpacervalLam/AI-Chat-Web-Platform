🚧 Still a WIP! Any cool bro wanna polish it up? I'd be mega happy! (≧▽≦)

> *This is a tentative assumption and needs further validation.*

# My Platform

This is a full-stack application with backend and frontend components, designed to provide interactive functionality with chat models.

## Features Overview
- **Backend**: RESTful API built with FastAPI, supporting model listing and chat functionality.
- **Frontend**: Modern user interface built with React and TypeScript, enabling interaction with the backend.

## Backend
The backend is a FastAPI-based application that provides the following features:
- **API Routes**: Defined in `backend/app/api/v1/endpoints/`.
- **Core Configuration**: Managed in `backend/app/core/config.py`.
- **Database**: Uses SQLite, configured in `backend/app/core/database.py`.
- **Models and Schemas**: Defined in `backend/app/models/` and `backend/app/schemas/`.
- **Services**: Business logic implemented in `backend/app/services/`.

### Backend Development Setup
1. Enter to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the server:  `uvicorn app.main:app --reload --port 8000`

The backend runs by default at `http://localhost:8000`.

## Ollama Configuration

At this stage, the backend temporarily supports only the Ollama library for model interaction. To ensure proper functionality, make sure to:

1. Install the required version of Ollama:
   ```bash
   pip install ollama==0.4.8
   ```
 
2. Verify that the Ollama service is properly configured and accessible in your environment. The default configuration assumes that the Ollama service is running on http://localhost:11434. You can refer to the [Ollama documentation](https://ollama.ai/docs) for detailed setup instructions.

3. Ensure network connectivity if the Ollama service is hosted remotely.


## Frontend
The frontend is a React and TypeScript-based application that provides the following features:
- **Main Entry Point**: Defined in `frontend/src/main.tsx`.
- **Components**: Modular UI components located in `frontend/src/components/`.
- **Services**: API interaction logic defined in `frontend/src/services/api.ts`.
- **Styling**: Managed using Tailwind CSS.

### Frontend Development Setup
1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

The frontend runs by default at `http://localhost:5173`.

## API Examples
### List Models
**GET** `/api/v1/models`

### Chat Endpoint
**POST** `/api/v1/chat`
- Request Body Example:
```json
{
  "messages": [
    { "role": "user", "content": "Hello!" }
  ],
  "model": "gpt-3.5",
  "stream": false
}
```

## Testing
- Backend tests are located in `tests/api/test_v1/`.
- Run backend tests: `pytest tests/`

## Project Structure
```
My-Platform/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── database.db
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── main.tsx
│   ├── package.json
│   └── tailwind.config.js
└── tests/
    └── api/
        └── test_v1/
```

## Contribution
Feel free to submit issues and contribute to the code!
