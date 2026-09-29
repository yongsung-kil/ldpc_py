---
summary: 긴 진입 함수를 흐름 함수 하나와 목적 이름의 단계 함수, 상태 묶음 객체로 나누되 교체 지점 시그니처는 그대로 두는 절차 7단계
type: pattern
tags: [refactor, extraction, decoder]
date: 2026-08-07
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/done/20260807_가독성리팩토링/20260806_가독성리팩토링.md:21-29`, `src/decoder.py:7-15, 54-56, 475`, `docs/profile/replacement_points.md:35`
- ㉮ 결과 구조 (현재 코드)
  - ㉠ `decoder_main()`은 흐름만 (`src/decoder.py:475`). 단계 함수를 순서대로 부른다
  - ㉡ 단계 함수 7개: `_read_channel_input`, `_init_state`, `_run_iteration`, `_process_column`, `_record_iteration`, `_check_errors`, `_build_result` (docstring 도식 `src/decoder.py:7-15`)
  - ㉢ 상태 묶음 `_DecodeState` (`src/decoder.py:54-56`): 단계 함수 사이를 오가는 배열 전부. 필드 목록은 클래스 주석에 있다
  - ㉣ 교체 지점 6개(`_c2v_reconstruct`, `_vnu_quantize`, `_vn_decide`, `_cnu_update`, `_column_order`, `_is_edge_clear_iter`)는 단계 함수와 다른 층이다. 단계 함수는 재정의 대상이 아니다
- 절차 7단계
  - 1. 회귀 기준을 저장한다 (고정 입력 회귀 문서)
  - 2. 진입 함수를 순서 호출만 남긴다 (약 10줄)
  - 3. 단계마다 함수를 만든다. 이름은 단계의 목적이다 (에러 검사가 목적이면 `_check_errors`, 수단인 genie를 이름에 쓰지 않는다)
  - 4. 함수 사이를 오가는 배열은 묶음 객체 하나로 넘긴다
  - 5. 교체 지점(재정의 대상) 시그니처는 바꾸지 않는다
  - 6. 각 함수 docstring에 C++ 대응 함수와 줄 번호를 적는다
  - 7. 배열 단위 회귀 일치를 확인한다
- ㉯ 원칙: 이름 변경과 블록 단위 주석 보강을 함께 한다. 동작은 불변이다

## 사용 방법

- ㉮ 언제: 함수 하나가 여러 단계를 품어 C++ 대응 위치를 찾기 어려울 때. 새 상태 배열을 넣기 전에 구조를 정리할 때
- ㉯ 어떻게: 절차 1~7 순서대로. 단계 3에서 이름이 막히면 "이 단계의 목적이 무엇인가"를 묻는다
- ㉰ 주의
  - ㉠ 단계 함수 하나가 새 상태를 필요로 하면 `_DecodeState`와 `_init_state`, `_check_errors`의 배치 압축 목록을 함께 고친다 (성공 프레임을 빼는 마스킹에서 새 배열이 빠지면 축이 어긋난다)
  - ㉡ 뒤에 추가된 보조 함수 `_seed_channel_magnitudes`, `_collect_error_metrics`(`src/decoder.py:294, 316`)처럼 함수는 늘 수 있다. docstring 도식은 흐름 단계 7개만 보이므로 보조 함수는 부르는 단계 함수의 docstring에서 찾는다
- 관련 문서
  - [20260930_decoder-stages-and-state.md](../tech/20260930_decoder-stages-and-state.md)
  - [20260807_fixed-input-array-regression.md](20260807_fixed-input-array-regression.md)
  - [20260807_purpose-is-the-name.md](../decisions/20260807_purpose-is-the-name.md)
  - `../../docs/profile/replacement_points.md`
