"""Converter Router API 테스트"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.converter.domain.tone_message import ToneMessage
from app.shared.vo.mbti import MBTI


@pytest.fixture
def test_app():
    """FastAPI 앱 인스턴스"""
    from app.converter.adapter.input.web.converter_router import converter_router

    app = FastAPI()
    app.include_router(converter_router, prefix="/converter")
    return app


@pytest.fixture
def client(test_app):
    """FastAPI 테스트 클라이언트"""
    return TestClient(test_app)


@pytest.fixture
def mock_converter():
    """Mock MessageConverter"""
    converter = Mock()
    converter.convert.return_value = ToneMessage(
        tone="공손한",
        content="안녕하세요, 내일 회의 시간을 조정해주실 수 있을까요?",
        explanation="ESTP 유형에게는 직설적이면서도 존중하는 표현이 효과적입니다.",
    )
    return converter


class TestConverterRouter:
    """Converter Router 테스트"""

    @patch("app.converter.adapter.input.web.converter_router.OpenAIMessageConverter")
    def test_should_convert_message_with_valid_request(
        self, mock_converter_class, client, mock_converter
    ):
        """유효한 요청으로 메시지를 변환할 수 있어야 함"""
        # Given
        mock_converter_class.return_value = mock_converter

        request_body = {
            "original_message": "내일 회의 시간 바꿀 수 있어?",
            "sender_mbti": "INTJ",
            "receiver_mbti": "ESTP",
            "tone": "공손한",
        }

        # When
        response = client.post("/converter/convert", json=request_body)

        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["tone"] == "공손한"
        assert data["content"] == "안녕하세요, 내일 회의 시간을 조정해주실 수 있을까요?"
        assert "ESTP" in data["explanation"]

    @patch("app.converter.adapter.input.web.converter_router.OpenAIMessageConverter")
    def test_should_reject_invalid_mbti(self, mock_converter_class, client):
        """잘못된 MBTI는 거부해야 함"""
        # Given
        request_body = {
            "original_message": "안녕",
            "sender_mbti": "INVALID",
            "receiver_mbti": "ESTP",
            "tone": "공손한",
        }

        # When
        response = client.post("/converter/convert", json=request_body)

        # Then
        assert response.status_code == 422  # Validation error

    @patch("app.converter.adapter.input.web.converter_router.OpenAIMessageConverter")
    def test_should_reject_empty_message(self, mock_converter_class, client):
        """빈 메시지는 거부해야 함"""
        # Given
        request_body = {
            "original_message": "",
            "sender_mbti": "INTJ",
            "receiver_mbti": "ESTP",
            "tone": "공손한",
        }

        # When
        response = client.post("/converter/convert", json=request_body)

        # Then
        assert response.status_code == 422  # Validation error

    @patch("app.converter.adapter.input.web.converter_router.OpenAIMessageConverter")
    def test_should_call_converter_with_correct_parameters(
        self, mock_converter_class, client, mock_converter
    ):
        """올바른 파라미터로 converter를 호출해야 함"""
        # Given
        mock_converter_class.return_value = mock_converter

        request_body = {
            "original_message": "테스트 메시지",
            "sender_mbti": "INTJ",
            "receiver_mbti": "ESTP",
            "tone": "캐주얼한",
        }

        # When
        client.post("/converter/convert", json=request_body)

        # Then
        mock_converter.convert.assert_called_once()
        call_args = mock_converter.convert.call_args
        assert call_args.kwargs["original_message"] == "테스트 메시지"
        assert call_args.kwargs["sender_mbti"].value == "INTJ"
        assert call_args.kwargs["receiver_mbti"].value == "ESTP"
        assert call_args.kwargs["tone"] == "캐주얼한"
