---
summary: argpartition으로 뽑은 앞 k개는 집합만 균일하고 내부 순서는 균일하지 않다. 결과를 구간 슬라이스로 나눠 쓰면 위치 편향이 생긴다
type: antipattern
tags: [rng, sampling, channel]
date: 2026-08-06
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/done/20260806_review/r3_round3_lv2_verification/team_a_verification.md`, `_pm/done/20260807_리뷰후속수정/20260807_리뷰후속수정.md`

### ㉮ 증상 (리뷰 시점 사실, 2026-08-06)

- strong_error 채널이 `argpartition` 결과의 앞부분을 strong 구간으로 잘라 썼다
- strong 위치 분포의 블록 카이제곱 약 244만(자유도 146). 상위 2개 column block 점유 36.7%. 프레임 간 strong 집합 교집합이 균일 기대의 48배

### ㉯ 원인

- 원본 `rand_sel_ep`는 부분 Fisher-Yates라 앞 k개의 순서까지 균일하고, 소비 측이 그 순서를 구간별로 잘라 쓴다
- Python `argpartition`(introselect)은 뽑힌 k개의 집합만 균일하다. 내부 순서는 알고리즘의 결정적 잔여라 그대로 자르면 특정 위치가 몰린다

### ㉰ 점검 항목

- ㉠ 부분 선택 결과는 "집합 전체를 같은 방식으로 쓰는" 경우에만 그대로 쓴다. 나눠 쓰려면 행별 독립 셔플 `rng.permuted(arr, axis=1)`을 거친다
- ㉡ `rng.permutation`과 `rng.shuffle`은 전 행에 같은 순열을 적용하므로 대체가 아니다
- ㉢ 셔플은 rng 상태를 소비한다. 공유 함수에 넣으면 다른 소비자(fixed_error)의 비트 단위 재현성이 깨진다. 필요한 채널 안에서만 적용한다
- ㉣ 분포 검정(블록 카이제곱, 교집합 크기)을 검증 도구로 쓴다. 눈으로는 안 보인다

### ㉱ 현재 코드 (수리된 위치)

- ㉠ `_rand_positions` docstring이 "집합 전체를 같은 방식으로 쓰는 경우 전용, 구간 슬라이스 금지"를 명시한다 (`src/channel.py:71-75`). fixed_error는 이 함수를 그대로 쓴다 (`:78-88`)
- ㉡ strong_error는 2단계 추출이다. 에러 위치 E개는 `argpartition`으로 집합만 뽑고, strong과 weak 배정은 `permuted`로 행별 셔플한 뒤 앞 `e2`개를 strong으로 남긴다. 정정 비트의 weak은 에러 위치를 2.0으로 막은 여집합에서 하위 `c1`개 (`src/channel.py:98-103, 119-133`)
- ㉢ 균일 순열의 앞 k개는 균일 부분집합과 분포가 같으므로 원본과 통계적으로 등가다 (사용자 확정 2026-08-07)

## 사용 방법

- 언제: `argpartition`, `argsort` 일부, 상위 k 선택 결과를 두 용도 이상으로 나눠 쓰려 할 때
- 어떻게: 결과를 나눠 쓰는 코드가 있으면 "이 순서가 균일한가"를 묻는다. 아니면 그 소비자 안에서만 `permuted(axis=1)`을 넣고, 다른 소비자의 고정 seed 회귀가 그대로인지 확인한다
- 주의: 수리 뒤 검증은 분포 검정으로 한다. 원문 전사 순열 검정과 블록 카이제곱을 함께 돌린 기록이 근거 문서에 있다

관련 문서
- [20260807_strong-error-two-stage-extraction.md](../decisions/20260807_strong-error-two-stage-extraction.md)
- [20260930_channel-models.md](../tech/20260930_channel-models.md)
- [20260808_equivalence-verification-methods.md](20260808_equivalence-verification-methods.md)
- [20260930_reusable-code-patterns.md](20260930_reusable-code-patterns.md)
