from fastapi import APIRouter
from services.login import login  # 🚀 비동기 login 함수 가져오기

router = APIRouter()

@router.post("/create/internal_group")
async def create_internal_group():
    result = await login("jp2", "real")  # ✅ 비동기 호출

    return {"message": "요청 성공"}