---
summary: 균일 LLR matrix는 파일로 생성해 `output.dir/_generated/`에 저장한 뒤 파일 매트릭스와 같은 로더로 읽는 단일 경로이고, 균일 여부는 파일명이 아니라 th 값 패턴으로 판별한다
status: Accepted
tags: [llr-matrix, uniform, single-path]
date: 2026-08-08
commit: 0394b81 (시험장 사본에 포함)
source: _pm/DONE.md:207-231; _pm/tasks/20260808_review/종합보고.md:41-53, 104-105; src/llr_matrix.py:3-9, 92-120, 273-279; src/run.py:412-442
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ LLR 파일 없이 균일 양자화 레벨로 돌리는 경로가 필요했다 (2026-08-08 사용자 확정 설계)
  - ㉡ 처음 구현은 파일명의 `uniform` 문자열로 레벨을 정했다. 2026-08-08 딥 리뷰에서 `nonuniform`도 균일로 오탐되고, 같은 파일을 이름만 바꿔 로드하면 FER가 달라지며 경고가 0건임이 확인됐다
  - ㉢ 생성물이 추적 폴더 `Input/LLR/`을 오염하고, 파일명에 dv_max가 없어 무경고 덮어쓰기가 있었다
- ㉯ 거부한 대안
  - ㉠ 디코더가 메모리 합성 매트릭스와 파일 매트릭스를 다른 경로로 소비
  - ㉡ 파일명 부분문자열로 레벨 판별
  - ㉢ 생성 파일을 `Input/LLR/`에 저장
  - ㉣ `.gitignore` 패턴만으로 해결 (커밋된 파일에 무효, 파일명 규약에 결합)
- ㉰ 이유
  - ㉠ 단일 경로면 균일 경로와 파일 경로의 산술이 같음이 구조로 보장되고, 합성 후 저장 후 로드 왕복 검증이 가능하다
  - ㉡ 같은 내용의 파일이 이름에 따라 다르게 복호되면 안 된다. 판정 근거는 파일 내용이다
  - ㉢ 생성물은 git 무시 영역에 두고, 실제로 쓴 사본은 실행 폴더에 남겨 재현성을 확보한다
- ㉱ 결과로 생긴 규칙 (값 기반 판별, `_generated`, 사본 저장은 2026-08-09 확정)
  - ㉠ 생성 위치 `output.dir/_generated/`, 파일명 `LLR_MATRIX_{mode}_uniform_{bits}bit_max{max}_ch{값-값}_dv{dv_max}_iter{max_iter}.txt` (ch 자리는 region 수만큼의 값을 `-`로 잇는다). dv_max가 들어가므로 H 로드 뒤에야 확정된다 (`src/run.py:430-439`)
  - ㉡ 어느 경로든 `LLRMatrix.load` 한 곳으로 읽는다 (`:441`). `output.save_llr_matrix`(기본 true)가 사용 파일 사본을 실행 폴더에 저장하며 파일 로드 경로에도 적용된다
  - ㉢ 균일 판별식: 전 row와 전 dv의 th가 같고, 공차 d(1 이상)의 등차 감소이며, 마지막 항이 `2*d-1` (`src/llr_matrix.py:92-120`). 파일명의 uniform은 "사람이 만든 파일이 아니다"라는 표시일 뿐이다
  - ㉣ 파일명에 uniform이 있는데 패턴이 아니면 에러 (`:275-279`)
  - ㉤ 판정 결과는 `has_uniform_levels` 속성으로 노출하고 디코더가 생성자에서 한 번 읽는다
- ㉲ 비용
  - ㉠ 균일 모드는 전 dv 공통 ch라 dv별 차등을 표현하지 못한다. dv 차등은 파일 경로로 한다

## 하위 링크

- [20260809_uniform-min-level-one](20260809_uniform-min-level-one.md): 균일 레벨의 최소값 결정
- [20260813_edge-quantization-bits-max-split](20260813_edge-quantization-bits-max-split.md): 생성 레벨을 정하는 bit 수와 최대값
- [../assets/20260809_antipattern-filename-decides-semantics](../assets/20260809_antipattern-filename-decides-semantics.md): 파일명이 의미를 결정하면 생기는 오탐과 무경고 오답
- [../tech/20260930_uniform-llr-matrix-synthesis](../tech/20260930_uniform-llr-matrix-synthesis.md): 생성식, 저장 왕복, 값 기반 역판별의 현행 코드
