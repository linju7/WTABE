from fastapi import APIRouter
from app.services.login.login import perform_login
from app.services.internal_group.create_internal_group import create_internal_group

router = APIRouter()

@router.post("/api/create/internal_group")
async def create_internal_group_endpoint():
    try:
        # 로그인 하기 
        page = await perform_login("real", "jp2")  

        # 페이지 객체가 None인지 확인
        if page is None:
            return {"status": "error", "message": "페이지 초기화 실패"}
        
        # 내부 그룹 생성 실행
        result = await create_internal_group(page)
        
        return result

    except Exception as e:
        return {"status": "error", "message": f"내부 그룹 생성 중 오류 발생: {str(e)}"}
        