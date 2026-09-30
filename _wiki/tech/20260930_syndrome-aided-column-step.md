---
summary: syndrome-aided flip 도메인 규약과 한 iteration 안에서 column block 하나를 처리하는 순서 (C2V 합산, 판정, VNU 양자화, CNU 갱신)
tags: [decoder, syndrome-aided, column-schedule]
sources: [src/decoder.py:17-36, src/decoder.py:336-370, src/decoder.py:372-413, src/pcm.py:4-5, docs/차이.md:32-34]
last_verified: 2026-09-30
---

## 하는 일

디코더의 메시지는 전부 초기 read bit 기준 상대값이다 (flip 도메인). read bit는 고정하고 syndrome을 한 번 계산해 유지하며, iteration마다 column block을 하나씩 돌며 판정과 CN 갱신을 한다. 이 문서는 그 규약과 `_run_iteration`, `_process_column`의 순서를 적는다.

## 동작 방식

- ㉮ 도메인 규약 (`src/decoder.py:17-36`)
  - ㉠ read_bit 고정, `syndrome = H * read_bit`을 1회 계산 후 유지 (`:18-20`). C++ iteration 0 Pre-update와 등가
  - ㉡ VN: `sum_t = ch + Σ vnu_in`. ch는 항상 양수 (iteration과 dv별 테이블값). `sum_t <= 0`이면 현재 bit 반전, 동점 포함 (`:21-22`)
  - ㉢ C2V (vnu_in): 크기 = min1 또는 min2, 부호 = syndrome ⊕ check_sum ⊕ edge_sgn (`:23-24`)
  - ㉣ CSW = Σ(check_sum ⊕ syndrome). iteration 1 진입 시 prev_csw = |syndrome| (`:30-31`)
- ㉯ `_run_iteration(state, iteration)` (`:336-370`)
  - ㉠ `num_active_frames` 갱신 (`:340`) → `_is_edge_clear_iter`가 True면 CN 상태 클리어 (`:342-349`) → SD이고 restart면 Pre 단계 재실행 후 return (`:350-359`)
  - ㉡ `row_index(iteration, prev_csw)`로 프레임별 row (`:360`) → `cur_ch_all` (F, num_dv, ch_len), `cur_ch` (F, num_dv), `cur_th` (F, num_dv, th_len) (`:361-363`). F는 활성 프레임 수
  - ㉢ `for col in _column_order(iteration): _process_column` (`:365-366`) → `_collect_error_metrics` (`:368`) → `prev_csw` 갱신 (`:370`)
- ㉰ `_process_column(state, iteration, col)` (`:372-413`)
  - ㉠ sum_t 초기값 (F, z) float32: HD는 `cur_ch[:, dv_idx]` 브로드캐스트 (`:381-384`), SD는 `take_along_axis(cur_ch_all[:, dv_idx, :], region[:, col, :])`로 비트별 region이 ch 열을 고른다 (`:385-388`)
  - ㉡ edge마다 `_c2v_reconstruct`에 CN row 슬라이스를 넘겨 c2v (CN 정렬) → `np.roll(c2v, +shift)`로 VN 정렬 → `sum_t += vnu_in`, vnu_in은 목록에 보관 (`:389-398`)
  - ㉢ `flip = _vn_decide(sum_t)` → `decision_bits[:, col, :] = read_bit[:, col, :] ^ flip` (`:400-403`). 정답 all-zero 기준 1이 에러
  - ㉣ edge마다 `raw = sum_t - vnu_in` (float32, 포화 없음, `:407`) → `_vnu_quantize(raw, vnu_in, cur_th[:, dv_idx, :])` → `np.roll(-shift)`로 CN 정렬 → `new_sgn = (vnu_out < 0)` uint8, `new_mag = |vnu_out|` → `_cnu_update` (`:405-413`)
- ㉱ roll 규약 (`src/pcm.py:4-5`): edge (i, j, s)에서 VN 정렬 → CN 정렬은 `np.roll(v, -s)`, CN → VN은 `np.roll(c, +s)`
- ㉲ column 직렬 스케줄: column 하나를 끝내면 CN 상태가 바로 바뀌어 뒤 column이 갱신값을 본다. flooding이나 row 단위 layered 경로는 없다
- ㉳ 등가 확인: 판정식, C2V 부호, CSW 정의는 C++ 원문과 같다 (`docs/차이.md:32-34, 39`)

## 쓰는 법

- ㉮ 교체 지점 4개가 이 함수 안에서 불린다: `_c2v_reconstruct` (`src/decoder.py:392`), `_vn_decide` (`:400`), `_vnu_quantize` (`:408`), `_cnu_update` (`:412`). 입력 축은 (F, z)
- ㉯ 스케줄을 바꾸려면 `_column_order`만 재정의한다. 일부 column만 방문해도 에러 집계는 column 루프 밖에서 세므로 유지된다. column을 두 번 방문하면 remove old가 두 번 돌아 복호가 무너진다
- ㉰ sum_t는 포화가 없다. 반전 불가 조건 `ch > dv * top` 같은 대수 조건은 이 식에서 나온다
- ㉱ 디버그: `state.cur_th[:, dv_idx, :]`와 `raw` 분포를 보면 양자화가 어느 레벨에 몰리는지 알 수 있다

## 관련 문서

- ㉮ [20260930_cnu-min1-min2-update.md](20260930_cnu-min1-min2-update.md): `_c2v_reconstruct`와 `_cnu_update`
- ㉯ [20260930_vnu-quantize-cascade.md](20260930_vnu-quantize-cascade.md): `_vnu_quantize`
- ㉰ [20260930_table-row-select-and-restart.md](20260930_table-row-select-and-restart.md): `row_index`와 Edge Clear
- ㉱ [20260930_decoder-stages-and-state.md](20260930_decoder-stages-and-state.md): 상태 배열의 꼴
- ㉲ [20260930_sd-region-and-pre-stage.md](20260930_sd-region-and-pre-stage.md): SD region과 Pre 단계
- ㉳ [20260807_flip-condition-ch-le-7dv.md](20260807_flip-condition-ch-le-7dv.md): sum_t 하한식
- ㉴ [../../docs/profile/techniques.md](../../docs/profile/techniques.md), [../../docs/차이.md](../../docs/차이.md)
