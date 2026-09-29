---
summary: iteration과 직전 CSW로 LLR 테이블 row를 고르는 규칙 (ITER, CSW 그룹), 그룹 겹침 금지와 정방향 순회가 한 쌍인 이유, restart (Edge Clear)의 CN 클리어와 -1 값 동작
tags: [llr-matrix, row-select, restart, csw]
sources: [src/llr_matrix.py:21-29, src/llr_matrix.py:46, src/llr_matrix.py:179-197, src/llr_matrix.py:211-219, src/llr_matrix.py:359-386, src/llr_matrix.py:402-417, src/decoder.py:25-29, src/decoder.py:137-144, src/decoder.py:342-363, docs/차이.md:35-36, docs/차이.md:40]
last_verified: 2026-09-30
---

## 무엇을 하는가

LLR 테이블은 row마다 dv별 (ch, th)와 CSW 임계, iteration 구간을 갖는다. 매 iteration 디코더가 `row_index(iteration, prev_csw)`로 프레임별 row 하나를 고른다. restart iteration은 CN 상태를 지우고 그 row의 -1 값을 그대로 써서 순수 syndrome bit-flip iteration이 된다.

## 어떻게 도는가

- ㉮ 그룹 결정 `_group_of_iter` (`src/llr_matrix.py:362-367`): `group_slices`를 정방향으로 돌며 `row_iter[row_start, 0] <= iteration <= row_iter[row_end - 1, 1]`인 첫 그룹. 없으면 ValueError
- ㉯ `row_index(iteration, prev_csw)` (`:369-386`), 반환은 (F,) int64
  - ㉠ ITER 타입 (`GROUP_TYPE_ITER = 0`, `:46`) 또는 단일 row 그룹: iteration 구간에 맞는 row 하나를 전 프레임에 (`:377-381`)
  - ㉡ CSW 타입: 그룹 첫 row로 시작해 뒤 row 순서로 `prev_csw <= row_csw[row]`면 덮어쓴다. 결과는 아래에서부터 처음 매칭되는 row, 없으면 그룹 첫 row (`:383-386`). C++ `Get_Cur_LLR_Idx_FILE`과 같다 (`docs/차이.md:40`)
- ㉰ 겹침 금지와 정방향 순회 한 쌍 (`src/llr_matrix.py:179-182`, `:189-192`): C++는 그룹을 역방향 순회해 겹치면 마지막 매칭을 고른다. Python은 정방향 첫 매칭이다. 겹침 금지 제약이 정방향 순회의 안전 근거이므로 겹침을 허용하려면 순회도 역방향으로 함께 바꾼다. 1..max_iter 빈틈 검사 (`:193-196`)는 C++보다 엄격하다. C++는 미커버 iteration에서 미정의 동작을 한다
- ㉱ restart 판정 `is_restart(iteration)` (`src/llr_matrix.py:359-360`). 디코더 기본 `_is_edge_clear_iter`는 이 값을 그대로 반환한다 (`src/decoder.py:137-144`). HD의 iteration 1 클리어는 하지 않는다 (사용자 결정 2026-08-09, iteration 1의 CN 상태가 초기값 그대로라 산술 결과가 같다)
- ㉲ 클리어 동작 (`src/decoder.py:342-349`): min1, min2 ← RESET, min1_pos ← -1, check_sum ← 0, edge_sgn ← 0. syndrome은 유지. 그 iteration의 `_cnu_update`는 remove old를 건너뛴다
- ㉳ restart row의 -1 값 (`src/llr_matrix.py:25-28`, `src/decoder.py:28-29`, `src/llr_matrix.py:372`): 그대로 산술에 넣는다. ch = -1은 채널 기여 거의 0, th = -1은 `|raw| >= -1`이 항상 참이라 전 메시지가 최대 레벨. LLR 최적화 도구가 이 동작을 기준으로 튜닝하므로 같게 따른다
- ㉴ 로더 제약 (`src/llr_matrix.py:211-219`): restart 그룹은 단일 row 단일 iteration이고 마지막 그룹일 수 없다
- ㉵ SD restart는 Pre 단계 재실행이며 row 값을 쓰지 않는다 (`src/decoder.py:350-359`). `_is_edge_clear_iter`가 아니라 `is_restart`를 직접 본다
- ㉶ 관찰: restart iteration 자체가 성공 판정을 낼 수 있다 (리뷰 실측 512프레임 중 445). 다만 잔여 에러를 크게 늘리는 교란 단계라 뒤에 회복 iteration이 없으면 품질이 나쁘다. "restart는 마지막 그룹 금지" 제약의 실질 근거

## 쓰는 법

- ㉮ restart 정책 (어느 iteration에 클리어할지)을 바꾸려면 `_is_edge_clear_iter`를 재정의한다. SD Pre 재실행은 바뀌지 않는다
- ㉯ 그룹 구성은 `llr_matrix.summary()`가 `g1[1~k]Rxn` 꼴로 보여준다 (R은 restart, n은 row 수, `src/llr_matrix.py:408-417`). `needs_csw`는 다중 row CSW 그룹 유무 (`:402-406`)
- ㉰ 겹치는 그룹을 허용하는 변경은 `_validate`와 `_group_of_iter`를 함께 고친다. 하나만 바꾸면 조용히 다른 row를 고른다
- ㉱ CSW 임계는 `prev_csw` (직전 iteration 종료 시점 값)와 비교한다. iteration 1의 prev_csw는 |syndrome|

## 관련 문서

- ㉮ [20260930_sd-region-and-pre-stage.md](20260930_sd-region-and-pre-stage.md): SD restart의 Pre 재실행
- ㉯ [20260930_llr-matrix-file-format-and-loader.md](20260930_llr-matrix-file-format-and-loader.md): 그룹 구조와 `_validate` 전체
- ㉰ [20260930_syndrome-aided-column-step.md](20260930_syndrome-aided-column-step.md): `row_index` 호출과 cur_ch, cur_th
- ㉱ [20260930_cnu-min1-min2-update.md](20260930_cnu-min1-min2-update.md): edge_clear 인자
- ㉲ [../trials/20260806_rejected-unification-and-relaxation.md](../trials/20260806_rejected-unification-and-relaxation.md): `_validate` 완화가 기각된 경위
- ㉳ [../../docs/profile/constraints.md](../../docs/profile/constraints.md), [../../docs/차이.md](../../docs/차이.md)
