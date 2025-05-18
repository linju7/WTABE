from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router

# FastAPI 애플리케이션 객체 정의
app = FastAPI()

# 애플리케이션 상태 초기화
app.state.global_page = None
app.state.global_user_id = None
app.state.global_domain = None
app.state.global_instance = None
app.state.global_server = None

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (필요에 따라 제한 가능)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 라우터 등록
app.include_router(router)