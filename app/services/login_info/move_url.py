async def move_url(page, url):
    try:
        print(f"🔍 이동할 URL: {url}")  # 디버깅용 출력
        await page.goto(url, wait_until="domcontentloaded", timeout=6000)  # ✅ `await` 추가
    except Exception as e:
        print(f"❌ URL 이동 실패: {e}")
    else:
        print("✅ URL 이동 성공")
    finally:
        await page.wait_for_load_state("networkidle")  # 페이지가 완전히 로드될 때까지 대기
    
    return page