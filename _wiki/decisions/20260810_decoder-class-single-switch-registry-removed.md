---
summary: 디코더 선택은 실험 폴더 run.py의 `DECODER_CLASS` 한 곳이 한다 (None이면 BaseDecoder). config의 `decoder.type` 키와 registry(이름에서 클래스 경로로 가는 변환표)를 없앴고, 실험 공간을 `workspace/`(당시 이름 `Ideas/`)로 개명했다
status: Accepted
tags: [decoder, launcher, workspace]
date: 2026-08-10
commit: 0394b81 (시험장 사본에 포함)
source: _pm/done/20260810_workspace전환/20260810_workspace전환.md:10-31, 44-51, 55, _pm/DONE.md 2026-08-10 "workspace 전환" 항목, README.md:33, 108-109, 174-175, src/run.py:14-15, 393-396, 443-445, workspace/_template/run.py:22-33, docs/profile/constraints.md:27
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 2026-08-07 구조에서는 진입점이 config(JSON) 하나라 config의 `decoder.type` 이름을 클래스로 바꾸는 registry가 필요했다
  - ㉡ 2026-08-10 사용자 결정: 실험마다 폴더(논문이나 실험 환경별로 자유 명명)를 만들고 그 안의 run.py 하나만 실행한다. 본체 `src/`는 복사하지 않는다
- ㉯ 거부한 대안
  - ㉠ config에 디코더 이름을 적고 registry로 찾는 것 (기존 방식)
  - ㉡ 실험마다 본체를 복사하는 것
- ㉰ 이유
  - ㉠ run.py(코드)가 진입점이면 자기 폴더의 decoder.py에서 클래스를 직접 import할 수 있어 변환표가 불필요하다
  - ㉡ config에는 파라미터만 남겨 코드와 설정의 역할을 나눈다
- ㉱ 결과로 생긴 규칙이나 비용
  - ㉠ `main(argv, decoder_class=)`와 `setup(config, decoder_class=)`가 클래스를 주입받는다. None이면 BaseDecoder다 (src/run.py:443-445). 실험 요약에 디코더 클래스 이름이 찍힌다
  - ㉡ config에 디코더 선택 키가 없다. 새 실험은 `workspace/_template/`를 복사하고 run.py의 `DECODER_CLASS` 한 줄만 바꾼다
  - ㉢ 런처는 자기 위치에서 상위로 올라가며 본체 폴더를 찾아 `sys.path`에 넣으므로 복사 후 무수정으로 동작한다. 단 이 시험장 사본은 폴더 이름이 달라 런처가 `SystemExit`로 끝나고, `python -m src.run` 경로는 BaseDecoder 고정이라 자식 디코더를 실행할 경로가 없다 (판정요청 대기)
  - ㉣ 입력은 공용 `Input/`, 출력은 config 위치 기준 실행 폴더다
  - ㉤ 검증: 기준 실험 재실행이 이전 실행과 수치 동일(FER CSV와 로그 CSV 전부 일치, 차이는 경과시간 열뿐), 변형 디코더 주입으로 BER이 달라짐을 실증, `python -m` 경로 회귀 확인
  - ㉥ 뒤따른 결정: 루트 config.json 삭제 (2026-08-10), config 골자는 `workspace/_template/config.json` 하나
- 날짜: 2026-08-10 (폴더명 소문자 workspace 확정 포함)

## 하위 링크

- [../tech/20260930_testbed-copy-vs-original-layout.md](../tech/20260930_testbed-copy-vs-original-layout.md): 시험장 사본과 원본 배치의 차이, 런처 탐색과 주입 사슬
- [20260930_variant-decoder-run-path.md](20260930_variant-decoder-run-path.md): 이 사본에서 변형 디코더를 돌릴 런처 수정 여부 (판정요청)
- [20260807_replacement-point-cpp-function-boundary.md](20260807_replacement-point-cpp-function-boundary.md): 주입되는 자식 클래스가 재정의하는 교체 지점 구조
- [20260813_config-slots-and-flags.md](20260813_config-slots-and-flags.md): 루트 config 삭제와 설명 정본 단일화
