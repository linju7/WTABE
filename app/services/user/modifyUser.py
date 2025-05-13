# 다른 파일
from app.services.url.move_url import move_url_by_url
from app.services.security import url

async def process_modify_user(page, instance, server, app_state):
    """
    사용자 수정 프로세스
    """
    try:
        # 1. 어드민 > 구성원 페이지로 이동
        target_url = url[server][instance]["user"]
        await move_url_by_url(page, target_url)

        # 2. app.state에서 user_id 읽기
        user_id = app_state.global_user_id
        print(f"수정할 사용자 ID: {user_id}")

        # 3. id값을 이용하여 구성원 상세 > 구성원 수정 접근
        # ...

        # 성공 메시지 반환
        return {"status": "success", "message": "사용자 수정 완료"}

    except Exception as e:
        # 에러 메시지 반환
        return {"status": "error", "message": str(e)}