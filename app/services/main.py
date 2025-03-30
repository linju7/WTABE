import sys
import os
import asyncio  # asyncio를 사용하여 비동기 함수 실행

# 현재 파일(main.py)이 있는 디렉터리의 부모 디렉터리(프로젝트 루트)를 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from playwright.async_api import async_playwright  # 비동기 Playwright API 사용
from login_info.login import login  # 경로 유지

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 비동기 login 함수 호출 (필요 시)
        page = await login(page, "real", "jp2")

        await page.pause()  # 페이지 일시 정지

if __name__ == "__main__":
    asyncio.run(main())  # asyncio 이벤트 루프에서 실행