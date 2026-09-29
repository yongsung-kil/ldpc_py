# 탐색 C 보고: 컨벤션과 패턴, 제약 (이름 규칙, 오류 처리, 로그, 설정, 테스트 구조, 변경 금지 대상)

> 작성: 2026-09-30 (explorer 에이전트 보고 원문, 메인이 저장. 경로는 저장소 루트 기준 상대 경로로 바꿨다)

사전 확인: 프로젝트 루트에 CLAUDE.md는 없고, 상위 폴더 `AI_Assisted_Dev/CLAUDE.md`의 규칙(한국어, 줄표와 가운뎃점 금지, ㉮㉯㉰ 나열)이 적용된다. `docs/profile/` 다섯 문서는 탐색 도중 빈 골격(양식만) 상태로 생겼고 내용은 아직 없다. `docs/adr/README.md`도 목록이 빈 양식이다.

## 확인한 것

### 1. 이름 규칙

- ㉮ 모듈: 영어 snake_case 단어 하나 또는 둘 (`src/run.py`, `sim.py`, `decoder.py`, `pcm.py`, `llr_matrix.py`, `channel.py`, `encoder.py`). 패키지 공개 이름은 `src/__init__.py:6-10`의 `__all__ = ["QCCode", "BaseDecoder", "channel", "encoder", "sim"]`
- ㉯ 클래스: PascalCase. `QCCode` (`src/pcm.py:23`), `BaseDecoder` (`src/decoder.py:99`), `LLRMatrix` (`src/llr_matrix.py:123`), 모듈 내부용은 밑줄 접두 `_DecodeState` (`src/decoder.py:54`)
- ㉰ 함수: snake_case. 모듈 밖에서 쓰지 않는 함수는 전부 밑줄 접두 (`src/run.py:120-268`의 `_visible`, `_check_keys`, `_require`, `_check_int`, `_path_pair`, `_check_channel_values`, `_check_channels`, `_check_edge_quantization`; `src/decoder.py:137-472`의 단계별 함수 전부). 공개 진입은 `load_config`, `setup`, `run_experiment`, `report`, `main` (`src/run.py:270, 393, 548, 736, 780`), `run_fer_point`, `save_csv` (`src/sim.py:29, 170`), `decoder_main` (`src/decoder.py:475`)
- ㉱ 상수: UPPER_SNAKE. 공개 `LOG_ITEMS` (`src/decoder.py:51`), `MODE_CH_LEN`, `GROUP_TYPE_ITER, GROUP_TYPE_CSW` (`src/llr_matrix.py:45-46`), `CHANNELS`, `CHANNEL_MODES` (`src/channel.py:138-149`). 모듈 내부 상수는 밑줄 접두 `_TOP_KEYS` 계열 키맵과 `_RUN_DEFAULTS`, `_SUMMARY_DIVIDER` (`src/run.py:98-117, 449`), `_R_OFFSET`, `_NAME_RE` (`src/channel.py:21`, `src/llr_matrix.py:48`)
- ㉲ 수식과 하드웨어 유래 대문자 변수는 예외로 허용: `B, N_b, M_b, z, E, K, N`(치수), `RESET`(함수 안 지역 상수, `src/decoder.py:204, 256, 339`), `J, K`(H 파일 헤더, `src/pcm.py:51, 71`). 디코더 변수명은 원본 C++ 용어를 그대로 따르는 것이 명시 규칙 (`src/decoder.py:3-5`: sum_t, vnu_in, check_sum, edge_sgn, min1/min2/min1_pos, prev_csw)
- ㉳ 설정 키: snake_case 영어. 모드 값은 대문자 `HD/2SD/3SD` (`src/run.py:300`), 비율 키는 대문자 `SER/SCR` (`src/run.py:111`)
- ㉴ 파일명 규칙(코드가 파싱함): LLR 파일은 `LLR_MATRIX_{HD|2SD|3SD}_*.txt` 정규식으로 모드 판별 (`src/llr_matrix.py:48, 237-241`), 균일 생성물은 `LLR_MATRIX_{mode}_uniform_{bits}bit_max{max}_ch{..}_dv{..}_iter{..}.txt` (`src/run.py:433-438`), 실행 폴더는 `YYMMDD_HHMMSS_{label}` (`src/run.py:722-723`), 결과 CSV는 `{csv_prefix}_{label}.csv`, `log_iter_{label}_p{point}.csv`, `log_iter_hist_...`, `log_fail_...` (`src/run.py:745-762`). H 파일 확장자는 고정이 없음 (`Input/H_matrix/example_18x147_z256.qc`와 `matrix_sel_1.txt` 혼재)
- ㉵ 폴더 규칙: 밑줄 접두는 실험이 아닌 보조물 (`workspace/_template/`, `workspace/matrix_sel_1_HD/_probe/`, 생성물 `_generated/` `src/run.py:430`). 실험 폴더는 소문자 snake (`base_run`, `test`, `matrix_sel_1_HD`). `_pm` 폴더는 `{YYYYMMDD}_{주제}` (`_pm/done/20260807_가독성리팩토링/`)
- ㉶ 언어 배치: 식별자와 CSV 헤더와 진행 줄 지표는 영어 (`src/sim.py:124-131` `e/fr, fer, ber, avg_iter, f/s, it/s, elapsed`; `src/sim.py:174-175` CSV 헤더), docstring과 주석과 예외 문구와 README와 모든 md 문서는 한국어. summary.txt 항목 이름은 영어이고 값 설명은 한국어 혼용 (`src/run.py:469-490` "파일 로드", "(전부 꺼짐)"). 문서 파일명에 한국어 사용 (`docs/차이.md`, `_pm/done/*`)
- ㉷ 나열 기호: README와 workspace README와 `src/llr_matrix.py:4-6` docstring은 ㉮㉯㉰. 예외로 `src/channel.py:99-101` docstring이 ①②를 씀. 화살표 `→ ← ↔`는 src 전반의 주석에서 흐름 표기로 광범위하게 사용 (56건, `src/decoder.py:8-15` 트리 그림 등)

### 2. 오류 처리

- ㉮ 예외 종류: 형식과 값 위반은 전부 `ValueError` (`src/run.py` 전 검증부, `src/llr_matrix.py:135, 145, 172-219, 239, 262-279`, `src/pcm.py:27-29, 67-81`, `src/channel.py:47, 81, 105-112`, `src/decoder.py:230-243`). 파일 부재는 `FileNotFoundError` (`src/run.py:404, 409-411`). 지원 범위 밖은 `NotImplementedError` (`src/decoder.py:109` 모드, `src/llr_matrix.py:138-141` 3-bit 아닌 th 개수). 사용법 오류와 런처 실패는 `SystemExit` (`src/run.py:783`, `workspace/_template/run.py:15-16`). 형상 불일치는 `assert` 한 곳 (`src/decoder.py:246`). 경고는 `warnings.warn` 한 곳 (`src/llr_matrix.py:224-226` th 비단조)
- ㉯ 종료 방식: `sys.exit` 호출은 없음. 예외를 잡지 않고 전파해 트레이스백으로 종료. 예외를 잡는 곳은 세 곳만: git 해시 실패를 "(git 없음)"으로 대체 (`src/run.py:617-618`), 그림 저장 실패를 안내문으로 흡수 (`src/run.py:771-775`), 레벨 생성 오류에 config 문맥을 덧붙여 재발생 (`src/run.py:333-337`)
- ㉰ 안내 문구 패턴: `config [섹션] 키=값!r: 조건이어야 함` 꼴 (`src/run.py:129-143`), 필수값은 `config [섹션] 키 없음 또는 null (필수 값)` (`src/run.py:135`), 파일 계열은 `{path}: 문제 (기대값)` (`src/pcm.py:68-69`, `src/llr_matrix.py:262-270`), 다음 행동 안내를 괄호나 문장 끝에 붙임 (`src/run.py:404` "H-matrix를 먼저 준비할 것", `:409-411` "use_input_llr_matrix를 false로 바꿔 균일 생성을 쓸 것")
- ㉱ 설계 방침: "조용한 대체 금지". dv 미매칭은 C++의 조용한 fallback을 재현하지 않고 에러 (`src/llr_matrix.py:31-32, 353-355`, `docs/차이.md:25`). 플래그 값과 무관하게 존재하는 값 공간은 전부 형식 검사해 통과와 실패가 플래그에 따라 갈리지 않게 함 (`src/run.py:184-187, 252-254, 296-298`). 측정 시작 전에 전 채널의 모드 호환을 미리 확인 (`src/run.py:504-506, 568-569`). 검증을 우회한 직접 호출에도 최소 가드 (`src/sim.py:58-70`)
- ㉲ config 검증 구조 (`src/run.py`): 섹션별 허용 키 집합 8개 (`:98-111`), `_visible()`이 `_` 시작 키 제외 (`:120-122`), `_check_keys()`가 허용 밖 키를 에러 (`:125-130`), `load_config()`가 최상위 → H_matrix → decoder → output → run → log → channels 순서로 검증하며 정규화 (`:270-390`). 정규화 결과로 `config["seed"]` 승격 (`:357`), `config["log"]` 평탄화 (`:385-387`), `config["channels"]` 리스트화 (`:389`), 경로 결합 (`:287-288, 323-324`). `_desc` 키는 dict 어느 층에도 둘 수 있음 (`_path_pair`, `strong_ratios`, `log.items`, `edge_quantization` 전부 `_check_keys` 사용)

### 3. 설정 패턴

- ㉮ 기본값 출처: run 섹션은 `_RUN_DEFAULTS` 한 곳 (`src/run.py:115-117`), 검증(`:358-360`), 소비(`:557-563`), 요약(`:486-489`)이 전부 이 dict를 읽음 (setdefault 하지 않고 매번 `.get(key, default)`). 다른 기본값은 `setdefault`로 인라인: `use_input_llr_matrix` True(`:292`), `mode` "HD"(`:299`), `use_default_edge_quantization` True(`:315`), `edge_resolution_bits` 3과 `edge_max_value` 7(`:260, 267`), `output.dir` "Sim_Output"(`:343`), `save_llr_matrix` True(`:346`), `print_progress` True(`:361`), `log.enabled` True(`:374`), `seed` 0(`:357`)
- ㉯ 기본값 이중 정의 지점: edge 기본 (3, 7)이 `_check_edge_quantization`(`:260, 267`)과 `setup()`(`:419`)에 각각 하드코딩. 3-bit 레벨 `[7, 5, 3, 1]`도 `src/llr_matrix.py:142`에 별도. `print_progress` 기본 True가 `:361`과 `:561` 두 곳. `csv_prefix` "fer"는 `:743`의 `.get`에만 있음
- ㉰ README 스키마와 코드 대조 (`README.md:57-130` 대 `src/run.py:98-111`): 허용 키는 여섯 섹션 모두 일치. README JSON 예시 블록에는 `run.print_progress`, `output.label`, `output.save_llr_matrix`가 빠져 있고 산문(㉵㉶)으로만 설명. README는 `max_frame_errors`, `max_frames`, `frames_per_batch`의 기본값(50, 20000, 128)을 적지 않으며 이 값은 `src/run.py:56-58` docstring과 `_RUN_DEFAULTS`에만 있음. 스키마 문장 규칙 "정본"이 둘: 스키마 정본은 README(`workspace/_template/config.json:3`), 키 설명 정본은 `workspace/_template/config.json` (`workspace/test/config.json:4`)
- ㉱ 상대 경로 규칙: `H_matrix`, `decoder.llr_matrix`, `output.dir`의 상대 경로는 config 파일 위치 기준 (`src/run.py:147-155, 277, 343-345`; `README.md:35-36`). 실험 config는 `../../Input/...`로 공용 Input을 가리킴 (`workspace/base_run/config.json:8, 13`)
- ㉲ 디코더 선택은 config에 없음. 실험 폴더 `run.py`의 `DECODER_CLASS` 한 곳이 `main(decoder_class=...)`로 주입 (`workspace/_template/run.py:24-33`, `src/run.py:780, 786`)
- ㉳ LLR 공급 두 경로가 결국 "파일 로드 단일 경로"로 합류: 균일 생성도 DAO 포맷 파일을 `_generated/`에 저장한 뒤 다시 `LLRMatrix.load`로 읽음 (`src/run.py:397-399, 423-441`)

### 4. 로그와 진행 표시

- ㉮ `logging` 모듈 미사용, 전부 `print`. 콘솔 메시지는 `generated LLR matrix:`, `saved:`, `run dir:` 접두 (`src/run.py:440, 747, 773, 776`), 실험 요약은 `=`×64 구분선 사이의 `- 이름  값` 불릿 (`src/run.py:449, 458-501`)
- ㉯ `print_progress`: 진행 줄의 캐리지 리턴 갱신은 `sys.stdout.isatty()`일 때만 (`src/sim.py:85-86`), 파일 리다이렉트면 최종 줄만 남김 (`:162-163`). `progress_interval_frames` 단위로 다음 갱신 프레임을 계산 (`src/sim.py:93, 121, 136-137`)
- ㉰ summary.txt 실시간 기록: `create_run_dir`가 측정 전에 머리(run 이름, code commit, start 시각, 실험 요약)를 씀 (`src/run.py:715-733`), `run_fer_point`가 파일 크기를 offset으로 잡고 (`src/sim.py:89-92`) 진행 줄을 `_rewrite_file_tail`로 제자리 갱신하다가 (`:21-26, 134-135`) 최종 결과 줄로 대체 (`:164-166`). 콘솔 결과 줄과 같은 문자열 (`:156-161`)
- ㉱ git 커밋 해시: `git rev-parse --short HEAD`를 `src/` 폴더 기준으로 실행, `git status --porcelain` 출력이 있으면 `+dirty` 접미, 실패 시 "(git 없음)" (`src/run.py:603-618`). 기록 예: `code commit: ecec8ae+dirty` (`workspace/matrix_sel_1_HD/_probe/260818_225547_probe/summary.txt:2`). 시각 형식 `%Y-%m-%d %H:%M:%S` (`src/run.py:728`)
- ㉲ 분석 로그: `log.enabled`가 상위 스위치 (`src/run.py:384-387`), JSON 키와 디코더 내부 항목 이름이 다르고 `_LOG_TO_ITEM`이 매핑 (`src/run.py:112-114`, 디코더 쪽 허용 집합 `src/decoder.py:51`). 켠 항목만 iteration별로 집계해 속도 비용을 한정 (`src/decoder.py:415-431`)

### 5. 테스트 구조

- ㉮ `tests/` 폴더, `test_*.py`, pytest 설정 파일 전부 없음 (glob 결과 0건). `requirements.txt`는 `numpy`, `matplotlib` 두 줄 (`requirements.txt:1-2`)
- ㉯ `workspace/test/`는 단위 테스트가 아니라 "전체 파이프라인이 도는지 빠르게 확인하는 스크래치 실험"이며 성능 기록을 하지 않음 (`workspace/test/README.md:7-8, 17`). 설정은 `log.enabled=false`, fixed_error [100, 200, 300] (`workspace/test/config.json:53-54, 46`)
- ㉰ 실제 검증 관습(문서로만 확인): 같은 seed 수치 완전 일치 회귀 (`docs/차이.md:23` "HD 회귀로 산출물 동일 확인", `_pm/TODO.md:21` "회귀 완전 일치 확인"), AST 대조로 로직 무변경 확인 (`_pm/TODO.md:20`), 무효과 조건에서 vanilla와 수치 일치로 구현 검증 (`_pm/DONE.md:31`). DONE.md는 "단위 24건 + 스키마 14건 + E2E 3경로" 검증을 언급하지만 (`_pm/DONE.md:71-75`) 그 테스트 파일은 저장소에 없음
- ㉱ 코드 안의 테스트 편의 장치: `decoder_main`이 dict 대신 signed LLR 배열도 받음 (HD 전용, `src/decoder.py:241-244, 479`), `run_fer_point` 직접 호출용 최소 가드 (`src/sim.py:58-65`)
- ㉲ 재현성 조건: 같은 seed로 수치를 재현하려면 `frames_per_batch`까지 같아야 함 (`README.md:120-121`, `src/run.py:58-59`). 난수 스트림은 `[seed, 채널 인덱스, int(1e6*point)]`로 파생하고 (`src/run.py:586`) 파생값 중복을 검증에서 금지 (`src/run.py:175-179`)

### 6. 문서 규칙

- ㉮ 줄표(U+2014): README, docs/차이.md, src, workspace md에서 0건 (grep). `_pm/DONE.md`에는 69건 남아 있으며 "이력물은 보존" 방침 (`_pm/TODO.md:20`)
- ㉯ 가운뎃점(U+00B7): 나열 용법은 0건. 남은 11건은 전부 곱셈 기호 (`README.md:184, 186` `2·r_offset`, `E·SER`; `docs/차이.md:22, 35` `H·r`; `src/decoder.py:18, 268, 300` `H·read_bit`; `src/channel.py:45, 94-95`; `_pm/TODO.md:30` `7·dv`). 프로젝트 방침은 "가운뎃점 나열 용법 제거" (`_pm/TODO.md:25`)이고 상위 CLAUDE.md는 가운뎃점 자체를 금지하므로 곱셈 표기를 어떻게 다룰지는 부른 쪽 판단 사항
- ㉰ 나열은 ㉮㉯㉰ (README 전반, `workspace/README.md:7-13`, `workspace/base_run/README.md:5-11`). 주소를 받는 갈래 `- 1.`은 프로파일 양식 `docs/profile/replacement_points.md:26-28`에만 등장
- ㉱ 용어 표 관습: README "용어" 절이 약어와 원어와 뜻 세 칸 표 (`README.md:43-55`, LDPC, QC, LLR, VNU/CNU, dv, CSW, FER/BER, HD/2SD/3SD, DAO). 프로파일 `constraints.md:19-22`도 같은 두 칸 표 양식
- ㉲ 결정 기록 관습: 사용자 결정은 날짜를 붙여 "사용자 결정 YYYY-MM-DD" 또는 "사용자 확정"으로 코드 docstring과 문서 양쪽에 적음 (`src/llr_matrix.py:17, 29, 34, 68`, `src/decoder.py:139`, `src/channel.py:1, 16, 98`, `src/pcm.py:7-8`, `docs/차이.md:23-26`). 정리 표는 `README.md:213-224` "확정 결정 기록"
- ㉳ 실험 폴더 README 양식: 날짜, 출처, 상태 머리줄과 "목적, 바꾼 것, 결과, 결론" 네 절 (`workspace/_template/README.md:1-22`)
- ㉴ C++ 대응 표기 관습: 함수와 주석마다 원본 C++ 함수 이름과 줄 번호를 괄호에 적음 (`src/decoder.py:138, 147, 152, 160, 165, 199` "[교체 지점: X 대응]", `src/channel.py:20, 52, 56` "channel.cpp:11-29")

### 7. 변경 금지와 고정 대상 (근거 위치 포함)

| 항목 | 내용 | 근거 |
|---|---|---|
| 상대 비교 전용 | py는 on/off 상대 비교 전용이며 C++ Ref-C와 절대 FER 일치를 보장하지 않음 | `README.md:4, 215`, `src/__init__.py:3-4` |
| all-zero codeword | `encode()`는 all-zero 반환 임시 함수. genie 판정과 BER 집계가 all-zero 전제이므로 인코딩을 실제로 바꾸면 셋을 함께 바꿔야 함 | `src/encoder.py:3-8, 18-21`, `README.md:207, 219`, `src/decoder.py:32-34, 401` |
| genie 성공 판정 | 매 iteration 판정을 정답과 information 구간에서 비교, 일치 시 성공 확정 (CRC 조기종료 이상화) | `README.md:218`, `docs/차이.md:24`, `src/decoder.py:316-327, 433-452` |
| Ref-C 헤더 전용 | H 파일은 `N_b M_b / J K / z / 빈 줄 / 행렬`만 지원, 구 포맷 지원 제거(2026-08-06), 행렬 뒤 무시, column block은 DV 내림차순 배치 전제 | `src/pcm.py:7-18, 58-82`, `README.md:13` |
| DAO LLR_MATRIX 형식만 | 모드는 파일명으로 판별(2026-08-06), max_iter는 마지막 iter_end, _validate는 DAO 산출 규칙 기준(2026-08-07) | `src/llr_matrix.py:11-37`, `README.md:14, 86-88` |
| 3-bit 전용 | 사람이 만든 LLR 파일은 th 3개 아니면 `NotImplementedError`. "LLR은 3-bit만 사용, 4-bit 확장 계획 없음 (사용자 확정 2026-08-06)". 균일 생성물만 n-bit | `src/llr_matrix.py:136-142`, `docs/차이.md:26`, `README.md:201-202` |
| DECODER_CLASS 한 곳 | 디코더 선택은 config가 아니라 실험 폴더 run.py의 `DECODER_CLASS`. `python -m src.run` 경로는 BaseDecoder 고정 | `README.md:33, 108-109, 175`, `workspace/_template/run.py:24-28`, `workspace/_template/config.json:6` |
| src 본체 무수정 | 디코더 변형은 src를 고치지 않고 BaseDecoder 상속 자식에서 교체용 함수 6개만 재정의. 정본은 `3_LDPC_ideas/새논문적용규칙.md` (이 저장소 밖) | `README.md:159-163`, `src/decoder.py:40-46` |
| base_run은 재정의 0개 | base_run 폴더에 decoder.py를 두지 않는다. "재정의 0개가 곧 본체와 완전히 같다는 보증" | `workspace/base_run/README.md:5-9`, `workspace/README.md:7` |
| workspace 용도 | 기준 실험(base_run) 전용, 논문 실험은 `3_LDPC_ideas/`에서 | `README.md:159-160`, `workspace/README.md:3-5` |
| seed 하나 | 실험 전체 난수 seed는 `run.seed` 하나, 스트림은 파생 | `README.md:110-111`, `src/run.py:554-555, 586` |
| H_matrix 폴더 고정 운용 | `Input/H_matrix` 고정 | `src/run.py:18-19`, `workspace/_template/config.json:13` |
| 입력 파일 외부 공급 | 평가할 H-matrix와 LLR 테이블은 저장소에 담지 않고 `Input/`에 넣어 config로 지정. 저장소의 파일은 예시 | `README.md:205-206, 223` |
| 비교 제외 항목 | dual update, pipeline store 지연, CRC, HCU, puncturing, shortening은 비교와 구현 범위 밖 | `docs/차이.md:8-9`, `README.md:216-217, 220`, `src/decoder.py:35-36` |
| HD iteration 1 edge clear 안 함 | 전 모드 restart만 클리어 (사용자 결정 2026-08-09) | `src/decoder.py:137-144`, `docs/차이.md:23` |
| 동점 반전 유지 | `sum_t <= 0` 반전, C++ 원문과 동일 유지 | `src/decoder.py:159-162`, `docs/차이.md:33` |
| dv 미매칭은 에러 | C++의 조용한 col_idx 0 fallback 재현 금지 (2026-08-06) | `src/llr_matrix.py:31-32, 347-357`, `docs/차이.md:25` |
| 겹침 금지와 순회 방향 한 쌍 | 그룹 겹침 금지를 풀려면 `_group_of_iter` 순회를 C++처럼 역방향으로 함께 바꿔야 함 | `src/llr_matrix.py:179-182, 362-367` |
| _cnu_update 제자리 수정 | 재정의해도 받은 배열을 제자리에서 고쳐야 함 (반환값 미사용) | `src/decoder.py:199-203` |
| _uniform_saturate 등가 조건 | 정수 raw에서만 캐스케이드와 등가. 비정수 raw를 만드는 재정의는 이 함수도 함께 재정의 | `src/decoder.py:189-195` |
| th = 레벨값 | 균일 생성 th 배치는 레벨값과 동일 (사용자 결정 2026-08-13) | `src/llr_matrix.py:60-68`, `README.md:224` |
| 균일 판별은 값 기준 | 레벨 구성 인식은 파일명이 아니라 th 패턴. uniform 파일명인데 패턴이 아니면 에러 | `README.md:106-107`, `src/llr_matrix.py:92-120, 275-279` |
| 채널 모드 전용 | fixed_error HD 전용, strong_error 2SD 전용, rber 세 모드 | `src/channel.py:78-81, 91-105, 145-149` |
| 난수 numpy Generator | XOR25 대신 numpy (2026-07-29). `_rand_positions`는 집합만 균일하므로 구간 슬라이스 금지 (리뷰 F1) | `src/channel.py:16, 71-75` |
| qfunc_inv 계수 유지 | channel.cpp 계수 그대로, 근사식 동일 유지 | `src/channel.py:24-34` |
| 시뮬 방침 | max_iter 120 기준, numba 미사용, 병렬은 mpi4py 코어당 sim 1개 | `README.md:221` |
| 이력물 보존 | `_pm/`과 docs/review/ 이력물은 줄표 수리에서 제외 보존 | `_pm/TODO.md:20` |
| floor flag | 로드 시 row의 다섯째 값(floor)을 저장하지 않고 (`rows` 튜플의 r[4] 미사용) 저장 시 항상 -1 기록. "왕복 보존은 현행 유지, 필요 시 재개" | `src/llr_matrix.py:156-161, 339-340`, `_pm/TODO.md:26` |

### 8. 알려진 한계와 기술 부채

- ㉮ README "남은 근사/제한" (`README.md:199-207`): 3-bit 전용, 파이프라인 store 지연 미재현, BF 구간 미구현, 예시 입력 파일, all-zero 임시 인코더
- ㉯ docs/차이.md 1절 미구현 목록 (`docs/차이.md:17-26`): 1.5SD와 Jump_Iter, BF, error floor 상태머신, 비 AUTO 테이블 전환, power stopping
- ㉰ src 안에 `TODO`와 `FIXME` 표시는 0건. "임시" 표시는 인코더 관련 세 곳만 (`src/encoder.py:3, 19`, `src/channel.py:14`, `src/run.py:7`)
- ㉱ `_pm/TODO.md` 미완 항목 (`:12-43`): 딥 리뷰 후속(floor flag 보존만 잔류), config checker 키별 허용값 확장(`:28`), dv range 상한 `ch ≤ 7·dv`(`:29-31`), mpi_runner 재설계와 슈퍼컴 이관(`:32-33, 41`), 후순위 로그 7종(`:34-37`), 평가 대상 H와 LLR 반입(`:38-40`), 프로파일 작성(`:42-43`)
- ㉲ 정의만 있고 저장소 안에서 호출되지 않는 코드: `QCCode.count_cycles4`, `QCCode.summary` (`src/pcm.py:94, 112`), `LLRMatrix.summary`, `needs_csw` (`src/llr_matrix.py:403, 408`), `collect_profile`과 `profile` 결과 (`src/decoder.py:430-431, 459-460`, run.py와 sim.py는 항상 False). `channel_config.get("label")` 두 곳 (`src/run.py:465, 577`)은 `_check_channels`가 label을 만들지 않으므로 죽은 경로 (DONE.md `:62` "points와 label 키 폐기"의 잔재로 추정)
- ㉳ 문서 참조 불일치: `README.md:15`가 `docs/review/`를 말하지만 폴더 없음 (리뷰 기록은 `_pm/done/*_review/`). `src/decoder.py:46`은 정본을 `docs/새논문적용규칙.md`로, `README.md:163`은 `3_LDPC_ideas/새논문적용규칙.md`로 적음 (둘 다 이 저장소에 없음). `_pm/DONE.md:1`은 프로젝트를 "2_LDPC_light"로, README는 "2_LDPC_base"로 부름. DONE.md가 언급하는 `workspace/minsum_dual_clip/`, `workspace/vanilla/`, `workspace/실험로그.md` (`_pm/DONE.md:17-21, 28, 77`)는 이 사본에 없음. 글로벌 규칙의 `_pm/tasks/_template/README.md`도 없음

## 관계와 흐름

- ㉮ 설정 흐름: `workspace/{실험}/run.py`가 상위로 올라가며 `2_LDPC_base/src`를 찾아 `sys.path`에 넣고 (`workspace/_template/run.py:11-20`) `src.run.main([config], decoder_class=DECODER_CLASS)`를 config마다 호출 (`:30-33`). `main`은 `load_config → setup → print_experiment_summary → create_run_dir → run_experiment → report` 순서 (`src/run.py:780-791`). 검증과 정규화는 `load_config` 한 함수에 모여 있고 이후 단계는 정규화된 dict만 신뢰함
- ㉯ 기본값과 검증과 소비의 삼각 관계: run 섹션은 `_RUN_DEFAULTS` 하나를 세 곳이 읽어 단일 출처가 성립 (`src/run.py:115-117, 358-360, 486-489, 557-563`). 그 밖의 섹션은 `setdefault`로 config dict에 기본값을 써 넣어 뒤 단계가 키 존재를 전제할 수 있게 함
- ㉰ 오류 전파 흐름: 검증 단계는 첫 위반에서 `ValueError`를 던지고 아무것도 만들지 않음. 파일 부재는 `setup`에서 (`src/run.py:403-411`) 실행 폴더 생성 전에 걸러지므로 빈 실행 폴더가 남지 않음. 실행 폴더는 `create_run_dir`에서 생성되며 (`:715-733`) 그 뒤의 실패(그림 저장)는 흡수해 측정 결과를 보존
- ㉱ 로그 흐름: JSON `log.items` 키 → `load_config` 평탄화 (`:385-387`) → `_LOG_TO_ITEM`으로 디코더 항목 이름 변환 (`:566`) → `run_fer_point(log=...)` (`src/sim.py:29-32`) → `decoder_main(log=...)` (`src/decoder.py:475`) → `_record_iteration`이 iteration별 합계 수집 (`:415-431`) → `run_fer_point`가 배치를 넘어 누적 (`src/sim.py:104-119`) → `report`가 CSV로 기록 (`src/run.py:748-763`)
- ㉲ summary.txt는 두 주체가 씀: `create_run_dir`가 머리를, `run_fer_point`가 포인트별 진행 줄과 결과 줄을 실시간으로 (`src/run.py:789-790`이 경로를 넘김)
- ㉳ 재현성 사슬: `run.seed` → `[seed, channel_index, int(1e6*point)]` 스트림 (`src/run.py:586`) → `channel_fn(batch, rng)` (`:524-528`) → 배치 크기가 난수 소비 순서를 정하므로 `frames_per_batch`까지 같아야 수치 재현 (`README.md:121`)

## 못 본 것과 추정

- ㉮ 런처 동작 제약 (중요): 실험 폴더 `run.py`는 상위 어딘가에 `2_LDPC_base/src`가 있어야 하는데, 이 사본의 루트 이름은 `ldpc_py`이고 상위 경로(`testbed`, `AI_Assisted_Dev`)에 `2_LDPC_base`가 없다 (glob 0건. 원본은 `LDPC_dev/2_LDPC_base/src/run.py`에 별도 존재). 따라서 이 사본에서 `python run.py`는 `SystemExit("상위 폴더에서 2_LDPC_base/src를 찾지 못함")`으로 끝날 것으로 추정되며, 동작하는 실행 경로는 루트에서 `python -m src.run <config>`뿐이다 (`README.md:32-33`). 실제 실행은 하지 않았으므로 미확인
- ㉯ `.gitignore`가 이 저장소에 없다 (glob 0건). README와 config가 말하는 "Sim_Output은 git 무시", "`_generated/`는 git 무시 영역" (`README.md:104, 170`, `workspace/README.md:12`)이 이 사본에서 실제로 성립하는지 미확인. `workspace/matrix_sel_1_HD/_probe/` 산출물 폴더 두 개는 저장소 안에 있음
- ㉰ `_pm/DONE.md`는 상단 80줄만 읽었고 `_pm/done/`, `_pm/tasks/20260808_review/`는 읽지 않았다 (지시대로 깊이 읽지 않음). 리뷰 이력 안의 추가 제약이나 결정이 있을 수 있음
- ㉱ 저장소 밖 정본 문서 `3_LDPC_ideas/새논문적용규칙.md`(교체용 함수 표, 상속 경계 규칙)와 `4_H_matrix_tool/README.md`는 확인하지 못했다. 교체 지점 규칙의 세부는 이 문서에만 있을 가능성이 높음
- ㉲ `Input/` 파일 중 `matrix_sel_1.txt`와 `LLR_MATRIX_HD_matrix_sel_1.txt`는 README의 "예시 파일" 서술(`README.md:205`)에 포함되는지, 평가 대상 실물인지 문서상 판별할 수 없었다 (`workspace/matrix_sel_1_HD_fixed/README.md:7`은 "4_H_matrix_tool에서 선별"이라고만 함). 프로파일 `constraints.md` 2절(입력 파일의 출처와 성격 기재 금지)에 걸릴 수 있는 문구가 `README.md:223`("LLR 값은 원본 소스 손상으로 소실")과 `_pm/TODO.md:31`("벤더 참고값")에 있음을 부른 쪽에 알린다
- ㉳ DONE.md `:71-75`가 말하는 단위 테스트 24건 등의 소재는 미확인 (저장소에 없음. 글로벌 규칙의 `_test/` 폴더에 있었다면 git 무시 대상이었을 것으로 추정)
- ㉴ 표면 탐색으로 남긴 곳: `Input/LLR/*.txt`의 내용 검증(파일 형식 확인은 `LLR_MATRIX_HD_1.txt` 앞 22줄만), `workspace/matrix_sel_1_HD/_probe/*` 두 폴더의 결과 파일
