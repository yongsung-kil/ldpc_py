---
summary: 이름은 수단이 아니라 목적을 말하고, 길어져도 명확한 쪽을 고르며, C++에 대응 개념이 있으면 C++ 용어를 따른다
status: Accepted
tags: [naming, readability, cpp-terms]
date: 2026-08-07
commit: 0394b81 (시험장 사본에 포함)
source: _pm/DONE.md (2026-08-07 이름 정확성 일괄 수정, 2026-08-08 의견1 반영), _pm/done/20260807_가독성리팩토링/20260806_가독성리팩토링.md:21-29, 66-76, 98, _pm/done/20260808_의견1_반영/의견1.md:1-22, 32-34, src/decoder.py:3-5, docs/profile/constraints.md:56-58
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - 가독성 리팩토링 착수(2026-08-06) 시점의 개정본은 축약 이름(mx, er, es, Ba)과 원본 C++와 다른 이름(total, csum, esgn)이 많아 코드와 decoder.cpp를 나란히 놓고 읽기 어려웠다
  - 사용자 지적(2026-08-07): `_apply_genie`는 수단(genie)이 이름이다. 목적은 에러 검사다. 같은 기준으로 전수 감사해 일괄 수정했다
  - 사용자 리뷰 노트(2026-08-08): 코드 한 줄을 인용하고 "X는 Y야?"라고 묻는 항목이 스무 개 남짓. 물어봐야 아는 이름은 결함으로 본다
- ㉯ 거부한 대안
  - ㉠ 짧은 관용 축약 유지 (rng, res, cfg, b, s)
  - ㉡ 메시지 방향 용어 c2v, v2c를 본 이름으로 (C++ 용어 vnu_in, vnu_out으로 확정. c2v는 roll 전 임시값 이름으로만 남았다)
  - ㉢ 이름만 바꾸고 주석은 그대로 (이름 변경과 블록 단위 주석 보강을 함께 한다)
- ㉰ 이유
  - 축약은 사용자 읽기와 C++ 대조 양쪽을 막는다. 코드만 보고 decoder.cpp의 대응 위치를 찾을 수 있어야 한다 (`src/decoder.py:3-5`)
  - `n_iter`처럼 "iteration 수"로 오독되는 이름은 결과 해석을 틀리게 한다 (실제 뜻은 성공한 iteration 번호)
  - `self.matrix`는 H-matrix와 LLR matrix 중 어느 것인지 드러나지 않았다
- ㉱ 이름 명확화 기준 (확정)
  - ㉠ C++에 대응 개념이 있으면 C++ 이름 (sum_t, check_sum, edge_sgn, syndrome, min1_pos, prev_csw, vnu_in, vnu_out)
  - ㉡ 축약어는 풀어 쓴다. 한 글자 변수와 축약(b, r, p, s, res, rng, agg, n_it)은 전부 대상
  - ㉢ 수단이 아니라 목적이 이름 (`_apply_genie` → `_check_errors`, `_restart_policy` → `_is_edge_clear_iter`)
  - ㉣ 길어져도 명확한 쪽 (`n_iter` → `decode_success_iteration`, `mx` → `llr_matrix`, `rng` → `random_generator`)
  - ㉤ 뜻이 여럿인 단어는 풀어 쓴다 (`points` → `point_results`). 인자를 만드는 함수 호출은 변수로 받아 넘긴다
  - ㉥ 구현 용어를 docstring에 노출하지 않는다 (frozenset). 같은 개념에 두 이름을 두지 않는다 (dvmap과 col_dv_idx)
  - ㉦ 원본에 없는 Python 고유 개념은 뜻이 드러나는 이름으로 (idx_active, keep)
- ㉲ 유지 기준 (바꾸지 않는 이름)
  - hd, sd, cc는 원본 HD_input, SD_input, CC_input 대응. cwr은 C++ 동명 변수. pcm의 J, K는 Ref-C 헤더 표기라 유지하고 주석으로 뜻을 적는다
- ㉳ 결과로 생긴 규칙과 비용
  - 식별자, CSV 헤더, 진행 줄 지표는 영어. docstring, 주석, 예외 문구는 한국어 (`docs/profile/constraints.md` 2절)
  - 코드 주석은 원본 C++ 대응 함수와 줄 번호를 괄호에 적는다
  - 이름 변경마다 고정 입력 회귀(배열 단위 완전 일치)와 기계 치환 후유증 검사(조사 어긋남, 부분문자열 오염)를 한다. 2026-08-09 리뷰에서 후유증 0건 확인
  - CSV 열 이름도 바뀌므로 옛 실행 결과와 열 이름이 다르다 (`avg_iter_ok` → `avg_decode_success_iteration`, 2026-08-10에 다시 `avg_decoding_iteration`)

## 하위 링크

- [20260808_rewrite-not-patch-positive-rules.md](20260808_rewrite-not-patch-positive-rules.md): 같은 리뷰 노트에서 승격된 문장 규칙 (다시 쓰기, 긍정문)
- [../assets/20260808_user-review-note-handling.md](../assets/20260808_user-review-note-handling.md): 사용자 리뷰 노트를 항목별 변경 표로 옮겨 반영하는 방식
- [../../docs/profile/constraints.md](../../docs/profile/constraints.md): 언어와 표기 규칙 정본 (2절)
