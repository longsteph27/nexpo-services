from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import qrcode
import io
import base64

app = FastAPI(title="QR Code Generator API", version="1.0.0")

class QRCodeRequest(BaseModel):
    text: str

class QRCodeResponse(BaseModel):
    qr_code_base64: str
    success: bool
    message: str

@app.get("/")
async def root():
    return {"message": "QR Code Generator API is running!"}

@app.post("/gen-qr", response_model=QRCodeResponse)
async def generate_qr_code(request: QRCodeRequest):
    """
    Tạo QR code từ string và trả về base64
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text không được để trống")
        
        # Tạo QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(request.text)
        qr.make(fit=True)
        
        # Tạo image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Chuyển đổi thành base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return QRCodeResponse(
            qr_code_base64=img_base64,
            success=True,
            message="QR code được tạo thành công"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi tạo QR code: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
