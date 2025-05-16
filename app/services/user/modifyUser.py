# 다른 파일
from app.services.url.move_url import move_url_by_url
from app.services.security import url

async def access_user_detail(page, user_id):
    """
    사용자 상세 페이지 접근
    """

    # 검색바 열기 버튼 선택
    await page.wait_for_selector('button.btn_search', state='visible', timeout=10000)  # 버튼이 보이는 상태를 기다림
    await page.locator('button.btn_search').click()  # 버튼 클릭

    # 검색 바에 입력하기
    await page.wait_for_selector('#search_input', state='visible', timeout=10000)  # 검색 input 태그가 보이는 상태를 기다림
    await page.fill('#search_input', user_id)  # user_id 값을 검색 input에 입력

    # 엔터키 누르기
    await page.locator('#search_input').press('Enter')  
    
    # 검색 결과가 나타날 때까지 대기
    await page.wait_for_selector('div.lw_td.user_name', state='visible', timeout=10000)

    # 검색 결과 중 첫 번째 요소 선택 및 클릭
    await page.locator('div.lw_td.user_name').first.click()
    
    # "구성원 수정" 텍스트를 가진 버튼을 기다림
    await page.wait_for_selector('button.lw_btn_point:has-text("구성원 수정")', state='visible', timeout=10000)
    await page.locator('button.lw_btn_point:has-text("구성원 수정")').click()

    return page
    
async def process_modify_user(page, instance, server, app_state):
    """
    사용자 수정 프로세스
    """
    try:
        # 1. 어드민 > 구성원 페이지로 이동
        target_url = url[server][instance]["user"]
        await move_url_by_url(page, target_url)

        # 2. app.state에서 user_id 읽기
        user_id = app_state.global_user_id

        # 3. id값을 이용하여 구성원 상세 > 구성원 수정 접근
        page = await access_user_detail(page, user_id)
        
        # 성공 메시지 반환
        return {"status": "success", "message": "사용자 수정 완료"}

    except Exception as e:
        # 에러 메시지 반환
        return {"status": "error", "message": str(e)}