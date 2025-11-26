# main.py - FastAPI backend server for Protocol Improver (FIXED)

from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from datetime import datetime
from typing import List, Dict
import json

from text_extractor import TextExtractor
from analyzer import ProtocolAnalyzer
from config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Protocol Improver API",
    description="AI-powered laboratory protocol analysis and improvement",
    version="1.0.0"
)

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
text_extractor = TextExtractor()
analyzer = ProtocolAnalyzer()

# Store analysis results temporarily (in production, use a database)
analysis_cache = {}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Protocol Improver API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    api_working = analyzer.quick_check()
    
    return {
        "status": "healthy" if api_working else "degraded",
        "api_connection": "ok" if api_working else "failed",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/upload")
async def upload_protocol(file: UploadFile = File(...)):
    """
    Upload a protocol file for analysis
    
    Args:
        file: PDF or DOCX file
        
    Returns:
        File information and extracted text preview
    """
    
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size (roughly)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB"
        )
    
    # Save uploaded file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = Path(settings.UPLOAD_FOLDER) / safe_filename
    
    try:
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text
        text, metadata = text_extractor.extract(file_path)
        
        # Create preview
        preview = text_extractor.preview_text(text, max_chars=500)
        
        return {
            "success": True,
            "filename": safe_filename,
            "original_filename": file.filename,
            "file_size": file_size,
            "text_length": len(text),
            "preview": preview,
            "metadata": metadata,
            "message": "File uploaded and processed successfully"
        }
        
    except Exception as e:
        # Clean up file if extraction failed
        if file_path.exists():
            file_path.unlink()
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@app.post("/api/analyze")
async def analyze_protocol(file: UploadFile = File(...)):
    """
    Analyze a protocol file and return improvement suggestions
    
    Args:
        file: PDF or DOCX file
        
    Returns:
        Analysis results with suggestions
    """
    
    # First, upload and extract text
    upload_result = await upload_protocol(file)
    
    if not upload_result['success']:
        raise HTTPException(status_code=500, detail="Failed to process file")
    
    # Get the saved file
    file_path = Path(settings.UPLOAD_FOLDER) / upload_result['filename']
    
    try:
        # Extract full text
        text, metadata = text_extractor.extract(file_path)
        
        # Analyze with Claude
        analysis_result = analyzer.analyze_protocol(
            text, 
            upload_result['original_filename']
        )
        
        if analysis_result.get('error'):
            raise HTTPException(
                status_code=500,
                detail=analysis_result.get('message', 'Analysis failed')
            )
        
        # Generate unique analysis ID
        analysis_id = f"{upload_result['filename']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Cache the results
        analysis_cache[analysis_id] = {
            'original_text': text,
            'analysis': analysis_result,
            'filename': upload_result['original_filename'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Return analysis
        return {
            "success": True,
            "analysis_id": analysis_id,
            "filename": upload_result['original_filename'],
            "summary": analysis_result.get('summary', ''),
            "overall_score": analysis_result.get('overall_score', 'N/A'),
            "total_issues": analysis_result.get('total_issues', 0),
            "suggestions": analysis_result.get('suggestions', []),
            "metadata": analysis_result.get('metadata', {})
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during analysis: {str(e)}"
        )


# FIXED: Changed to accept JSON body instead of query parameters
@app.post("/api/improve")
async def generate_improved_protocol(
    request_body: Dict = Body(...)
):
    """
    Generate improved protocol with accepted suggestions
    
    Args:
        request_body: JSON with analysis_id and accepted_indices
        
    Returns:
        Improved protocol text
    """
    
    # Extract parameters from request body
    analysis_id = request_body.get('analysis_id')
    accepted_indices = request_body.get('accepted_indices', [])
    
    if not analysis_id:
        raise HTTPException(
            status_code=400,
            detail="analysis_id is required"
        )
    
    # Get cached analysis
    if analysis_id not in analysis_cache:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found. Please analyze the protocol again."
        )
    
    cached = analysis_cache[analysis_id]
    original_text = cached['original_text']
    all_suggestions = cached['analysis']['suggestions']
    
    # Get accepted suggestions
    accepted_suggestions = [
        all_suggestions[i] for i in accepted_indices 
        if i < len(all_suggestions)
    ]
    
    if not accepted_suggestions:
        return {
            "success": True,
            "improved_protocol": original_text,
            "message": "No suggestions accepted, returning original protocol",
            "suggestions_applied": 0
        }
    
    try:
        # Generate improved protocol
        improved_text = analyzer.generate_improved_protocol(
            original_text,
            accepted_suggestions
        )
        
        # Save improved protocol
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"improved_{cached['filename']}_{timestamp}.txt"
        output_path = Path(settings.OUTPUT_FOLDER) / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(improved_text)
        
        return {
            "success": True,
            "improved_protocol": improved_text,
            "output_filename": output_filename,
            "suggestions_applied": len(accepted_suggestions),
            "message": "Protocol improved successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating improved protocol: {str(e)}"
        )


@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """
    Download an improved protocol file
    
    Args:
        filename: Name of the file to download
        
    Returns:
        File download
    """
    
    file_path = Path(settings.OUTPUT_FOLDER) / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='text/plain'
    )


@app.get("/api/stats")
async def get_stats():
    """Get usage statistics"""
    
    uploads_dir = Path(settings.UPLOAD_FOLDER)
    outputs_dir = Path(settings.OUTPUT_FOLDER)
    
    return {
        "total_uploads": len(list(uploads_dir.glob("*"))),
        "total_analyses": len(analysis_cache),
        "total_improved": len(list(outputs_dir.glob("*"))),
        "cache_size": len(analysis_cache)
    }


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Protocol Improver API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API docs available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
