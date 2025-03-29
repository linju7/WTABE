from fastapi import APIRouter

router = APIRouter()

@router.post("/api/create/internal_group")
async def create_internal_group():
    try:

        # 성공한 경우 결과를 반환
        return {"message": "요청 성공"}

    except Exception as e:
        # 실패한 경우 오류 메시지 반환
        return {"message": f"Error occurred: {str(e)}", "data": None}