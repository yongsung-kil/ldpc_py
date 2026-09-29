---
summary: 파일에 없는 정보(VNU 출력 레벨)를 파일명 부분문자열로 정하면 오탐과 무경고 오답이 생긴다. 판정은 파일 내용의 값 패턴으로 한다
type: antipattern
tags: [llr-matrix, filename, loader]
date: 2026-08-09
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/tasks/20260808_review/종합보고.md`, `_pm/tasks/20260808_review/r3_round3_lv2_verification/team_a_verification.md`

### ㉮ 증상 (리뷰 시점 사실, 2026-08-08)

- ㉠ 로더가 `"uniform" in basename` 검사로 레벨 구성을 골랐다. `nonuniform`, `uniformity` 같은 이름도 균일로 오탐했다
- ㉡ 같은 파일을 이름만 바꿔 로드하니 FER 0.8906 대 0.9688. 예외와 경고 0건
- ㉢ 반대 방향도 조용했다. 3-bit 생성 파일 이름에서 `uniform`을 지우면 th 3개 검사를 통과해 레벨이 `[3,2,1,0]`에서 `[7,5,3,1]`로 바뀐 채 완주했다

### ㉯ 원인

- LLR_MATRIX 파일 포맷에는 VNU 출력 레벨(edge_mag) 목록이 없다. 로더가 파일 밖 정보로 정해야 했고 그 정보를 이름에서 취했다
- 파일명은 사람이 바꿀 수 있는 표시라 내용과 어긋나도 아무것도 막지 않는다

### ㉰ 점검 항목

- ㉠ 동작을 정하는 판정은 파일 내용(값 패턴)으로 한다. 이름은 힌트일 뿐이고, 이름과 값이 어긋나면 에러를 낸다
- ㉡ 부분문자열 포함 검사를 판정에 쓰지 않는다. 반의어 접두(`non`)가 자연스러운 분야 용어에서 특히 위험하다
- ㉢ 판정 결과를 데이터 객체의 속성으로 노출해 여러 소비자가 같은 판정을 쓴다

### ㉱ 현재 코드 (수리된 위치)

- ㉠ `_detect_uniform_edge_mag`가 th 값 패턴(전 row와 전 dv 동일, 공차 d 등차 감소, 마지막 항 `2*d-1`)으로 레벨을 복원한다 (`src/llr_matrix.py:92-120`)
- ㉡ `load`가 파일명에 `uniform`이 있는데 패턴이 아니면 에러를 낸다. 이름은 이제 일관성 검사에만 쓰인다 (`src/llr_matrix.py:273-279`)
- ㉢ `has_uniform_levels` 속성이 값 기반 판정을 노출하고 (`src/llr_matrix.py:388-400`) 디코더가 생성자에서 한 번 읽는다 (`src/decoder.py:117`)
- ㉣ 파일명 파싱이 남은 곳은 모드 판별 `LLR_MATRIX_{HD|2SD|3SD}_` 하나다 (`src/llr_matrix.py:48, 237-241`). 파일에 모드 필드가 없어 유지한 결정이며, 같은 부류라는 점을 알고 쓴다

## 사용 방법

- 언제: 파일명이나 경로 문자열을 코드가 파싱해 동작을 고르는 자리를 추가하거나 리뷰할 때
- 어떻게: "내용으로 판별할 수 있는가, 이름과 내용이 어긋나면 에러를 내는가" 두 물음을 묻는다. 둘 다 아니면 포맷에 필드를 넣거나 값 패턴 판별을 만든다
- 주의: 이름을 힌트로 남길 때는 일관성 검사(이름이 X라 하는데 내용이 X가 아니면 에러)까지 붙인다. 검사 없는 힌트는 다시 판정 근거로 굳는다

관련 문서
- [20260808_uniform-llr-file-then-load.md](../decisions/20260808_uniform-llr-file-then-load.md)
- [20260930_uniform-llr-matrix-synthesis.md](../tech/20260930_uniform-llr-matrix-synthesis.md)
- [20260930_llr-matrix-file-format-and-loader.md](../tech/20260930_llr-matrix-file-format-and-loader.md)
