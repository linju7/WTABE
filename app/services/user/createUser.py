""" 
    createUser.py 알고리즘 
    1. 어드민 > 구성원 페이지로 이동 
    2. 구성원 추가 버튼 클릭
    3. 사용자 정보 입력
    4. 사용자 추가 버튼 클릭
    5. 사용자 추가 완료 확인
"""

from app.services.url.move_url import move_url_by_url
from app.services.security import url
from datetime import datetime

async def fill_user_info(page, app_state):
    """
    사용자 정보 입력
    """
    timestamp = datetime.now().strftime("%m%d%H%M")
    user_id = "junil_" + timestamp

    # app.state에 user_id 저장
    app_state.global_user_id = user_id

    # 모든 항목 표시 버튼 클릭
    await page.wait_for_selector('button.opt_toggle.fold', state='visible', timeout=5000)
    button = page.locator('button.opt_toggle.fold')
    if await button.is_visible():
        await button.click()

    # 기본 필드 입력
    basic_fields = [
        ("성", 'input.lw_input[placeholder="성"][maxlength="80"]', "자동화_"),
        ("이름", 'input.lw_input[placeholder="이름"][maxlength="80"]', timestamp),
        ("닉네임", 'input.lw_input[placeholder="닉네임"]', "자동화_닉네임"),
        ("ID", 'input.lw_input[placeholder="ID"]', user_id),
        ("사내 번호", 'input.lw_input[placeholder="사내 번호"]', f"P-{timestamp}"),
        ("전화번호", 'input.lw_input[placeholder="전화번호"]', f"T-{timestamp}"),
        ("근무처", 'input.lw_input[placeholder="근무처"]', "자동화_근무처"),
        ("담당 업무", 'input.lw_input[placeholder="담당 업무"]', "자동화_담당업무"),
        ("사원 번호", 'input.lw_input[placeholder="사원 번호"]', f"자동화_{timestamp}"),
        ("생일", 'input.lw_input[name="birthday"]', "1999. 12. 31"),
        ("입사일", 'input.lw_input[name="hiredDate"]', "2000. 01. 01")
    ]
    for label, selector, value in basic_fields:
        if await page.locator(selector).count() > 0:
            await page.locator(selector).fill(value)
            
    # 사용자 유형 1번째 선택
    user_type_select = page.locator("//div[i[text()='사용자 유형']]//select[@id='member_type']")
    first_value = await user_type_select.locator('option').nth(1).get_attribute('value')
    await user_type_select.select_option(value=first_value)

    # 직급 1번째 선택
    user_type_select = page.locator("//div[i[text()='직급']]//select[@id='member_type']")
    first_value = await user_type_select.locator('option').nth(1).get_attribute('value')
    await user_type_select.select_option(value=first_value)

    # 다국어 필드 입력
    multilingual_fields = [
        ("姓(日本語)", "일본어성"),
        ("名(日本語)", "일본어이름"),
        ("Last", "영어성"),
        ("First", "영어이름"),
        ("성", "한국어성", 'maxlength="100"'),
        ("이름", "한국어이름", 'maxlength="100"'),
        ("姓(简体中文)", "번체성"),
        ("名(简体中文)", "번체이름"),
        ("姓(繁體中文)", "간체성"),
        ("名(繁體中文)", "간체이름")
    ]
    for placeholder, value, *extra in multilingual_fields:
        selector = f'input.lw_input[placeholder="{placeholder}"]'
        if extra:
            selector += f'[{extra[0]}]'
        if await page.locator(selector).count() > 0:
            await page.locator(selector).fill(value)



    # 보조 이메일 추가
    await page.locator('button.generate', has_text="보조 이메일 추가").click()
    await page.wait_for_selector('input.lw_input.email_id[placeholder="보조 이메일"]', timeout=5000)
    await page.locator('input.lw_input.email_id[placeholder="보조 이메일"]').fill(f"sub_email_{timestamp}")

    # 개인 이메일 입력
    await page.locator('input.lw_input[placeholder="개인 이메일"]').fill(f"private_email_{timestamp}")
    await page.locator('input.lw_input[placeholder="직접 입력"]').fill("private.domain")

    return page

async def process_create_user(page, instance, server, app_state):
    """
    사용자 생성 프로세스
    """
    try:
        # 1. 어드민 > 구성원 페이지로 이동
        target_url = url[server][instance]["user"]
        await move_url_by_url(page, target_url)

        # 2. 구성원 추가 버튼 클릭
        await page.locator('button.lw_btn_point:text-is("구성원 추가")').click()

        # 3. 사용자 정보 입력
        page = await fill_user_info(page, app_state)

        # 4. 사용자 추가 버튼 클릭
        await page.locator('button.lw_btn_point:text-is("추가")').click()
        await page.locator('button.lw_btn:text-is("확인")').click()

        # 성공 메시지 반환
        return {"status": "success", "message": "사용자 생성 완료"}

    except Exception as e:
        # 에러 메시지 반환
        return {"status": "error", "message": str(e)}