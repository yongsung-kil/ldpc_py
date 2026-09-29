---
summary: LLR 파일 해석 규칙 다섯 묶음. 파일에 없는 정보(모드는 파일명, max_iter는 마지막 iter_end), 형식 검증은 DAO 규칙 정본, 사람이 만든 파일은 3-bit 전용, dv 미매칭은 에러이고 기준은 H-matrix, floor flag는 보존하지 않는다
status: Accepted
tags: [llr-matrix, loader, dao]
date: 2026-08-07
commit: 0394b81 (시험장 사본에 포함)
source: src/llr_matrix.py:17-37, 136-142, 172-226, 237-241; docs/차이.md:25-26; _pm/done/20260807_리뷰후속수정/20260807_리뷰후속수정.md:21, 25, 51-62; docs/profile/constraints.md
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 공통 맥락
  - ㉠ LLR 파일은 DAO(decoder auto optimizer, LLR 테이블 최적화 도구)의 산출물이고 C++ 로더에는 검사가 거의 없다
  - ㉡ 2026-08-06 딥 리뷰 Round 3가 "C++에 근거 없음"을 이유로 완화를 처방했고 사용자가 되돌렸다. 아래 규칙마다 날짜와 이유를 적는다
- ㉯ 규칙 1: 파일에 없는 정보는 파일명과 마지막 row가 정한다 (2026-08-06)
  - ㉠ 디코딩 모드는 파일명 `LLR_MATRIX_{HD|2SD|3SD}_`로 판별한다 (`src/llr_matrix.py:17-18, 237-241`). 이유: 파일 포맷에 모드 필드가 없다. 거부한 대안: 파일 안에 모드 필드 추가 (DAO 포맷 변경)
  - ㉡ max_iter는 마지막 row의 iter_end다 (`:29, 162`). 파일 로드 경로에서 config의 `max_iter`는 읽지 않는다. 이유: C++가 같은 값을 쓰며 파일이 iteration 범위의 정본이다
- ㉰ 규칙 2: `_validate`의 형식 제약은 DAO 산출 규칙이 정본이다 (2026-08-07)
  - ㉠ 검사 항목: 그룹 겹침 금지, 1..max_iter 커버리지(미커버 iteration을 에러에 나열), restart 그룹은 단일 row 단일 iteration, restart 그룹은 마지막 금지 (`:34-37, 179-219`)
  - ㉡ 거부한 대안: C++ 로더(local_opt.cpp) 수준으로 완화, 겹침 허용, "빈틈 금지 + iteration 1 시작 강제"는 커버리지 검사로 교체
  - ㉢ 이유: DAO는 실제 운용용이라 규칙이 C++보다 정확하다. C++에 검사가 없는 것은 검증을 생략한 것일 뿐이다. 겹치는 파일은 오류가 있는 파일이다
  - ㉣ 비용: 겹침 금지와 `_group_of_iter`의 정방향 첫 매칭 순회가 한 쌍이다. 겹침을 허용하려면 순회를 C++처럼 역방향으로 함께 바꾼다. 비단조 th는 경고만 내고 캐스케이드 의미로 소비한다 (`:220-226`)
- ㉱ 규칙 3: 사람이 만든 LLR 파일은 3-bit 전용이다 (2026-08-06)
  - ㉠ `edge_mag` 미지정에 th가 3개가 아니면 NotImplementedError, 기본 레벨 {7,5,3,1} (`:136-142`). 4-bit 빌드(th 7개) 확장은 계획하지 않는다
  - ㉡ 이유: 사용자 확정이며 상세 이유는 기록에 없다. 넓은 레벨 실험은 균일 생성 경로로만 한다
- ㉲ 규칙 4: dv 미매칭은 에러이고 기준은 H-matrix다 (2026-08-06 fallback 미재현, 2026-08-07 기준 확정)
  - ㉠ column degree가 파일의 어느 dv 구간에도 없으면 에러 (`:31-32`)
  - ㉡ 거부한 대안: C++ `Get_VNU_LLR_SET_FILE`처럼 조용히 첫 구간을 쓰기
  - ㉢ 이유: 조용한 대체는 실수를 유발한다. 비용: 새 dv가 있는 부호를 쓰려면 LLR 파일의 dv 구간을 먼저 맞춘다
- ㉳ 규칙 5: floor flag는 보존하지 않는다 (2026-08-09 현행 유지 확인)
  - ㉠ 로드 시 버리고 저장 시 `-1`을 쓴다. 거부한 대안: 왕복 보존. 이유: 지금 쓰는 곳이 없고 나중에 쓰일 수 있어 현행을 유지한다

## 하위 링크

- [../tech/20260930_llr-matrix-file-format-and-loader](../tech/20260930_llr-matrix-file-format-and-loader.md): 파일 형식과 로더 검사 항목의 현행 코드
- [../trials/20260806_rejected-unification-and-relaxation](../trials/20260806_rejected-unification-and-relaxation.md): 기각된 완화 처방의 경위
- [20260807_config-keymap-fail-fast](20260807_config-keymap-fail-fast.md): 조용한 fallback을 재현하지 않는 같은 원칙
