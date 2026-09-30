---
summary: 정보 구간을 정답 all-zero와 비교하는 genie 성공 판정, 성공 프레임을 배치에서 빼는 압축 목록, 결과 버퍼의 의미, 함께 바꿔야 하는 전제 묶음
tags: [decoder, genie, batch]
sources: [src/decoder.py:32-34, src/decoder.py:283-289, src/decoder.py:316-334, src/decoder.py:415-431, src/decoder.py:433-452, src/decoder.py:503-507, src/encoder.py:3-8, src/encoder.py:18-21, src/pcm.py:18, docs/차이.md:24, docs/차이.md:45]
last_verified: 2026-09-30
---

## 하는 일

매 iteration 끝에 판정비트 배열을 훑어 정보 구간 (앞쪽 N_b - M_b개 column block)에 에러가 없는 프레임을 성공으로 확정하고 배치에서 뺀다. 정답은 all-zero codeword다. genie는 CRC 조기 종료의 이상화 (미스검출 없음)이고, 압축은 속도 최적화라 결과가 바뀌지 않는다 (`docs/차이.md:24, 45`).

## 동작 방식

- ㉮ `_collect_error_metrics(state)` (`src/decoder.py:316-334`): `num_info_col_blocks = N_b - M_b` (`:324`). `frame_err` = 정보 구간 `decision_bits.any()` (`:326`), `info_err_bits` = 정보 구간 합 (post_fec_ber 분자, `:327`), `err_bits` = codeword 전체 합 (`:328`). `err_by_dv`는 `need_by_dv` (bit_err_by_dv 또는 fail_detail 로그)일 때만 실제로 센다 (`:329-334`). 전부 int64
- ㉯ column 루프 밖에서 센다 (`:317-319`): `_column_order`가 일부 column만 방문해도 미방문 column의 에러가 집계에 남아 성공 오판정이 없다. 호출은 `_run_iteration` 끝 (`:368`)과 SD restart (`:357`)
- ㉰ `_record_iteration` (`:415-431`): 압축 전에 부른다 (`:505`). 로그 합 (log_active, log_csw_sum, log_err_sum, log_err_by_dv_sum)을 append하고 (`:417-424`), `final_err_bits`, `final_info_err_bits`를 `idx_active` 위치에 쓴다 (`:425-426`). fail_detail이면 `final_csw`, `final_err_by_dv`도 (`:427-429`)
- ㉱ `_check_errors(state, iteration)` (`:433-452`)
  - ㉠ `ok = ~frame_err` → `success[idx_active[ok]] = True`, `decode_success_iteration[idx_active[ok]] = iteration` (`:436-439`)
  - ㉡ `keep = frame_err`. 전부 성공이거나 `iteration == max_iter`면 True를 반환해 루프를 끝낸다 (`:440-442`)
  - ㉢ 아니면 keep으로 압축 (`:443-451`)

| 압축 대상 | 조건 | 근거 |
|---|---|---|
| idx_active | 항상 | `:443` |
| read_bit, syndrome, prev_csw | 항상 | `:444-445` |
| decision_bits | 항상 | `:446` |
| region, seed_mag | SD만 | `:447-449` |
| min1, min2, min1_pos | 항상 | `:450` |
| check_sum, edge_sgn | 항상 | `:451` |

- ㉲ 결과 버퍼 의미 (`:283-289`): 원 배치 B 크기 고정. 매 iteration 활성 프레임 위치에 덮어써서 "마지막 처리 iteration의 값"이 남는다. 성공 프레임은 정보 구간 에러 0이지만 parity 구간 잔여 에러는 남을 수 있다. `decode_success_iteration`이 0이면 실패
- ㉳ 전제 묶음: ㉠ `encode`가 all-zero를 반환하는 임시 함수 (`src/encoder.py:18-21`) ㉡ genie 정답 참조가 all-zero (`src/decoder.py:32-34`) ㉢ sim의 BER 집계. 실제 인코딩으로 바꿀 때 셋을 함께 고친다 (`src/encoder.py:3-8`) ㉣ column block은 DV 내림차순 배치 전제이며 코드 검사가 없다 (`src/pcm.py:18`). 정보 구간이 앞쪽 블록이라는 가정이 여기서 온다
- ㉴ syndrome check 조기 종료는 없다. CSW는 row 선택에만 쓴다

## 쓰는 법

- ㉮ 프레임별 상태 배열을 새로 두면 압축 목록 (`src/decoder.py:443-451`)에 반드시 넣는다. 빠지면 다음 iteration에서 축이 어긋난다
- ㉯ `_column_order` 재정의로 방문 집합을 바꿔도 회계는 그대로다. 회계를 column 루프 안으로 옮기는 변경은 성공 오판정을 만든다
- ㉰ H 파일의 column block 순서가 DV 내림차순이 아니면 genie가 잘못된 구간을 본다. 새 부호를 들여올 때 확인한다
- ㉱ 디버그: `fail_detail` 로그를 켜면 실패 프레임의 `final_csw`, `final_err_by_dv`가 남는다. `final_err_bits`와 `final_info_err_bits`의 차이가 parity 구간 잔여 에러다

## 관련 문서

- ㉮ [../decisions/20260730_genie-check-and-all-zero-codeword.md](../decisions/20260730_genie-check-and-all-zero-codeword.md): genie와 all-zero 결정
- ㉯ [../assets/20260808_decision-bit-array-count-outside-loop.md](../assets/20260808_decision-bit-array-count-outside-loop.md): 루프 밖 집계 패턴
- ㉰ [20260930_decoder-stages-and-state.md](20260930_decoder-stages-and-state.md): 상태 배열과 반환 dict
- ㉱ [20260930_qccode-and-h-file.md](20260930_qccode-and-h-file.md): column block 배치 전제
- ㉲ [20260930_fer-point-loop-and-metrics.md](20260930_fer-point-loop-and-metrics.md): 결과 dict를 소비하는 지표 산식
- ㉳ [../../docs/차이.md](../../docs/차이.md)
