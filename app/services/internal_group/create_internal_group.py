from datetime import datetime
from playwright.async_api import Page
from app.services.security import url
async def access_create_group_service(page: Page):
    try:
        # "새로 만들기" 버튼 클릭
        await page.locator('a.skin_corp_bg.skin_corp_txt.has_dropdown:has-text("새로 만들기")').click()

        # "그룹 추가" 항목 선택
        await page.locator('a:has-text("그룹 추가")').first.click()
        await page.wait_for_selector('div.layer_content', state='attached')

        # 새로운 페이지로 포커싱 이동 (팝업창)
        new_page = None
        def handle_new_page(new):
            nonlocal new_page
            new_page = new

        page.context.on('page', handle_new_page)

        # "그룹 만들기" 버튼 클릭
        await page.locator('a.link:has-text("그룹 만들기")').first.click()

        # 새 페이지가 생성될 때까지 대기
        while new_page is None:
            await page.wait_for_timeout(100)

        # 새 페이지가 로딩될 때까지 대기
        await new_page.wait_for_load_state('domcontentloaded')

        return new_page

    except Exception as e:
        print(f"그룹 생성 서비스 접근 중 오류 발생: {str(e)}")
        raise e

async def fill_field(page: Page):
    try:
        timestamp = datetime.now().strftime("%m%d%H%M")
        
        # 그룹명
        await page.wait_for_selector('input[placeholder="그룹명을 입력해주세요."]', timeout=5000)
        await page.locator('input[placeholder="그룹명을 입력해주세요."]').fill(f"자동화_{timestamp}")
        
        # 설명
        await page.locator('textarea[placeholder="설명을 입력해주세요."]').fill(f"자동화로 생성된 그룹입니다. (준일)")
        
        return page

    except Exception as e:
        print(f"필드 입력 중 오류 발생: {str(e)}")
        raise e

async def click_save(page: Page):
    try:
        # "추가" 버튼 클릭
        await page.locator('button.btn_point:has-text("추가")').first.click()

        # URL 패턴 대기
        await page.wait_for_url(url["common"]["group"]["finish"])

        # "닫기" 버튼 클릭
        await page.locator('button.btn:has-text("닫기")').first.click()

        return page

    except Exception as e:
        print(f"저장 버튼 클릭 중 오류 발생: {str(e)}")
        raise e

async def create_internal_group(page: Page):
    try:
        new_page = await access_create_group_service(page)
        new_page = await fill_field(new_page)
        new_page = await click_save(new_page)

        return {"status": "success", "message": "내부 그룹이 성공적으로 생성되었습니다."}

    except Exception as e:
        return {"status": "error", "message": f"내부 그룹 생성 중 오류 발생: {str(e)}"}