# Plan: MBTI 관계 솔루션 서비스 (Phase 1 MVP)

## 아키텍처 개요

핵사고날 아키텍처 (Hexagonal Architecture)

```
app/
├── consult/                    # 상담 도메인
│   ├── domain/
│   ├── application/
│   └── adapter/
├── converter/                  # 변환기 도메인
│   ├── domain/
│   ├── application/
│   └── adapter/
└── shared/                     # 공통 모듈 (MBTI, Gender)
```

---

## Backlog

### MBTI/성별 값 객체

- [x] `HAIS-1` [Shared] MBTI 값 객체 생성 - "INTJ" 형식의 유효한 4글자 조합만 허용
- [x] `HAIS-2` [Shared] MBTI 유효성 검증 - "XXXX", "INXX" 등 유효하지 않은 값 거부
- [x] `HAIS-3` [Shared] MBTI 차원별 조회 - E/I, S/N, T/F, J/P 각각 개별 접근 가능
- [ ] `HAIS-4` [Shared] 성별 값 객체 생성 - MALE, FEMALE 두 가지 값만 허용
- [ ] `HAIS-5` [Shared] 성별 유효성 검증 - 유효하지 않은 성별 값 거부

### 사용자 프로필

- [ ] `HAIS-6` [Shared] 사용자 프로필 생성 - 성별과 MBTI를 담은 프로필 객체 생성
- [ ] `HAIS-7` [Shared] 사용자 프로필 필수값 검증 - 성별 또는 MBTI 누락 시 생성 거부

### 상담 세션

- [ ] `HAIS-8` [Consult] 상담 세션 생성 - 각 상담을 구분하는 고유 ID 부여
- [ ] `HAIS-9` [Consult] 상담 세션에 프로필 연결 - 세션 생성 시 사용자 프로필 저장
- [ ] `HAIS-10` [Consult] 상담 세션 초기화 - 빈 대화 목록으로 세션 시작

### 대화 메시지

- [ ] `HAIS-11` [Consult] 대화 메시지 생성 - AI/USER 역할 구분과 메시지 내용 저장
- [ ] `HAIS-12` [Consult] 대화 메시지 추가 - 세션에 새 메시지 순차 추가
- [ ] `HAIS-13` [Consult] 대화 히스토리 조회 - 분석을 위해 전체 대화 내역 반환

### 턴 카운트

- [ ] `HAIS-14` [Consult] 턴 카운트 계산 - 사용자가 보낸 메시지 수 집계
- [ ] `HAIS-15` [Consult] 잔여 턴 반환 - "2턴 남음" 표시를 위한 잔여 횟수 계산
- [ ] `HAIS-16` [Consult] 턴 제한 도달 감지 - 3턴 완료 시 분석 단계로 전환 트리거

### AI 상담사 응답

- [ ] `HAIS-17` [Consult] AI 인사 메시지 생성 - "어떤 관계 고민이 있으세요?" 첫 메시지
- [ ] `HAIS-18` [Consult] AI 대화 응답 생성 - 사용자 메시지에 공감하며 질문하는 응답
- [ ] `HAIS-19` [Consult] AI MBTI 맞춤 응답 - 사용자 MBTI 특성 고려한 응답 생성

### 상담 시작 유스케이스

- [ ] `HAIS-20` [Consult] 상담 시작 세션 생성 - 프로필 받아 새 세션 생성
- [ ] `HAIS-21` [Consult] 상담 시작 인사 포함 - 세션 생성과 동시에 AI 인사 메시지 추가
- [ ] `HAIS-22` [Consult] 상담 시작 세션 ID 반환 - 이후 대화에 사용할 세션 ID 응답

### 메시지 전송 유스케이스

- [ ] `HAIS-23` [Consult] 메시지 전송 저장 - 전송된 메시지를 세션에 기록
- [ ] `HAIS-24` [Consult] 메시지 전송 AI 응답 트리거 - 메시지 저장 후 자동으로 AI 응답 요청
- [ ] `HAIS-25` [Consult] 메시지 전송 턴 정보 포함 - AI 응답과 함께 남은 대화 횟수 반환
- [ ] `HAIS-26` [Consult] 메시지 전송 턴 초과 차단 - 3턴 완료 후 추가 메시지 거부

### 분석 결과

- [ ] `HAIS-27` [Consult] 분석 결과 상황 분석 섹션 - 대화 내용 종합 및 핵심 갈등 원인 도출
- [ ] `HAIS-28` [Consult] 분석 결과 유형별 특성 섹션 - 사용자/상대방 MBTI 특성 및 차이점
- [ ] `HAIS-29` [Consult] 분석 결과 해결 방안 섹션 - 우선순위별 실행 가능한 액션 3-5개
- [ ] `HAIS-30` [Consult] 분석 결과 주의사항 섹션 - 피해야 할 말/행동 및 역효과 가능성
- [ ] `HAIS-31` [Consult] 분석 결과 대화 기반 생성 - 전체 대화 내용을 활용해 맞춤 분석

### 상담 API

- [ ] `HAIS-32` [Consult] 상담 API 시작 엔드포인트 - POST /consult/start → 201 응답
- [ ] `HAIS-33` [Consult] 상담 API 메시지 엔드포인트 - POST /consult/{id}/message → 200 응답
- [ ] `HAIS-34` [Consult] 상담 API SSE 스트리밍 - AI 응답을 글자 단위 실시간 전송
- [ ] `HAIS-35` [Consult] 상담 API 분석 조회 엔드포인트 - GET /consult/{id}/analysis → 200 응답
- [ ] `HAIS-36` [Consult] 상담 API 분석 미완료 처리 - 3턴 미완료 시 404 반환

### 메시지 변환 도메인

- [ ] `HAIS-37` [Converter] 톤 메시지 생성 - 톤별 메시지 내용을 담는 도메인 모델
- [ ] `HAIS-38` [Converter] 톤 메시지 해설 포함 - "왜 이 표현이 효과적인가" 설명 추가
- [ ] `HAIS-39` [Converter] 공손한 톤 메시지 생성 - 격식, 존댓말, 완곡 표현 버전
- [ ] `HAIS-40` [Converter] 캐주얼 톤 메시지 생성 - 친근한 대화체, 자연스러운 버전
- [ ] `HAIS-41` [Converter] 간결한 톤 메시지 생성 - 핵심만, 결론부터 전달하는 버전

### 메시지 변환 유스케이스

- [ ] `HAIS-42` [Converter] 메시지 변환 발신자 MBTI 반영 - 내 성향에 맞는 표현 방식 적용
- [ ] `HAIS-43` [Converter] 메시지 변환 수신자 MBTI 반영 - 상대방이 잘 받아들이는 표현
- [ ] `HAIS-44` [Converter] 메시지 변환 3가지 톤 동시 생성 - 공손/캐주얼/간결 모두 반환

### 변환기 API

- [ ] `HAIS-45` [Converter] 변환기 API 변환 엔드포인트 - POST /converter/convert → 200 응답
- [ ] `HAIS-46` [Converter] 변환기 API MBTI 검증 - 잘못된 MBTI 형식 시 400 에러
- [ ] `HAIS-47` [Converter] 변환기 API 내용 길이 검증 - 20-500자 위반 시 400 에러

### 통합 테스트

- [ ] `HAIS-48` [E2E] 상담 전체 플로우 검증 - 시작 → 3턴 대화 → 분석 결과까지 연결
- [ ] `HAIS-49` [E2E] 변환 전체 플로우 검증 - 입력 → 3가지 톤 결과 반환까지 연결