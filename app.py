# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import random
import re
import asyncio
import base64
import io

load_dotenv()

app = FastAPI()

# ... [Your existing helper functions: remove_markdown, etc.] ...

class InterviewRequest(BaseModel):
    role: str
    audio: str  # Base64 encoded audio

class InterviewResponse(BaseModel):
    response: str
    audio: str  # Base64 encoded audio response

def remove_markdown(text):
    # Remove asterisks, backticks, and other markdown formatting
    text = re.sub(r'\*+|`+|#+|\[|\]|\(|\)|_+', '', text)
    return text.strip()

@app.post("/interview", response_model=InterviewResponse)
async def conduct_interview(request: InterviewRequest):
    # Decode the audio
    audio_data = base64.b64decode(request.audio)
    
    # Set up speech recognition
    recognizer = sr.Recognizer()
    
    # Convert audio data to AudioData object
    audio = sr.AudioData(audio_data, sample_rate=44100, sample_width=2)
    
    try:
        # Perform speech recognition
        text = recognizer.recognize_google(audio)
        
        # Initialize Gemini AI
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        # Set up chat context
        interviewer_context = """
        You are an AI interviewer conducting a job interview. Your personality is funny, intelligent, and clever. 
        Keep your responses concise and engaging. Do not use any markdown formatting in your responses.
        """
        
        chat_history = [
            {"role": "user", "parts": [interviewer_context]},
            {"role": "model", "parts": ["Understood. I'm ready to conduct the interview as a funny, intelligent, and clever AI interviewer."]},
            {"role": "user", "parts": [f"The role being interviewed for is: {request.role}. Respond to the candidate's statement."]},
        ]
        
        chat = model.start_chat(history=chat_history)
        
        # Get response from Gemini
        response = chat.send_message(text)
        gemini_response = remove_markdown(response.text)
        
        # Convert response to speech
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 170)
        
        # Save speech to a byte stream
        audio_stream = io.BytesIO()
        engine.save_to_file(gemini_response, audio_stream)
        engine.runAndWait()
        audio_stream.seek(0)
        
        # Encode audio to base64
        audio_base64 = base64.b64encode(audio_stream.getvalue()).decode('utf-8')
        
        return InterviewResponse(response=gemini_response, audio=audio_base64)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)