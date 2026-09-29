---
summary: 2026-08-06 딥 리뷰의 처방 셋(genie 동점 규칙 통일, 비단조 th 거부, `_validate` 제약 완화)이 원본 C++와의 관계를 잘못 잡아 기각됐다
result: failed
tags: [review, rejected, cpp-relation, llr-file]
date: 2026-08-06
source:
  - _pm/done/20260806_review/r3_round3_lv2_verification/team_b_verification.md
  - _pm/done/20260806_review/r3_round3_lv2_verification/report.md
  - _pm/done/20260806_review/r4_round2_lv1_fix_review/report.md
  - _pm/done/20260807_리뷰후속수정/20260807_리뷰후속수정.md
adopted_as: decisions/20260807_llr-file-interpretation-rules
---

## 시도 내용

- ㉮ genie 동점 규칙 통일 (리뷰 F14): matrix 경로는 `sum_t <= 0`(동점 반전)이고 당시 남아 있던 legacy signed 경로 둘은 `<`라 경로마다 다르니 하나로 통일하자
- ㉯ 비단조 th 검사와 거부 (F8): LLR 파일의 th(VNU 양자화 임계값)가 내림차순이 아니면 로더가 거부하자
- ㉰ `_validate` 제약 완화 (F11): C++ 로더에 근거가 없는 제약 4종(그룹 겹침 금지, 빈틈 금지와 iteration 1 시작 강제, restart 그룹 단일 row, restart 마지막 금지)을 제거하거나 경고로 바꾸자

## 결과

- ㉮ 동점 통일: 반박. matrix 경로는 C++ 원문(decoder.cpp:4044) 강제이고 legacy 경로는 대조할 원문이 없다. `<=`로 통일하면 편향 방향만 뒤집힌다 (무작위 tie-break 기준선 0.1536이 `<`의 0.1458과 `<=`의 0.1562 사이). 현행 유지로 확정했고 legacy 경로 삭제(2026-08-07)로 문제 자체가 소멸
- ㉯ 비단조 th 거부: 반대. C++는 정렬 검사 없이 캐스케이드(elif 체인)로 소비한다. Python이 거부하면 원본이 받는 파일을 못 읽는다. 캐스케이드 교체를 채택하고 검사는 경고까지만
- ㉰ 제약 완화: Round 3가 "겹침 금지 유지, 커버리지 검사로 교체, restart 단일화 제거, restart 마지막 금지는 경고"로 수정 권고했으나 사용자는 DAO(decoder auto optimizer, 테이블 최적화 도구) 산출 규칙을 정본으로 삼아 유지를 확정 (2026-08-07). "빈틈 금지와 iteration 1 시작 강제"만 1..max_iter 커버리지 검사(미커버 iteration 번호 나열)로 바꿨다. 재리뷰가 완화 처방이 실수로 들어가지 않았음을 확인
- 교훈:
  - ㉠ 경로 간 "다르다"는 결함 근거가 아니다. 원문이 있는 쪽이 기준이고 원문 없는 쪽은 삭제 후보다
  - ㉡ 원본이 받는 입력을 Python이 거부하지 않는다. 의미가 어긋나면 경고
  - ㉢ "원본 로더에 검사가 없다"는 "제약이 없다"가 아니다. 실운용 도구의 산출 규칙이 정본일 수 있다
  - ㉣ 동점 쏠림의 뿌리는 all-zero 송신이며 근본 해법은 실제 인코더다

## 대안 선택 (있을 경우)

- ㉮ legacy 경로 삭제로 동점 규칙은 `sum_t <= 0` 하나만 남았다
- ㉯ 비단조 th는 경고만 내고 C++와 같은 캐스케이드 의미로 소비한다
- ㉰ `_validate`는 겹침 거부, 1..max_iter 커버리지, restart 단일 row, restart 마지막 금지를 유지한다. 겹침 금지와 `_group_of_iter` 정방향 순회는 한 쌍이라 겹침을 허용하려면 순회를 C++처럼 역방향으로 함께 바꾼다
- 관련 문서
  - ㉠ [20260807_llr-file-interpretation-rules.md](../decisions/20260807_llr-file-interpretation-rules.md)
  - ㉡ [20260807_legacy-deleted-not-repaired.md](../decisions/20260807_legacy-deleted-not-repaired.md)
  - ㉢ [20260930_llr-matrix-file-format-and-loader.md](../tech/20260930_llr-matrix-file-format-and-loader.md)
  - ㉣ [20260930_vnu-quantize-cascade.md](../tech/20260930_vnu-quantize-cascade.md)
