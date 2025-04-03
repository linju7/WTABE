# playwright 를 이용해서 브라우저 열기
from fastapi import security
from playwright.async_api import async_playwright
from app.services.security import url, account

async def open_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    return page
    
# url에 접근하기. url = security.py 에 있는 url 사용, server, instance 를 통해 접근
async def access_url(page, server, instance):
    target_url = url[server][instance]["service"]  # service URL을 사용
    await page.goto(target_url)
    return page

# 로그인을 수행하는 함수
async def login_web(page, server, instance):
    user_info = account[server][instance]
    await page.fill("#user_id", user_info["userid"])
    await page.click("#loginStart")
    
    await page.fill("#user_pwd", user_info["password"])
    await page.click("#loginBtn")

    # 로그인 후 팝업창이 나타날 때까지 대기
    await page.wait_for_timeout(2000)  # 로그인 처리 시간 대기
    
    # 모든 팝업창 닫기
    for popup in page.context.pages:
        if popup != page:  # 메인 페이지가 아닌 경우
            await popup.close()

    return page

async def perform_login(server, instance):
    page = await open_browser()
    page = await access_url(page, server, instance)
    page = await login_web(page, server, instance)
    
    return page