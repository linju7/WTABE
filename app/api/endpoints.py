from fastapi import APIRouter, Request
from app.services.login.login import perform_login
from app.services.url.move_url import move_url
from playwright.async_api import async_playwright

router = APIRouter()

@router.post("/api/login")
async def login_endpoint(request: Request):
    playwright = None
    browser = None
    page = None

    try:
        # 브라우저 열기
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()

        # 요청 파싱
        body = await request.json()
        domain = body.get("domain")
        instance = body.get("instance")
        server = body.get("server")

        # URL 이동=
        page = await move_url(page, server, instance)
        
        # 로그인 수행
        page = await perform_login(page, domain)
        
        if page is None:
            print("로그인 실패: 도메인이 잘못되었습니다.")
            return {"status": "error", "message": "로그인 실패: 도메인이 잘못되었습니다."}
        
        await page.pause()

        return {"status": "success"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()