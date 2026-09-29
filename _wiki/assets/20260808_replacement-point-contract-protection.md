---
summary: 성능 최적화나 방어 코드를 본체에 넣을 때 자식 클래스의 교체 지점 재정의 계약을 깨지 않는 규칙 다섯
type: pattern
tags: [replacement-point, inheritance, contract]
date: 2026-08-08
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/tasks/20260808_review/r3_round3_lv2_verification/team_a_verification.md`, `docs/profile/replacement_points.md`

### ㉮ 규칙과 현재 코드

- ㉠ 인스턴스 바인딩 금지. `__init__`에서 `self._vnu_quantize = 빠른함수`로 바꾸면 인스턴스 속성이 클래스 속성보다 먼저 조회되어 자식의 재정의가 조용히 무시된다 (리뷰 시점 실측: 재정의 호출 0회). 옳은 꼴은 별도 함수와 본문 조건부 호출이다. 현재는 플래그 `_uniform_levels`를 생성자에서 정하고 (`src/decoder.py:117`) `_vnu_quantize` 본문이 조건 분기로 `_uniform_saturate`를 부른다 (`:175-176`)
- ㉡ 등가 조건 명시. O(1) 등가식 `max(min(|raw|, top), 1)`은 정수 raw에서만 캐스케이드와 같다. 비정수 raw를 만드는 재정의(offset min-sum, normalized min-sum, damping)가 오면 `_uniform_saturate`도 함께 재정의하거나 캐스케이드 경로를 쓴다. docstring이 조건을 적는다 (`src/decoder.py:189-195`)
- ㉢ dtype 계약. `_cnu_update`가 교체 지점이므로 본체는 `new_sgn`을 `.astype(np.uint8)`로 넘겨 기존 계약을 유지한다 (`src/decoder.py:410`). `-0.0` 같은 부동소수점 성질에 기대는 처방은 정수 dtype 재정의에서 무력해진다
- ㉣ 판정은 데이터 객체에. 균일 여부는 `LLRMatrix.has_uniform_levels` 속성이고 (`src/llr_matrix.py:388-400`) 디코더는 생성자에서 한 번 읽는다. 여러 소비자가 같은 판정을 쓴다
- ㉤ 회계는 방문과 독립. 방문 집합을 바꾸는 재정의(`_column_order`)에 대비해 에러 집계는 column 루프 밖에서 판정비트 배열을 훑는다 (`src/decoder.py:316-334`)

### ㉯ 적용 단계

- 1. 고치려는 함수가 교체 지점인지 본다. docstring 첫 줄 `[교체 지점: ...]` 표지 (`src/decoder.py:136-220`)
- 2. 교체 지점이면 함수 자체를 바꿔치기하지 않는다. 새 경로는 별도 함수로 두고 본문에서 조건으로 고른다
- 3. 새 경로가 성립하는 조건(정수 raw, dtype, 방문 집합)을 docstring에 적는다
- 4. 자식 재정의가 실제로 호출되는지 실측한다 (호출 횟수 세기)
- 5. 재정의 0개 자식과 본체의 고정 입력 회귀가 완전 일치하는지 확인한다

### ㉰ 조건

- 경계 규칙의 정리는 프로파일에 있다 (`docs/profile/replacement_points.md:24-31`)
- `isinstance` 검사가 없어 상속은 관례다. 본체가 디코더에서 읽는 속성은 `max_iter`와 `llr_matrix`의 `num_dv`, `dv_from`, `dv_to`, `mode`뿐이다

## 사용 방법

- 언제: 본체 디코더에 속도 최적화, 방어 코드, 캐시를 넣을 때. 리뷰 처방을 본체에 반영할 때
- 어떻게: 위 적용 단계 5개를 순서대로 밟는다. 특히 4번(호출 실측)은 "정적으로 봐서 괜찮다"로 대신하지 않는다
- 주의: 처방은 독립이 아니다. 각각 유효해도 함께 넣으면 갈릴 수 있으니(signbit 처방과 O(1) 등가식의 충돌) 상호작용을 따로 판정한다

관련 문서
- [20260930_replacement-points-six.md](../tech/20260930_replacement-points-six.md)
- [20260807_replacement-point-cpp-function-boundary.md](../decisions/20260807_replacement-point-cpp-function-boundary.md)
- [20260808_decision-bit-array-count-outside-loop.md](20260808_decision-bit-array-count-outside-loop.md)
- [20260813_paper-idea-single-override-procedure.md](20260813_paper-idea-single-override-procedure.md)
- `../../docs/profile/replacement_points.md`
