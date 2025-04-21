""" 
    createUser.py 알고리즘 
    1. 어드민 > 구성원 페이지로 이동 
    2. 구성원 추가 버튼 클릭
    3. 사용자 정보 입력
    4. 사용자 추가 버튼 클릭
    5. 사용자 추가 완료 확인
"""

from app.services.url.move_url import move_url_by_url
from app.services.security import url, accounts
from datetime import datetime

async def fill_user_info(page):
    """
    사용자 정보 입력
    """
    timestamp = datetime.now().strftime("%m%d%H%M")

    # 모든 항목 표시 버튼 클릭
    await page.wait_for_selector('button.opt_toggle.fold', state='visible', timeout=5000)  # await 추가
    button = page.locator('button.opt_toggle.fold')
    is_visible = await button.is_visible()  # await 추가
    if is_visible:
        await button.click()  # await 추가

    # 성
    await page.wait_for_selector('input.lw_input[placeholder="성"][maxlength="80"]', timeout=5000)  # await 추가
    await page.locator('input.lw_input[placeholder="성"][maxlength="80"]').fill("자동화_")  # await 추가

    # 이름
    await page.locator('input.lw_input[placeholder="이름"][maxlength="80"]').fill(timestamp)  # await 추가

    # 다국어
    # 다국어 off 시 입력란이 없기 때문에, 조건문으로 존재하는지 체크를 하는 로직 추가함
    if await page.locator('input.lw_input[placeholder="姓(日本語)"]').count() > 0:  # await 추가
        await page.locator('input.lw_input[placeholder="姓(日本語)"]').fill("일본어성")  # await 추가
    if await page.locator('input.lw_input[placeholder="名(日本語)"]').count() > 0:  # await 추가
        await page.locator('input.lw_input[placeholder="名(日本語)"]').fill("일본어이름")  # await 추가
    if await page.locator('input.lw_input[placeholder="Last"]').count() > 0:  # await 추가
        await page.locator('input.lw_input[placeholder="Last"]').fill("영어성")  # await 추가
    if await page.locator('input.lw_input[placeholder="First"]').count() > 0:  # await 추가
        await page.locator('input.lw_input[placeholder="First"]').fill("영어이름")  # await 추가
    if await page.locator('input.lw_input[placeholder="성"][maxlength="100"]').count() > 0:  # await 추가
        await page.locator('input.lw_input[placeholder="성"][maxlength="100"]').fill("한국어성")  # await 추가
    if await page.locator('input.lw_input[placeholder="이름"][maxlength="100"]').count() > 0:  # await 추가
        await page.locator('input.lw_input[placeholder="이름"][maxlength="100"]').fill("한국어이름")  # await 추가
    if await page.locator('input.lw_input[placeholder="姓(简体中文)"]').count() > 0:  # await 추가
        await page.locator('input.lw_input[placeholder="姓(简体中文)"]').fill("번체성")  # await 추가
    if await page.locator('input.lw_input[placeholder="名(简体中文)"]').count() > 0:  # await 추가
        await page.locator('input.lw_input[placeholder="名(简体中文)"]').fill("번체이름")  # await 추가
    if await page.locator('input.lw_input[placeholder="姓(繁體中文)"]').count() > 0:  # await 추가
        await page.locator('input.lw_input[placeholder="姓(繁體中文)"]').fill("간체성")  # await 추가
    if await page.locator('input.lw_input[placeholder="名(繁體中文)"]').count() > 0:  # await 추가
        await page.locator('input.lw_input[placeholder="名(繁體中文)"]').fill("간체이름")  # await 추가

    # 닉네임
    await page.locator('input.lw_input[placeholder="닉네임"]').fill("자동화_닉네임")  # await 추가

    # ID
    await page.locator('input.lw_input[placeholder="ID"]').fill(f"junil_{timestamp}")  # await 추가

    # 사용자 유형 1번째 선택
    user_type_select = page.locator("//div[i[text()='사용자 유형']]//select[@id='member_type']")
    first_value = await user_type_select.locator('option').nth(1).get_attribute('value')  # await 추가
    await user_type_select.select_option(value=first_value)  # await 추가

    # 직급 1번째 선택
    user_type_select = page.locator("//div[i[text()='직급']]//select[@id='member_type']")
    first_value = await user_type_select.locator('option').nth(1).get_attribute('value')  # await 추가
    await user_type_select.select_option(value=first_value)  # await 추가

    # 사내번호
    await page.locator('input.lw_input[placeholder="사내 번호"]').fill(f"P-{timestamp}")  # await 추가

    # 전화번호
    await page.locator('input.lw_input[placeholder="전화번호"]').fill(f"T-{timestamp}")  # await 추가

    # 보조 이메일
    await page.locator('button.generate', has_text="보조 이메일 추가").click()  # await 추가
    await page.wait_for_selector('input.lw_input.email_id[placeholder="보조 이메일"]', timeout=5000)  # await 추가
    await page.locator('input.lw_input.email_id[placeholder="보조 이메일"]').fill(f"sub_email_{timestamp}")  # await 추가

    # 개인 이메일
    await page.locator('input.lw_input[placeholder="개인 이메일"]').fill(f"private_email_{timestamp}")  # await 추가
    await page.locator('input.lw_input[placeholder="직접 입력"]').fill(f"private.domain")  # await 추가

    # 사용 언어 한국어 선택
    await page.locator('select#language_type').select_option(label="Korean")  # await 추가

    # 근무처
    await page.locator('input.lw_input[placeholder="근무처"]').fill(f"자동화_근무처")  # await 추가

    # 담당 업무
    await page.locator('input.lw_input[placeholder="담당 업무"]').fill(f"자동화_담당업무")  # await 추가

    # 생일
    await page.locator('input.lw_input[name="birthday"]').fill("1999. 12. 31")  # await 추가

    # 입사일
    await page.locator('input.lw_input[name="hiredDate"]').fill("2000. 01. 01")  # await 추가

    # 사원 번호
    await page.locator('input.lw_input[placeholder="사원 번호"]').fill(f"자동화_{timestamp}")  # await 추가

    return page

async def process_create_user(page, instance, server):
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
        page = await fill_user_info(page)

        # 4. 사용자 추가 버튼 클릭
        await page.locator('button.lw_btn_point:text-is("추가")').click()
        await page.locator('button.lw_btn:text-is("확인")').click()

        # 성공 메시지 반환
        return {"status": "success", "message": "사용자 생성 완료"}

    except Exception as e:
        # 에러 메시지 반환
        return {"status": "error", "message": str(e)}