---
summary: 2SD/3SD에서 채널 플래그를 ch 열 인덱스(region)로 바꾸는 식, 채널 magnitude를 CN에 심는 Pre 단계, SD restart의 동작과 C++ 함수 대응 사슬
tags: [decoder, soft-decision, pre-stage, cpp-mapping]
sources: [src/decoder.py:120-134, src/decoder.py:223-247, src/decoder.py:265-266, src/decoder.py:276-277, src/decoder.py:294-314, src/decoder.py:350-359, src/decoder.py:385-388, src/decoder.py:447-449, src/channel.py:9-11, src/llr_matrix.py:45, docs/차이.md:35, docs/차이.md:41, _pm/done/20260809_2SD3SD구현/cpp_sd_analysis.md:23-92, _pm/done/20260809_2SD3SD구현/cpp_sd_analysis.md:129-215, _pm/done/20260809_2SD3SD구현/cpp_sd_analysis.md:358-426]
last_verified: 2026-09-30
---

## 무엇을 하는가

SD(soft decision, 연판정) 모드에서 HD(hard decision, 경판정)와 달라지는 것은 셋뿐이다. ㉮ 채널 항이 비트별 region 선택값이 된다 ㉯ iteration 0과 SD restart가 채널 magnitude를 CN(check node, 검사 노드)에 심는 Pre 단계가 된다 ㉰ Edge Clear 대상 iteration 집합. 판정식, C2V(check-to-variable) 합산, VNU(variable node unit) 양자화, CNU 갱신은 HD와 같다.

## 어떻게 도는가

- 1. 채널 dict 플래그 (`src/channel.py:9-11`): `hd`는 read bit, `sd`는 strong 플래그, `cc`는 3SD의 very 플래그. 3SD 조합은 sd=1,cc=1 very strong / 1,0 normal strong / 0,0 normal weak / 0,1 very weak
- 2. region 매핑 `_read_channel_input` (`src/decoder.py:223-247`): 2SD `region = 1 - sd` (`:236`), 3SD `region = 2*(1 - sd) + (cc ^ sd)` (`:240`). 0이 가장 강한 신뢰. HD는 None. 채널 dict의 mode가 LLR(log-likelihood ratio) 매트릭스의 모드와 다르면 에러 (`:230-232`). signed LLR 배열 입력은 HD 전용 테스트 편의 (`:241-244`)
- 3. ch 개수 = region 수 (`MODE_CH_LEN` HD 1, 2SD 2, 3SD 4, `src/llr_matrix.py:45`). column 처리에서 비트별 region이 `cur_ch_all`의 ch 열을 `take_along_axis`로 고른다 (`src/decoder.py:386-388`). 판정 `sum_t <= 0`은 HD와 같다
- 4. seed 레벨 `_channel_seed_levels` (`:120-134`): 균일 레벨이면 `round(1 + (top - 1)*(R - 1 - k)/(R - 1))` (R = region 수, k = region, `:129-133`). 아니면 C++ 고정 상수 2SD [5, 1], 3SD [7, 5, 3, 1] (`:134`). LLR 파일에서 읽지 않는다. `seed_mag = _seed_levels[region]`은 (B, N_b, z) (`:265-266`)
- 5. Pre 단계 `_seed_channel_magnitudes` (`:294-314`): `_column_order(0)` 순서로 (`:303`) column마다 부호 = read_bit, 크기 = seed_mag (`:304-305`). edge마다 `roll(-shift)`로 CN 정렬 뒤 `_cnu_update(edge, True, ...)` (`:308-312`). 끝에 check_sum과 edge_sgn을 0으로 (`:313-314`). syndrome은 `H*read_bit`과 같아 재계산하지 않는다. `_init_state`가 SD일 때 부른다 (`:276-277`). min1_pos가 방문 순서에 의존하므로 순서를 `_column_order`와 맞춘다
- 6. SD restart (`:350-359`): `is_restart(iteration)`를 직접 보고 (`:350`) CN 클리어 뒤 Pre 재실행, `decision_bits = read_bit`, 에러 집계, `prev_csw = |check_sum ^ syndrome|` 갱신 후 return. 그 iteration의 row 값(ch, th)은 쓰이지 않는다. HD restart가 -1 값을 산술에 그대로 쓰는 것과 정반대
- 7. 배치 압축 때 region과 seed_mag도 함께 압축 (`:447-449`)

C++ 함수 대응 사슬 (원본 `decoder.cpp`와 `channel.cpp`, 근거 `_pm/done/20260809_2SD3SD구현/cpp_sd_analysis.md`):

| Python | C++ (파일:줄) | 무엇 |
|---|---|---|
| `_read_channel_input` region 식 | `Get_Mag_2SD`, `Get_Mag_3SD` (channel.cpp:42-56) → `Make_LLR` (decoder.cpp:4884-4935)의 `Mapper_2bit_SD` (4870-4880), `Mapper_3bit_SD` (4839-4853) → `VN_Cal_SD` (4537-4557) → `Get_VNU_LLR_SET_FILE` (7074-7133) 열 오프셋 | 플래그 → magnitude → ch 열 |
| `_channel_seed_levels` | `Make_LLR`의 EDGE_MAG 상수 (4905, 4924) | 시딩 magnitude, 파일에서 읽지 않음 |
| `_seed_channel_magnitudes` | `Is_Iter_Type_Init` (6606-6676) → `V2C_Cal` (5715-5722) → `VN_Cal_Pre` (3554-3754, 부호 3663, 크기 3666), edge sign 0 (2783-2785), check_sum을 syndrome으로 복사 후 리셋 (2993-3008) | Pre 단계 |
| `_is_edge_clear_iter` | `Is_Iter_Type_Edge_Clear` (6538-6598), `Clear_Edge_Restart` (709-739) | 원본 HD 0,1,restart와 SD 0,restart. Python은 전 모드 restart만 |
| SD restart 판정 복귀 | `cwc = Variable_mem` (3733-3736), CSW = \|syndrome\| (3464-3465) | 판정을 read bit로 |
| edge sign 겉보기 어긋남 | `C2V_Cal_New_Sgn` (2299-2335)은 `Edge_Clear(iter-1)`, `CNU_Remove_Old_Sgn` (3476-3509)은 `Edge_Clear(iter)` | Pre가 0을 써 두어 결과 일관 |

## 쓰는 법

- ㉮ SD 실행: 채널 type이 그 모드를 지원해야 한다 (rber는 세 모드, strong_error는 2SD, fixed_error는 HD). 파일 경로는 `LLR_MATRIX_2SD_*.txt`, 균일 경로는 `mode`와 `channel_llr_2SD` 리스트(강한 region부터)
- ㉯ 재정의: seed 레벨을 바꾸려면 `_channel_seed_levels`를 재정의한다 (교체 지점 표지는 없다). `_is_edge_clear_iter`를 재정의해도 SD restart의 Pre 재실행은 바뀌지 않는다 (`src/decoder.py:350`이 `is_restart`를 직접 본다)
- ㉰ 디버그: `log.items.bit_err_per_iter`를 켜면 SD restart iteration에서 에러 수가 채널 에러 수로 복귀하는 것이 보인다. 그것이 Pre 재실행의 실증이다
- ㉱ 주의: 3-bit 균일 2SD는 seed가 [7, 1]이 되어 C++ [5, 1]과 다르다 (사용자가 실행하며 조정). 비균일 넓은 레벨(예 {15,11,7,3}) 파일의 SD seed는 3-bit 상수로 떨어지는데 의도인지 미확인. toy 2SD/3SD 값의 출처는 소실됐다 (trial 참조)

## 관련 문서

- decision [20260809_sd-decoding-decisions.md](../decisions/20260809_sd-decoding-decisions.md)
- trial [20260809_toy-sd-values-source-lost.md](../trials/20260809_toy-sd-values-source-lost.md)
- asset [20260809_cpp-static-analysis-procedure.md](../assets/20260809_cpp-static-analysis-procedure.md)
- tech [20260930_table-row-select-and-restart.md](20260930_table-row-select-and-restart.md), [20260930_channel-models.md](20260930_channel-models.md), [20260930_cnu-min1-min2-update.md](20260930_cnu-min1-min2-update.md), [20260930_diff-from-cpp-original.md](20260930_diff-from-cpp-original.md)
- profile `../../docs/profile/techniques.md`, 정본 차이 목록 `../../docs/차이.md`
