# 탐색 B 보고: 데이터 흐름과 보유 기법

> 작성: 2026-09-30 (explorer 에이전트 보고 원문, 메인이 저장)

근거 경로 표기: 아래 본문의 `pcm.py:NN` 등은 `src/` 아래 파일의 줄 번호다. 런처는 `workspace/base_run/run.py` (다른 실험 폴더의 run.py도 동일 내용).

## 확인한 것

### 1. H-matrix .qc 파싱 (pcm.py)

- ㉮ 헤더 형식: `N_b M_b` / `J K` / `z` / 빈 줄 / M_b행 x N_b열 shift 행렬, 행렬 뒤 내용 무시 (pcm.py:7-17). 실제 파일 `Input/H_matrix/example_18x147_z256.qc`:1-5는 `147 18`, `4 31`, `256`, 빈 줄, 행 (공백 구분). `Input/H_matrix/matrix_sel_1.txt`:1-5는 `145 15`, `11 52`, `256` (탭 구분, 뒤에 공백 다수). 두 파일 모두 확장자가 달라도 같은 로더로 읽음.
- ㉯ 로드 절차 (`QCCode.load` pcm.py:58-82): 빈 줄 제거 → lines[0] 두 정수 N_b, M_b (첫 줄이 정수 2개 아니면 에러) → lines[1] J, K → lines[2] z → lines[3:] 전부 이어 붙여 split, 앞 M_b*N_b개만 사용 (73-76) → J/K보다 실제 degree가 크면 에러 (78-81). 생성자에서 shift >= z면 에러 (28-29).
- ㉰ 메모리 자료구조 `QCCode` (pcm.py:24-46): `base` (M_b, N_b) int32, -1은 zero block. 스칼라 M_b, N_b, z, N=N_b*z, M=M_b*z, K=N-M, rate. edge 목록은 column 우선 정렬(lexsort) 1차원 배열 `edge_row`, `edge_col`, `edge_shift` (각 (E,) int32), `E` = base edge 수. `col_edges` = N_b개 리스트, 각 column block에 속한 edge 인덱스 배열 (44). `row_deg` (M_b,), `col_deg` (N_b,) bincount.
- ㉱ 연결 규칙: edge (i, j, s)에서 CN block i의 lane k는 VN block j의 lane (k+s) mod z와 연결. VN 정렬 → CN 정렬은 `np.roll(v, -s)`, 반대는 `np.roll(c, +s)` (pcm.py:4-5). `syndrome(bits)` (85-92)가 (..., N_b, z) → (..., M_b, z)로 이 규칙대로 XOR 누적.
- ㉲ 부수 유틸: `save` Ref-C 포맷 저장 (49-55), `count_cycles4` (94-110), `summary` (112-118).

### 2. LLR_MATRIX 텍스트 파일 (llr_matrix.py)

- ㉮ 파일 형식 (llr_matrix.py:11-15): 빈 줄 무시하고 순서대로 `num_parameter_each_set` / `num_dv` / `dv_from` / `dv_to` / `num_group` / `num_row_each_group` / `type_each_group` / `num_restart` / [`restart_iter`, num_restart>0일 때만] / `max_value` / `min_value` / row들. row 하나 = [dv별 (ch..., th...) x num_dv] + CSW + iter_start + iter_end + floor_flag (길이 num_dv*num_param+4, 검사 269-270).
- ㉯ 실제 파일 확인:
  - ㉠ `Input/LLR/LLR_MATRIX_HD_0.txt`:1-24: num_param 4, num_dv 4, dv_from `11 4 3 2`, dv_to `11 4 3 2`, 3그룹, 그룹당 row 1개, type 전부 1(CSW), restart 1개(iter 2), max `31 31 31 31`, min `0 0 0 0`. row1 `1 28 9 5 | 10 10 9 4 | 13 31 10 7 | 28 12 10 8 | -1 1 1 -1` (dv=11 구간 ch=1, th=[28,9,5]; 꼬리 CSW=-1, iter 1..1, floor -1). row2 전부 -1, iter 2..2 (restart row). row3 iter 3..5. 따라서 max_iter=5.
  - ㉡ `LLR_MATRIX_HD_1.txt`:1-21: 2그룹, restart 없음, row iter 1..1과 2..20 → max_iter 20.
  - ㉢ `LLR_MATRIX_2SD_toy0.txt`: num_param 5 (ch 2개 + th 3개), num_dv 1, dv 1..11, 3그룹 type 0(ITER), restart iter 11, rows iter 1..10 / 11..11 / 12..20. row 예 `12 4 8 4 2 -1 1 10 -1` (ch=[12,4], th=[8,4,2]).
  - ㉣ `LLR_MATRIX_3SD_toy0.txt`: num_param 7 (ch 4개 + th 3개), 구조 동일.
  - ㉤ `LLR_MATRIX_HD_matrix_sel_1.txt` (workspace/matrix_sel_1_HD/_probe/260818_225547_probe/ 사본): 8그룹, row 수 `1 5 5 7 6 10 10 13`, 전부 CSW type, restart 없음, iter 1..120. 다중 row CSW 그룹의 실례 (CSW 임계 984, 352, 96, 32 등 내림차순).
- ㉰ 모드 판별은 파일 내용이 아니라 파일명 정규식 `LLR_MATRIX_(HD|2SD|3SD)_` (llr_matrix.py:48, 237-241). ch 개수는 `MODE_CH_LEN` HD 1 / 2SD 2 / 3SD 4 (45), th 개수 = num_param - ch 개수 (133).
- ㉱ edge 레벨(edge_mag) 판별: 파일에 없으므로 `_detect_uniform_edge_mag` (92-120)가 전 row와 전 dv의 th가 같고 공차 d 등차 감소이며 마지막 항이 2d-1이면 균일 생성물로 보고 레벨 복원. 아니면 None → 기본 [7,5,3,1], 이때 th가 3개가 아니면 NotImplementedError (136-142). 파일명에 uniform이 있는데 패턴이 아니면 에러 (275-279).
- ㉲ 파싱 결과 자료구조 `LLRMatrix` (123-170): `row_values` (R, num_dv, num_param) float32 → 뷰 `row_ch` (R, num_dv, ch_len), `row_th` (R, num_dv, th_len); `row_csw` (R,) int64; `row_iter` (R, 2) int32; `max_iter` = row_iter[-1, 1] (162); `group_slices` [(row_start, row_end)]; `group_type` 리스트; `restart_iters` set; `edge_mag` float32 내림차순, 길이 th_len+1; `dv_from`, `dv_to` int32; `max_value`, `min_value` int32 (저장 시 재기록용 외 소비처 없음).
- ㉳ `_validate` (172-226): 그룹 iteration 구간 겹침 금지, 1..max_iter 빈틈 금지, ITER 다중 row 그룹 내부 연속, restart 그룹은 단일 row 단일 iteration이며 마지막 그룹이면 안 됨, th 비단조는 경고만.
- ㉴ 런타임 API: `col_dv_idx(code)` (347-357) → (N_b,) column별 dv 구간 인덱스, 미매칭 dv는 에러. `row_index(iteration, prev_csw)` (369-386) → 그룹 탐색(`_group_of_iter` 362-367, 정방향 첫 매칭) → ITER 그룹 또는 단일 row면 그 row를 전 프레임에, CSW 그룹이면 row_start+1부터 순회하며 `prev_csw <= row_csw[row]`인 row로 갱신(결과적으로 아래에서부터 첫 매칭, 없으면 그룹 첫 row) → (활성 프레임 수,) int64. `is_restart` (359-360). `has_uniform_levels` (388-400), `needs_csw` (402-406).
- ㉵ 균일 생성 경로: `edge_quantization_levels(bits, max)` (60-89): 레벨 수 2^(bits-1), step=(max+1)/레벨 수, step 1이면 `uniform_edge_mag` [top..1, 1]과 th [top..1], step 2 이상이면 edge_mag = range(max, 0, -step), th = edge_mag[:-1]. `make_internal_uniform_matrix` (285-316): 그룹 1개 ITER, iter 1..max_iter, restart 없음, dv 구간 [1, dv_max] 하나, ch 전 dv 공통, csw -1, floor -1. `save` (318-344)로 DAO 포맷 정수 저장 후 `load`로 다시 읽어 파일 경로와 동일하게 소비 (run.py:423-441).

### 3. config JSON 처리 (run.py)

- ㉮ `load_config(path)` (270-390): `json.load` → dict를 제자리 수정. `base_dir = dirname(abspath(config 경로))` (277)이 모든 상대 경로의 기준. 허용 키 집합 `_TOP_KEYS` 등 (99-111)으로 키맵 검사, `_`로 시작하는 키는 무시 (120-122).
- ㉯ 변환 결과 (내부 자료 구조):
  - ㉠ `config["H_matrix"]`: `{"dir","file"}` → `os.path.join` 후 상대면 base_dir 결합한 경로 문자열 (147-155, 287-288).
  - ㉡ `config["decoder"]`: `use_input_llr_matrix` 기본 True (292); `mode` 기본 "HD" (299); `max_iter` 있으면 정수 검사 (302-303); `channel_llr_{HD,2SD,3SD}` 길이 = region 수 검사 (304-314); `use_default_edge_quantization` 기본 True (315); `edge_quantization` setdefault {} 후 bits 기본 3, max 기본 7 채움 (258-267). true 경로면 `decoder["llr_matrix"]`가 경로 문자열로 대체 (323-324); false 경로면 max_iter와 channel_llr_{mode} 필수, 커스텀 양자화면 조합 제약 검사 (326-337).
  - ㉢ `config["output"]`: dir 기본 `base_dir/Sim_Output`, 상대면 base_dir 결합 (343-345); `save_llr_matrix` 기본 True (346); csv_prefix, label 문자열 검사.
  - ㉣ `config["seed"]` = run.seed (기본 0, 최상위로 복사) (357). run 섹션의 max_frame_errors 50, max_frames 20000, frames_per_batch 128, progress_interval_frames 100 기본값은 `_RUN_DEFAULTS` (116-117)에 있고 검증만 하며 config에 써넣지 않음. 소비는 `run_experiment`가 `.get(key, _RUN_DEFAULTS[key])` (557-563). `print_progress` 기본 True (361), `stop_below_fer` None 허용, 양수만 (365-370).
  - ㉤ `config["log"]`: `{"enabled": bool, 항목키 7개: enabled and 값}`으로 평탄화 (385-387).
  - ㉥ `config["channels"]`: `_check_channels` (183-247) → 리스트 `[{"type", "points", ("SER","SCR" strong_error만)}]`. type은 문자열 또는 리스트, 중복 금지, `chan.CHANNELS` 안에 있어야 함. 값 공간 rber는 0<p<0.5, fixed_error는 0 이상 정수, `int(1e6*값)` 중복 금지 (175-179, 난수 스트림 키와 CSV 파일명 충돌 방지). rber type은 rber 공간, fixed_error와 strong_error type은 fixed_error 공간을 공용 소비.
- ㉰ `setup(config, decoder_class)` (393-446): `QCCode.load` → use_input이면 파일 존재 확인, 아니면 합성 매트릭스를 `output.dir/_generated/LLR_MATRIX_{mode}_uniform_{bits}bit_max{max}_ch{ch}_dv{dv_max}_iter{max_iter}.txt`로 저장 (430-439) → `LLRMatrix.load` → `config["decoder"]["_used_llr_matrix_path"]` 기록 (442) → `decoder_class(code, llr_matrix=llr_matrix)` (445), None이면 BaseDecoder.
- ㉱ 진입: `main(argv, decoder_class)` (780-791): load_config → setup → print_experiment_summary → create_run_dir → run_experiment → report. 실험 폴더 런처 (workspace/base_run/run.py:11-33)는 상위로 올라가며 `2_LDPC_base/src` 폴더를 찾아 sys.path에 넣고 `main([config], decoder_class=DECODER_CLASS)` 호출. 이 testbed 사본에는 `2_LDPC_base` 폴더가 없음을 Glob으로 확인했으므로 런처는 SystemExit로 끝날 것으로 추정 (실행은 안 해봄). 루트에서 `python -m src.run <config>`는 코드상 동작 경로.

### 4. 시뮬레이션 루프 (sim.py)

- ㉮ `run_fer_point` (29-167) 누적자 (74-83): `frames`, `errors` 스칼라; `success_iteration_sum`; `total_residual_info_err_bits`; `iter_hist` (max_iter+1,) int64 ([k]=iteration k 성공 수, [0]=실패 수); `total_active_frames`, `total_csw`, `total_bit_err` (max_iter,) int64; `total_bit_err_by_dv` (max_iter, num_dv) int64; `fail_frame_details` 리스트.
- ㉯ 루프 (95-137): `while frames < max_frames and errors < max_frame_errors`; `batch = min(frames_per_batch, max_frames - frames)`; `channel_fn(batch, rng)` → `decoder.decoder_main(channel_out, log)` → `errors += (~success).sum()`, `np.add.at(iter_hist, decode_success_iteration, 1)`, 로그 합산, fail_detail이면 프레임 번호 `frames + k`로 상세 기록; `frames += batch`.
- ㉰ 종료 조건: 위 while 조건 두 개 (max_frame_errors 도달 또는 max_frames 소진). `stop_below_fer`는 sim.py가 아니라 run.py `run_experiment`의 포인트 루프에서 `fer < stop_below_fer`면 break (597-598), 채널 단위이고 다음 채널은 계속.
- ㉱ 난수 seed 파생: 포인트마다 `np.random.default_rng([seed, channel_index, int(1e6 * point)])` (run.py:586). 같은 Generator를 채널 함수의 메시지 생성과 채널 잡음이 순서대로 소비하므로 frames_per_batch가 같아야 수치 재현 (README.md:120-121).
- ㉲ 프레임 배치 배열: 채널 출력 hd (B, N_b, z) uint8이 디코더로 들어가고, 디코더 결과는 (B,) 단위 배열 (아래 6절).
- ㉳ 성공 판정(genie): decoder.py `_collect_error_metrics` (316-334)에서 `decision_bits[:, :N_b-M_b, :]`가 전부 0이면 성공 (정답 all-zero 전제, decision_bits의 1이 에러). `_check_errors` (433-452)가 성공 프레임을 확정하고 배치에서 제외.
- ㉴ 진행 줄 (121-137): `progress_interval_frames` 단위로 터미널이면 `\r` 제자리 갱신, `summary_path`가 있으면 `_rewrite_file_tail` (21-26)로 파일 끝을 제자리 갱신하다가 최종 결과 줄로 대체 (164-166).
- ㉵ 결과 dict (142-161): frames, errors, fer, `post_fec_ber` = 정보 구간 잔여 에러 합/(frames*K), `avg_decoding_iteration` = (성공 iteration 합 + errors*max_iter)/frames, sec, fps, ips, iter_hist, log 시 `iteration_totals` {active_frames, csw_sum, bit_err_sum, bit_err_by_dv_sum}, fail_detail 시 `fail_frame_details`, `summary_line`. `save_csv` (170-182) 열: param, fer, post_fec_ber, frames, errors, avg_decoding_iteration, sec.

### 5. 채널 모델 (channel.py)

- ㉮ 공통 시그니처: `(code, cw, point, random_generator, mode=..., [scr, ser])` (run.py:524-528에서 호출). cw는 encoder.encode의 (B, N_b, z) uint8 all-zero. 출력 dict `{"mode", "hd", "sd", "cc"}` (channel.py:9-11): hd (B, N_b, z) uint8 read bit, sd와 cc는 None 또는 (B, N_b, z) uint8.
- ㉯ `rber_channel` (43-68): `dev_from_rber` (37-40, 역 Q함수 24-34) → BPSK `1-2cw` + N(0, dev) → hd = cwr<0. HD면 종료. SD면 `llr_mag = |2cwr/var|`, `th_k = 2*r_offset_k/var` (`_R_OFFSET` 2SD (0.35,), 3SD (0.15, 0.35, 0.55), 21). 2SD: sd = llr_mag>=th[0]. 3SD: sd = llr_mag>=th2, cc = (llr_mag>=th3) 또는 (llr_mag<th1). 지원 모드 HD/2SD/3SD.
- ㉰ `fixed_error_channel` (78-88): HD 전용. `_rand_positions` (71-75, argpartition)로 프레임별 정확히 n_err개 위치 flip. (B, N)으로 펴서 처리 후 (B, N_b, z)로 복원.
- ㉱ `strong_error_channel` (91-135): 2SD 전용. e2=round(E*SER) strong 에러, c2=round((N-E)*SCR) strong 정정, c1=N-E-c2 weak 정정. sd 초기 1(strong). 에러 위치 E개 argpartition → 행별 `permuted` 셔플 뒤 e2 이후를 weak → 정정 중 rand 마스킹(에러 위치에 2.0)해 하위 c1개를 weak.
- ㉲ 등록 `CHANNELS` (138-142)와 지원 모드 `CHANNEL_MODES` (145-149). 모드 호환은 run.py `_check_channel_mode` (504-512)가 디코더의 `llr_matrix.mode`와 비교하고, 측정 전 전 채널을 사전 확인 (568-569).
- ㉳ HD/2SD/3SD 차이가 디코더에 들어가는 지점: decoder.py `_read_channel_input` (223-247)에서 `region` = 2SD `1-sd`, 3SD `2*(1-sd) + (cc ^ sd)` (0 very strong, 1 normal strong, 2 normal weak, 3 very weak), HD는 None. region이 ch 열 인덱스가 됨 (386-388).

### 6. 디코더 (decoder.py)

- ㉮ `BaseDecoder.__init__` (99-118): `max_iter = llr_matrix.max_iter`, `_col_dv_idx` (N_b,), `_cols_by_dv` (dv 구간별 column 목록), `_edge_mag` float32, `_uniform_levels` bool, `_seed_levels` (SD Pre 단계 채널 magnitude: 2SD [5,1], 3SD [7,5,3,1]는 C++ 고정 상수, 균일 레벨이면 1..top 등분, 120-134). 모드는 llr_matrix.mode가 결정.
- ㉯ `decoder_main(channel_out, collect_profile=False, log=None)` (475-508) 흐름: `_read_channel_input` → `_init_state` → `for iteration in 1..max_iter: _run_iteration → _record_iteration → _check_errors (True면 break)` → `_build_result`. iteration 번호는 1부터.
- ㉰ 상태 배열 `_DecodeState` (54-96), 값은 `_init_state` (249-292)가 채움. B는 활성 프레임 수(압축되며 줄어듦), 결과 버퍼는 원 배치 크기 고정:
  - ㉠ 프레임 데이터: `read_bit` (B, N_b, z) uint8; `region` (B, N_b, z) int64 또는 None; `seed_mag` (B, N_b, z) float32 (SD만); `decision_bits` (B, N_b, z) uint8 (read_bit 사본, 1=에러); `syndrome` (B, M_b, z) = `code.syndrome(read_bit)` 1회 계산 후 유지; `prev_csw` (B,) int64 초기 = syndrome 합.
  - ㉡ CN 상태: `min1`, `min2` (B, M_b, z) float32 초기 RESET = edge_mag[0]; `min1_pos` (B, M_b, z) int32 초기 -1; `check_sum` (B, M_b, z) uint8 0; `edge_sgn` (B, E, z) uint8 0.
  - ㉢ 결과와 로그: `idx_active` (B,) 원 배치 인덱스; `success` (B,) bool; `decode_success_iteration` (B,) int32; `final_err_bits`, `final_info_err_bits`, `final_csw` (B,) int64; `final_err_by_dv` (B, num_dv) int64; `log_active`, `log_csw_sum`, `log_err_sum`, `log_err_by_dv_sum` 리스트.
  - ㉣ iteration 임시값: `cur_ch_all` (활성, num_dv, ch_len), `cur_ch` (활성, num_dv), `cur_th` (활성, num_dv, th_len), `edge_clear` bool, `frame_err`, `err_bits`, `info_err_bits`, `err_by_dv`.
- ㉱ SD Pre 단계 `_seed_channel_magnitudes` (294-314): column 순회하며 각 edge에 sign=read_bit, mag=seed_mag를 `roll(-shift)`해 `_cnu_update(edge_clear=True)`로 min1/min2에 심고, 끝에 check_sum과 edge_sgn을 0으로 되돌림. `_init_state`에서 region이 있으면 1회 호출 (276-277).
- ㉲ `_run_iteration` (336-370) 단계:
  - ㉠ `edge_clear = _is_edge_clear_iter(iteration)` (137-144, restart iteration만 True) → True면 min1/min2=RESET, min1_pos=-1, check_sum=0, edge_sgn=0, syndrome은 유지 (343-349).
  - ㉡ SD이고 restart iteration이면 Pre 재실행 + `decision_bits[:] = read_bit` + 에러 지표 + `prev_csw` 재계산 후 return (row 값 미사용) (350-359).
  - ㉢ `table_row_idx = llr_matrix.row_index(iteration, prev_csw)` → `cur_ch_all`, `cur_ch`, `cur_th` 프레임별 선택 (360-363).
  - ㉣ `for col in _column_order(iteration): _process_column` (365-366; `_column_order` 기본 range(N_b), 146-148).
  - ㉤ `_collect_error_metrics` → `prev_csw = (check_sum ^ syndrome).sum` (368-370, Compute_CSW 대응).
- ㉳ `_process_column(state, iteration, col)` (372-413):
  - ㉠ `sum_t` 초기 = 채널 항 (항상 +). HD: `cur_ch[:, dv_idx]` 브로드캐스트 (382-384); SD: `take_along_axis(cur_ch_all[:, dv_idx, :], region[:, col, :])` (386-388). float32.
  - ㉡ 각 edge: `_c2v_reconstruct` (150-157): mag = (min1_pos==edge ? min2 : min1), sign = syndrome ^ check_sum ^ edge_sgn → `np.roll(c2v, +shift)`로 VN 정렬 → `vnu_in` 목록에 저장하고 sum_t에 누적 (390-398).
  - ㉢ `flip = _vn_decide(sum_t)` = `sum_t <= 0` (159-162, 동점 반전) → `decision_bits[:, col, :] = read_bit ^ flip` (403).
  - ㉣ 각 edge: `vnu_out_raw = sum_t - vnu_in` (407) → `_vnu_quantize(raw, vnu_in, cur_th[:, dv_idx, :])` (164-187): 캐스케이드 |raw| >= th_k → edge_mag[k] (위쪽 th 우선), 전부 아니면 마지막 레벨; 균일 레벨이면 `_uniform_saturate` = max(min(|raw|, top), 1) (189-195); raw==0이면 부호는 vnu_in에서 → `roll(-shift)`로 CN 정렬 → `new_sgn = vnu_out<0`, `new_mag = |vnu_out|` → `_cnu_update` (197-220): edge_clear 아니면 remove old (check_sum ^= edge_sgn[edge], 자신이 min1이면 min1=min2, min2=RESET), insert new (`<=` 비교, 새 min1이면 min2=RESET로 기존 min1을 내리지 않음), check_sum ^= new_sgn, edge_sgn[edge]=new_sgn. 제자리 갱신.
- ㉴ `_record_iteration` (415-431): log 리스트 append (csw는 prev_csw 합, bit_err는 codeword 전체 err_bits 합, by_dv), `final_err_bits`와 `final_info_err_bits`를 idx_active 위치에 덮어씀, fail_detail이면 final_csw와 final_err_by_dv, collect_profile이면 (활성 수, 평균 에러) 튜플.
- ㉵ `_check_errors` (433-452): `ok = ~frame_err`로 success와 decode_success_iteration 확정 → 전부 성공 또는 iteration==max_iter면 True → 아니면 keep 마스크로 read_bit, syndrome, prev_csw, decision_bits, region, seed_mag, min1, min2, min1_pos, check_sum, edge_sgn을 압축.
- ㉶ `_build_result` (454-472): success, decode_success_iteration, final_err_bits, final_info_err_bits 항상. profile, log_active, log_csw_sum, log_err_sum, log_err_by_dv_sum, final_csw, final_err_by_dv는 옵션.
- ㉷ 구현된 알고리즘 기법 (이름과 근거):
  - ㉠ 배치 벡터화 quantized min-sum: min1/min2 두 최솟값 CN 상태와 z lane과 프레임 배치를 numpy 축으로 동시 처리 (decoder.py:1, 38, 197-220).
  - ㉡ syndrome-aided flip 도메인: read_bit 고정, 모든 메시지가 read_bit 기준 상대값, C2V sign = syndrome ^ check_sum ^ edge_sgn (17-31, 156).
  - ㉢ column 순차(layered) 스케줄과 즉시 CN 갱신: column 하나 처리 후 바로 CN 상태 갱신, 뒤 column이 갱신값을 봄 (365-366, 405-413).
  - ㉣ 테이블 기반 iteration/CSW 적응 파라미터: iteration 그룹과 직전 CSW로 row를 골라 ch(채널 LLR)와 th(양자화 임계)를 프레임별로 바꿈 (llr_matrix.py:369-386, decoder.py:360-363).
  - ㉤ restart(Edge Clear): 지정 iteration에 CN 상태 클리어, restart row의 -1을 산술에 그대로 써서 순수 syndrome bit-flip iteration (137-144, 342-349; llr_matrix.py:25-28).
  - ㉥ SD Pre 단계: 2SD/3SD 채널 신뢰도 magnitude를 CN에 심는 초기화, SD restart도 Pre 재실행 (294-314, 350-359).
  - ㉦ edge 양자화 3-bit {7,5,3,1}과 n-bit 균일 확장, th 캐스케이드 (llr_matrix.py:60-89, 142; decoder.py:164-195).
  - ㉧ min1 교체 시 min2=RESET (HW 특성 재현) (215-216).
  - ㉨ genie 성공 판정과 성공 프레임 마스킹(배치 압축) (316-334, 433-452).
  - ㉩ 동점(sum_t==0) 반전 (159-162).
  - ㉪ 없는 것 (차이.md:17-27): BF(hard bit flipping) 구간, error floor 감지 상태머신, power stopping, 1.5SD, dual update, pipeline store 지연, CRC 조기종료, HCU, 쇼트닝/펑처링.

### 7. 출력

- ㉮ 실행 폴더 `create_run_dir` (run.py:715-733): `output.dir/{YYMMDD_HHMMSS}_{label}` (label = output.label 없으면 첫 채널 type), 측정 시작 전 생성. `config.json` = 원본 config 파일을 `shutil.copy` (725, 파싱 결과가 아니라 원문). `summary.txt` 머리 = run 이름, code commit (`_git_commit_hash` 603-618, 미커밋 변경이면 `+dirty`), start 시각, 실험 요약 불릿 (`_experiment_summary_lines` 458-493: H matrix, code 치수, col/row degree 히스토그램, LLR matrix 이름과 출처, max iteration, decoder 클래스, seed, channels, run 값, log 항목).
- ㉯ summary.txt 본문: 포인트별 진행 줄과 결과 줄을 sim.py가 실시간 기록 (121-137, 164-166). 실제 예시 `workspace/matrix_sel_1_HD/_probe/260818_225547_probe/summary.txt`:1-17.
- ㉰ `report` (736-777) 저장 파일:
  - ㉠ `{csv_prefix}_{label}.csv`: `save_csv` (sim.py:170-182), 항상. 예시 `_probe/260818_225547_probe/fer_fixed_error.csv`.
  - ㉡ `log_iter_{label}_p{param}.csv`: `_write_iter_log` (627-653), csw_per_iter/bit_err_per_iter/bit_err_by_dv 중 하나라도 켜면. 열 iter, active_frames, [csw_mean], [bit_err_mean], [bit_err_{dv라벨}_mean]. 평균 = 합/활성 프레임.
  - ㉢ `log_iter_hist_{label}_p{param}.csv`: `_write_iter_hist_log` (656-677), iter_histogram/fer_vs_iter 시. 열 iter, [success_at_iter], [fer_if_max_iter_k = 1 - 누적 성공/frames].
  - ㉣ `log_fail_{label}_p{param}.csv`: `_write_fail_log` (680-689), fail_frame_detail 시. 열 frame, final_err_bits, final_csw, err_{dv라벨}.
  - ㉤ LLR matrix 사본: `_used_llr_matrix_path`를 basename 그대로 복사 (764-768), save_llr_matrix 기본 True.
  - ㉥ `fer_curves.png`: `_plot_fer_curves` (692-712), fer_curve_png 시, 로그 y축, 0 에러 포인트는 0.5/frames 위치에 역삼각 상한 마커. 실패해도 측정 결과는 남김 (770-775).
- ㉱ 로그 항목별 수집 위치와 목적지 (JSON 키 → 내부 항목 매핑 `_LOG_TO_ITEM` run.py:113-114, 디코더 허용 집합 `LOG_ITEMS` decoder.py:51):
  - ㉠ csw_per_iter → "csw": decoder.py:419-420 (`prev_csw.sum()` 매 iteration) → `log_csw_sum` (464) → sim.py:107-108 `total_csw` → log_iter csv `csw_mean`.
  - ㉡ bit_err_per_iter → "bit_err": decoder.py:421-422 (`err_bits.sum()`, codeword 전체) → `log_err_sum` → sim.py:109-110 → `bit_err_mean`.
  - ㉢ bit_err_by_dv → "bit_err_by_dv": decoder.py:329-332 (`need_by_dv`일 때 dv 구간별 합), 423-424 → sim.py:111-113 → `bit_err_{dv}_mean`.
  - ㉣ fail_frame_detail → "fail_detail": decoder.py:427-429 (`final_csw`, `final_err_by_dv`), 470-471 → sim.py:114-119 `fail_frame_details` → log_fail csv.
  - ㉤ `log_active`: 어느 로그 항목이든 켜면 decoder.py:418 → sim.py:105-106 → `active_frames` 열.
  - ㉥ iter_histogram, fer_vs_iter: 디코더 로그가 아님. `iter_hist`는 sim.py:103에서 항상 수집되고, 두 키는 CSV 저장 여부만 결정 (run.py:755-759).
  - ㉦ fer_curve_png: 그림 저장 여부만.
  - ㉧ post_fec_ber: 로그와 무관하게 항상. decoder.py:326-327 `info_err_bits` → 426 `final_info_err_bits` → sim.py:102, 144 → FER csv.
  - ㉨ 후순위 로그 7종 미구현 (README.md:155, 목록은 `_pm/TODO.md`에 있다고 하며 읽지 않았음).

### 8. encoder.py 현재 동작

- ㉮ `generate_message(code, batch, rng)` (13-15): (batch, K) uint8 무작위 비트. 난수를 실제로 소비하므로 채널 잡음의 난수 위치에 영향.
- ㉯ `encode(msg, code)` (18-21): msg 무시, (batch, N_b, z) uint8 all-zero 반환 (임시). docstring (3-8)에 실제 인코딩으로 바꾸면 디코더의 정답 참조(genie all-zero)와 sim.py BER 집계도 함께 바꿔야 한다고 명시.
- ㉰ 호출 위치: run.py `_make_channel_fn` (515-530)의 `channel_fn(batch, rng)` 안에서 msg → cw → 채널 함수 순서.

## 관계와 흐름

```
config.json ──load_config──▶ config dict
   (경로 결합, 기본값, 검증)      │ H_matrix 경로, decoder.llr_matrix 경로 또는 합성 파라미터,
                                 │ channels [{type, points}], seed, log 평탄화, output
                                 ▼
.qc 파일 ──QCCode.load──▶ QCCode(base, edge_row/col/shift, col_edges, N/M/K)
LLR 파일 ──LLRMatrix.load──▶ LLRMatrix(row_ch, row_th, row_iter, row_csw, edge_mag, max_iter)
   (또는 make_internal_uniform_matrix → save → load)
                                 │ setup: decoder_class(code, llr_matrix)
                                 ▼
create_run_dir ─▶ Sim_Output/YYMMDD_HHMMSS_label/{config.json, summary.txt 머리}
                                 ▼
run_experiment: for 채널 index, for point:
    rng = default_rng([seed, ch_idx, int(1e6*point)])
    run_fer_point: while frames<max_frames and errors<max_frame_errors:
        batch ─▶ generate_message (B,K) ─▶ encode all-zero (B,N_b,z)
              ─▶ channel (B,N_b,z) hd[, sd, cc]
              ─▶ decoder_main:
                   read_bit, region ─▶ syndrome (B,M_b,z), CN 상태 RESET [SD: Pre seeding]
                   iteration 1..max_iter:
                     [restart: CN 클리어 / SD Pre 재실행]
                     row_index(iteration, prev_csw) → ch, th (프레임별)
                     column 순차: sum_t = ch + Σ roll(C2V) → flip = sum_t<=0
                                  → decision_bits; vnu_out = quantize(sum_t - vnu_in)
                                  → roll → CNU 갱신 (min1/min2/min1_pos/check_sum/edge_sgn)
                     prev_csw = Σ(check_sum ^ syndrome); 로그 집계
                     genie: info 구간 decision_bits 전부 0 → 성공, 배치 압축
                   ─▶ {success, decode_success_iteration, final_*_err_bits, log_*}
        집계(errors, iter_hist, totals, fail details), 진행 줄 → summary.txt 제자리 갱신
    결과 줄 → summary.txt; stop_below_fer면 채널 내 남은 포인트 중단
                                 ▼
report ─▶ fer_{label}.csv, log_iter_*.csv, log_iter_hist_*.csv, log_fail_*.csv,
          LLR matrix 사본, fer_curves.png
```

- ㉮ 자료의 축 규약: 프레임 배치 B x column block N_b x lane z (VN 정렬), CN 정렬은 B x M_b x z, edge 상태는 B x E x z. VN과 CN 사이 이동은 항상 `np.roll(±shift, axis=-1)` (pcm.py:4-5, decoder.py:308-309, 396, 409).
- ㉯ 모드(HD/2SD/3SD)의 단일 출처는 LLR matrix 파일명이고, 채널 dict의 "mode"와 대조(decoder.py:230-232), 채널 지원 모드와 대조(run.py:504-512)한다. 파일 로드 경로에서는 config의 decoder.mode와 max_iter가 읽히지 않는다 (run.py:296-298).
- ㉰ 디코더 파라미터의 단일 출처는 LLRMatrix다: max_iter, edge_mag(양자화 레벨), ch와 th 테이블, restart iteration, dv 구간. BaseDecoder는 이 값 외에 설정을 받지 않는다 (decoder.py:100-118).
- ㉱ 난수 소비 순서는 포인트마다 새 Generator에서 메시지 생성 → 채널 순서이며 배치 크기가 소비 경계라 frames_per_batch가 재현 조건에 들어간다.

## 못 본 것과 추정

- ㉮ 실행은 하지 않았다. 실험 폴더 런처(workspace/*/run.py:11-17)가 찾는 `2_LDPC_base/src` 폴더가 이 testbed 경로 상위에 없음을 Glob으로 확인했으므로, 이 사본에서 `python run.py`는 SystemExit로 끝날 것으로 추정한다. `python -m src.run <config>`는 루트에서 동작할 것으로 보이나 미실행.
- ㉯ decoder.py:46이 참조하는 `docs/새논문적용규칙.md`는 docs/에 없음 (docs에는 차이.md, profile/, adr/만 존재). README.md:163은 외부 `3_LDPC_ideas/새논문적용규칙.md`를 가리키며 이 저장소 밖이라 미확인.
- ㉰ `_pm/` 폴더는 지시대로 읽지 않았다. README.md:155의 "후순위 로그 7종 미구현" 목록은 미확인.
- ㉱ `.gitignore` 존재 여부는 Glob으로 잡히지 않아 미확인 (`_generated/`와 `Sim_Output/`이 git 무시 대상이라는 것은 README 서술만 확인).
- ㉲ `workspace/matrix_sel_1_HD/_probe.json`은 열지 않았다. `4_H_matrix_tool`, `0_LDPC_original`, `1_LDPC_revised`(C++ 원본)는 저장소 밖이라 차이.md의 대응 서술만 인용했다.
- ㉳ docs/profile/ 다섯 문서는 모두 빈 템플릿임을 확인했다 (overview.md, structure.md, replacement_points.md, techniques.md, constraints.md). docs/adr/README.md도 목록이 비어 있다.
- ㉴ 표면 탐색으로 남긴 부분: `_detect_uniform_edge_mag`의 th_len==1 분기(llr_matrix.py:102-105)와 `count_cycles4`(pcm.py:94-110)는 읽었으나 실제 입력으로 검증하지 않았다. `_plot_fer_curves`의 matplotlib 동작도 미실행.
