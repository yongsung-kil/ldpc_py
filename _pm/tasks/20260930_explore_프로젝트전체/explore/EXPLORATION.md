# 프로젝트 전체 탐색 결과

> 작성: 2026-09-30. 탐색 작업자 4명(아키텍처, 데이터 흐름과 기법, 컨벤션과 제약, 의존성)의 보고를 취합하고 검증 작업자 4명(사실, 누락, 관계, 실용성)의 대조를 반영한 최종본이다. 경로는 저장소 루트 기준이고 `파일:줄`은 그 파일의 줄 번호다. 메인이 직접 실행해 확인한 것은 "[실행 확인]"으로 표시했다. 원재료는 `_pm/tasks/20260930_explore_프로젝트전체/explore/`에 있다.

## 개요

Python으로 짠 QC-LDPC(quasi-cyclic low-density parity-check, 순환 시프트 블록 구조의 저밀도 패리티 검사 부호) 복호 시뮬레이터다. 원본 C++ 시뮬레이터(Ref-C)의 DAO(decoder auto optimizer) 연동 빌드가 쓰는 syndrome-aided quantized min-sum 디코더를 numpy 프레임 배치로 재현하고, 채널 3종으로 FER(frame error rate, 프레임 에러율)를 측정한다. 목적은 후보 기법의 on/off 상대 비교이며 C++와의 절대 FER 일치는 보장하지 않는다 (README.md:4, 215). 디코더 변형은 `src/`를 고치지 않고 `BaseDecoder`를 상속한 자식에서 교체 지점 함수 6개만 재정의한다 (README.md:161-162, src/decoder.py:40-46).

## 아키텍처

### 폴더

| 경로 | 역할 | 비고 |
|---|---|---|
| `src/` | 본체 코드 8모듈 (pcm, encoder, channel, decoder, llr_matrix, sim, run, `__init__`) | 합계 2,200줄 |
| `workspace/` | 실험 폴더. `_template/`(복사 원본), `base_run/`(기준선), `test/`(파이프라인 점검), `matrix_sel_1_HD/`, `matrix_sel_1_HD_fixed/` | README.md:165-172 구조도에는 `_template`와 `base_run`만 |
| `Input/H_matrix/` | `example_18x147_z256.qc` (행렬 1벌), `matrix_sel_1.txt` (탭 구분, 15×145) | Ref-C 헤더 형식, 확장자 무관 |
| `Input/LLR/` | HD_0 (restart 포함 토이, max_iter 5), HD_1 (max_iter 20), 2SD_toy0, 3SD_toy0 (max_iter 20), HD_matrix_sel_1 (그룹 8개 전부 CSW, 57 row, max_iter 120) | README.md:14는 앞 4개만 기재 |
| `docs/` | `차이.md`(C++ 대비 로직 차이), `profile/`(프로파일 6문서), `adr/README.md`, `explore/` | README.md:15의 `docs/review/`는 없다 |
| `_pm/` | 작업 관리. `tasks/20260808_review/`는 미완 리뷰 항목 | |
| 루트 | `README.md`(224줄), `requirements.txt`(numpy, matplotlib), `__init__.py`(docstring만), `CLAUDE.md`(온보딩으로 채움) | `.gitignore` 없음 [실행 확인] |

### 모듈과 import 방향

`run` → {`channel`, `encoder`, `decoder`, `llr_matrix`, `pcm`, `sim`}, `sim` → `decoder`, `__init__` → {`pcm`, `decoder`, `channel`, `encoder`, `sim`}. `pcm`, `encoder`, `channel`, `llr_matrix`, `decoder` 다섯은 `src/` 안의 다른 모듈을 import하지 않는 잎 모듈이다 (서드파티는 numpy만, `llr_matrix`는 표준 라이브러리 os, re, warnings도 쓴다). `decoder`는 `QCCode`와 `LLRMatrix` 객체를 생성자 인자로 받아 속성 이름으로만 쓰므로 두 클래스의 속성 목록이 사실상 인터페이스다 (src/decoder.py:100-118). 순환 없음. `src/__init__.py:6-10`의 공개 API는 `QCCode`, `BaseDecoder`, `channel`, `encoder`, `sim`이다.

| 모듈 | 역할 | 공개 심볼 (줄) |
|---|---|---|
| `src/pcm.py` | QC 부호 표현과 Ref-C 포맷 입출력 | `QCCode` :23 (`load` :58, `save` :49, `syndrome` :85, `count_cycles4` :94, `summary` :112). 속성 `base`, `M_b`, `N_b`, `z`, `N`, `M`, `K`, `rate`, `edge_row`, `edge_col`, `edge_shift`, `E`, `col_edges`, `row_deg`, `col_deg` (:30-46) |
| `src/encoder.py` | 메시지 생성과 인코딩 자리 | `generate_message` :13, `encode` :18 (all-zero 반환 임시) |
| `src/channel.py` | 채널 3종과 레지스트리 | `qfunc_inv` :24, `dev_from_rber` :37, `rber_channel` :43, `fixed_error_channel` :78, `strong_error_channel` :91, `CHANNELS` :138, `CHANNEL_MODES` :145 |
| `src/llr_matrix.py` | DAO LLR_MATRIX 로더, 균일 합성, row 선택 | `MODE_CH_LEN` :45, `GROUP_TYPE_ITER/CSW` :46, `uniform_edge_mag` :51, `edge_quantization_levels` :60, `LLRMatrix` :123 (`load` :230, `make_internal_uniform_matrix` :286, `save` :318, `col_dv_idx` :347, `is_restart` :359, `row_index` :369, `has_uniform_levels` :389, `needs_csw` :403, `summary` :408) |
| `src/decoder.py` | 배치 벡터화 syndrome-aided min-sum 디코더 | `LOG_ITEMS` :51, `_DecodeState` :54, `BaseDecoder` :99 (메서드 19개), `decoder_main` :475 |
| `src/sim.py` | 한 포인트 FER 측정 루프 | `run_fer_point` :29, `save_csv` :170 |
| `src/run.py` | 설정 로드와 검증, 구성, 실험 루프, 출력, CLI | `load_config` :270, `setup` :393, `print_experiment_summary` :496, `run_experiment` :548, `create_run_dir` :715, `report` :736, `main` :780. 비공개 함수 14개 (검증, 요약, 로그 CSV, 그림) |

### 진입점 두 갈래

- ㉮ 실험 폴더 런처 `workspace/{실험}/run.py` (5개 파일 내용 동일, 33줄): 부모로 올라가며 `<조상>/2_LDPC_base/src` 폴더가 있는 조상을 찾아 그 `<조상>/2_LDPC_base`를 `sys.path[0]`에 넣고 `from src.run import main` (run.py:11-22). `DECODER_CLASS` 상수 하나로 디코더를 주입 (:24-28), 인자가 없으면 형제 `config.json` (:31-33). **이 사본에서는 폴더 이름이 `ldpc_py`라 `SystemExit("상위 폴더에서 2_LDPC_base/src를 찾지 못함")`로 끝난다** [실행 확인: `workspace/test`에서 `python run.py`]
- ㉯ 루트에서 `python -m src.run <config 경로>` (src/run.py:780-795): 폴더 이름과 무관하게 동작하고 디코더는 `BaseDecoder` 고정 (`main()`을 인자 없이 부름). config의 상대 경로(`../../Input/...`)는 config 파일 위치 기준이라 그대로 맞는다 (:277). [실행 확인: 스크래치 설정으로 32프레임 20 iteration, 결과 파일 7종 생성, 약 2.7초, 콘솔 `162 it/s`, Python 3.11.7, numpy 1.26.4, matplotlib 3.10.7]
- ㉰ 따라서 이 사본에는 자식 디코더를 실행할 경로가 없다. 런처 수정이나 새 런처 추가는 코드 변경이라 판정요청 물음 1로 올렸다 (`_pm/tasks/20260930_explore_프로젝트전체/판정요청_시험장사본_260930.md`)

### 계층과 호출 순서

```
main(argv, decoder_class)                                              src/run.py:780-791
├─ load_config          키맵(허용 키 집합 9개), 필수값, 값 제약, 정규화   src/run.py:98-111, 270-390
├─ setup                QCCode.load :405 → LLRMatrix.load :441
│                        (또는 make_internal_uniform_matrix :423 → save :439 → load :441)
│                        → decoder_class(code, llr_matrix=...) :443-445
├─ print_experiment_summary                                             :496
├─ create_run_dir       YYMMDD_HHMMSS_{label}/, config 사본, summary.txt 머리 (git 해시)  :715-733
├─ run_experiment       채널 × 포인트 루프                               :548-600
│   ├─ _check_channel_mode 사전 확인 :568-569 (포인트마다 :519에서도)
│   ├─ rng = default_rng([seed, channel_index, int(1e6*point)])          :586
│   ├─ _make_channel_fn  generate_message → encode → CHANNELS[type]      :515-530
│   └─ sim.run_fer_point                                                 src/sim.py:29-167
│        └─ decoder.decoder_main(channel_out, log)                       src/decoder.py:475-508
│             ├─ _read_channel_input :501 → _init_state :502 (SD면 _seed_channel_magnitudes :277)
│             └─ iteration 1..max_iter (:503-507)
│                  ├─ _run_iteration :336-370
│                  │    ├─ [_is_edge_clear_iter] :342 → CN 클리어 :343-349
│                  │    ├─ SD restart (is_restart 직접 판단 :350) → Pre 재실행 후 return :350-359
│                  │    ├─ llr_matrix.row_index(iteration, prev_csw) :360 → ch, th
│                  │    ├─ for col in [_column_order]: _process_column :365-366
│                  │    │     ├─ [_c2v_reconstruct] × edge → sum_t :390-398
│                  │    │     ├─ [_vn_decide] → decision_bits :400-403
│                  │    │     └─ [_vnu_quantize] → roll → [_cnu_update] × edge :405-413
│                  │    └─ _collect_error_metrics :368 → prev_csw :370
│                  ├─ _record_iteration :415-431
│                  └─ _check_errors (genie, 배치 압축) :433-452
│             └─ _build_result :454-472
└─ report               fer CSV, 로그 CSV 3종, LLR 사본, fer_curves.png   src/run.py:736-777
```

대괄호는 교체 지점이다.

### 교체 지점 (src/decoder.py:136-220)

모듈 docstring(:40-46)이 "교체 단위 = 원본 C++ 함수 경계"인 함수 6개를 명시하고, 각 docstring 첫 줄에 `[교체 지점: C++ 함수 대응]` 표지가 있다.

| 함수 (줄) | 입력 | 출력 | 호출 위치 | C++ 대응 |
|---|---|---|---|---|
| `_is_edge_clear_iter(iteration)` :137-144 | iteration 번호 | bool | `_run_iteration` :342 | Is_Iter_Type_Edge_Clear |
| `_column_order(iteration)` :146-148 | iteration 번호 (SD Pre 단계는 0) | column block 인덱스 iterable | `_run_iteration` :365, `_seed_channel_magnitudes` :303 | 메인 루프 스케줄 |
| `_c2v_reconstruct(iteration, edge, min1_row, min2_row, min1_pos_row, syndrome_row, check_sum_row, edge_sgn_row)` :150-157 | CN row block 슬라이스 (활성 프레임, z) | 부호 있는 C2V (CN 정렬). mag = min1(자기 위치면 min2), sign = syndrome ⊕ check_sum ⊕ edge_sgn | `_process_column` :392 | C2V_Cal |
| `_vn_decide(sum_t)` :159-162 | sum_t (활성 프레임, z) | bool (반전 여부), 기본 `sum_t <= 0` | `_process_column` :400 | VN_Cal_HD 판정부 |
| `_vnu_quantize(raw, vnu_in, th)` :164-187 | raw = sum_t − vnu_in, th (활성 프레임, th 개수) | 부호 있는 양자화 값 | `_process_column` :408 | VN_Cal_HD 양자화부 |
| `_cnu_update(edge, edge_clear, new_sgn, new_mag, row_blk, min1, min2, min1_pos, check_sum, edge_sgn)` :197-220 | 새 메시지와 CN 상태 배열 | None (제자리 갱신) | `_process_column` :412, `_seed_channel_magnitudes` :310 | CNU_Remove_Old_Sgn, CNU_Update_New_Mag |

경계 규칙: ㉮ `_cnu_update`는 받은 배열을 제자리에서 고쳐야 한다 (:202-203). ㉯ `_uniform_saturate`(:189-195)는 비정수 raw를 만드는 재정의에서 함께 재정의한다. ㉰ `_collect_error_metrics`(:316-334)는 column 루프 밖에서 세므로 부분 스케줄에도 집계가 유지된다. ㉱ 자식 생성자는 `decoder_class(code, llr_matrix=...)`에 맞아야 하고 (src/run.py:445), 본체가 디코더 객체에서 읽는 것은 `max_iter`와 `llr_matrix`의 `num_dv`, `dv_from`, `dv_to`, `mode`다 (src/sim.py:72-73, src/run.py:482, 507, 623-624, 742). `isinstance` 검사는 없다. ㉲ `_is_edge_clear_iter`는 CN 클리어에만 관여하고 SD restart의 Pre 재실행은 `llr_matrix.is_restart`가 직접 정한다 (:350). ㉳ 단계별 함수 7개(`_read_channel_input`, `_init_state`, `_run_iteration`, `_process_column`, `_record_iteration`, `_check_errors`, `_build_result`)와 보조 3개(`_channel_seed_levels`, `_seed_channel_magnitudes`, `_uniform_saturate`)는 표지가 없다. 재정의 예시 `decoder.py`는 workspace 어디에도 없다. 정본 문서 `새논문적용규칙.md`는 저장소 밖(`3_LDPC_ideas/`)이고 `src/decoder.py:46`은 `docs/새논문적용규칙.md`라고 다른 경로를 적어 어긋난다.

## 핵심 흐름

### 입력 파일 두 종류

- ㉮ H-matrix (`src/pcm.py:58-82`): `N_b M_b` / `J K` / `z` / 빈 줄 / M_b×N_b shift 행렬 (−1은 zero block). `lines[3:]`를 이어 붙여 앞 `M_b*N_b`개만 쓰므로 뒤 내용은 무시. 확장자 검사 없음. 헤더 J/K보다 실제 degree가 크면 에러 (:78-81), shift가 z 이상이면 에러 (:28-29). edge (i, j, s)에서 VN 정렬 → CN 정렬은 `np.roll(v, -s)`, 반대는 `+s` (:4-5). column block은 DV 내림차순 배치 전제 (:18, 코드 검사 없음)
- ㉯ LLR_MATRIX (`src/llr_matrix.py:230-283`): num_param / num_dv / dv_from / dv_to / num_group / num_row_each_group / type_each_group / num_restart / [restart_iter] / max_value / min_value / row들. row = [dv별 (ch..., th...)] + CSW + iter_start + iter_end + floor. 모드는 파일명 정규식 `LLR_MATRIX_(HD|2SD|3SD)_` (:48, 237-241), ch 개수 HD 1 / 2SD 2 / 3SD 4 (:45), th 개수 = num_param − ch. 사람이 만든 파일은 th 3개 전용 (:136-142). `max_iter` = 마지막 row의 iter_end (:162). `_validate`(:172-226): 그룹 겹침 금지, 1..max_iter 빈틈 금지, ITER 다중 row 그룹 내부 연속, restart 그룹 단일 row이며 마지막 그룹 금지, th 비단조는 경고. `max_value`, `min_value`, floor는 디코딩에 쓰이지 않는다 (:153-161, :334-340)
- ㉰ 균일 생성 경로: `use_input_llr_matrix=false`면 `edge_quantization_levels(bits, max)`(:60-89)로 레벨을 만들고 `make_internal_uniform_matrix`(:285-316)로 그룹 1개 ITER 매트릭스를 합성해 `output.dir/_generated/LLR_MATRIX_{mode}_uniform_...txt`로 저장한 뒤 같은 `load`로 읽는다 (src/run.py:412-441)

### config JSON (`src/run.py:270-390`)

`base_dir`은 config 파일 위치 (:277). 허용 키 집합 9개(:99-111)로 키맵 검사, `_`로 시작하는 키는 무시 (:120-122). 정규화: 경로 문자열 대체, `output.dir` 기본 `Sim_Output`, `config["seed"]` 승격 (:357), `log` 평탄화 (:385-387), `channels` 리스트화 (:183-247). run 기본값 `_RUN_DEFAULTS`(50, 20000, 128, 100)는 검증, 소비, 요약 세 곳이 같은 dict를 읽는다 (:116-117, 358-360, 486-489, 557-563). 값 제약: rber 0 < p < 0.5, 에러 bit 수 0 이상 정수, `int(1e6*값)` 중복 금지, type 중복 금지, `channel_llr_*` 길이 = region 수, `edge_resolution_bits` 2..16, `edge_max_value` 2^n − 1, seed 0 이상, `stop_below_fer` 양수 또는 null. 기본값 이중 정의: edge (3, 7)이 :260/:267과 :419에, print_progress True가 :361과 :561에.

### 시뮬레이션 루프 (`src/sim.py:29-167`)

`while frames < max_frames and errors < max_frame_errors` (:95). 배치마다 채널 → `decoder_main` → 집계. 진행 줄은 콘솔 `\r` 갱신(tty일 때만)과 summary.txt 꼬리 제자리 갱신 (:21-26, 121-137). 결과 dict(:142-161): fer = errors/frames, post_fec_ber = 정보 구간 잔여 에러 합/(frames × K), avg_decoding_iteration = (성공 iteration 합 + errors × max_iter)/frames, iter_hist, iteration_totals, fail_frame_details, summary_line. `stop_below_fer`는 `run_experiment`에서 판단 (src/run.py:597-598). 난수는 포인트마다 `default_rng([seed, channel_index, int(1e6*point)])`이고 메시지 생성과 채널이 순서대로 소비하므로 재현에는 `frames_per_batch`까지 같아야 한다.

### 채널 (`src/channel.py`)

공통 출력 dict `{"mode", "hd", "sd", "cc"}` (:9-11). `rber_channel`(:43-68) RBER → σ 환산, BPSK+가우시안, HD/2SD/3SD (`_R_OFFSET` :21). `fixed_error_channel`(:78-88) HD 전용, 정확히 E개 flip (`_rand_positions` :71-75, 구간 슬라이스 금지). `strong_error_channel`(:91-135) 2SD 전용, SER/SCR 비율. 모드 정합 검사는 세 층: `_check_channel_mode` (src/run.py:504-512, 호출 :519, :569), 채널 함수의 mode 인자 검사 (:46-47, 80-81, 104-105), 디코더 `_read_channel_input` (src/decoder.py:230-232).

### 디코더 (`src/decoder.py`)

- ㉮ 생성자(:100-118): `max_iter`, `_col_dv_idx`, `_cols_by_dv`, `_edge_mag`, `_uniform_levels`, `_seed_levels`. `_channel_seed_levels`(:120-134): 3-bit 파일은 C++ 상수 2SD [5,1], 3SD [7,5,3,1], 균일 n-bit는 1..top 균등 분할 (C++ 대응 없음)
- ㉯ 상태 `_DecodeState`(:54-96): `read_bit`, `decision_bits` (B, N_b, z), `syndrome` (B, M_b, z) 1회 계산, `prev_csw` (B,), `region`과 `seed_mag` (SD), CN 상태 `min1`, `min2` (float32, 초기 RESET = edge_mag[0]), `min1_pos` (int32, 초기 −1), `check_sum` (uint8), `edge_sgn` (B, E, z). B는 성공 프레임이 빠지며 줄어든다
- ㉰ `_read_channel_input`(:223-247): region = 2SD `1−sd`, 3SD `2(1−sd)+(cc⊕sd)`. dict 대신 부호 있는 LLR 배열도 받는다 (HD 전용, 테스트 편의, :241-244)
- ㉱ `_run_iteration`(:336-370)과 `_process_column`(:372-413): sum_t = ch(항상 +) + Σ roll(+shift) C2V, float32 무포화 → flip = `sum_t <= 0` → `decision_bits = read_bit ^ flip` → edge마다 `_vnu_quantize(sum_t − vnu_in, ...)` (캐스케이드 또는 `_uniform_saturate`) → roll(−shift) → `_cnu_update` (remove old, insert new `<=`, 새 min1이면 min2=RESET)
- ㉲ genie(:316-334): `decision_bits[:, :N_b−M_b, :]` 전부 0이면 성공. `_check_errors`(:433-452)가 성공 프레임을 확정하고 배치 압축. `final_err_bits`는 codeword 전체, `final_info_err_bits`는 정보 구간
- ㉳ SD Pre `_seed_channel_magnitudes`(:294-314): `_column_order(0)`과 `_cnu_update(edge_clear=True)`로 seed magnitude를 CN에 심고 check_sum과 edge_sgn을 0으로

### 출력 (`src/run.py:715-777`)

실행 폴더 `output.dir/YYMMDD_HHMMSS_{label}/`. 측정 전: config 원문 사본, summary.txt 머리 (`code commit` 해시와 `+dirty`, 실험 요약). 측정 중: 진행 줄과 결과 줄 실시간. 측정 후 `report`: `{csv_prefix}_{label}.csv`, `log_iter_*`, `log_iter_hist_*`, `log_fail_*` CSV, LLR 사본 (`_used_llr_matrix_path`, :442, :765), `fer_curves.png` (0 에러 포인트는 0.5/frames 상한 마커, 실패해도 계속). 로그 JSON 키 → 디코더 이름은 `_LOG_TO_ITEM`(:113-114). 네 항목 모두 JSON 키 → 디코더 버퍼 → sim 누적 → CSV 열까지 끊긴 고리 없이 이어진다 (검증 C).

## 주요 컴포넌트

| 컴포넌트 | 역할 | 위치 |
|---|---|---|
| `QCCode` | H-matrix 로드, edge 목록, syndrome | `src/pcm.py:23-118` |
| `LLRMatrix` | DAO 파일 파싱과 검증, 균일 합성, row 선택 | `src/llr_matrix.py:123-411` |
| 채널 함수 3종과 `CHANNELS` | rber, fixed_error, strong_error | `src/channel.py:43-149` |
| `BaseDecoder` | 디코더 본체. 교체 지점 6, 단계별 7, 보조 3 | `src/decoder.py:99-472` |
| `decoder_main` | 디코더 진입 | `src/decoder.py:475-508` |
| `run_fer_point` | 한 포인트 배치 루프와 집계 | `src/sim.py:29-167` |
| `load_config`, `setup`, `run_experiment`, `report` | 설정, 구성, 순회, 저장 | `src/run.py:270-777` |
| 런처 `run.py` | 실험 폴더에서 본체 탐색과 디코더 주입 | `workspace/*/run.py` (5개 동일, 33줄) |

## 외부 의존성

| 이름 | 용도 | 버전 제약 |
|---|---|---|
| numpy | 전 모듈 필수 | 명시 없음. `Generator.permuted`(src/channel.py:125)로 1.20 이상 추정. 삭제 별칭 0건. [실행 확인] 1.26.4 |
| matplotlib | `_plot_fer_curves`(src/run.py:692-712) 지연 import, `Agg` | 명시 없음. 실패는 `report`가 흡수 (:769-775). [실행 확인] 3.10.7 |
| Python | f-string, `subprocess.run(capture_output=, text=)` (:608-615), `raise ... from None` | 명시 없음. 3.7 이상 추정. [실행 확인] 3.11.7 |
| 표준 라이브러리 | os, sys, json, shutil, subprocess, datetime, csv, re, warnings, numbers, time | |
| git 실행 파일 | summary.txt 커밋 해시 (src/run.py:603-618) | 없으면 "(git 없음)" |

병렬화 라이브러리(mpi4py, numba, multiprocessing) import 0건. `README.md:221`의 mpi4py 방침과 mpi_runner 재설계는 계획만 있다.

## 주의 사항

### 이 사본(testbed/ldpc_py)에서 원본과 다른 점

- ㉮ 다섯 런처가 `2_LDPC_base` 폴더 이름을 하드코딩해 동작하지 않는다. 동작하는 실행 경로는 루트에서 `python -m src.run <config>`뿐이고 이 경로는 자식 디코더를 주입할 수 없다 → 판정요청 물음 1
- ㉯ `.gitignore`가 없다. README.md:104, 170의 "git 무시" 서술이 성립하지 않고 `workspace/matrix_sel_1_HD/_probe/` 결과물 2건과 `_probe.json`이 커밋에 들어 있다 [실행 확인: `git ls-files`]. 실행하면 `src/__pycache__/`가 untracked로 남는다
- ㉰ `docs/review/`(README.md:15)가 없다. 리뷰 기록은 `_pm/done/*_review/`에 있다
- ㉱ 이력 문서 11개에 개인 계정이 든 절대 경로 15곳이 남아 있다 (상위 CLAUDE.md ㉴와 충돌) → 판정요청 물음 2

### 문서와 코드가 어긋난 곳

- ㉮ 교체 지점 정본 경로: `src/decoder.py:46`은 `docs/새논문적용규칙.md`, README.md:163은 `3_LDPC_ideas/새논문적용규칙.md`. 둘 다 없다
- ㉯ `workspace/matrix_sel_1_HD_fixed/README.md:8, 14`와 `config.json` `_desc`는 max_frame_errors 20, max_frames 200000이라 적었지만 값은 15, 2000000. `matrix_sel_1_HD/_probe.json` `_desc`도 "20개"인데 값은 5
- ㉰ `workspace/matrix_sel_1_HD/`에 README.md가 없다
- ㉱ README.md:14 LLR 목록에 `LLR_MATRIX_HD_matrix_sel_1.txt`가 없고, README.md:13은 `.qc`라 했지만 `matrix_sel_1.txt`는 `.txt`
- ㉲ README JSON 예시(:59-83)에 `run.print_progress`, `output.label`, `output.save_llr_matrix`가 없고 산문으로만. run 기본값(50, 20000, 128)은 README에 없다
- ㉳ `_pm/DONE.md:1`은 "2_LDPC_light", README는 "2_LDPC_base". `_pm/TODO.md:6`은 삭제된 `docs/plan.md`를 참조. README.md:5의 `_test/20260806_setup_구성_실험/`은 없다
- ㉴ `_pm/DONE.md:71-75`가 말하는 단위 테스트 24건 등의 파일은 저장소에 없다

### 알려진 한계와 기술 부채

- ㉮ 미구현 (README.md:199-207, docs/차이.md:17-26): BF 구간, error floor 감지, power stopping, 1.5SD와 Jump_Iter, 파이프라인 store 지연, dual update, CRC 조기종료, HCU, 쇼트닝과 펑처링, 비 AUTO 테이블 전환
- ㉯ `encoder.encode()`는 all-zero 반환 임시. 바꾸면 genie 정답 참조와 BER 집계를 함께 (src/encoder.py:3-8)
- ㉰ 정의만 있고 호출되지 않는 코드: `QCCode.count_cycles4`, `QCCode.summary`, `LLRMatrix.summary`, `LLRMatrix.needs_csw`, `collect_profile` 경로, `channel_config.get("label")` 두 곳 (src/run.py:465, 577)
- ㉱ floor flag는 로드 시 버리고 저장 시 −1 (`_pm/TODO.md:26` 현행 유지)
- ㉲ 토이 LLR 파일(HD_0, HD_1)의 dv=2 ch=28은 반전 가능 조건 `ch <= 7*dv`(=14) 위반 상태 (`_pm/TODO.md:29-31`)
- ㉳ `_channel_seed_levels`는 비균일 넓은 레벨(예: max 15)의 SD 경로에서 3-bit 상수로 떨어진다. 의도인지 미확인
- ㉴ 콘솔 print에 한국어가 있어 한국어를 못 내는 콘솔 인코딩에서 오류 가능성 (추정)
- ㉵ `_pm/TODO.md` 미완: config checker 허용값 확장, dv range 상한, mpi_runner 재설계와 슈퍼컴 이관, 후순위 로그 7종, 평가 대상 H와 LLR 반입
- ㉶ `_probe/` 결과: E=380에서 128프레임 0 에러 (약 196 it/s), E=500에서 512/512 실패 후 중단. 원본 커밋 `ecec8ae+dirty` 시점

### 컨벤션 요약

- ㉮ 이름: 모듈과 함수 snake_case, 클래스 PascalCase, 상수 UPPER_SNAKE, 모듈 밖에서 안 쓰는 것은 밑줄 접두. 디코더 변수명은 C++ 원본 용어 그대로. 치수 변수 대문자 허용. 이름 충돌: `E`(edge 수 / 에러 bit 수), `K`(정보 bit 수 / 헤더 최대 row degree), `th`(LLR 임계 / rber 채널 region 경계), `floor`(row flag / error floor)
- ㉯ 언어: 식별자, CSV 헤더, 진행 줄 지표는 영어. docstring, 주석, 예외 문구, md는 한국어
- ㉰ 오류: `ValueError`, `FileNotFoundError`, `NotImplementedError`, `SystemExit`. 예외를 잡는 곳은 세 곳만. "조용한 대체 금지"
- ㉱ 로그: `logging` 미사용, 전부 `print`
- ㉲ 테스트: `tests/` 없음. 검증 관습은 같은 seed 수치 완전 일치 회귀
- ㉳ 문서: 줄표와 가운뎃점 나열 금지 (가운뎃점은 곱셈 기호로 `_pm/` 밖 12건 잔존), 나열은 ㉮㉯㉰, 사용자 결정은 날짜와 함께 코드 docstring과 문서 양쪽에, C++ 대응은 함수 이름과 줄 번호를 괄호에
- ㉴ 파일명 규칙(코드가 파싱): `LLR_MATRIX_{HD|2SD|3SD}_*.txt`, 균일 생성물 `..._uniform_{bits}bit_max{max}_ch{..}_dv{..}_iter{..}.txt`, 실행 폴더 `YYMMDD_HHMMSS_{label}`, 밑줄 접두 폴더는 보조물

### 변경 금지로 읽히는 것

프로파일 `docs/profile/constraints.md` 1절에 근거와 함께 30행으로 정리했다. 요지: 상대 비교 전용, 단순화 형태는 Python에만, all-zero와 genie와 BER 집계 한 묶음, Ref-C 헤더와 DAO 형식 전용, 3-bit 전용, DECODER_CLASS 한 곳, src 무수정, base_run 재정의 0개, seed 하나, 입력 파일 외부 공급, HD iteration 1 클리어 안 함, 동점 반전, dv 미매칭 에러, `_cnu_update` 제자리 갱신, th = 레벨값, 균일 판별 값 기준, 채널 모드 전용, DV 내림차순 배치 전제, `edge_max_value`와 `channel_llr_*` 같은 배율, 이력물 보존.

## 프로파일과 어긋난 것

탐색 시점에 `docs/profile/`은 빈 양식이었고 이 문서와 함께 채웠다. 해당 없음.

## 미탐색 영역

- ㉮ 저장소 밖: `3_LDPC_ideas/새논문적용규칙.md`(교체 지점 정본), `4_H_matrix_tool`, C++ 원본, DAO 도구. 상속 경계의 "공식" 규칙은 코드 docstring 수준으로만 파악했으므로 프로파일 `replacement_points.md`가 원문과 어긋날 가능성은 판단하지 못했다
- ㉯ `_pm/done/`, `_pm/DONE.md` 본문, `_pm/tasks/20260808_review/`는 읽지 않았다 (개인 경로와 벤더 실값이 있는 파일 위치만 grep으로 확인)
- ㉰ 2SD/3SD 경로는 코드로만 읽고 실행하지 않았다. `count_cycles4`, `_detect_uniform_edge_mag`의 th_len==1 분기도 실행 검증 없음
- ㉱ `_probe_sweep`가 중단된 실행이라는 것은 파일 구성으로부터의 추정
