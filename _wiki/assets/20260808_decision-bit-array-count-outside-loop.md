---
summary: 에러 집계는 column 루프 밖에서 판정비트 배열 전체를 훑는다. 루프 안에서 세면 부분 스케줄이 성공으로 오판정된다
type: pattern
tags: [decoder, genie, schedule]
date: 2026-08-08
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/tasks/20260808_review/r3_round3_lv2_verification/team_b_verification.md`, `docs/profile/replacement_points.md`

### ㉮ 피해야 할 형태와 증상 (리뷰 시점 사실, 2026-08-08)

- 에러 집계가 column 루프 안에 있었다. `_column_order` 재정의로 일부 column만 방문하면 미방문 column의 에러가 집계에서 빠졌다
- 빈 스케줄에서 64/64 프레임이 success. column 하나 생략 시 49프레임 오판정
- 중복 방문은 이중 계상에 더해 remove old를 두 번 태워 복호 자체가 무너졌다

### ㉯ 처방 셋 비교

| 처방 | 본체 수치 | 오판정 | 비용 | 판정 |
|---|---|---|---|---|
| ㉠ 루프 뒤 flip 합산 | 보존 | 그대로 남음 | 0 | 반대 |
| ㉡ 루프 뒤 전 column 재계산 | 바뀜 (avg_iter, BER) | 0 | +7.8% | 반대. 미방문 column에 판정을 새로 만들어 스케줄 아이디어의 실제 동작을 감춘다 |
| ㉢ 판정비트 배열 (B, N_b, z) 지속과 루프 밖 집계 | 완전 보존 | 0 | -0.1%, 메모리 소폭 증가 | 채택. 원본 C++ `cwc[]` 구조와 같다 |

### ㉰ 패턴의 단계

- 1. 판정비트 배열을 상태로 둔다. 초기값은 read_bit 사본 (`src/decoder.py:267`)
- 2. column 처리는 자기 column의 판정비트만 갱신한다. `decision_bits[:, col, :] = read_bit[:, col, :] ^ flip` (`src/decoder.py:400-403`)
- 3. 집계는 column 루프가 끝난 뒤 배열 전체를 훑는다. `_collect_error_metrics` (`src/decoder.py:316-334`, 호출 `:365-368`)
- 4. 배치 압축 목록에 판정비트 배열을 넣는다 (`src/decoder.py:446`). SD restart처럼 루프를 건너뛰는 경로도 같은 집계 함수를 부른다 (`:356-357`)

### ㉱ 조건

- 교체 지점이 "방문 집합"을 바꿀 수 있으면 회계는 방문과 독립인 상태에서 계산한다
- 회계 수리가 디코더 동작(본체 수치)을 바꾸면 안 된다. 수리 3차 뒤 고정 입력 회귀로 완전 일치를 확인했다 (2026-08-09)
- 프로파일이 경계 규칙 ㉰로 등재했다 (`docs/profile/replacement_points.md:27`)

## 사용 방법

- 언제: 처리 순서나 방문 집합을 바꾸는 재정의(스케줄, 부분 갱신)를 허용하는 루프에 성공 판정이나 통계 집계가 붙어 있을 때
- 어떻게: "루프를 비워도 집계가 맞는가"를 시험한다. 빈 스케줄과 column 하나 생략 두 경우를 돌려 오판정 0을 확인한다
- 주의: ㉡처럼 집계 시점에 판정을 다시 만드는 처방은 오판정을 없애지만 아이디어의 실제 동작을 가린다. 회계는 관찰만 하고 상태를 만들지 않는다

관련 문서
- [20260930_genie-check-and-batch-compress.md](../tech/20260930_genie-check-and-batch-compress.md)
- [20260730_genie-check-and-all-zero-codeword.md](../decisions/20260730_genie-check-and-all-zero-codeword.md)
- [20260808_replacement-point-contract-protection.md](20260808_replacement-point-contract-protection.md)
- `../../docs/profile/replacement_points.md`
