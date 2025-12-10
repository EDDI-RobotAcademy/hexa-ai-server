"""OpenAI 기반 메시지 변환 어댑터"""

import json
from openai import OpenAI

from app.converter.application.port.message_converter_port import MessageConverterPort
from app.converter.domain.tone_message import ToneMessage
from app.shared.vo.mbti import MBTI


class OpenAIMessageConverter(MessageConverterPort):
    """OpenAI API를 사용한 메시지 변환 구현체"""

    def __init__(self):
        """OpenAI 클라이언트 초기화"""
        self.client = OpenAI()

    def convert(
        self,
        original_message: str,
        sender_mbti: MBTI,
        receiver_mbti: MBTI,
        tone: str,
    ) -> ToneMessage:
        """메시지를 특정 톤으로 변환

        Args:
            original_message: 원본 메시지
            sender_mbti: 발신자 MBTI
            receiver_mbti: 수신자 MBTI
            tone: 변환할 톤

        Returns:
            ToneMessage: 변환된 메시지
        """
        prompt = self._build_prompt(original_message, sender_mbti, receiver_mbti, tone)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 MBTI 기반 커뮤니케이션 전문가입니다. 메시지를 지정된 톤으로 변환하고 JSON 형식으로 응답하세요.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        # JSON 응답 파싱
        content = response.choices[0].message.content
        result = json.loads(content)

        return ToneMessage(
            tone=tone, content=result["content"], explanation=result["explanation"]
        )

    def _build_prompt(
        self, original_message: str, sender_mbti: MBTI, receiver_mbti: MBTI, tone: str
    ) -> str:
        """프롬프트 생성

        Args:
            original_message: 원본 메시지
            sender_mbti: 발신자 MBTI
            receiver_mbti: 수신자 MBTI
            tone: 변환할 톤

        Returns:
            str: 생성된 프롬프트
        """
        return f"""다음 메시지를 '{tone}' 톤으로 변환해주세요.

발신자 MBTI: {sender_mbti.value}
수신자 MBTI: {receiver_mbti.value}
원본 메시지: {original_message}

수신자의 MBTI 특성을 고려하여 효과적으로 전달될 수 있도록 메시지를 변환하고,
왜 이 표현이 {receiver_mbti.value} 유형에게 효과적인지 설명해주세요.

JSON 형식으로 응답:
{{
    "content": "변환된 메시지",
    "explanation": "왜 이 표현이 효과적인지 설명 (2-3줄)"
}}"""
