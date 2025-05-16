from app.services.url.move_url import move_url_by_url
from app.services.security import url
from app.services.security import access_token
import httpx

async def retreive_user_ui(page, instance, server, app_state):
    """
    구성원 조직도 팝업에서 사용자 정보를 추출하는 함수
    """
    # 구성원 조직도 팝업 URL 생성
    base_url = "https://"
    if server != "real":
        base_url += f"{server}."
    base_url += url["user"]["popup"]
    
    # app_state에서 global_user_id 가져오기
    keyword = app_state.global_user_id + app_state.global_domain
    popup_url = f"{base_url}?keyword={keyword}"
    
    await move_url_by_url(page, popup_url)
    
    # 팝업 페이지에서 데이터 추출
    ui_data = {
        "이름": await page.locator("div.profile_area strong").text_content(),
        "닉네임": await page.locator("div.profile_area p.txt.nickname span").text_content(),
        "직급": await page.locator("div.profile_area p.txt").nth(1).text_content(),
        "다국어명": await page.locator("div.profile_area p.txt.global_name").text_content(),
        "사내번호": await page.locator("ul.infor_list li:has(span.tit:has-text('전화')) p").nth(0).text_content(),
        "전화번호": await page.locator("ul.infor_list li:has(span.tit:has-text('전화')) p").nth(1).text_content(),
        "이메일": await page.locator("ul.infor_list li:has(span.tit:has-text('이메일')) p a").nth(0).text_content(),
        "개인이메일": await page.locator("ul.infor_list li:has(span.tit:has-text('이메일')) p a").nth(1).text_content(),
        "근무처": await page.locator("ul.infor_list li:has(span.tit:has-text('근무처')) p").text_content(),
        "담당업무": await page.locator("ul.infor_list li:has(span.tit:has-text('담당업무')) p").text_content(),
        "생일": await page.locator("ul.infor_list li:has(span.tit:has-text('생일')) p").text_content(),
        "입사일": await page.locator("ul.infor_list li:has(span.tit:has-text('입사일')) p").text_content(),
        "사원번호": await page.locator("ul.infor_list li:has(span.tit:has-text('사원 번호')) p").text_content(),
    }

    # 닉네임에서 양 끝의 [] 제거
    ui_data["닉네임"] = ui_data["닉네임"].strip("[]")

    # 생일과 입사일 날짜 형식 조정 및 "양력" 제거
    ui_data["생일"] = ui_data["생일"].replace(".", "-").replace("(양력)", "").strip()
    ui_data["입사일"] = ui_data["입사일"].replace(".", "-").strip()

    return ui_data


async def call_retreive_user_api(app_state):
    """
    사용자 조회 API 호출 및 데이터 추출
    """
    # 조회할 ID와 엑세스 토큰 가져오기
    user_id = app_state.global_user_id + app_state.global_domain
    

    # API URL 구성
    api_url = f"https://www.worksapis.com/v1.0/users/{user_id}"

    # HTTP 요청 헤더 설정
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        # HTTP GET 요청 보내기
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)

        # 응답 결과 반환
        if response.status_code == 200:
            api_response = response.json()

            # 필요한 데이터 추출
            api_data = {
                "이름": f"{api_response['userName'].get('lastName', '')}{api_response['userName'].get('firstName', '')}",
                "닉네임": api_response.get('nickName', ''),
                "직급": api_response['organizations'][0].get('levelName', '') if api_response.get('organizations') else '',
                "다국어명": " / ".join(
                    [
                        f"{name.get('lastName', '')}{name.get('firstName', '')}"
                        for name in api_response.get('i18nNames', [])
                    ]
                ),
                "사내번호": api_response.get('telephone', ''),
                "전화번호": api_response.get('cellPhone', ''),
                "이메일": api_response.get('email', ''),
                "개인이메일": api_response.get('privateEmail', ''),
                "근무처": api_response.get('location', ''),
                "담당업무": api_response.get('task', ''),
                "생일": api_response.get('birthday', ''),
                "입사일": api_response.get('hiredDate', ''),
                "사원번호": api_response.get('employeeNumber', ''),
            }
            return {"status": "success", "data": api_data}
        else:
            return {"status": "error", "message": f"HTTP {response.status_code}: {response.text}"}

    except Exception as e:
        # 예외 처리
        return {"status": "error", "message": str(e)}
    
async def compare_user_data(popup_data, api_data):
    """
    팝업 페이지 데이터와 API 데이터를 비교하여 불일치 항목과 일치 여부 반환
    """
    mismatched_fields = []  # 불일치한 항목을 저장할 리스트
    all_match = True  # 모든 값이 일치하는지 확인하기 위한 플래그

    for key in popup_data.keys():
        # 공백 제거 후 비교
        popup_value = popup_data.get(key, '').strip()
        api_value = api_data.get(key, '').strip()

        if popup_value != api_value:
            # 불일치한 항목의 키를 저장
            mismatched_fields.append(key)
            all_match = False  # 불일치가 하나라도 있으면 플래그를 False로 설정

    return mismatched_fields, all_match

async def process_retreive_user(page, instance, server, app_state):
    """
    사용자 조회 프로세스
    """
    try:
        # 1. 구성원 조직도 팝업에서 데이터 추출 
        popup_data = await retreive_user_ui(page, instance, server, app_state)

        # 2. API로 사용자 정보 조회 및 데이터 추출
        api_response = await call_retreive_user_api(app_state)
        if api_response["status"] != "success":
            # API 호출 실패 시 에러 메시지 반환
            return {"status": "error", "message": api_response["message"]}

        # API 데이터 추출
        api_data = api_response["data"]
        
        # 3. UI 데이터와 API 데이터 비교
        mismatched_fields, all_match = await compare_user_data(popup_data, api_data)

        # 4. 결과 반환
        if all_match:
            return {"status": "success", "message": "모든 값이 일치합니다."}
        else:
            mismatched_fields_str = ", ".join(mismatched_fields)
            return {"status": "error", "message": f"불일치한 항목: {mismatched_fields_str}"}

    except Exception as e:
        # 예외 처리 및 에러 메시지 반환
        return {"status": "error", "message": str(e)}