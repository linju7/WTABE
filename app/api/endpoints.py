from fastapi import APIRouter, Request
from app.services.login.login import process_login
from app.services.login.logout import process_logout
from app.services.user.createUser import process_create_user
from app.services.user.modifyUser import process_modify_user
from app.services.user.retreiveUser import process_retreive_user
from app.services.user.deleteUser import process_delete_user
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




"""
    -----------------------------------------------
    테스트 환경 선택 API 
"""

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

        # 전역 변수 업데이트
        request.app.state.global_domain = domain
        request.app.state.global_instance = instance
        request.app.state.global_server = server

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





"""
    -----------------------------------------------
    구성원 API 
"""

@router.post("/api/user/all")
async def user_all(request: Request):
    """
    구성원 추가/수정/조회/삭제를 순차적으로 수행하는 API 엔드포인트
    """
    try:
        body = await request.json()
        instance = body.get("instance")
        server = body.get("server")

        # 1. 사용자 추가
        create_response = await process_create_user(request.app.state.global_page, instance, server, request.app.state)
        if create_response.get("status") != "success":
            return {"status": "error", "message": "사용자 추가 실패", "details": create_response}

        # 2. 사용자 수정
        modify_response = await process_modify_user(request.app.state.global_page, instance, server, request.app.state)
        if modify_response.get("status") != "success":
            return {"status": "error", "message": "사용자 수정 실패", "details": modify_response}

        # 3. 사용자 조회
        retrieve_response = await process_retreive_user(request.app.state.global_page, instance, server, request.app.state)
        if retrieve_response.get("status") != "success":
            return {"status": "error", "message": "사용자 조회 실패", "details": retrieve_response}

        # 4. 사용자 삭제
        delete_response = await process_delete_user(request.app.state.global_page, instance, server, request.app.state)
        if delete_response.get("status") != "success":
            return {"status": "error", "message": "사용자 삭제 실패", "details": delete_response}

        # 모든 작업 성공 시 응답
        return {
            "status": "success",
            "message": "모든 작업이 성공적으로 완료되었습니다.",
            "details": {
                "create": create_response,
                "modify": modify_response,
                "retrieve": retrieve_response,
                "delete": delete_response,
            },
        }

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

@router.post("/api/user/retreive")
async def modify_user(request: Request):
    """
    사용자 조회 API 엔드포인트
    """
    try :
        body = await request.json()
        instance = body.get("instance")
        server = body.get("server")

        # 사용자 수정 처리 호출
        response = await process_retreive_user(request.app.state.global_page, instance, server, request.app.state)
        return response
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@router.post("/api/user/delete")
async def delete_user(request: Request):
    """
    사용자 조회 API 엔드포인트
    """
    try :
        body = await request.json()
        instance = body.get("instance")
        server = body.get("server")

        # 사용자 수정 처리 호출
        response = await process_delete_user(request.app.state.global_page, instance, server, request.app.state)
        request.app.state.global_user_id = ""
        return response
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    
    
    
"""
    -----------------------------------------------
    조직 API 
"""
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