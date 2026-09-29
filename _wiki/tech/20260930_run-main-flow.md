---
summary: src/run.py의 main이 부르는 5단계, 직접 실행과 런처 실행 두 경로, 실험 요약 불릿 11개, 공개 API
tags: [run, entry-point, main-flow]
sources: [src/run.py:1-15, src/run.py:393-446, src/run.py:458-493, src/run.py:504-512, src/run.py:548-600, src/run.py:780-795, workspace/_template/run.py:9-33, src/__init__.py:6-10]
last_verified: 2026-09-30
---

## 무엇을 하는가

- ㉮ `src/run.py`는 config JSON 하나로 실험 전체를 도는 진입점이다. 파라미터(config)와 코드(디코더 클래스)를 분리한다 (`src/run.py:1-15`)
- ㉯ `main(argv, decoder_class)`가 5단계를 순서대로 부른다. 디코더는 인자로 주입하고 config에는 디코더 선택 키가 없다

## 어떻게 도는가

- ㉮ 5단계와 요약 출력 한 번 (`src/run.py:780-791`)
  - ㉠ `load_config(argv[0])`: JSON 읽기와 검증 (키맵, 필수값, 값 제약) (`:785`)
  - ㉡ `setup(config, decoder_class)`: H-matrix 로드, LLR matrix 준비, 디코더 생성. `decoder_class`가 None이면 `BaseDecoder` (`:786`, `:443-445`)
  - ㉢ `print_experiment_summary`: 실험 요약을 콘솔에 출력 (단계 번호 없음, docstring의 5단계 밖) (`:787`)
  - ㉣ `create_run_dir(config, argv[0], code, decoder)`: 실행 폴더, config 사본, summary.txt 머리 (`:788`)
  - ㉤ `run_experiment(..., summary_path=run_dir/summary.txt)`: 채널 x 포인트 측정, summary.txt 꼬리 실시간 갱신 (`:789-790`)
  - ㉥ `report(results, config, decoder, run_dir)`: FER CSV, 로그 CSV, 그림, LLR 사본 저장 (`:791`)
- ㉯ 두 실행 경로
  - ㉠ 직접 실행: 저장소 루트에서 `python -m src.run <config.json>`. `__main__`이 `main()`을 인자 없이 부르므로 디코더는 BaseDecoder 고정 (`:783`, `:794-795`)
  - ㉡ 런처 실행: `workspace/{실험}/run.py`가 조상 폴더에서 `2_LDPC_base/src`를 찾아 그 `2_LDPC_base`를 `sys.path` 앞에 넣고, config마다 `main([config], decoder_class=DECODER_CLASS)`를 부른다. 인자가 없으면 형제 `config.json` (`workspace/_template/run.py:11-20`, `:30-33`)
  - ㉢ 이 사본은 폴더 이름이 `ldpc_py`라 런처가 `SystemExit`로 끝난다. 동작하는 경로는 직접 실행뿐 (`workspace/_template/run.py:14-16`)
- ㉰ 실험 요약 불릿 11개 (`_experiment_summary_lines`, `src/run.py:458-493`): H matrix, code(base, z, N, K, rate, E), col degree, row degree, LLR matrix(파일명과 공급 경로), max iteration, decoder(모듈.클래스), seed, channels, run 값, log 켠 항목. 콘솔과 summary.txt가 같은 줄을 쓴다
- ㉱ 측정 전 전 채널 모드 사전 확인 `_check_channel_mode` (`:504-512`, 호출 `:568-569`). 뒤 채널의 불일치로 앞 채널 측정이 버려지는 일을 막는다. 포인트마다 `_make_channel_fn`에서도 한 번 더 부른다 (`:519`)
- ㉲ 공개 API (`src/__init__.py:6-10`): `QCCode`, `BaseDecoder`, `channel`, `encoder`, `sim`

## 쓰는 법

- ㉮ 기준선 실험: 저장소 루트에서 `python -m src.run workspace/test/config.json`. 결과는 config 위치 기준 `output.dir` 아래 실행 폴더에 쌓인다
- ㉯ 변형 디코더 실험: 실험 폴더 `run.py`의 `DECODER_CLASS`에 `BaseDecoder` 자식을 지정하고 런처로 실행한다 (원본 배치에서만 동작). 이 사본에서 돌릴 경로는 판정요청 대기
- ㉰ 어느 디코더가 돌았는지는 summary.txt 머리의 `decoder` 줄로 확인한다
- ㉱ 같은 seed 수치 재현에는 `frames_per_batch`까지 같아야 한다 (`src/run.py:58-59`)

## 관련 문서

- ㉮ [시험장 사본과 원본 배치의 차이](20260930_testbed-copy-vs-original-layout.md)
- ㉯ [config 검증 규칙](20260930_config-validation-rules.md)
- ㉰ [channels 섹션과 실험 루프](20260930_channels-section-and-experiment-loop.md)
- ㉱ [setup의 LLR 공급 두 경로](20260930_setup-llr-supply-paths.md)
- ㉲ [실행 폴더와 출력 파일](20260930_run-dir-and-output-files.md)
- ㉳ 프로파일 [structure](../../docs/profile/structure.md), [overview](../../docs/profile/overview.md)
