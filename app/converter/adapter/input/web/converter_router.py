"""Converter Router"""

from fastapi import APIRouter, status

from app.converter.adapter.input.web.request.convert_request import ConvertRequest
from app.converter.adapter.input.web.response.convert_response import ConvertResponse
from app.converter.infrastructure.service.openai_message_converter import (
    OpenAIMessageConverter,
)
from app.shared.vo.mbti import MBTI

converter_router = APIRouter()


@converter_router.post(
    "/convert",
    response_model=ConvertResponse,
    status_code=status.HTTP_200_OK,
    summary="메시지 변환",
    description="원본 메시지를 특정 톤으로 변환합니다 (MBTI 기반)",
)
def convert_message(request: ConvertRequest) -> ConvertResponse:
    """메시지를 특정 톤으로 변환

    Args:
        request: 변환 요청 (원본 메시지, MBTI, 톤)

    Returns:
        ConvertResponse: 변환된 메시지
    """
    # MessageConverter 인스턴스 생성
    converter = OpenAIMessageConverter()

    # MBTI 값 객체 생성
    sender_mbti = MBTI(request.sender_mbti)
    receiver_mbti = MBTI(request.receiver_mbti)

    # 메시지 변환
    tone_message = converter.convert(
        original_message=request.original_message,
        sender_mbti=sender_mbti,
        receiver_mbti=receiver_mbti,
        tone=request.tone,
    )

    # 응답 DTO로 변환
    return ConvertResponse.from_domain(tone_message)
