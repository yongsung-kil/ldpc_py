---
title: 구조
tags: [profile, structure]
---
# 구조 (모듈 지도와 흐름)

> onboard와 explore 스킬이 채운다 (최초 2026-09-30). 언어에 기대지 않는 낱말로 적고, 근거 파일과 줄을 붙인다. 경로는 저장소 루트 기준이다.

## 1. 모듈 지도

| 모듈 | 역할 | 위치 | 들어오는 것 | 나가는 것 |
|---|---|---|---|---|
| 부호 (`QCCode`) | H-matrix 파일 로드와 저장, edge 목록, syndrome 계산 | `src/pcm.py:23-118` | H 파일 경로 | `base` (M_b, N_b), `edge_row`, `edge_col`, `edge_shift` (E,), `col_edges`, `col_deg`, `row_deg`, N, M, K, rate |
| 인코더 | 정보 비트 생성과 인코딩 자리 (현재 all-zero 반환 임시) | `src/encoder.py:13-21` | 부호, 배치 크기, 난수 생성기 | codeword (B, N_b, z) uint8 |
| 채널 | rber, fixed_error, strong_error 3종. 레지스트리 `CHANNELS`, 지원 모드 `CHANNEL_MODES` | `src/channel.py:43-149` | 부호, codeword, 포인트 값, 난수 생성기, mode, (SER, SCR) | dict `{"mode", "hd", "sd", "cc"}`, hd는 (B, N_b, z) uint8 |
| LLR 테이블 (`LLRMatrix`) | DAO 파일 파싱과 검증, 균일 매트릭스 합성과 저장, iteration/CSW별 row 선택, column별 dv 구간 | `src/llr_matrix.py:123-411` | 파일 경로 또는 합성 파라미터 (mode, max_iter, 채널 LLR, edge 레벨, dv_max) | `row_ch`, `row_th`, `row_iter`, `row_csw`, `edge_mag`, `max_iter`, `mode`, `restart_iters`, `row_index()`, `col_dv_idx()` |
| 디코더 (`BaseDecoder`) | 배치 벡터화 syndrome-aided quantized min-sum. 교체 지점 6개와 단계별 함수 7개 | `src/decoder.py:99-508` | 부호, LLR 테이블 (생성자), 채널 dict와 log 집합 (`decoder_main`) | dict `success`, `decode_success_iteration`, `final_err_bits`, `final_info_err_bits` (+ `log_*`, `final_csw`, `final_err_by_dv`) |
| 측정 루프 | 한 포인트의 배치 while 루프, 집계, 진행 줄, CSV 저장 | `src/sim.py:29-182` | 부호, 채널 함수, 디코더, 난수 생성기, 종료 조건, log | point_result dict (frames, errors, fer, post_fec_ber, avg_decoding_iteration, sec, iter_hist, iteration_totals, fail_frame_details, summary_line) |
| 실행 (`run`) | 설정 로드와 검증, 구성, 실행 폴더, 채널과 포인트 순회, 결과 저장, CLI | `src/run.py:270-791` | config JSON 경로, 디코더 클래스 (주입) | 실행 폴더 안 파일들 |
| 런처 | 실험 폴더에서 부모 폴더로 올라가며 `2_LDPC_base/src`가 있는 조상을 찾아 그 `2_LDPC_base`를 `sys.path`에 넣고, `main`에 config와 디코더 클래스를 넘김 | `workspace/*/run.py` (5개 동일, 33줄) | 명령 인자 (config 경로들) | `main([config], decoder_class=DECODER_CLASS)` 호출 |

import 방향: `run` → {`channel`, `encoder`, `decoder`, `llr_matrix`, `pcm`, `sim`}, `sim` → `decoder`, `__init__` → {`pcm`, `decoder`, `channel`, `encoder`, `sim`}. `pcm`, `encoder`, `channel`, `llr_matrix`, `decoder` 다섯은 `src/` 안의 다른 모듈을 import하지 않는 잎 모듈이다 (서드파티는 numpy만, `llr_matrix`는 표준 라이브러리 os, re, warnings도 쓴다). `decoder`는 부호와 LLR 테이블 객체를 생성자 인자로 받아 속성 이름으로만 쓴다 (`src/decoder.py:100-118`). 순환 없음. `src/__init__.py:6-10`의 공개 API는 `QCCode`, `BaseDecoder`, `channel`, `encoder`, `sim`이다.

## 2. 호출 관계

```
workspace/{실험}/run.py            (런처. 이 사본에서는 2_LDPC_base 부재로 SystemExit)
└─ src.run.main(argv, decoder_class)                                   src/run.py:780-791
   ├─ load_config(path)            키맵, 필수값, 값 제약 검사와 정규화     src/run.py:270-390
   ├─ setup(config, decoder_class) QCCode.load                          src/run.py:405
   │                                LLRMatrix.load                        src/run.py:441
   │                                  또는 make_internal_uniform_matrix → save → load   src/run.py:412-440
   │                                decoder_class(code, llr_matrix=...)   src/run.py:443-445
   ├─ print_experiment_summary                                          src/run.py:496
   ├─ create_run_dir               실행 폴더, config 사본, summary.txt 머리 src/run.py:715-733
   ├─ run_experiment               채널 × 포인트 루프                     src/run.py:548-600
   │   ├─ _check_channel_mode (전 채널 사전 확인)                        src/run.py:504-512, 568-569
   │   ├─ rng = default_rng([seed, channel_index, int(1e6*point)])       src/run.py:586
   │   ├─ _make_channel_fn         generate_message → encode → CHANNELS[type]  src/run.py:515-530
   │   └─ sim.run_fer_point        배치 while 루프                        src/sim.py:29-167
   │        └─ decoder.decoder_main(channel_out, log)                    src/decoder.py:475-508
   │             ├─ _read_channel_input                                  src/decoder.py:223-247
   │             ├─ _init_state (SD면 _seed_channel_magnitudes)          src/decoder.py:249-314
   │             └─ iteration 1..max_iter
   │                  ├─ _run_iteration                                  src/decoder.py:336-370
   │                  │    ├─ [_is_edge_clear_iter] → CN 상태 클리어      src/decoder.py:342-349
   │                  │    ├─ llr_matrix.row_index(iteration, prev_csw)  src/decoder.py:360
   │                  │    └─ for col in [_column_order]: _process_column src/decoder.py:365-366
   │                  │         ├─ [_c2v_reconstruct] × edge → sum_t      src/decoder.py:390-398
   │                  │         ├─ [_vn_decide] → decision_bits           src/decoder.py:400-403
   │                  │         └─ [_vnu_quantize] → roll → [_cnu_update] × edge  src/decoder.py:405-413
   │                  ├─ _record_iteration                               src/decoder.py:415-431
   │                  └─ _check_errors (genie, 배치 압축)                 src/decoder.py:433-452
   └─ report                       CSV, 로그 CSV 3종, LLR 사본, PNG       src/run.py:736-777
```

대괄호는 교체 지점이다.

## 3. 데이터 흐름

- 1. 설정: config JSON → `load_config`가 허용 키 집합 9개로 키맵을 검사하고 (`src/run.py:98-111`), 상대 경로를 config 파일 위치 기준으로 풀고 (`:277`), `channels`를 `[{"type", "points", (SER, SCR)}]` 리스트로, `log`를 `{"enabled", 항목 7개}` 평탄 dict로, run 기본값은 `_RUN_DEFAULTS`로 정규화한다 (`:116-117, 183-247, 385-387`). 값 제약: rber는 0 < p < 0.5, 에러 bit 수는 0 이상 정수, 같은 공간 안 `int(1e6*값)` 중복 금지 (난수 스트림과 CSV 파일명 충돌 방지), type 중복 금지, `channel_llr_*` 길이는 region 수, `edge_resolution_bits` 2..16, `edge_max_value`는 2^n − 1 꼴, seed 0 이상, `stop_below_fer`는 양수 또는 null (`:166-179, 200-201, 258-267, 309-314, 331-337, 357, 365-370`). `setup`이 `decoder._used_llr_matrix_path`를 심어 `report`가 LLR 사본 저장에 쓴다 (`:442, 765`)
- 2. 부호: H 파일 → `QCCode.load`가 헤더 3줄과 행렬 앞 M_b×N_b개만 읽어 (`src/pcm.py:58-82`) column 우선 정렬 edge 배열을 만든다. edge (i, j, s)에서 VN 정렬 → CN 정렬은 `np.roll(v, -s)`, 반대는 `+s` (`src/pcm.py:4-5`)
- 3. LLR 테이블: DAO 파일 → `LLRMatrix.load`가 row 배열 `row_values` (R, num_dv, num_param)를 `row_ch`, `row_th` 뷰와 `row_csw`, `row_iter`로 나누고 (`src/llr_matrix.py:230-283`), 모드는 파일명 정규식 (`:48, 237-241`), `max_iter`는 마지막 iter_end (`:162`), edge 레벨은 th 패턴으로 판별 (`:92-120`, 기본 [7,5,3,1])
- 4. 디코더 구성: `decoder_class(code, llr_matrix=)` → column별 dv 구간 `_col_dv_idx`, edge 레벨 사본, SD Pre 단계 seed 레벨 (`src/decoder.py:100-134`)
- 5. 배치 생성: 포인트마다 새 난수 생성기 → `generate_message` (B, K) → `encode` all-zero (B, N_b, z) → 채널 → dict `{"mode", "hd", "sd", "cc"}` (`src/run.py:515-530`, `src/channel.py:9-11`)
- 6. 복호 상태: `read_bit` (B, N_b, z) 고정, `syndrome` (B, M_b, z) 1회 계산, `decision_bits` (B, N_b, z), CN 상태 `min1`, `min2`, `min1_pos`, `check_sum` (B, M_b, z)와 `edge_sgn` (B, E, z), `prev_csw` (B,) (`src/decoder.py:54-96, 249-292`). 축 규약은 프레임 배치 B × column block N_b × lane z (VN 정렬), CN 정렬은 B × M_b × z
- 7. iteration: restart면 CN 클리어 → 프레임별 row 선택으로 ch, th → column 순차로 sum_t = ch + Σ C2V, 판정, VNU 양자화, CNU 즉시 갱신 → `prev_csw = Σ(check_sum ⊕ syndrome)` → genie 판정으로 성공 프레임을 배치에서 제외 (`src/decoder.py:336-452`)
- 8. 집계: 디코더 결과 dict → `run_fer_point`가 errors, iter_hist, iteration별 합계, 실패 프레임 상세를 누적하고 진행 줄을 콘솔과 summary.txt에 제자리 갱신 (`src/sim.py:95-137`) → point_result dict (`:142-161`)
- 9. 저장: `report`가 FER CSV, `log_iter_*`, `log_iter_hist_*`, `log_fail_*` CSV, LLR 사본, PNG를 실행 폴더에 쓴다 (`src/run.py:736-777`). 로그 JSON 키와 디코더 내부 항목 이름은 `_LOG_TO_ITEM`이 잇는다 (`src/run.py:113-114`, `src/decoder.py:51`)

## 4. 실행 모드와 분기

| 모드 또는 설정 | 무엇이 달라지는지 | 어디서 정하는지 |
|---|---|---|
| 디코딩 모드 HD / 2SD / 3SD | 채널 dict의 sd, cc 사용 여부, region으로 ch 열 선택, SD Pre 단계와 SD restart 동작, ch 개수 1/2/4 | LLR 파일명 (`src/llr_matrix.py:48, 237-241`). 균일 생성 경로에서만 `decoder.mode` (`src/run.py:299`)가 생성 파일명을 거쳐 반영. 정합 검사는 세 층: `_check_channel_mode` (`src/run.py:504-512`, 호출 `:519, :569`), 채널 함수의 mode 인자 검사 (`src/channel.py:46-47, 80-81, 104-105`), 디코더 `_read_channel_input` (`src/decoder.py:230-232`) |
| `decoder.use_input_llr_matrix` | true면 지정 파일 로드 (mode와 max_iter는 파일이 결정), false면 균일 매트릭스를 합성해 `_generated/`에 저장 후 로드 (`decoder.mode`, `max_iter`, `channel_llr_{mode}`, edge 양자화 키 소비) | `src/run.py:292-337, 412-441` |
| `decoder.use_default_edge_quantization` | true면 edge 레벨 {7,5,3,1}, false면 `edge_resolution_bits`, `edge_max_value`로 레벨 생성 | `src/run.py:250-267, 315-322`, `src/llr_matrix.py:60-89` |
| `channels.type` | rber (HD, 2SD, 3SD), fixed_error (HD), strong_error (2SD). 문자열이나 리스트, 리스트면 순서대로 전부 | `src/run.py:183-247`, `src/channel.py:138-149` |
| 디코더 클래스 | None이면 BaseDecoder, 자식 클래스면 그 교체 지점이 적용 | 런처 `DECODER_CLASS` (`workspace/_template/run.py:24-28`) → `main(decoder_class=)` (`src/run.py:780-786`) |
| restart iteration 유무 | LLR 파일에 restart_iter가 있으면 그 iteration에 CN 상태 클리어 (SD면 Pre 재실행). 없으면 클리어 없음 | `src/llr_matrix.py:359-360`, `src/decoder.py:342-359` |
| 그룹 타입 ITER / CSW | ITER 그룹(또는 단일 row 그룹)은 iteration 구간으로 row 선택, CSW 그룹은 직전 CSW를 row 임계와 비교해 프레임별 선택 | `src/llr_matrix.py:377-386` |
| 균일 레벨 여부 | th가 [top..1] 연속 정수 패턴이고 restart가 없으면 캐스케이드 대신 등가식 `_uniform_saturate` | `src/llr_matrix.py:388-400`, `src/decoder.py:175-181` |
| `log.enabled`와 `log.items` | 상위 스위치가 false면 전부 끔. 항목별로 iteration 집계와 CSV 저장 여부 | `src/run.py:373-387, 748-763` |
| `run.stop_below_fer` | 측정 FER가 이 값 미만이면 그 채널의 남은 포인트 중단, 다음 채널은 계속 | `src/run.py:597-598` |
| `run.print_progress`, `progress_interval_frames` | 콘솔 진행 줄 갱신 여부와 간격. `\r` 갱신은 tty일 때만 | `src/sim.py:85-86, 121-137` |
| `output.save_llr_matrix` | 사용한 LLR 파일 사본을 실행 폴더에 남길지 | `src/run.py:764-768` |
| `log.items.fer_curve_png` | matplotlib 지연 import로 그림 저장. 실패해도 결과 보존 | `src/run.py:692-712, 769-775` |

## 5. 외부 의존성

| 이름 | 용도 | 버전 제약 |
|---|---|---|
| numpy | 전 모듈 필수. `default_rng`, `Generator.permuted`, `integers`, `take_along_axis`, `argpartition` | 명시 없음. 1.20 이상 추정 (`permuted`, `src/channel.py:125`). 1.26.4에서 동작 확인 |
| matplotlib | `_plot_fer_curves`에서만 지연 import, `Agg` 백엔드 (`src/run.py:694-696`) | 명시 없음. 미설치나 실패는 `report`가 흡수. 3.10.7에서 동작 확인 |
| Python | f-string, `subprocess.run(capture_output=, text=)`, `raise ... from None` | 명시 없음. 3.7 이상 추정. 3.11.7에서 동작 확인 |
| git 실행 파일 | summary.txt에 `git rev-parse --short HEAD`와 `+dirty` 기록 (`src/run.py:603-618`) | 없으면 "(git 없음)"으로 계속 |

병렬화 라이브러리(mpi4py, numba, multiprocessing)는 import 0건이다. `README.md:221`의 mpi4py 방침과 `_pm/TODO.md`의 mpi_runner 재설계는 계획만 있다.
