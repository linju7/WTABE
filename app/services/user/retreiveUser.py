from app.services.url.move_url import move_url_by_url
from app.services.security import url
import httpx

async def make_popup_url(server, instance, app_state):
    """
    팝업 URL 생성
    """
    base_url = "https://"
    if server != "real":
        base_url += f"{server}."
    base_url += url["user"]["popup"]
    
    # app_state에서 global_user_id 가져오기
    keyword = app_state.global_user_id + app_state.global_domain
    popup_url = f"{base_url}?keyword={keyword}"
    
    return popup_url

async def call_retreive_user_api(page, app_state):
    """
    사용자 조회 API 호출
    """
    # 조회할 ID와 엑세스 토큰 가져오기
    user_id = app_state.global_user_id + app_state.global_domain
    from app.services.security import access_token

    # API URL 구성
    api_url = f"https://www.worksapis.com/v1.0/users/{user_id}"

    # HTTP 요청 헤더 설정
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        # HTTP GET 요청 보내기
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)

        # 응답 결과 반환
        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        else:
            return {"status": "error", "message": response.text}

    except Exception as e:
        # 예외 처리
        return {"status": "error", "message": str(e)}

async def process_retreive_user(page, instance, server, app_state):
    """
    사용자 조회 프로세스
    """
    try:
        # 1. 구성원 조직도 팝업 접근
        target_url = await make_popup_url(server, instance, app_state)  # await 추가
        await move_url_by_url(page, target_url)
        
        # 2. 구성원 3단뷰 데이터 조회

        # 3. API로 사용자 정보 조회
        call_retreive_user_api_result = await call_retreive_user_api(page, app_state)
        print(call_retreive_user_api_result)
        
        # 4. UI 데이터와 API 데이터 비교

        
        # 5. 결과 반환 
        return {"status": "success", "message": "사용자 조회 완료"}

    except Exception as e:
        # 에러 메시지 반환
        return {"status": "error", "message": str(e)}
