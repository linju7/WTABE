from app.services.url.move_url import move_url_by_url

async def make_popup_url(server, instance, app_state):
    """
    팝업 URL 생성
    """
    base_url = "https://"
    if server != "real":
        base_url += f"{server}."
    base_url += "contact.worksmobile.com/v2/p/popup/organization/chart"
    
    # app_state에서 global_user_id 가져오기
    keyword = app_state.global_user_id
    popup_url = f"{base_url}?keyword={keyword}"
    
    return popup_url
    
    
    
async def process_retreive_user(page, instance, server, app_state):
    """
    사용자 조회 프로세스
    """
    try:
        # 1. 구성원 조직도 팝업 접근
        target_url = await make_popup_url(server, instance, app_state)  # await 추가
        await move_url_by_url(page, target_url)
        
        # 2. 구성원 3단뷰 데이터 조회
        # (추가 로직 작성 필요)
        
        # 3. API로 사용자 정보 조회
        # (추가 로직 작성 필요)
        
        # 4. UI 데이터와 API 데이터 비교
        # (추가 로직 작성 필요)
        
        # 5. 결과 반환 
        return {"status": "success", "message": "사용자 조회 완료"}

    except Exception as e:
        # 에러 메시지 반환
        return {"status": "error", "message": str(e)}
