from fastapi import APIRouter, Request
from app.services.login.login import process_login
from app.services.login.logout import process_logout

router = APIRouter()

@router.post("/api/login")
async def login(request: Request):
    try:
        # 요청 파싱
        body = await request.json()
        domain = body.get("domain")
        instance = body.get("instance")
        server = body.get("server")

        # 로그인 처리 호출
        response = await process_login(domain, instance, server, request.app.state)
        return response

    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/api/logout")
async def logout(request: Request):
    try:
        # 로그아웃 처리 호출
        response = await process_logout(request.app.state)
        return response

    except Exception as e:
        return {"status": "error", "message": str(e)}


