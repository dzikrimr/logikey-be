import torch
from fastapi import FastAPI, Depends, HTTPException
from app.services.ai_service import ai_logic_service
from app.services.logic_parser import logic_parser
from app.core.security import validate_api_key
from app.models.schema import LogicRequest, LogicResponse

app = FastAPI(
    title="Logiclyst Backend API",
    description="Infrastruktur AI untuk analisis Logical Fallacy",
    version="1.0.0"
)

@app.post("/analyze", response_model=LogicResponse)
async def analyze_argument(
    request: LogicRequest, 
    _ : str = Depends(validate_api_key) 
):
    """
    Endpoint utama untuk keyboard Android.
    Menerima teks, memproses lewat LLM, dan mengembalikan analisis terstruktur.
    """
    try:
        # Kirim input ke model Llama-3
        raw_output = await ai_logic_service.analyze_logic(request.text)
        
        # Parsing output mentah
        parsed_result = logic_parser.parse_response(raw_output)
        
        # Return Response sesuai Schema
        return LogicResponse(
            input=request.text,
            label=parsed_result["label"],
            explanation=parsed_result["explanation"],
            is_fallacy=parsed_result["is_fallacy"],
            counter_arguments=parsed_result["counter_arguments"],
            status="success"
        )
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Terjadi kesalahan pada mesin penalaran AI."
        )

@app.get("/health")
async def health_check():
    """Cek status server dan kesiapan model."""
    return {
        "status": "ready",
        "model": "Logiclyst-Llama-3-8B",
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    }