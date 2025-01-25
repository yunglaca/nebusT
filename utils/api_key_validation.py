from fastapi import HTTPException, Header, status
from db.config import settings

# Получаем ключ из настроек
API_KEY = settings.api_key

def verify_api_key(api_key: str = Header(...)):  # Указываем, что ключ ожидается в заголовке
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key
