# playwright 를 이용해서 브라우저 열기
from fastapi import security
from playwright.async_api import async_playwright  # playwright 추가
from app.services.security import password

# 로그인을 수행하는 함수
async def login_web(page, domain):
    user_id = "automation@" + domain 

    # id 입력 
    await page.fill("#user_id", user_id)
    await page.click("#loginStart")
    
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