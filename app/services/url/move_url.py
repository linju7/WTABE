from app.services.security import url
from app.services.url.url_selector import url_selector

async def move_url_by_url(page, url):
    target_url = url
    await page.goto(target_url)
    await page.wait_for_load_state('networkidle')  # 네트워크 요청이 안정된 상태를 기다림
    return page

async def move_url(page, server, instance) :
    target_url = url_selector(server, instance)
    await page.goto(target_url)
    await page.wait_for_load_state('networkidle')  # 네트워크 요청이 안정된 상태를 기다림
    return page