# Speech-to-Speech Interview API

This project is an AI-powered Speech-to-Speech Interview API that conducts job interviews using voice input and output. It leverages FastAPI, Google's Speech Recognition, pyttsx3 for text-to-speech conversion, and Google's Gemini AI for generating interview responses.

## Features

- Speech-to-text conversion
- AI-powered interview responses
- Text-to-speech conversion
- RESTful API interface

## Prerequisites

- Python 3.7+
- A Gemini AI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/speech-to-speech-api.git
   cd speech-to-speech-api
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Gemini AI API key to the `.env` file

## Usage

1. Start the FastAPI server:
   ```
   uvicorn app:app --reload
   ```

2. The API will be available at `http://localhost:8000`

3. Use the `/interview` endpoint with a POST request containing:
   - `role`: The job role being interviewed for
   - `audio`: Base64-encoded audio of the candidate's response

4. The API will return:
   - `response`: Text of the AI interviewer's response
   - `audio`: Base64-encoded audio of the spoken response

## API Documentation

Once the server is running, you can access the automatic API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.