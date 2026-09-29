---
summary: DAO LLR_MATRIX 텍스트 형식, 파일명 모드 판별, LLRMatrix.load와 _validate의 검사 항목, 생성자가 만드는 배열
tags: [llr-matrix, file-format, loader, validation]
sources: [src/llr_matrix.py:11-48, src/llr_matrix.py:123-170, src/llr_matrix.py:172-226, src/llr_matrix.py:229-282, src/llr_matrix.py:347-357, src/llr_matrix.py:408-417, src/run.py:406-411, src/run.py:441, docs/차이.md:25-26, docs/차이.md:40]
last_verified: 2026-09-30
---

## 무엇을 하는가

`src/llr_matrix.py`의 `LLRMatrix.load`가 DAO(decoder auto optimizer, LLR 테이블 최적화 외부 도구) 산출 텍스트 파일을 읽어 row 배열과 그룹 구조를 만들고, `_validate`가 DAO 규칙으로 형식을 검사한다. 균일 생성물도 같은 로더가 읽는다 (합성 문서 참조). LLR은 log-likelihood ratio(비트 신뢰도)다.

## 어떻게 도는가

- 1. 파일 형식 (`src/llr_matrix.py:11-15`): 빈 줄 무시, 정수만. 줄 순서는 아래 표

| 줄 | 뜻 |
|---|---|
| num_parameter_each_set | dv 하나당 값 개수 (ch 개수 + th 개수) |
| num_dv | dv(variable node degree, column degree) 구간 수 |
| dv_from / dv_to | 구간 하한과 상한 (각 한 줄) |
| num_group / num_row_each_group / type_each_group | 그룹 수, 그룹별 row 수, 타입 (0 ITER, 1 CSW) |
| num_restart / [restart_iter] | restart 수, 0보다 클 때만 iteration 줄 |
| max_value / min_value | 값 상한과 하한 (num_param개씩) |
| row들 | `[dv별 (ch..., th...) x num_dv] + CSW + iter_start + iter_end + floor_flag`, 길이 = `num_dv*num_param + 4` |

- 2. 모드 판별: 파일에 없어 파일명 정규식 `LLR_MATRIX_(HD|2SD|3SD)_` (대소문자 무시, `:48`, `:237-241`). ch 개수 = 모드별 1/2/4, th 개수 = num_param - ch 개수 (`:19`, `:131-133`)
- 3. `load` (`:229-282`): 헤더 파싱 (`:246-259`) → 개수 필드와 배열 길이 (`:261-262`) → row 수 = 그룹별 합 (`:263-266`) → row 길이 (`:269-270`) → edge_mag 역판별 `_detect_uniform_edge_mag` (`:273-274`) → 파일명에 uniform이 있는데 패턴이 아니면 에러 (`:275-279`). floor_flag는 튜플 다섯째 값으로 읽히지만 생성자가 쓰지 않고 (`:271-272`, `:156-161`) 저장 시 -1로 쓴다 (`:339-340`)
- 4. 생성자 (`:124-170`): th_len이 0 이하면 에러 (`:134-135`). edge_mag 미지정은 th 3개 전용이며 아니면 NotImplementedError (`:136-142`), 기본 [7,5,3,1]. `len(edge_mag) = th_len + 1` (`:144-146`). `row_values` (R, num_dv, num_param)을 `row_ch`, `row_th` 뷰로 나눔 (`:156-159`). `row_csw` (R,), `row_iter` (R, 2) (`:160-161`). `max_iter = row_iter[-1, 1]` (`:162`). `group_slices` (`:164-169`)
- 5. `_validate` (`:172-226`): dv 길이, 그룹 수, 총 row 수 (`:173-178`) → 그룹 겹침 금지와 1..max_iter 빈틈 금지 (`:183-197`) → ITER 다중 row 그룹 내부 row 구간 연속 (`:200-210`) → restart 그룹은 단일 row 단일 iteration이고 마지막 그룹이 아님 (`:211-219`) → th 내림차순이 아니면 경고만 (`:220-226`, `th_nonmonotonic`)
- 6. 겹침 금지와 `_group_of_iter`의 정방향 첫 매칭 순회는 한 쌍이다 (`:179-182`). 겹침을 허용하려면 순회를 C++처럼 역방향으로 함께 바꾼다
- 7. `col_dv_idx(code)` (`:347-357`): column degree가 어느 dv 구간에도 없으면 에러. C++의 조용한 col_idx 0 대체를 재현하지 않는다 (`docs/차이.md:25`). `summary()` (`src/llr_matrix.py:408-417`)가 그룹 구성을 `g1[1~k]Rxn` 꼴로 표시
- 8. 호출 지점: `setup`이 파일 존재를 확인하고 (`src/run.py:406-411`) `LLRMatrix.load(path)` 한 곳으로 읽는다 (`:441`)

## 쓰는 법

- ㉮ 파일 준비: `Input/LLR/`에 두고 config `decoder.llr_matrix`로 지정, `use_input_llr_matrix: true`. 파일명은 `LLR_MATRIX_{HD|2SD|3SD}_*.txt`. 모드와 max_iter는 파일이 정하고 config의 `mode`, `max_iter`는 읽지 않는다
- ㉯ 에러 읽기: 문구가 파일 이름과 위반 항목(그룹 번호, iteration 범위, row 번호)을 담는다. "덮는 그룹 없음"은 1..max_iter 빈틈, "겹침 (DAO 규칙 위반)"은 그룹 구간 중첩
- ㉰ 경고 "th가 내림차순이 아닌 row 존재"는 캐스케이드 의미(th1부터 순서 비교)로 소비되므로 실행은 계속된다. 작성 실수인지 확인한다
- ㉱ 주의: 사람이 만든 파일은 3-bit(th 3개)만 받는다 (사용자 확정 2026-08-06). 4-bit 파일은 NotImplementedError. dv 구간이 H-matrix의 column degree를 덮지 못하면 디코더 생성 시 에러이므로 LLR 파일 쪽을 맞춘다
- ㉲ 디버그: `LLRMatrix.load(path).summary()`로 모드, dv 구간, max_iter, 그룹 구성을 한 줄로 본다

## 관련 문서

- decision [20260807_llr-file-interpretation-rules.md](../decisions/20260807_llr-file-interpretation-rules.md)
- trial [20260806_rejected-unification-and-relaxation.md](../trials/20260806_rejected-unification-and-relaxation.md)
- asset [20260809_antipattern-filename-decides-semantics.md](../assets/20260809_antipattern-filename-decides-semantics.md)
- tech [20260930_uniform-llr-matrix-synthesis.md](20260930_uniform-llr-matrix-synthesis.md), [20260930_table-row-select-and-restart.md](20260930_table-row-select-and-restart.md), [20260930_setup-llr-supply-paths.md](20260930_setup-llr-supply-paths.md), [20260930_vnu-quantize-cascade.md](20260930_vnu-quantize-cascade.md)
- profile `../../docs/profile/constraints.md`
