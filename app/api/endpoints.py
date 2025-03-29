from fastapi import APIRouter
from app.services.selenium_service import run_selenium_task
from app.schemas import ResponseSchema

router = APIRouter()

@router.post("/create/internal_group", response_model=ResponseSchema)
async def create_internal_group():
    try:
        # 셀레니움 작업을 실행
        result = await run_selenium_task()

        # 성공한 경우 결과를 반환
        return {"message": "Internal group created successfully", "data": result}

    except Exception as e:
        # 실패한 경우 오류 메시지 반환
        return {"message": f"Error occurred: {str(e)}", "data": None}