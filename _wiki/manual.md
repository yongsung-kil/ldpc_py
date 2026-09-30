---
summary: 프로젝트가 무엇이고 어떻게 도는지 한 장으로
tags: [manual]
last_verified: 2026-09-30
---
# 매뉴얼

> wiki 스킬의 첫 실행(2026-09-30)이 `docs/profile/overview.md`와 `README.md`를 바탕으로 썼다. 프로젝트 설명이 바뀌는 결정이 있을 때 갱신한다.

## 무엇을 하는가

- ㉮ QC-LDPC(quasi-cyclic low-density parity-check, 순환 시프트 블록 구조의 저밀도 패리티 검사 부호) 복호 기법을 on/off로 상대 비교하는 Python 프레임 배치 시뮬레이터
- ㉯ 원본 C++ 시뮬레이터(Ref-C)의 syndrome-aided quantized min-sum 디코더를 flip/magnitude 도메인 그대로 재현한다
- ㉰ 디코더 변형은 본체 `src/`를 고치지 않고 `BaseDecoder`의 자식 클래스에서 교체 지점 함수 6개 중 필요한 것만 재정의해 붙인다
- ㉱ C++와의 절대 FER(frame error rate, 프레임 에러율) 일치는 보장하지 않는다. FER 1e-2에서 1e-4 영역의 상대 비교가 목적이다
- ㉲ 입력은 H-matrix 파일(Ref-C 헤더 형식), LLR 테이블 파일(DAO LLR_MATRIX 형식), 실험 설정 JSON 세 가지다. 출력은 실행 폴더 `output.dir/YYMMDD_HHMMSS_{label}/` 안의 config 사본, summary.txt, FER CSV, 로그 CSV 3종, 사용한 LLR 파일 사본, FER 커브 그림이다
- ㉳ 기준 치수는 base M_b=18, N_b=147, z=256 (codeword 37,632 bit, 정보 33,024 bit). 전 파라미터는 H-matrix와 LLR 파일에서 읽는다

## 어떻게 실행하는가

- ㉮ 의존 패키지: numpy(필수), matplotlib(그림 저장에만). `pip install -r requirements.txt`
- ㉯ 이 저장소(시험장 사본, 폴더 이름 `ldpc_py`)에서 동작하는 경로는 저장소 루트의 `python -m src.run <config.json 경로>` 하나다. 디코더는 BaseDecoder 고정이다
- ㉰ 원본 배치(`LDPC_dev/2_LDPC_base/`)에서는 실험 폴더 안의 `python run.py`가 정식 경로다. 런처가 조상 폴더에서 `2_LDPC_base/src`를 찾기 때문에 이 사본에서는 SystemExit로 끝난다 (2026-09-30 확인). 변형 디코더는 그 `run.py`의 `DECODER_CLASS` 한 곳에서 고른다
- ㉱ 새 실험은 `workspace/_template/`를 복사해서 만든다. 설정 스키마의 정본은 `workspace/_template/config.json`의 `_desc` 키와 `README.md` "JSON 설정 스키마" 절이다
- ㉲ 빠른 파이프라인 점검은 `workspace/test/config.json`(로그 끔, fixed_error 3포인트)으로 한다. 저장소 예시 LLR 파일로는 FER 1.0이 나오는 것이 정상이다 (예시 데이터 특성, [결정 20260809](decisions/20260809_fer-one-no-action-example-data.md))
- ㉳ 같은 seed로 수치를 재현하려면 config, seed, `frames_per_batch`까지 같아야 한다. 로직 무변경 확인은 두 실행의 FER CSV와 summary 결과 줄 완전 일치로 한다

## 어디를 보면 되는가

| 알고 싶은 것 | 볼 곳 |
|---|---|
| 프로젝트 지식의 정본 | `docs/profile/` 다섯 문서 (overview, structure, replacement_points, techniques, constraints) |
| 설정 키와 의미 | `README.md` "JSON 설정 스키마" 절, `workspace/_template/config.json` |
| 사용자가 확정한 결정 | `README.md` "확정 결정 기록" 절, 이 위키의 [결정 목록](decisions/MOC-decisions.md) |
| C++ 원본과 다른 점 | `docs/차이.md` |
| 코드가 어떻게 도는지 | 이 위키의 [기술 문서 목록](tech/MOC-tech.md) |
| 시도했지만 반영하지 않은 것 | 이 위키의 [시도 목록](trials/MOC-trials.md) |
| 다시 쓸 검증 방법과 점검 항목 | 이 위키의 [재사용 패턴 목록](assets/MOC-assets.md) |
| 진행 중 작업과 완료 이력 | `_pm/TODO.md`, `_pm/DONE.md` |
| 미결 판정 (status Proposed 3건) | [변형 디코더 실행 경로](decisions/20260930_variant-decoder-run-path.md), [이력 문서의 개인 경로](decisions/20260930_history-docs-personal-path.md), [입력 파일 출처 표기 규칙](decisions/20260930_input-source-notation-rule.md). 원문 경로는 각 문서의 `source` |
