from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

from services.genai import YoutubeProcessor, GeminiProcessor

class VideoAnalysisRequest(BaseModel):
    youtube_link: HttpUrl

    # Advanced Settings

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/analyze_video")
def analyze_video(request: VideoAnalysisRequest):

    # Analysis
    
    processor = YoutubeProcessor()
    result = processor.retrive_youtube_documents(str(request.youtube_link))

    genai_processor = GeminiProcessor(
        model_name = 'gemini-pro',
        project = 'gemini-dynamo-426318'
    )

    summary = genai_processor.generate_document_summary(result, verbose=True)

    return {
        'summary': summary
    }