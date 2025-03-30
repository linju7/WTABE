from playwright.async_api import async_playwright
from app.services.login_info.move_url import move_url
from app.services.security import account, url

async def get_user_info(server, instance):
    userid = account[server][instance]["userid"]
    password = account[server][instance]["password"]
    target_url = url[server][instance]["service"]  

    return (userid, password, target_url)

async def login_do(page, server, instance):
    # 비동기 함수 호출 시 await 사용
    userid, password, target_url = await get_user_info(server, instance)
    page = await move_url(page, target_url)  # URL 이동
    
    try:
        await page.fill("#user_id", userid)
        await page.click("#loginStart")
        
        await page.fill("#user_pwd", password)
        await page.click("#loginBtn")
        
        print("✅ 로그인 성공")
    except Exception as e:
        print(f"❌ 로그인 실패: {e}")

    return page

async def login(page, server, instance):
    page = await login_do(page, server, instance)
    return page