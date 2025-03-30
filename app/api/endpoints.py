from fastapi import APIRouter
from app.services import main  # services.main 모듈 임포트

router = APIRouter()

@router.post("/api/create/internal_group")
async def create_internal_group():
    try:
        # services.main의 함수 호출 예시
        result = await main.main()  # main.py의 main 함수 호출

        # 성공한 경우 결과를 반환
        return {"message": "요청 성공?", "data": result}

    except Exception as e:
        # 실패한 경우 오류 메시지 반환
        return {"message": f"Error occurred: {str(e)}", "data": None}