# CLAUDE.md: AI 작업 진입점

> 모든 작업 시작 전 이 파일을 읽을 것.

## 프로젝트

- ㉮ 이름: 2_LDPC_base (경량 QC-LDPC 시뮬레이터. 이 저장소는 시험장 사본이라 폴더 이름이 `ldpc_py`다)
- ㉯ 한 문장: QC-LDPC(quasi-cyclic low-density parity-check, 순환 시프트 블록 구조의 저밀도 패리티 검사 부호) 복호 기법을 on/off 상대 비교하기 위한 Python 프레임 배치 시뮬레이터. 원본 C++ 시뮬레이터의 syndrome-aided quantized min-sum 디코더를 재현하고, 디코더 변형은 본체를 고치지 않고 교체 지점 함수만 재정의해 붙인다
- ㉰ 실행: 저장소 루트에서 `python -m src.run <config.json 경로>` (예: `python -m src.run workspace/test/config.json`). 실험 폴더의 `python run.py`는 이 사본에서 `2_LDPC_base/src`를 찾지 못해 동작하지 않는다

## 지식의 정본

- ㉮ `docs/profile/`의 다섯 문서(overview, structure, replacement_points, techniques, constraints)가 이 프로젝트 지식의 정본이다. 코드를 넓게 읽기 전에 먼저 읽는다
- ㉯ 코드가 바뀌면 프로파일을 먼저 고친다
- ㉰ 설계 결정은 `docs/adr/`에 기록한다 (코드에서 읽을 수 없는 "왜"만). 이미 확정된 사용자 결정의 정리 표는 `README.md` "확정 결정 기록" 절이다
- ㉱ 탐색 결과는 `docs/explore/`, 위키는 `_wiki/`

## 작업 관리

- ㉮ `_pm/` (TODO, DONE, tasks, done). 절차는 pm 스킬
- ㉯ 변경 등급: Safe(로그, 주석, 포맷)는 자동 진행, Review(로직 변경)는 브리핑 뒤 진행, Decision(설계 변경)은 멈추고 사용자 확인

## 문장 규칙 (코드 주석과 문서 공통)

- ㉮ 수리는 덧대기가 아니라 다시 쓰기
- ㉯ 규칙은 긍정문
- ㉰ 이름과 용어는 명확성 우선. 약어는 첫 등장에서 풀어 쓴다
- ㉱ 줄표(U+2014)와 가운뎃점(U+00B7)을 쓰지 않는다. 나열은 ㉮㉯㉰와 ㉠㉡, 주소를 받는 갈래는 `- 1.`
- ㉲ 변경 금지 대상과 기밀 규칙은 `docs/profile/constraints.md`를 따른다
