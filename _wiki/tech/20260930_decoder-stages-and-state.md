---
summary: decoder_main이 부르는 단계 함수 7개의 순서, _DecodeState 배열의 축과 dtype, 반환 dict의 키
tags: [decoder, state, batch]
sources: [src/decoder.py:7-15, src/decoder.py:54-96, src/decoder.py:100-118, src/decoder.py:249-292, src/decoder.py:454-472, src/decoder.py:475-508, src/pcm.py:85-92]
last_verified: 2026-09-30
---

## 무엇을 하는가

`BaseDecoder.decoder_main`이 프레임 배치 하나를 복호하는 흐름이다. 진입 함수는 흐름만 갖고, 단계 함수 7개가 `_DecodeState` 객체 하나를 주고받으며 일한다. 이 문서는 그 순서와 상태 배열의 꼴을 적는다. 교체 지점 6개는 별도 문서다.

## 어떻게 도는가

- ㉮ 호출 순서 (`src/decoder.py:475-508`): log 항목이 `LOG_ITEMS` 밖이면 에러 (`:496-499`) → `_read_channel_input` → `_init_state` → iteration 1..max_iter 동안 `_run_iteration`, `_record_iteration`, `_check_errors` (True면 break) → `_build_result`. `_record_iteration`은 압축 전 인덱스를 쓰므로 `_check_errors`보다 먼저 부른다 (`:505`)
- ㉯ 생성자 (`:100-118`): `llr_matrix` 필수, 모드는 HD, 2SD, 3SD만. `max_iter`는 `llr_matrix.max_iter`. `_col_dv_idx` (N_b,)는 column마다 dv 구간 인덱스, `_cols_by_dv`는 dv 구간별 column 목록, `_edge_mag`는 float32 내림차순 사본, `_uniform_levels`는 값 기반 균일 판정, `_seed_levels`는 SD Pre 단계 레벨 (HD는 None)
- ㉰ `_DecodeState` 필드 3그룹 (`:54-96`): ㉠ 설정과 치수 (log, need_by_dv, z, num_dv) ㉡ 프레임 데이터 (배치 압축 대상)와 결과 버퍼 (원 배치 B 고정) ㉢ iteration 임시값 (num_active_frames, frame_err, err_bits, edge_clear, cur_ch_all, cur_ch, cur_th)
- ㉱ 축 규약 (`:38`): 프레임 배치 B, column block N_b, lane z 순서의 (B, N_b, z)가 VN 정렬. CN 정렬은 (B, M_b, z). 배열 초기값은 아래 표 (`:253-291`)
- ㉲ 결과 버퍼 의미 (`:283-289`): 매 iteration 활성 프레임 위치에 덮어써서 "마지막 처리 iteration의 값"이 남는다. 성공 프레임도 parity 구간 잔여 에러는 남을 수 있다

| 배열 | 축 | dtype | 초기값 | 근거 |
|---|---|---|---|---|
| read_bit | (B, N_b, z) | uint8 | 채널 hd | `:263` |
| region, seed_mag | (B, N_b, z) | int64, float32 | SD만. HD는 None | `:264-266` |
| decision_bits | (B, N_b, z) | uint8 | read_bit 사본 | `:267` |
| syndrome | (B, M_b, z) | uint8 (bits와 같음) | `code.syndrome(read_bit)` | `:268`, `src/pcm.py:88` |
| prev_csw | (B,) | int64 | syndrome 합 | `:269` |
| min1, min2 | (B, M_b, z) | float32 | RESET = edge_mag[0] | `:271-272` |
| min1_pos | (B, M_b, z) | int32 | -1 | `:273` |
| check_sum | (B, M_b, z) | uint8 | 0 | `:274` |
| edge_sgn | (B, E, z) | uint8 | 0 | `:275` |
| idx_active | (B,) | 플랫폼 기본 정수 (`np.arange` 기본, Windows numpy 1.26에서 int32) | `arange(B)` | `:281` |
| success, decode_success_iteration | (B,) | bool, int32 | False, 0 | `:279-280` |
| final_err_bits, final_info_err_bits, final_csw | (B,) | int64 | 0 | `:286-288` |
| final_err_by_dv | (B, num_dv) | int64 | 0 | `:289` |

- ㉳ 반환 dict (`src/decoder.py:456-472`, 설명 `src/decoder.py:482-494`)

| 키 | 꼴 | 조건 |
|---|---|---|
| success | (B,) bool. 정보 구간 에러 0 | 항상 |
| decode_success_iteration | (B,) int32. 1-base, 실패는 0 | 항상 |
| final_err_bits, final_info_err_bits | (B,) int64. codeword 전체, 정보 구간 | 항상 |
| profile | (활성 프레임 수, 평균 잔여 에러) 리스트 | collect_profile |
| log_active, log_csw_sum, log_err_sum | iteration별 int64 합 | log 항목별 |
| log_err_by_dv_sum | (iteration, num_dv) int64 | bit_err_by_dv |
| final_csw, final_err_by_dv | (B,), (B, num_dv) int64 | fail_detail |

## 쓰는 법

- ㉮ 단계 함수 7개 (`_read_channel_input`, `_init_state`, `_run_iteration`, `_process_column`, `_record_iteration`, `_check_errors`, `_build_result`)는 교체 지점 표지가 없다. 재정의 대상은 교체 지점 6개다
- ㉯ 새 프레임별 상태 배열이 필요하면 `_DecodeState` 필드, `_init_state` 초기화, `_check_errors` 압축 목록 (`src/decoder.py:443-451`) 셋을 함께 고친다. 하나라도 빠지면 iteration 도중 축이 어긋난다
- ㉰ 디버그: `collect_profile=True`로 iteration별 (활성 프레임 수, 평균 잔여 에러)를 본다. 로그는 `log={"csw", "bit_err", "bit_err_by_dv", "fail_detail"}` 부분집합 (`src/decoder.py:51`)
- ㉱ 재정의 메서드가 받는 배열 축은 (활성 프레임 수, z)이며 활성 프레임 수는 iteration마다 줄어든다

## 관련 문서

- ㉮ [20260930_syndrome-aided-column-step.md](20260930_syndrome-aided-column-step.md): `_run_iteration`과 `_process_column`의 내부
- ㉯ [20260930_genie-check-and-batch-compress.md](20260930_genie-check-and-batch-compress.md): `_check_errors`와 압축 목록
- ㉰ [20260930_replacement-points-six.md](20260930_replacement-points-six.md): 교체 지점 6개
- ㉱ [../assets/20260807_function-extraction-refactoring.md](../assets/20260807_function-extraction-refactoring.md): 진입 함수를 단계 함수로 나눈 절차
- ㉲ [../../docs/profile/structure.md](../../docs/profile/structure.md): 호출 관계 그림
