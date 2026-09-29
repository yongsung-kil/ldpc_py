# 탐색 D 보고: 의존성 (라이브러리, 외부 연동, 버전 제약, 형제 프로젝트 참조)

> 작성: 2026-09-30 (explorer 에이전트 보고 원문, 메인이 저장. 경로는 저장소 루트 기준 상대 경로로 바꿨다)

사전에 읽은 `docs/profile/` 다섯 문서는 전부 빈 양식이었고 (예: `docs/profile/structure.md:27-30`의 "외부 의존성" 표가 비어 있음), 아래가 그 표의 원재료다.

## 확인한 것

### 1. 서드파티 라이브러리와 파일별 import

`requirements.txt:1-2`는 `numpy`, `matplotlib` 두 줄이고 버전 고정이 없다. 실제 import를 전수 대조한 결과 서드파티는 이 둘뿐이다.

| 파일 | 서드파티 | 표준 라이브러리 | 패키지 내부 |
|---|---|---|---|
| `src/pcm.py:20` | numpy | 없음 | 없음 |
| `src/channel.py:18` | numpy | 없음 | 없음 |
| `src/encoder.py:10` | numpy | 없음 | 없음 |
| `src/decoder.py:48` | numpy | 없음 | 없음 |
| `src/llr_matrix.py:39-43` | numpy | os, re, warnings | 없음 |
| `src/sim.py:2-9, 171` | numpy | numbers, os, sys, time, csv(함수 안 지연) | `.decoder` (BaseDecoder, LOG_ITEMS) |
| `src/run.py:82-96, 629, 658, 682, 694-696` | numpy, matplotlib(함수 안 지연) | datetime, json, os, shutil, subprocess, sys, csv(지연) | `.channel`, `.encoder`, `.decoder`, `.llr_matrix`, `.pcm`, `.sim` |
| `src/__init__.py:6-8` | 없음 | 없음 | QCCode, BaseDecoder, channel, encoder, sim 재노출 (`llr_matrix`, `run`은 `__all__`에 없음) |
| 루트 `__init__.py` | 없음 (docstring만) | | |
| `workspace/{_template,base_run,test,matrix_sel_1_HD,matrix_sel_1_HD_fixed}/run.py:6-7, 22` | 없음 | os, sys | `from src.run import main` |

- ㉮ numpy는 6개 모듈 전부의 필수 의존이고, matplotlib은 `run.py`의 그림 저장 한 함수에서만 쓰인다.
- ㉯ 다섯 런처(`workspace/*/run.py`)는 내용이 글자 단위로 동일하다.

### 2. 버전 제약 (명시 문구 없음, API 사용처로 추정)

Python 버전이나 라이브러리 버전을 요구하는 문구는 어느 파일에도 없다 (`pyproject`, `setup.py`, `python_requires` 없음. README:19-23은 `pip install -r requirements.txt`만).

- ㉮ Python 최소 3.7 (추정): `subprocess.run(..., capture_output=True, text=True, timeout=10)` (`src/run.py:608-615`, 두 인자 모두 3.7 추가). f-string 전역 사용, 클래스 본문 변수 주석 `read_bit: np.ndarray` (`src/decoder.py:58-96`, 3.6+), `raise ... from None` (`src/run.py:337`). 3.8 이후 문법(walrus, `list[int]`, match, dataclass)은 grep 0건.
- ㉯ numpy 최소 1.20 (추정): `random_generator.permuted(err_pos, axis=1)` (`src/channel.py:125`, Generator.permuted는 1.20 추가). 그 밖에 `np.random.default_rng([seed, channel_index, int(1e6 * point)])` (`src/run.py:586`, 1.17+), `Generator.integers(..., dtype=np.uint8)` (`src/encoder.py:15`, 1.17+), `np.take_along_axis` (`src/decoder.py:386`, 1.15+), `np.argpartition` (`src/channel.py:75, 121, 132`).
- ㉰ numpy 1.24 이상과 2.x 호환 (추정): 삭제된 별칭 `np.int`, `np.float`, `np.bool`, `np.object` 사용 0건 (grep). 실행으로 확인하지는 않았다.
- ㉱ matplotlib: `matplotlib.use("Agg")`, `pyplot.subplots`, `ax.plot`, `set_yscale("log")`, `grid`, `legend`, `tight_layout`, `savefig`, `close`만 사용 (`src/run.py:694-712`). 특정 버전 요구 없음 (추정).

### 3. 선택 의존과 지연 import

- ㉮ matplotlib은 `_plot_fer_curves()` 본문 첫 줄에서 지연 import하고 헤드리스 백엔드 `Agg`를 강제한다 (`src/run.py:694-696`).
- ㉯ 호출부 `report()`는 `log.fer_curve_png`가 true일 때만 부르고, `try: ... except Exception as exc:`로 감싸 "fer_curves.png 저장 실패 (측정 결과와 summary는 저장됨)"을 출력한 뒤 계속 진행한다 (`src/run.py:769-775`). matplotlib 미설치 시의 `ImportError`도 `Exception` 하위라 여기서 흡수된다. `try/except ImportError` 형태의 패턴은 저장소에 없다.
- ㉰ CSV/그림/LLR 사본 저장은 측정 뒤(`report`)이고, `summary.txt`와 config 사본은 측정 전(`create_run_dir`, `src/run.py:715-733`)과 측정 중(`sim.py:134-135, 164-166`)에 기록되므로 그림 실패가 결과 손실로 이어지지 않는다.
- ㉱ `csv`의 지연 import (`src/run.py:629, 658, 682`, `src/sim.py:171`)는 표준 라이브러리라 의존 보호 목적이 아니다.

### 4. 형제 프로젝트 참조 (저장소 밖을 가리키는 것 전수)

문서와 코드에서 저장소 밖을 가리키는 곳:

- 1. `README.md:1` 제목 "2_LDPC_base", `:15` `3_LDPC_ideas/새논문적용규칙.md`와 `docs/review/`, `:33` "`2_LDPC_base/`에서 `python -m src.run`", `:39-41` `4_H_matrix_tool/`와 `4_H_matrix_tool/README.md`, `:159-163` `3_LDPC_ideas/` 및 URL 인코딩된 상대 링크 `../3_LDPC_ideas/%EC%83%88...md`, `:221` mpi4py
- 2. 루트 `__init__.py:1, 4` "2_LDPC_base", "4_H_matrix_tool/"
- 3. `src/__init__.py:1, 3` "2_LDPC_base", "2_LDPC_base/README.md"
- 4. `src/run.py:12` "2_LDPC_base/에서 python -m src.run"
- 5. `src/decoder.py:46` `docs/새논문적용규칙.md` (저장소 안 경로로 적혀 있으나 `docs/`에 그 파일이 없음. README:15는 같은 문서가 `3_LDPC_ideas/`에 있다고 적어 두 곳이 어긋남)
- 6. `docs/차이.md:6` `0_LDPC_original/src/decoder.cpp`, `1_LDPC_revised/decoder.cpp`
- 7. `workspace/README.md:4-5` 3_LDPC_ideas
- 8. `workspace/base_run/README.md:24-25` `../../../3_LDPC_ideas/새논문적용규칙.md`, `3_LDPC_ideas/_template/`
- 9. `workspace/matrix_sel_1_HD_fixed/README.md:7` 4_H_matrix_tool
- 10. config `_desc`의 "../../ = 2_LDPC_base" (`workspace/base_run/config.json:4`, `test/config.json:5`, `_template/config.json:4`, `matrix_sel_1_HD/config.json:5`, `matrix_sel_1_HD/_probe.json:5`)

런처가 src를 찾는 방식 (`workspace/base_run/run.py:9-22`, 다섯 파일 동일):

- ㉮ 자기 폴더에서 시작해 부모로 올라가며 `{폴더}/2_LDPC_base/src`가 존재하는 첫 조상을 찾는다 (12-17행). 드라이브 루트까지 못 찾으면 `SystemExit("상위 폴더에서 2_LDPC_base/src를 찾지 못함 (이 파일은 LDPC_dev 하위 실험 폴더에 있어야 함)")`.
- ㉯ 찾으면 `{조상}/2_LDPC_base`를 `sys.path[0]`에 넣고 `from src.run import main` (18-22행). 디코더 선택은 `DECODER_CLASS` 변수 하나 (24행), `main([config_path], decoder_class=DECODER_CLASS)` 호출 (31-33행).
- ㉰ 즉 저장소 폴더 이름이 정확히 `2_LDPC_base`이고 그 위에 `LDPC_dev`가 있다는 원래 배치를 전제한다.

시험장 사본에서의 결과 (Glob으로 확인, 실행은 안 함):

- ㉮ 이 저장소 폴더 이름은 `ldpc_py`이고, 조상 폴더 어디에도 `2_LDPC_base/src`가 없다. 따라서 다섯 런처 전부 SystemExit로 끝날 것이다.
- ㉯ 원래 배치는 `LDPC_dev/2_LDPC_base/src/run.py`로 별도 존재함을 확인했다 (내용은 보지 않음).
- ㉰ 반면 저장소 루트에서 `python -m src.run workspace/base_run/config.json`을 실행하는 경로는 폴더 이름과 무관하다 (`src/run.py:780-791`). config의 상대경로 `../../Input/...`은 config 파일 위치 기준으로 풀리므로 (`src/run.py:147-155, 277`) `ldpc_py/Input`을 정확히 가리킨다.
- ㉱ 저장소 루트에 `.gitignore`가 없다 (Read 실패로 확인). README:104, 170의 "git 무시 영역" 서술과 어긋난다. `docs/review/`도 없다 (docs에는 `차이.md`, `profile/`, `adr/`만). 둘 다 원본에는 있고 사본에 안 담긴 것으로 추정한다.
- ㉲ "Ideas 임포트": 코드에 `Ideas`라는 import는 0건이다. `_pm/TODO.md:22`에 "Ideas 임포트 실패는 에러로 종료" 이력만 남아 있고, 현재는 런처의 SystemExit가 그 역할이다. `3_LDPC_ideas` 쪽이 src를 import하는 방식은 저장소 밖이라 미확인 (README:160 서술만).

### 5. 외부 도구와 포맷 의존

Ref-C H-matrix (.qc), `src/pcm.py`:

- ㉮ 포맷은 `N_b M_b` / `J K` / `z` / 빈 줄 / 행렬 (docstring 7-18행, 구 포맷 지원은 2026-08-06 제거).
- ㉯ 로더 `QCCode.load` (58-82행): 빈 줄 제거 후 첫 줄이 정수 2개가 아니면 ValueError (66-69행), `lines[3:]`를 통째로 `split()`해서 앞 `M_b*N_b`개만 사용 (73-76행) → 뒤 내용 무시 (행렬 2벌 파일은 첫 벌만), 헤더 J/K보다 실제 degree가 크면 에러 (78-81행). 확장자 검사 없음 (.qc와 .txt 모두 로드), 공백과 탭 모두 처리.
- ㉰ shift 값이 z 이상이면 에러 (28-29행). "column block DV 내림차순 배치"는 전제만 있고 코드 검사는 없다 (18행).

DAO LLR_MATRIX, `src/llr_matrix.py`:

- ㉮ 포맷은 `DAO_LLR_MATRIX.py Read_Input_LLR_Matrix`와 동일하다고 주장 (11-15행): num_parameter_each_set / num_dv / dv_from / dv_to / num_group / num_row_each_group / type_each_group / num_restart / [restart_iter] / max_value / min_value / row들. row 길이는 `num_dv*num_param + 4` (269행), 값은 정수만 파싱 (244행).
- ㉯ 디코딩 모드는 파일에 없어 파일명으로 판별: 정규식 `LLR_MATRIX_(HD|2SD|3SD)_` 대소문자 무시 `search` (48, 237-241행), 없으면 에러. ch 개수는 `MODE_CH_LEN = {"HD": 1, "2SD": 2, "3SD": 4}` (45행), th 개수 = num_param - ch.
- ㉰ 사람이 만든(DAO) 파일은 th 3개(3-bit, EDGE {7,5,3,1}) 전용 (137-142행 NotImplementedError). 파일명에 `uniform`이 있으면 th가 등차 감소 패턴이어야 함 (275-279행).
- ㉱ max_iter는 마지막 row의 iter_end (162행). DAO 규칙 검증(그룹 겹침 금지, 커버리지, restart 단일 row) 172-226행.
- ㉲ 균일 생성 파일은 `output.dir/_generated/LLR_MATRIX_{mode}_uniform_{bits}bit_max{max}_ch{...}_dv{dv_max}_iter{max_iter}.txt`로 저장 후 같은 로더로 읽음 (`src/run.py:430-441`, 저장은 탭 구분 정수 `src/llr_matrix.py:318-344`).

C++ 원본(Ref-C) 대응 상수와 위치 인용:

- ㉮ `GROUP_TYPE_ITER, GROUP_TYPE_CSW = 0, 1` (`src/llr_matrix.py:46`, common.h:756-757 인용)
- ㉯ SD Pre 단계 채널 magnitude 고정 상수 2SD [5,1], 3SD [7,5,3,1] (`src/decoder.py:122-123, 134`, decoder.cpp:4905/4924 인용). 파일에서 읽지 않음.
- ㉰ 채널 상수 `_R_OFFSET` (channel.cpp:11-29), `qfunc_inv` 계수 (`src/channel.py:20-34`)
- ㉱ 비교 기준 빌드는 DAO 연동 `__AUTO_LLR_OPT__` 경로 (`docs/차이.md:6-8`)

### 6. 실행 환경 의존

- ㉮ 파일 인코딩: 모든 `open()` 12곳에 `encoding="utf-8"` 명시 (`src/llr_matrix.py:242, 343`, `src/run.py:274, 640, 667, 683, 731`, `src/pcm.py:52, 64`, `src/sim.py:23, 91, 172`). CSV는 `newline=""` 지정.
- ㉯ 콘솔 출력: print 문에 한국어가 포함된다 ("(파일 로드)", "(전부 꺼짐)" `src/run.py:469-470, 490`, 그림 실패 메시지 `:775`). `sys.stdout.reconfigure`나 `PYTHONIOENCODING` 언급은 없어, 한국어를 못 내는 콘솔 인코딩에서는 UnicodeEncodeError 가능성이 있다 (추정). 화살표나 ⊕ 같은 기호는 docstring과 주석에만 있고 print에는 없다.
- ㉰ 진행 줄: `sys.stdout.isatty()`가 참일 때만 `\r`로 제자리 갱신 (`src/sim.py:86, 133`), 파일 리다이렉트 시 최종 줄만 출력 (163행).
- ㉱ 경로: `os.path`만 사용, `pathlib`과 하드코딩 구분자 0건 (grep). 실행 폴더 이름 `%y%m%d_%H%M%S_{label}` (`src/run.py:721-723`). README 명령 블록은 ```bat (README:21, 27) 이라 Windows 문서 관례이지만 코드는 POSIX에서도 동작할 것으로 추정한다.
- ㉲ git 호출: `_git_commit_hash()` (`src/run.py:603-618`)가 `git rev-parse --short HEAD`와 `git status --porcelain`을 `cwd=src 폴더`, `timeout=10`으로 실행, 빈 출력이나 `OSError`, `SubprocessError`면 "(git 없음)", 변경 있으면 `+dirty`. `summary.txt` 둘째 줄에 기록 (727행). 실제 기록 예 `workspace/matrix_sel_1_HD/_probe/260818_225547_probe/summary.txt:2` "code commit: ecec8ae+dirty". git 실행 파일이 PATH에 없어도 시뮬레이션은 계속된다. 추정: `.gitignore`가 없는 이 사본에서 `Sim_Output/`을 만들면 untracked 파일 때문에 이후 모든 실행이 `+dirty`로 기록될 것이다.
- ㉳ 병렬화: `mpi4py`, `numba`, `multiprocessing`, `threading` import 0건 (src grep). README:221 "numba 미사용, 병렬화는 mpi4py로 (mpi_runner 재설계 예정)"과 `_pm/TODO.md:32, 41` (mpi_runner 재설계, 슈퍼컴 이관 미착수)로 계획만 있다. 현재 병렬성은 numpy 프레임 배치 벡터화만 (`src/decoder.py:38`, `docs/차이.md:50`).

### 7. 입력 데이터

`Input/H_matrix/`

| 파일 | 첫 줄들 | 쓰는 config |
|---|---|---|
| `example_18x147_z256.qc` | `147 18` / `4 31` / `256` / 빈 줄 / 공백 구분 행렬 (N_b 147, M_b 18, J 4, K 31, z 256) | `base_run/config.json:7-10`, `test/config.json:11-14`, `_template/config.json:15-16` |
| `matrix_sel_1.txt` | `145 15` / `11 52` / `256` / 빈 줄 / 탭 구분 행렬 (후행 탭 다수) | `matrix_sel_1_HD/config.json:8-11`, `matrix_sel_1_HD_fixed/config.json:7-10`, `matrix_sel_1_HD/_probe.json:7-10`. 실행 기록: base 15x145, N 37120, K 33280, col degree {2:14, 3:69, 4:20, 11:42} (`_probe/260818_225547_probe/summary.txt:6-7`). 확장자가 .txt라 README:13의 ".qc" 서술과 다르지만 로더는 확장자를 보지 않음 |

`Input/LLR/`

| 파일 | 헤더 요약 | max_iter | 쓰는 config |
|---|---|---|---|
| `LLR_MATRIX_HD_0.txt` | num_param 4, num_dv 4, dv [11,4,3,2] 정확 매칭, 3그룹(각 1 row, 전부 CSW 타입), restart 1개(iter 2), max 31 | 5 (row 3: 3..5) | 없음 (README:14 "restart 포함 토이") |
| `LLR_MATRIX_HD_1.txt` | 2그룹(1..1, 2..20), restart 0 | 20 | `base_run:12-15`, `test:18-21`, `_template:48-51` |
| `LLR_MATRIX_2SD_toy0.txt` | num_param 5 (ch 2 + th 3), num_dv 1, dv 1..11, 3그룹 ITER, restart 11 | 20 | 없음 |
| `LLR_MATRIX_3SD_toy0.txt` | num_param 7 (ch 4 + th 3), 나머지 2SD_toy0과 같은 구조 | 20 | 없음 |
| `LLR_MATRIX_HD_matrix_sel_1.txt` | num_param 4, num_dv 4, dv [11,4,3,2], 8그룹 row 수 [1,5,5,7,6,10,10,13] 전부 CSW 타입, restart 0 | 120 (69-81행 마지막 그룹 101..120) | `matrix_sel_1_HD:15-18`, `matrix_sel_1_HD_fixed:14-17`, `_probe.json:14-17` |

- ㉮ `workspace/matrix_sel_1_HD/_probe/260818_225547_probe/LLR_MATRIX_HD_matrix_sel_1.txt`는 실행 시 저장된 사본이다 (`output.save_llr_matrix`, `src/run.py:764-768`).
- ㉯ 균일 생성 경로의 config 기본값: mode HD, max_iter 30, channel_llr_HD [8], 2SD [6,10], 3SD [4,6,8,10], bits 3, max 7 (`_template/config.json:52-61`). README:222-223 "입력 파일은 저장소에 담지 않는다"는 결정과 달리 예시 7파일이 들어 있고 README:205가 이를 "예시 파일"로 설명한다.

## 관계와 흐름

import 방향 (화살표는 "가 를 import한다"):

```
workspace/{실험}/run.py  (sys.path에 {조상}/2_LDPC_base 추가, 이름 하드코딩)
  └─ src.run.main
       ├─ src.channel, src.encoder, src.pcm, src.llr_matrix, src.decoder, src.sim  ── numpy (필수)
       │     └─ src.sim ── src.decoder
       ├─ matplotlib (report 단계, 지연 import, 실패 흡수)
       └─ subprocess git (create_run_dir 단계, 실패 시 "(git 없음)")
```

자료 흐름과 외부 경계:

- 1. `config.json` (상대경로는 config 위치 기준) → `Input/H_matrix/*.qc|txt` (Ref-C 포맷, 생산자는 저장소 밖 `4_H_matrix_tool`) → `pcm.QCCode`
- 2. `Input/LLR/LLR_MATRIX_{HD|2SD|3SD}_*.txt` (DAO 포맷, 생산자는 저장소 밖 DAO) 또는 `output.dir/_generated/` 자체 생성물 → `llr_matrix.LLRMatrix` → 모드와 max_iter를 결정해 `BaseDecoder`에 주입
- 3. `sim.run_fer_point` → `output.dir/YYMMDD_HHMMSS_{label}/` (config 사본, summary.txt에 git 해시, CSV, PNG, LLR 사본)
- 4. 저장소 밖 소비자: `3_LDPC_ideas`가 같은 런처 패턴으로 src를 import (README:160, 미확인). 등가성 비교 대상 `0_LDPC_original`, `1_LDPC_revised` C++는 문서 인용으로만 연결

이 저장소는 형제 프로젝트를 코드로 import하지 않고 ㉮ 파일 포맷(Ref-C, DAO) ㉯ 폴더 이름 규약(`2_LDPC_base`, `LDPC_dev`) ㉰ 문서 링크 세 가지로만 묶여 있다. 시험장 사본에서 실제로 끊어지는 것은 ㉯ 하나이며, 그 영향이 다섯 런처 전부다.

## 못 본 것과 추정

- ㉮ 코드를 실행하지 않았다. Python 3.7, numpy 1.20 최소치와 numpy 2.x 호환은 API 사용처와 grep에서 추정한 값이다.
- ㉯ 저장소 밖 `LDPC_dev/2_LDPC_base`, `3_LDPC_ideas`, `4_H_matrix_tool`, `0_LDPC_original`, `1_LDPC_revised`, DAO 도구는 존재 여부만 일부 확인(`LDPC_dev/2_LDPC_base/src/run.py` 존재)하고 내용은 보지 않았다. `3_LDPC_ideas`가 src를 import하는 실제 코드는 미확인이다.
- ㉰ `example_18x147_z256.qc`에 행렬이 2벌 들어 있는지 미확인이다 (로더가 첫 벌만 읽는 것은 코드로 확인).
- ㉱ `Sim_Output/`이 git에 추적되는지, `.gitignore` 부재가 사본 제작 시 누락인지 미확인이다 (git 명령을 돌리지 않음).
- ㉲ 콘솔 인코딩 문제(한국어 print)는 가능성 지적이며 재현하지 않았다.
- ㉳ `_pm/`은 `TODO.md` 앞 60줄과 grep 결과만 보았다.
