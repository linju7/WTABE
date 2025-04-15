# playwright 를 이용해서 브라우저 열기
from fastapi import security
from playwright.async_api import async_playwright  # playwright 추가
from app.services.security import password
from app.services.url.move_url import move_url
import asyncio

# 로그인을 수행하는 함수
async def login_web(page, domain):
    user_id = "automation@" + domain 

    # id 입력 
    await page.fill("#user_id", user_id)
    await page.click("#loginStart")
    
    # 아이디 입력 후 잘못된 경우 에러 DOM이 있는지 확인 (1초 대기 후)
    await page.wait_for_timeout(1000)
    try:
        error_element = await page.query_selector(".input_cover.writing.invalid")
        if error_element:
            return None
    except TimeoutError:
        # 셀렉터 탐색 시 타임아웃 날 경우 그냥 넘어감
        pass
    
    # 비밀번호 입력
    await page.fill("#user_pwd", password)
    await page.click("#loginBtn")

    # 로그인 후 팝업창이 나타날 때까지 대기
    await page.wait_for_timeout(2000)  # 로그인 처리 시간 대기
    
    # 모든 팝업창 닫기
    for popup in page.context.pages:
        if popup != page:  # 메인 페이지가 아닌 경우
            await popup.close()

    return page

async def perform_login(page, domain):
    
    page = await login_web(page, domain)
    
    return page

async def process_login(domain: str, instance: str, server: str) -> dict:
    """
    로그인 프로세스를 처리하는 함수
    """
    success = await handle_browser_session(domain, instance, server)

    if success:
        # 로그인 성공 시 응답 반환
        print("로그인 성공")
        return {"status": "success"}
    else:
        # 로그인 실패 시 응답 반환
        return {"status": "error", "message": "로그인 실패"}


async def handle_browser_session(domain: str, instance: str, server: str) -> bool:
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
        page = await perform_login(page, domain)
        
        if page is None:
            print("로그인 실패: 도메인이 잘못되었습니다.")
            return False
        
        # 페이지 유지 작업을 백그라운드에서 실행
        asyncio.create_task(keep_browser_alive(page))
        
        return True

    except Exception as e:
        print(f"오류 발생: {e}")
        return False

    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()


async def keep_browser_alive(page):
    """
    브라우저 페이지를 유지하기 위한 비동기 작업
    """
    try:
        print("페이지 유지 중...")
        await asyncio.Event().wait()  # 페이지를 유지하기 위해 무한 대기
    except Exception as e:
        print(f"페이지 유지 중 오류 발생: {e}")