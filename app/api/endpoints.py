from fastapi import APIRouter, Request
from app.services.login.login import process_login
from app.services.login.logout import process_logout
from app.services.user.createUser import process_create_user
from app.services.user.modifyUser import process_modify_user
from app.services.login.verification import process_verification
from app.services.orgunits.createOrgunits import process_create_orgunits

router = APIRouter()

@router.post("/api/security")
async def security(request: Request):
    """
    보안 API 엔드포인트
    """
    try:
        # 요청 파싱
        body = await request.json()
        password = body.get("password")
        response = await process_verification(password)
        
        return response

    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/api/login")
async def login(request: Request):
    """
    로그인 API 엔드포인트
    """
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
    """
    로그아웃 API 엔드포인트
    """
    try:
        # 로그아웃 처리 호출
        response = await process_logout(request.app.state)
        return response

    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/api/user/create")
async def create_user(request: Request):
    """
    사용자 생성 API 엔드포인트
    """
    try:
        body = await request.json()
        instance = body.get("instance")
        server = body.get("server")
        
        # 사용자 생성 처리 호출
        response = await process_create_user(request.app.state.global_page, instance, server, request.app.state)
        return response

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@router.post("/api/user/modify")
async def modify_user(request: Request):
    """
    사용자 수정 API 엔드포인트
    """
    try :
        body = await request.json()
        instance = body.get("instance")
        server = body.get("server")

        # 사용자 수정 처리 호출
        response = await process_modify_user(request.app.state.global_page, instance, server, request.app.state)
        return response
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

    
    
    
@router.post("/api/orgunits/create")
async def create_orgunit(request: Request):
    """
    조직 생성 API 엔드포인트
    """
    try:
        body = await request.json()
        instance = body.get("instance")
        server = body.get("server")
        
        # 조직 단위 생성 처리 호출
        response = await process_create_orgunits(request.app.state.global_page, instance, server)
        return response

    except Exception as e:
        return {"status": "error", "message": str(e)}