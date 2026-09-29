---
summary: 한 난수 생성기를 메시지와 잡음이 공유하고 종료 검사가 배치 단위라 frames_per_batch가 같은 seed의 수치를 바꾼다. 코드 수리 없이 문언 교정으로 종결
type: antipattern
tags: [rng, reproducibility, batch]
date: 2026-08-08
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/tasks/20260808_review/r3_round3_lv2_verification/team_b_verification.md`, `_pm/tasks/20260808_review/종합보고.md`

### ㉮ 증상 (리뷰 시점 사실, 2026-08-08)

- 같은 seed에서 `frames_per_batch` 128과 64가 FER 3.867e-1 대 3.750e-1로 갈렸다
- FER가 포화된 구간에서도 BER과 실패 프레임 상세는 배치 크기에 따라 달랐다

### ㉯ 원인 (두 겹)

- ㉠ 배치마다 `generate_message`가 `batch * K`개 난수를 먼저 소비하고 `encode`는 그 값을 버린다. 배치 경계가 바뀌면 잡음 난수의 위치가 밀린다
- ㉡ 난수를 완전히 정렬해도 `max_frame_errors` 종료 검사가 배치 단위라 종료 프레임 수가 배치 배수로 양자화된다
- ㉢ strong_error는 한 채널 함수 안에서 소비자 둘(`random`, `permuted`)을 섞어 써서 배치 분해가 안 된다

### ㉰ 점검 항목

- ㉠ "결과에 영향 없음"을 단언하기 전에 두 배치 크기로 end-to-end 실측한다
- ㉡ 스트림을 분리하려면 프레임 단위 파생(비용 1.0배)이 채널 3종 전부에 성립하는 유일한 안이다. "쓸모없는 호출 제거"는 실물 인코더가 들어오면 재발한다
- ㉢ 종료 규칙의 검사 단위(배치 대 프레임)도 재현성 계약에 포함해 문서에 적는다

### ㉱ 처리와 현재 코드

- 처리: 코드 수리 없이 문언 교정으로 종결했다 (2026-08-09 사용자 확정). 두 실행 모두 편향 없는 표본이라 프레임 수가 충분하면 같은 FER로 수렴하고, on/off 비교는 같은 config로 돌리므로 영향이 없다
- 교정된 문언: "통계 결과는 프레임 수가 충분하면 같고, 같은 seed 수치 재현에는 이 값까지 같아야 한다" (`src/run.py:58-59`, `docs/profile/overview.md:20`)
- 구조는 그대로다. 채널 함수 하나가 메시지 생성, 인코딩, 채널에 같은 생성기를 넘기고 (`src/run.py:524-528`), 종료 검사는 배치 루프 조건이며 (`src/sim.py:95-96`), strong_error는 `random`과 `permuted`를 함께 쓴다 (`src/channel.py:119-133`)

## 사용 방법

- 언제: 재현성 결함의 심각도를 매길 때, 배치 크기나 병렬 분할을 바꾼 결과를 이전 실행과 비교할 때
- 어떻게: 심각도는 "통계 결론을 바꾸는가"로 판정한다. 바꾸지 않으면 비트 단위 재현 조건(seed와 `frames_per_batch` 동일)을 계약으로 문서화하는 것으로 충분할 수 있다
- 주의: 회귀 비교와 on/off 비교는 seed와 `frames_per_batch`까지 같은 config로 돌린다. 이 조건을 어긴 수치 차이는 결함 근거가 아니다

관련 문서
- [20260807_single-seed-derived-streams.md](../decisions/20260807_single-seed-derived-streams.md)
- [20260930_channels-section-and-experiment-loop.md](../tech/20260930_channels-section-and-experiment-loop.md)
- [20260930_reusable-code-patterns.md](20260930_reusable-code-patterns.md)
