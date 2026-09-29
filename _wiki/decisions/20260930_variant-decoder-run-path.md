---
summary: 이 시험장 사본에서 변형 디코더(BaseDecoder 자식)를 실행할 경로를 만들지 정한다. 선택지 셋, 권고는 런처 탐색 조건에 한 줄 추가. 사용자 답 없음
status: Proposed
tags: [testbed, launcher, decoder-injection]
date: 2026-09-30
commit: 77d9bc2 (온보딩 커밋)
source: _pm/tasks/20260930_explore_프로젝트전체/판정요청_시험장사본_260930.md:8-28, workspace/test/run.py:11-33, src/run.py:780-795, docs/profile/replacement_points.md:63, docs/explore/프로젝트전체.md:37-41
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - 이 사본에서는 런처 `run.py`(조상 폴더에서 `2_LDPC_base/src`를 찾는데 사본 폴더 이름은 `ldpc_py`)도, `python -m src.run`(BaseDecoder 고정)도 자식 디코더를 실행하지 못한다 (2026-09-30 실행 확인). 사정은 [20260930_testbed-copy-vs-original-layout.md](../tech/20260930_testbed-copy-vs-original-layout.md)
  - 그래서 새 기법을 붙이는 절차(양식 복사, 자식 클래스에서 교체 지점 재정의, 실행해 base_run과 비교)가 "실행" 단계에서 막힌다
- ㉯ 선택지
  - 1. (권고) 다섯 `run.py`의 탐색 조건에 "이 저장소의 `src/run.py`가 있는 조상 폴더"도 허용하는 한 줄을 더한다. 파일 5개, 12행 근처 3줄씩. 원본 배치(`LDPC_dev/2_LDPC_base/`)에서도 사본에서도 같은 명령 `python run.py`가 통한다. README와 config의 실행 안내를 고칠 필요가 없다
  - 2. 기존 `run.py`는 그대로 두고 저장소 루트를 찾는 새 런처 하나(예: `workspace/run_local.py`)를 더한다. 실험 폴더마다 실행 명령이 원본과 달라진다
  - 3. 바꾸지 않는다. 이 사본에서는 BaseDecoder 실험만 `python -m src.run`으로 돌리고 변형 실험은 원본 배치에서만 한다
  - 탐색 검증에서 나온 대안 표현: 조건을 `os.path.isfile(os.path.join(_root, "src", "run.py"))`로 바꿔 폴더 이름 의존을 없앤다
- ㉰ 권고 이유와 예외
  - 원본과 사본 양쪽에서 같은 명령이 통하고 git으로 되돌리기 쉽다
  - 사본을 원본과 한 글자도 다르지 않게 유지해야 한다면 3
- ㉱ 현 상태와 비용
  - 현 상태는 3 (무변경). 급하지 않다. 변형 디코더 실험을 이 사본에서 돌리려 할 때 필요해진다
  - 온보딩(2026-09-30)은 코드 무수정 원칙이라 이 항목을 판정요청으로만 남겼다
  - 답이 정해지면 이 문서의 status를 Accepted로 바꾸고 고른 번호와 이유를 적는다

## 하위 링크

- [../tech/20260930_testbed-copy-vs-original-layout.md](../tech/20260930_testbed-copy-vs-original-layout.md): 사본과 원본 배치의 차이 (런처 탐색, `-m` 경로, `.gitignore`, 형제 프로젝트)
- [20260810_decoder-class-single-switch-registry-removed.md](20260810_decoder-class-single-switch-registry-removed.md): 디코더 선택이 `DECODER_CLASS` 한 곳인 이유와 `-m` 경로의 한계
- [../assets/20260813_paper-idea-single-override-procedure.md](../assets/20260813_paper-idea-single-override-procedure.md): 이 사본에서 실행 단계가 막히는 절차
