from playwright.async_api import async_playwright  
from app.services.security import accounts
from app.services.url.move_url import move_url
from fastapi import Request, APIRouter

router = APIRouter()

# 로그인을 수행하는 함수
async def login_web(page, domain):
    user_id = "automation" + domain 

    # id 입력 
    await page.fill("#user_id", user_id)
    await page.click("#loginStart")
    
    # 네트워크 요청이 안정된 상태가 될 때까지 대기
    await page.wait_for_load_state("networkidle")  
    
    # 비밀번호 입력
    await page.fill("#user_pwd", accounts["password"])
    await page.click("#loginBtn")

    return page


async def handle_browser_session(domain: str, instance: str, server: str) -> tuple:
    """
    브라우저 세션을 처리하는 함수
    """
    playwright = None
    browser = None
    page = None

    try:
        # 브라우저 열기
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()

        # URL 이동
        page = await move_url(page, server, instance)
        
        # 로그인 수행
        page = await login_web(page, domain)
        
        if page is None:
            print("로그인 실패: 도메인이 잘못되었습니다.")
            return False, None
        
        # 로그인 성공
        print("로그인 성공")
        return True, page

    except Exception as e:
        print(f"오류 발생: {e}")
        return False, None


async def process_login(domain: str, instance: str, server: str, state) -> dict:
    """
    로그인 프로세스를 처리하는 함수
    """
    success, page = await handle_browser_session(domain, instance, server)

    if success:
        # 로그인 성공 시 애플리케이션 상태에 페이지 저장
        state.global_page = page
        print("로그인 성공")
        return {"status": "success", "message": "로그인 성공"}
    else:
        # 로그인 실패 시 응답 반환
        return {"status": "error", "message": "로그인 실패"}