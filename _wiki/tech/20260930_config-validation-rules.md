---
summary: load_config가 config JSON에 거는 검사 3층(키맵, 필수값, 값 제약)의 순서와 헬퍼 4개, 정규화 결과의 꼴
tags: [config, validation, run]
sources: [src/run.py:79-80, src/run.py:98-117, src/run.py:120-155, src/run.py:250-267, src/run.py:270-390, src/sim.py:58-70, workspace/_template/config.json:2-8]
last_verified: 2026-09-30
---

## 무엇을 하는가

- ㉮ `load_config(path)`가 JSON을 읽어 키맵, 필수값, 값 제약 3층으로 검사하고 내부 소비 꼴로 정규화한다. 위반은 `ValueError`로 즉시 종료한다 (조용한 기본값 대체 없음) (`src/run.py:79-80`, `:270-390`)
- ㉯ 원칙: 소비 여부와 무관하게 형식은 항상 검사한다. 같은 config의 통과와 실패가 플래그 값에 따라 갈리지 않는다 (`:252-254`, `:296-298`)

## 어떻게 도는가

- ㉮ 허용 키 집합 9개 (`src/run.py:98-111`)

| 집합 | 키 |
|---|---|
| 최상위 | H_matrix, decoder, channels, run, output, log |
| decoder | llr_matrix, use_input_llr_matrix, mode, max_iter, channel_llr_HD, channel_llr_2SD, channel_llr_3SD, use_default_edge_quantization, edge_quantization |
| decoder.edge_quantization | edge_resolution_bits, edge_max_value |
| run | seed, max_frame_errors, max_frames, frames_per_batch, stop_below_fer, print_progress, progress_interval_frames |
| output | dir, csv_prefix, label, save_llr_matrix |
| log | enabled, items |
| log.items | csw_per_iter, bit_err_per_iter, bit_err_by_dv, iter_histogram, fer_vs_iter, fail_frame_detail, fer_curve_png |
| channels | type, rber, fixed_error, strong_ratios |
| channels.strong_ratios | SER, SCR |

- ㉯ `_`로 시작하는 키(`_desc`)는 `_visible`이 걸러 검사에서 뺀다 (`:120-122`)
- ㉰ 헬퍼 4개: `_check_keys`(허용 밖 키 에러, `:125-130`), `_require`(없음 또는 null 에러, `:133-136`), `_check_int`(bool 배제, 정수, 최소값, `:139-144`), `_path_pair`(`{"dir", "file"}` 결합, 상대경로는 config 파일 위치 기준, `:147-155`)
- ㉱ 검사 순서 (`:270-390`)
  - ㉠ 최상위가 객체인지와 키맵 (`:279-281`). decoder, run, output, log 섹션이 객체인지 (`:283-285`)
  - ㉡ `H_matrix` 경로 결합 (`:287-288`)
  - ㉢ decoder: `use_input_llr_matrix` bool, `mode`는 HD, 2SD, 3SD 중 하나, `max_iter` 1 이상, `channel_llr_{HD|2SD|3SD}`는 길이가 region 수(1, 2, 4)이고 원소가 1 이상 정수, `use_default_edge_quantization` bool, `edge_quantization` 형식은 항상 검사 (`:290-321`, `:250-267`)
  - ㉣ 파일 경로면 `llr_matrix` 필수. 균일 경로면 `max_iter`와 `channel_llr_{mode}` 필수이고 커스텀 양자화면 조합 제약을 `edge_quantization_levels`로 판정 (`:322-339`)
  - ㉤ output: `dir` 기본은 config 폴더의 `Sim_Output` (`:343-345`), `save_llr_matrix` bool, `csv_prefix`와 `label` 문자열 (`:346-353`)
  - ㉥ run: `seed` 0 이상을 `config["seed"]`로 (`:357`), 정수 4개 1 이상 (`:358-360`), `print_progress` bool, `stop_below_fer` 양수 또는 null (`:361-370`)
  - ㉦ log: `enabled` bool, `items`는 bool dict, 평탄화 (`:372-387`)
  - ㉧ channels 정규화 (`:389`, 별도 문서)
- ㉲ 값 제약: `edge_resolution_bits` 2 이상 16 이하 (`:258-265`), `edge_max_value` 1 이상 정수 (`:266-267`). 2^n-1 꼴과 레벨 수 대비 정수 자리는 균일 경로에서만 검사 (`:331-337`)
- ㉳ 정규화 결과
  - ㉠ `config["H_matrix"]`, `config["decoder"]["llr_matrix"]`: 경로 문자열
  - ㉡ `config["seed"]`: 정수
  - ㉢ `config["log"]`: `{"enabled", 항목 7개}` 평탄 dict. `enabled`가 false면 항목 전부 False (`:385-387`)
  - ㉣ `config["channels"]`: `[{"type", "points", ...}]` 리스트
  - ㉤ run 기본값은 `_RUN_DEFAULTS` 하나를 검증, 소비, 요약이 함께 쓴다 (`:116-117`)

## 쓰는 법

- ㉮ config는 `workspace/_template/config.json`을 복사해 필요한 값만 바꾼다. 설명은 `_desc` 배열에 넣는다 (`workspace/_template/config.json:2-8`)
- ㉯ 값 공간(rber, fixed_error, strong_ratios)을 미리 채워 두고 `type`으로 고른다. 안 쓰는 공간도 형식은 검사되므로 잘못된 값을 남기지 않는다
- ㉰ 키 오타는 "알 수 없는 키" 에러로 바로 잡힌다. 에러 메시지에 섹션과 허용 키가 나온다
- ㉱ `run_fer_point`를 직접 부르는 코드는 `load_config`를 우회하므로 그 진입부의 최소 가드만 받는다 (`src/sim.py:58-70`)

## 관련 문서

- ㉮ [결정: 키맵과 필수값과 값 제약 fail-fast](../decisions/20260807_config-keymap-fail-fast.md)
- ㉯ [결정: 값 자리와 플래그 config](../decisions/20260813_config-slots-and-flags.md)
- ㉰ [잘못된 패턴: 조용한 대체](../assets/20260806_silent-fallback-config-and-import.md)
- ㉱ [channels 섹션과 실험 루프](20260930_channels-section-and-experiment-loop.md)
- ㉲ [setup의 LLR 공급 두 경로](20260930_setup-llr-supply-paths.md)
- ㉳ 프로파일 [structure](../../docs/profile/structure.md)
