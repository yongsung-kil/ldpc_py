# 탐색 A 보고: 아키텍처 (폴더, 모듈 분리, 계층, 진입점, 빌드, 교체 지점)

> 작성: 2026-09-30 (explorer 에이전트 보고 원문, 메인이 저장)

## 확인한 것

### 1. 최상위 폴더와 역할, README 대조

루트 `testbed/ldpc_py` 의 실제 구성:

| 경로 | 실제 내용 | README 설명과의 차이 |
|------|-----------|---------------------|
| `README.md` | 프로젝트 설명 (225줄) | 제목이 "2_LDPC_base" (README.md:1). 실제 폴더명은 `ldpc_py` |
| `requirements.txt` | `numpy`, `matplotlib` 두 줄, 버전 고정 없음 | 일치 |
| `__init__.py` | docstring 5줄만 (`__init__.py:1-5`) | README 언급 없음 |
| `src/` | pcm, encoder, channel, decoder, llr_matrix, sim, run, `__init__` 8개 | 일치 (README.md:11) |
| `workspace/` | `README.md`, `_template/`, `base_run/`, `test/`, `matrix_sel_1_HD/`, `matrix_sel_1_HD_fixed/` | README.md:165-172 구조도에는 `_template`와 `base_run`만 그려져 있음. `test`, `matrix_sel_1_HD*` 3개는 미기재 |
| `Input/H_matrix/` | `example_18x147_z256.qc`, `matrix_sel_1.txt` | README.md:13은 파일명 미기재. 둘 다 Ref-C 헤더 확인 (아래 6절) |
| `Input/LLR/` | `LLR_MATRIX_HD_0.txt`, `HD_1`, `2SD_toy0`, `3SD_toy0`, `LLR_MATRIX_HD_matrix_sel_1.txt` | README.md:14는 앞 4개만 기재. `HD_matrix_sel_1`은 미기재 |
| `docs/` | `차이.md` 하나 | README.md:15 "차이.md, review/(리뷰 기록)" 중 `review/`는 없음 |
| `_pm/` | `TODO.md`, `DONE.md`, `tasks/`, `done/` | 작업 관리 (깊이 읽지 않음) |
| `.gitignore` | **없음** (Read 실패로 확인) | README.md:104, 170은 `_generated/`와 `Sim_Output/`을 "git 무시 영역"이라 함. 이 사본에는 그 규칙 파일이 없음 |

저장소 밖 참조 (이 사본에 없는 것): `3_LDPC_ideas/새논문적용규칙.md` (README.md:163, workspace/README.md:5, base_run/README.md:24), `4_H_matrix_tool/` (README.md:39), `0_LDPC_original`, `1_LDPC_revised` (docs/차이.md:6). 그리고 `src/decoder.py:46`은 같은 정본 문서를 `docs/새논문적용규칙.md`라고 다른 경로로 적고 있어 README와 서로 어긋난다. 두 경로 모두 존재하지 않는다.

### 2. src 모듈 8개: 역할, 공개 심볼, import 관계

| 모듈 | 역할 | 공개 함수와 클래스 (줄) | 내부 import |
|------|------|------------------------|-------------|
| `src/pcm.py` | QC-LDPC 부호 표현, Ref-C 포맷 파일 입출력 | `QCCode` :23. `__init__(base, z)` :24, 속성 `M_b N_b z N M K rate edge_row edge_col edge_shift E col_edges row_deg col_deg` :31-46, `save` :49, `load` :58, `syndrome` :85, `count_cycles4` :94, `summary` :112 | numpy만 |
| `src/encoder.py` | 메시지 생성과 인코딩 자리 | `generate_message(code, batch, rng)` :13, `encode(msg, code)` :18 (all-zero 반환 임시) | numpy만 |
| `src/channel.py` | 채널 3종 | `qfunc_inv` :24, `dev_from_rber` :37, `rber_channel` :43, `fixed_error_channel` :78, `strong_error_channel` :91, 레지스트리 `CHANNELS` :138, `CHANNEL_MODES` :145. 출력은 dict `{"mode","hd","sd","cc"}` | numpy만 |
| `src/llr_matrix.py` | DAO LLR_MATRIX 로더, 균일 합성, iteration/CSW별 row 선택 | `MODE_CH_LEN` :45, `uniform_edge_mag` :51, `edge_quantization_levels` :60, `LLRMatrix` :123 (`load` :230, `make_internal_uniform_matrix` :286, `save` :318, `col_dv_idx` :347, `is_restart` :359, `row_index` :369, `has_uniform_levels` :389, `needs_csw` :403, `summary` :408) | numpy, os, re, warnings. `code`는 인자로 받고 pcm을 import하지 않음 |
| `src/decoder.py` | 배치 벡터화 syndrome-aided min-sum 디코더 | `LOG_ITEMS` :51, `_DecodeState` :54, `BaseDecoder` :99, 진입 `decoder_main` :475 | numpy만 |
| `src/sim.py` | FER 측정 루프 (한 포인트) | `run_fer_point` :29, `save_csv` :170 | `.decoder` (BaseDecoder 타입 힌트, LOG_ITEMS 검증) :9 |
| `src/run.py` | 설정 로드와 검증, 구성, 실험 루프, 출력 저장, CLI | `load_config` :270, `setup` :393, `print_experiment_summary` :496, `run_experiment` :548, `create_run_dir` :715, `report` :736, `main` :780 | `.channel`, `.encoder`, `.decoder`, `.llr_matrix`, `.pcm`, `.sim` :91-96. matplotlib은 `_plot_fer_curves` 안에서 지연 import :694-696 |
| `src/__init__.py` | 공개 API | `QCCode`, `BaseDecoder`, `channel`, `encoder`, `sim` :6-10. `run`과 `llr_matrix`는 `__all__`에 없음 | |

import 방향 (화살표는 부르는 쪽에서 불리는 쪽):
- ㉮ `run` → `channel`, `encoder`, `decoder`, `llr_matrix`, `pcm`, `sim`
- ㉯ `sim` → `decoder`
- ㉰ `__init__` → `pcm`, `decoder`, `channel`, `encoder`, `sim`
- ㉱ `pcm`, `encoder`, `channel`, `llr_matrix`, `decoder` 다섯은 서로를 import하지 않는 잎 모듈 (numpy 표준만). `decoder`는 `code`와 `llr_matrix` 객체를 생성자 인자로 받고, `llr_matrix.col_dv_idx(code)`도 인자 전달로 결합 (decoder.py:113). 순환 없음

### 3. 진입점

`src/run.py main(argv=None, decoder_class=None)` :780-791
- argv[0] 하나만 config 경로로 쓴다 (:785, :788). 없으면 `usage: python -m src.run <config.json>` 종료 :783
- `decoder_class`는 `setup`에 그대로 전달 :786. None이면 `BaseDecoder` (setup :443-444)

workspace 런처 `run.py` 5개 (`_template`, `base_run`, `test`, `matrix_sel_1_HD`, `matrix_sel_1_HD_fixed`)는 34줄 내용이 완전히 동일:
- ㉮ src 탐색: `EXPERIMENT_DIR`에서 시작해 부모로 올라가며 `<조상>/2_LDPC_base/src` 디렉토리가 있는지 검사 (run.py:11-17). 드라이브 루트까지 없으면 `SystemExit("상위 폴더에서 2_LDPC_base/src를 찾지 못함 ...")` :15. 찾으면 `<조상>/2_LDPC_base`를 `sys.path[0]`에 넣고 `from src.run import main` :18-22
- ㉯ 디코더 선택: 모듈 상수 `DECODER_CLASS = None` :24. 주석 :25-28이 "이 폴더의 decoder.py에 BaseDecoder 자식을 만들고 `from decoder import MyDecoder; DECODER_CLASS = MyDecoder`"로 지정하라고 안내
- ㉰ config 인자: `sys.argv[1:]`가 있으면 그 파일들을 순서대로, 없으면 형제 `config.json` 하나 (:31). 각 config마다 `main([config_path], decoder_class=DECODER_CLASS)` 호출 (:32-33)

**이 사본에서 런처는 동작하지 않는다.** `2_LDPC_base/src`를 저장소 루트 `ldpc_py`부터 드라이브 루트까지 조상 폴더 여섯 단계에서 Glob으로 찾았으나 모두 없음. 루트에서 `python -m src.run workspace/base_run/config.json`으로 부르는 경로만 살아 있다 (config의 상대경로 `../../Input/...`는 config 파일 위치 기준이라 폴더명과 무관: run.py:277, :155).

workspace 폴더별 내용:

| 폴더 | 파일 | 특징 |
|------|------|------|
| `_template/` | `run.py`, `config.json`, `README.md` | config는 모든 키와 `_desc` 설명을 담은 풀버전 (label "실험이름"). README는 목적/바꾼 것/결과/결론 빈 틀 |
| `base_run/` | `run.py`, `config.json`, `README.md` | 최소 키 config: `example_18x147_z256.qc` + `LLR_MATRIX_HD_1.txt`, fixed_error [200, 300], log 전부 on, label base_run. README:6-8 "decoder.py가 없다. 재정의 0개가 곧 본체와 같다는 보증" |
| `test/` | `run.py`, `config.json`, `README.md` | 파이프라인 동작 확인 스크래치 (README:7-8). fixed_error [100,200,300], log off |
| `matrix_sel_1_HD/` | `run.py`, `config.json`, `_probe.json`, `_probe/` 결과 2개 | `matrix_sel_1.txt` + `LLR_MATRIX_HD_matrix_sel_1.txt`, fixed_error [390,380,370], max_frame_errors 20, max_frames 200000, log on. **README.md 없음**. `_probe.json`은 output.dir "_probe", fixed_error [500,460,440,420,400], frames_per_batch 512. `_probe/260818_225547_probe/summary.txt`: 커밋 `ecec8ae+dirty`, decoder `src.decoder.BaseDecoder`, code base 15x145 z=256 N=37120 K=33280, E=380에서 128프레임 0에러. `_probe/260818_225612_probe_sweep/summary.txt`: E=500에서 512/512 FER 1.0 후 중단 |
| `matrix_sel_1_HD_fixed/` | `run.py`, `config.json`, `README.md` | 같은 입력, max_frame_errors 15, max_frames 2000000, log off. README.md:8, 14는 "max_frame_errors=20, max_frames=200000"이라 적어 config(15, 2000000)와 어긋남. 결과 표는 빈칸 |

`workspace/**/decoder.py`는 어느 폴더에도 없음 (Glob 확인). 재정의 예시 부재.

### 4. 계층과 호출 순서

| 계층 | 위치 | 호출 순서 |
|------|------|-----------|
| 설정 로드와 검증 | `run.py load_config` :270-390 | 키맵 `_check_keys` :125, 필수 `_require` :133, 경로 결합 `_path_pair` :147, 채널 정규화 `_check_channels` :183-247, edge 양자화 `_check_edge_quantization` :250, log 평탄화 :384-387 |
| 구성 | `run.py setup` :393-446 | `QCCode.load` :405 → LLR 경로 결정 (파일 :406-411 또는 `LLRMatrix.make_internal_uniform_matrix` + `save` :412-440) → `LLRMatrix.load` :441 → `decoder_class(code, llr_matrix=...)` :445 |
| 출력 폴더 | `run.py create_run_dir` :715-733 | `YYMMDD_HHMMSS_{label}` 생성, config 사본, summary.txt 머리 (`_git_commit_hash` :603, `_experiment_summary_lines` :458) |
| 실험 루프 | `run.py run_experiment` :548-600 | 전 채널 모드 사전 확인 `_check_channel_mode` :568-569 → 채널별 라벨 중복 처리 :577-583 → 포인트별 `np.random.default_rng([seed, channel_index, int(1e6*point)])` :586 → `_make_channel_fn` :587 → `sim.run_fer_point` :588 → `stop_below_fer` 판단 :597 |
| 채널 함수 | `run.py _make_channel_fn` :515-530 | `encoder.generate_message` → `encoder.encode` → `chan.CHANNELS[type](code, cw, point, rng, mode=..., **extra)` :524-528 |
| 시뮬레이션 루프 | `sim.py run_fer_point` :29-167 | while :95 → `decoder.decoder_main(channel_fn(batch, rng), log=...)` :97 → 집계 :99-119 → 진행 줄 갱신 (콘솔 `\r` + summary.txt 꼬리 재작성 `_rewrite_file_tail` :21) :121-137 → 결과 dict :142-161 |
| 디코더 | `decoder.py decoder_main` :475-508 | `_read_channel_input` :501 → `_init_state` :502 → iteration 1..max_iter: `_run_iteration` :504 → `_record_iteration` :505 → `_check_errors` :506 (성공 프레임 배치 압축) → `_build_result` :508 |
| 출력 저장 | `run.py report` :736-777 | `sim.save_csv` :746 → `_write_iter_log` :752, `_write_iter_hist_log` :756, `_write_fail_log` :761 → LLR 사본 :764-768 → `_plot_fer_curves` :772 (실패해도 계속) |

`_run_iteration` :336-370 내부: `_is_edge_clear_iter` :342 → CN 상태 클리어 :344-349 → SD restart면 `_seed_channel_magnitudes` 후 return :350-359 → `llr_matrix.row_index(iteration, prev_csw)` :360 → `for col in _column_order(iteration)` :365 → `_process_column` :366 → `_collect_error_metrics` :368 → `prev_csw` :370.
`_process_column` :372-413 내부: edge마다 `_c2v_reconstruct` :392 → roll → sum_t 누적 :396-398 → `_vn_decide` :400 → `decision_bits` :403 → edge마다 `_vnu_quantize` :408 → roll → `_cnu_update` :412.

모드 정합 검사는 두 곳: `run.py _check_channel_mode` :504-512 (사전), `decoder.py _read_channel_input` :230-232 (채널 dict의 mode와 llr_matrix.mode 불일치 시 에러).

### 5. 교체 지점 (BaseDecoder에서 자식이 재정의하도록 설계된 함수)

`src/decoder.py:40-46` 모듈 docstring이 "교체 단위 = 원본 C++ 함수 경계"이며 6개 함수라고 명시하고, :136에 섹션 헤더 `# ---------- 논문 아이디어 교체 지점 ----------`가 있다. 각 docstring 첫 줄에 `[교체 지점: C++ 함수 대응]` 표지가 붙어 있다.

| 함수 (줄) | 인자 | 반환 | 호출 위치 | C++ 대응 |
|-----------|------|------|-----------|----------|
| `_is_edge_clear_iter(self, iteration)` :137-144 | iteration 번호 | bool | `_run_iteration` :342 | Is_Iter_Type_Edge_Clear |
| `_column_order(self, iteration)` :146-148 | iteration 번호 (Pre 단계는 0) | column block 인덱스 iterable | `_run_iteration` :365, `_seed_channel_magnitudes` :303 | 메인 루프 스케줄 |
| `_c2v_reconstruct(self, iteration, edge, min1_row, min2_row, min1_pos_row, syndrome_row, check_sum_row, edge_sgn_row)` :150-157 | CN row block 슬라이스 (num_active_frames, z) | 부호 있는 C2V (CN 정렬) | `_process_column` :392 | C2V_Cal |
| `_vn_decide(self, sum_t)` :159-162 | sum_t (num_active_frames, z) | bool 배열 (반전 여부) | `_process_column` :400 | VN_Cal_HD 판정부 |
| `_vnu_quantize(self, raw, vnu_in, th)` :164-187 | raw = sum_t − vnu_in, th (num_active_frames, th 개수) | 부호 있는 양자화 값 | `_process_column` :408 | VN_Cal_HD 양자화부 |
| `_cnu_update(self, edge, edge_clear, new_sgn, new_mag, row_blk, min1, min2, min1_pos, check_sum, edge_sgn)` :197-220 | 새 메시지와 CN 상태 배열 전체 | **None. 받은 배열을 제자리에서 고침** | `_process_column` :412, `_seed_channel_magnitudes` :310 | CNU_Remove_Old_Sgn / CNU_Update_New_Mag |

코드에 적힌 경계 규칙:
- ㉮ `_cnu_update` docstring :202-203 "재정의할 때도 받은 배열을 제자리에서 직접 고쳐야 한다 (반환값은 쓰이지 않는다)"
- ㉯ `_uniform_saturate` :189-195는 표지 없는 보조 함수지만 docstring이 "교체 지점 재정의로 비정수 raw가 생기면 이 함수를 함께 재정의하거나 캐스케이드 경로를 쓸 것"이라 함께 손댈 대상으로 지정
- ㉰ `_collect_error_metrics` docstring :316-320 "column 루프 안에서 세지 않으므로 `_column_order`가 일부 column만 방문해도 미방문 column의 에러가 집계에 남는다" (부분 스케줄 재정의를 전제로 한 안전장치)
- ㉱ 생성자 시그니처: `setup`이 `decoder_class(code, llr_matrix=llr_matrix)`로 호출 (run.py:445)하므로 자식은 이 두 인자를 받아야 함 (코드로 확인, 문서화된 규칙은 미확인)
- ㉲ README.md:161-162 "src를 고치지 않고 BaseDecoder를 상속한 자식 클래스에서 교체용 함수만 재정의한다". 단계별 함수 7개(`_read_channel_input`, `_init_state`, `_run_iteration`, `_process_column`, `_record_iteration`, `_check_errors`, `_build_result`)에는 표지가 없어 경계 밖으로 읽히지만, 재정의를 금지하는 문구는 코드에 없음
- ㉳ 실행 요약에 디코더 클래스가 `module.ClassName`으로 기록됨 (run.py:483, summary.txt "decoder src.decoder.BaseDecoder")

재정의 예시 decoder.py는 workspace 어디에도 없음.

### 6. 빌드와 실행

- ㉮ `requirements.txt`: numpy, matplotlib. matplotlib은 `log.items.fer_curve_png`가 true일 때만 import (run.py:694-696)
- ㉯ 패키지: setup.py, pyproject.toml 없음. 루트 `__init__.py`는 docstring만. `src/__init__.py`가 공개 API. `python -m src.run`은 루트를 cwd로 요구 (run.py:12)
- ㉰ 테스트: `tests/`, `_test/`, pytest 설정 없음. `workspace/test/`는 pytest가 아니라 실험 스크래치 (workspace/test/README.md:7)
- ㉱ 실행 명령: 루트에서 `python -m src.run <config.json>` (동작 가능), 실험 폴더에서 `python run.py [config...]` (이 사본에서는 3절대로 SystemExit)
- ㉲ Git: 브랜치 main, 커밋 1개 `0394b81 시험장 사본`. `.gitignore` 없음
- ㉳ 산출물 폴더 `Sim_Output/`은 어느 실험 폴더에도 없음. 결과물은 `matrix_sel_1_HD/_probe/` 2건만 (2026-08-18, 커밋 ecec8ae 시점)
- ㉴ Input 헤더 확인: `example_18x147_z256.qc:1-3` = `147 18 / 4 31 / 256` (N_b=147, M_b=18, J=4, K=31, z=256, README.md:222 기준 치수와 일치). `matrix_sel_1.txt:1-3` = `145 15 / 11 52 / 256` (탭 구분, N_b=145, M_b=15). `LLR_MATRIX_HD_1.txt`: num_param 4, num_dv 4, dv [11,4,3,2], 그룹 2개(각 1 row, type CSW), restart 0, 마지막 iter_end 20 (README.md:14 "restart 없는 20-iter" 일치). dv=2 열의 ch=28은 `_pm/TODO.md:31`이 위반으로 기록한 값

## 관계와 흐름

```
workspace/{실험}/run.py (런처, 이 사본에서는 2_LDPC_base 부재로 정지)
   └─ DECODER_CLASS ──▶ src/run.py main(argv, decoder_class)
                            ├─ load_config      (검증, 경로 결합, 채널 정규화, log 평탄화)
                            ├─ setup            pcm.QCCode.load ─┐
                            │                   llr_matrix.LLRMatrix.load / make_internal_uniform_matrix+save ─┤
                            │                   decoder_class(code, llr_matrix) ◀──────────────────────────────┘
                            ├─ create_run_dir   실행 폴더 + config 사본 + summary.txt 머리
                            ├─ run_experiment   채널 × 포인트 루프, rng 파생
                            │     └─ sim.run_fer_point (배치 while)
                            │           ├─ channel_fn = encoder.generate_message → encoder.encode → channel.CHANNELS[type]
                            │           └─ decoder.decoder_main
                            │                 ├─ _read_channel_input, _init_state
                            │                 └─ iteration 루프: _run_iteration → _record_iteration → _check_errors
                            │                       └─ _process_column: [_c2v_reconstruct] → [_vn_decide] → [_vnu_quantize] → [_cnu_update]
                            │                          (대괄호 = 교체 지점, 여기에 [_is_edge_clear_iter], [_column_order]가 iteration 단위로 더 있음)
                            └─ report           save_csv, 로그 CSV 3종, LLR 사본, fer_curves.png
```

- 데이터 계약: 채널 → 디코더는 dict `{"mode","hd","sd","cc"}` (channel.py:9, decoder.py:223-247). 디코더 → sim은 dict `success, decode_success_iteration, final_err_bits, final_info_err_bits (+log_*)` (decoder.py:482-494, sim.py:99-119). sim → run은 point_result dict (sim.py:142-161). 디코딩 모드와 max_iter는 config가 아니라 `LLRMatrix`가 결정 (decoder.py:112, llr_matrix.py:162, :237-241)
- 디코더 변형은 config가 아니라 런처의 클래스 주입 한 곳에서만 갈아끼움 (README.md:108-109, run.py:14-15). config는 파라미터 전용
- 설정 파일의 상대경로 해석 기준은 config 파일 위치 (run.py:277)이고, 출력 폴더도 config 위치 하위 `Sim_Output` 기본 (run.py:343-345)이라 실험 폴더 단위로 입력과 결과가 자기완결적

## 못 본 것과 추정

- ㉮ 실행 검증 미실시 (도구 제한). "런처 SystemExit"는 코드(run.py:11-17)와 조상 폴더 6단계 Glob 부재에 근거한 판단이며, `D:\` 최상위 Glob의 완전성은 도구 특성상 미확인
- ㉯ git 추적 상태 미확인: `_probe/` 결과물이 커밋에 포함됐는지, 전역 gitignore가 있는지 (추정: 저장소에 `.gitignore`가 없으므로 "시험장 사본" 커밋에 `_probe/`가 포함됐을 가능성)
- ㉰ `_pm/done/`, `_pm/DONE.md`, `_pm/tasks/20260808_review/` 안 읽음. `_pm/TODO.md`만 읽어 미구현 항목(후순위 로그 7종, mpi_runner 재설계, config checker 확장)을 확인
- ㉱ Input LLR 파일 중 `HD_0`, `2SD_toy0`, `3SD_toy0`, `HD_matrix_sel_1` 내용 미확인. `_probe/*/fer_fixed_error.csv` 미확인
- ㉲ 교체 지점의 정본 문서(새논문적용규칙.md)가 저장소에 없어 "공식" 상속 경계 규칙(예: 상태 필드 접근 허용 범위, 생성자 확장 허용 여부)은 코드 docstring 수준으로만 파악. 정본과의 일치 여부 미확인
- ㉳ 상위 `AI_Assisted_Dev/CLAUDE.md`는 plugin과 pytest를 전제한 다른 저장소의 규칙으로 읽힘. 이 프로젝트 전용 CLAUDE.md는 없음 (추정: 폴더 트리상 부모 파일이 함께 로드된 것)
