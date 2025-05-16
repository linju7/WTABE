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

async def update_user_info(page, app_state):
    """
    사용자 정보 수정
    """

    # 성 (기본 필드)
    if await page.locator('input.lw_input[placeholder="성"][maxlength="80"]').count() > 0:
        current_value = await page.locator('input.lw_input[placeholder="성"][maxlength="80"]').input_value()
        await page.locator('input.lw_input[placeholder="성"][maxlength="80"]').fill(current_value + "(수정됨)")

    # 성 (다국어 필드)
    if await page.locator('input.lw_input[placeholder="성"][maxlength="100"]').count() > 0:
        current_value = await page.locator('input.lw_input[placeholder="성"][maxlength="100"]').input_value()
        await page.locator('input.lw_input[placeholder="성"][maxlength="100"]').fill(current_value + "(수정됨)")

    # 이름 (기본 필드)
    if await page.locator('input.lw_input[placeholder="이름"][maxlength="80"]').count() > 0:
        current_value = await page.locator('input.lw_input[placeholder="이름"][maxlength="80"]').input_value()
        await page.locator('input.lw_input[placeholder="이름"][maxlength="80"]').fill(current_value + "(수정됨)")

    # 이름 (다국어 필드)
    if await page.locator('input.lw_input[placeholder="이름"][maxlength="100"]').count() > 0:
        current_value = await page.locator('input.lw_input[placeholder="이름"][maxlength="100"]').input_value()
        await page.locator('input.lw_input[placeholder="이름"][maxlength="100"]').fill(current_value + "(수정됨)")

    # 다국어 필드 처리
    placeholders = [
        "姓(日本語)", "名(日本語)", "Last", "First",
        "姓(简体中文)", "名(简体中文)",
        "姓(繁體中文)", "名(繁體中文)"
    ]
    for placeholder in placeholders:
        if await page.locator(f'input.lw_input[placeholder="{placeholder}"]').count() > 0:
            current_value = await page.locator(f'input.lw_input[placeholder="{placeholder}"]').input_value()
            await page.locator(f'input.lw_input[placeholder="{placeholder}"]').fill(current_value + "(수정됨)")

    # 닉네임
    if await page.locator('input.lw_input[placeholder="닉네임"]').count() > 0:
        current_value = await page.locator('input.lw_input[placeholder="닉네임"]').input_value()
        await page.locator('input.lw_input[placeholder="닉네임"]').fill(current_value + "(수정됨)")

    # ID
    if await page.locator('input.lw_input[placeholder="ID"]').count() > 0:
        current_value = await page.locator('input.lw_input[placeholder="ID"]').input_value()
        await page.locator('input.lw_input[placeholder="ID"]').fill(current_value + "(수정됨)")

    # 보조 이메일
    if await page.locator('input.lw_input.email_id[placeholder="보조 이메일"]').count() > 0:
        current_value = await page.locator('input.lw_input.email_id[placeholder="보조 이메일"]').input_value()
        await page.locator('input.lw_input.email_id[placeholder="보조 이메일"]').fill(current_value + "modified")

    # 개인 이메일
    if await page.locator('input.lw_input[placeholder="개인 이메일"]').count() > 0:
        current_value = await page.locator('input.lw_input[placeholder="개인 이메일"]').input_value()
        await page.locator('input.lw_input[placeholder="개인 이메일"]').fill(current_value + "modified")

    # 사용자 유형, 직급, 사내번호, 전화번호, 근무처, 담당 업무, 사원 번호
    fields = [
        ("사내 번호", 'input.lw_input[placeholder="사내번호"]', '--'),
        ("전화번호", 'input.lw_input[placeholder="전화번호"]', '--'),
        ("근무처", 'input.lw_input[placeholder="근무처"]', '(수정됨)'),
        ("담당 업무", 'input.lw_input[placeholder="담당 업무"]', '(수정됨)'),
        ("사원 번호", 'input.lw_input[placeholder="사원 번호"]', '(수정됨)')
    ]
    for label, selector, suffix in fields:
        if await page.locator(selector).count() > 0:
            current_value = await page.locator(selector).input_value()
            await page.locator(selector).fill(current_value + suffix)

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

        # 4. 사용자 정보 수정
        page = await update_user_info(page, app_state)
        
        # 5. 수정 완료 버튼 클릭
        await page.locator('button.lw_btn_point:has-text("저장")').click()
        
        # 성공 메시지 반환
        return {"status": "success", "message": "사용자 수정 완료"}

    except Exception as e:
        # 에러 메시지 반환
        return {"status": "error", "message": str(e)}