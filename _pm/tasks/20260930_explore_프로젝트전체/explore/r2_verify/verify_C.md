# 검증 C 보고: 관계 검증 (모듈 사이 관계와 의존 설명, import와 호출 추적)

> 작성: 2026-09-30 (explorer 에이전트 보고 원문, 메인이 저장). 검증 대상은 `explore/r1_perspectives/취합.md`. 대조한 코드: `src/` 8개 파일 전문, `workspace/*/run.py` 5개, 루트 `__init__.py`, 저장소 전체 `*.py`의 import 문 전수(grep).

## 확인한 것

### 1. "모듈과 import 방향" 절

- ㉮ 맞음: `run` → {channel, encoder, decoder, llr_matrix, pcm, sim}. 근거 `src/run.py:91-96`.
- ㉯ 맞음: `sim` → `decoder`. 근거 `src/sim.py:9`.
- ㉰ 맞음: 잎 모듈 다섯(pcm, encoder, channel, llr_matrix, decoder)은 `src/` 안의 다른 모듈을 import하지 않는다. 순환 없음.
- ㉱ 틀림(경미): "numpy만 import하는 잎 모듈"은 `llr_matrix`에 맞지 않는다. `src/llr_matrix.py:39-41`이 표준 라이브러리 `os`, `re`, `warnings`를 추가로 import한다. "src 안의 다른 모듈은 import하지 않는다"로 고치면 정확하다.
- ㉲ 맞음: `decoder`는 `QCCode`와 `LLRMatrix`를 import 없이 생성자 인자로 받는다. 쓰는 속성이 실제로 존재하는지 대조했다. `llr_matrix.mode` :130, `.max_iter` :162, `.col_dv_idx()` :347, `.num_dv` :149, `.edge_mag` :143, `.has_uniform_levels` :389, `.ch_len` :131, `.is_restart()` :359, `.row_index()` :369, `.row_ch` :158, `.row_th` :159 (전부 `src/llr_matrix.py`). `code.N_b, M_b, z, E, edge_row, edge_shift, col_edges, col_deg, syndrome()` (`src/pcm.py:31-46, 85`). 이름 불일치 없음.
- ㉳ 맞음: `src/__init__.py:6-10` `__all__`에 `run`, `llr_matrix` 없음. `__init__` → pcm, decoder, channel, encoder, sim 노드가 방향 그래프 문장에 빠져 있다. 순환에는 영향 없음.

### 2. "계층과 호출 순서" 트리

- ㉮ 맞음: `main` 순서. `src/run.py:785-791`.
- ㉯ 맞음: setup 내부. `QCCode.load` :405, `make_internal_uniform_matrix` :423, `save` :439, `LLRMatrix.load` :441, `decoder_class(code, llr_matrix=llr_matrix)` :445.
- ㉰ 맞음: run_experiment → `run_fer_point` :588-594, 난수 파생 :586, stop_below_fer :597-598. `channel_fn`은 `_make_channel_fn` :515-530에서 만들어 실제 호출은 `src/sim.py:97`.
- ㉱ 맞음: `decoder_main` :501-508.
- ㉲ 맞음: `_process_column` 안 순서 :392, :400, :408, :412. `_run_iteration` 안 :342, :365.
- ㉳ 빠짐(트리 한정): 트리에 `_build_result` :508, `_init_state` → `_seed_channel_magnitudes` :277, `_run_iteration` → `llr_matrix.row_index` :360, `_collect_error_metrics` :368, SD restart 경로 :350-359가 없다. 산문에는 있다.

### 3. 교체 지점 6개 호출 위치 줄 번호

전부 맞음.

| 함수 | 문서 | 실제 def | 실제 호출 |
|---|---|---|---|
| `_is_edge_clear_iter` | :342 | :137 | :342 |
| `_column_order` | :365, :303 | :146 | :365, :303 |
| `_c2v_reconstruct` | :392 | :150 | :392 |
| `_vn_decide` | :400 | :159 | :400 |
| `_vnu_quantize` | :408 | :164 | :408 |
| `_cnu_update` | :412, :310 | :197 | :412, :310 |

빠짐 두 가지 (교체 지점 경계):
- ㉮ `_column_order`는 SD Pre 단계에서 `iteration=0`으로 호출된다 (:303). 재정의 시 0을 받을 수 있다.
- ㉯ `_run_iteration` :350은 `_is_edge_clear_iter`를 거치지 않고 `self.llr_matrix.is_restart(iteration)`를 직접 본다. 따라서 `_is_edge_clear_iter`를 재정의해도 SD restart의 Pre 재실행 여부(:350-359)는 바뀌지 않고 CN 클리어(:343-349)만 바뀐다. `_seed_channel_magnitudes` :310은 `edge_clear=True`를 고정으로 넘긴다.

### 4. 데이터 계약

- ㉮ 채널 → 디코더. 맞음. 생산 `src/channel.py:53, 88, 134-135` 네 키, 소비 `src/decoder.py:230-246`. 호출 시그니처 `src/run.py:527-528`. 빠짐(경미): `_read_channel_input` :241-244는 dict가 아닌 부호 있는 LLR 배열도 받는다 (HD 전용, 테스트 편의).
- ㉯ 디코더 → sim. 맞음. `_build_result` :456-471 생산 키와 `src/sim.py:99-119` 소비 키 전부 대응. `profile`은 소비처 없음.
- ㉰ sim → run. 맞음. `src/sim.py:142-156` 생산, `save_csv` :178-182, `report` :749-760, `_write_*`, `_plot_fer_curves` :699-703, `run_experiment` :597 소비.

### 5. 로그 항목 흐름

네 항목 모두 JSON 키 → `_LOG_TO_ITEM` → `run_fer_point(log=)` → `decoder_main(log=)` → `_record_iteration` 버퍼 → `_build_result` → sim 누적 → CSV 열까지 이어진다. 끊긴 고리 없음. `iter_histogram`, `fer_vs_iter`, `fer_curve_png`는 저장 여부만 결정.

### 6. 모드 정합 검사와 LLRMatrix.mode

- ㉮ `LLRMatrix.mode`는 항상 파일명에서 온다 (균일 생성 경로도 저장 후 다시 load, `src/run.py:439-441`).
- ㉯ 맞음: `_check_channel_mode` `src/run.py:504-512`. 호출은 두 곳: :569 (사전 확인)와 :519 (`_make_channel_fn` 안). 문서는 사전 확인만 적었다.
- ㉰ 맞음: `_read_channel_input` :230-232.
- ㉱ 빠짐(관계): 검사 층이 셋이다. 채널 함수 자체가 `mode` 인자를 검증한다 (`src/channel.py:46-47, 80-81, 104-105`). run 경로에서 디코더 쪽 검사 :230은 실패할 수 없다 (직접 호출 방어용).
- ㉲ `BaseDecoder.__init__` :108-109도 mode를 검사한다.

### 7. 런처 주입 사슬

- ㉮ 맞음: `workspace/*/run.py:22, 24, 33` → `src/run.py:780, 786, 443-445`.
- ㉯ 5개 동일: grep 표본 줄로 확인.
- ㉰ 틀림(표현): "`<조상>/2_LDPC_base/src`를 찾아 `sys.path`에 넣고"는 부정확하다. 찾는 조건은 `_root/2_LDPC_base/src`가 폴더인지(:12)이고, `sys.path`에 넣는 것은 `_root/2_LDPC_base` :18-20이다.
- ㉱ 빠짐(관계): 주입되는 디코더 클래스의 암묵 계약이 생성자 시그니처만이 아니다. `run_fer_point`가 `decoder.max_iter` `src/sim.py:72`와 `decoder.llr_matrix.num_dv` :73을, `report`가 `decoder.llr_matrix.dv_from`, `dv_to` (`src/run.py:742`, :623-624)를, `_check_channel_mode`가 `decoder.llr_matrix.mode` :507을, 요약이 `decoder.max_iter` :482를 읽는다. `isinstance` 검사는 없어 `BaseDecoder` 상속은 관례이지 강제가 아니다.

### 8. 외부 경계

- ㉮ 맞음: 형제 프로젝트를 코드로 import하는 곳 0건. `importlib`, `__import__`, `exec`, `eval` 0건. `sys.path` 조작은 런처 :19-20뿐.
- ㉯ 맞음: 표준 라이브러리 목록 11개 전부 일치. `csv`는 지연 import 4곳.
- ㉰ 맞음: matplotlib은 `_plot_fer_curves` :694-696에서만. `try/except Exception` :771-775.
- ㉱ 맞음: git은 `_git_commit_hash` :603-618 하나. `check=True`가 없어 저장소가 아니면 "(git 없음)".

## 관계와 흐름

- ㉮ import 그래프는 두 층이다. 조립층(`run`, `sim`, `__init__`)이 잎 다섯을 향해 한 방향으로만 가리키고, 잎끼리는 객체 전달(duck typing)로만 묶인다. `QCCode`와 `LLRMatrix`의 속성 이름 목록이 사실상 인터페이스다.
- ㉯ 모드는 파일명 → `LLRMatrix.mode` → `BaseDecoder` 검사 → `_check_channel_mode` → 채널 인자 → 채널 검증과 echo → 디코더 재대조, 한 값이 한 방향으로 흐른다.
- ㉰ 디코더 인스턴스는 `setup`에서 한 번 만들어 전 채널과 전 포인트가 공유한다. 호출별 상태는 `_DecodeState`가 담는다.
- ㉱ 교체 지점 6개 중 `_column_order`와 `_cnu_update`는 일반 iteration과 SD Pre 두 문맥에서 불리고, `_is_edge_clear_iter`는 CN 클리어에만 관여한다.

## 못 본 것과 추정

- ㉮ 런처 5개 "내용 동일"은 grep 표본 줄로 확인, 전문 diff는 안 함.
- ㉯ 실행 검증은 하지 않았다.
- ㉰ `_collect_error_metrics`의 실제 정의 범위는 :316-334다.
