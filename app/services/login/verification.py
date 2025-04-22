from app.services.security import verification_code

async def process_verification(password: str) -> dict:
    """
    보안 코드와 입력된 비밀번호를 비교하는 함수
    """
    try:
        # 보안 코드와 입력된 비밀번호 비교
        if password == verification_code:
            return {"status": "success", "message": "비밀번호가 일치합니다."}
        else:
            return {"status": "error", "message": "비밀번호가 일치하지 않습니다."}
    except Exception as e:
        return {"status": "error", "message": f"오류 발생: {str(e)}"}