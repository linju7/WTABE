async def process_logout(state) -> dict:
    """
    로그아웃 프로세스를 처리하는 함수
    """
    try:
        if hasattr(state, "global_page") and state.global_page:
            # 페이지 닫기
            await state.global_page.close()
            state.global_page = None
            print("로그아웃 성공: 페이지가 닫혔습니다.")
            return {"status": "success", "message": "로그아웃 성공"}
        else:
            print("로그아웃 실패: 열려 있는 페이지가 없습니다.")
            return {"status": "error", "message": "열려 있는 페이지가 없습니다."}

    except Exception as e:
        print(f"로그아웃 중 오류 발생: {e}")
        return {"status": "error", "message": str(e)}