---
summary: 딥 리뷰 검증 라운드에서 효과가 확인된 운영 규칙 6과 거짓 양성으로 판명된 지적의 공통 원인 5, 처방 채택 전 점검 4
type: pattern
tags: [review, verification, false-positive]
date: 2026-08-08
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/done/20260806_review/r3_round3_lv2_verification/team_a_verification.md:83-89, 203-212`, `_pm/tasks/20260808_review/r3_round3_lv2_verification/team_a_verification.md:56-58, 302-320, 336`, `_pm/done/20260806_review/r3_round3_lv2_verification/report.md:37-40`
- ㉮ 운영 규칙 6
  - ㉠ 발견과 처방을 가설로 형식화한다: "X 조건에서 Y 코드가 Z 동작을 해 P가 생긴다", "Q를 적용하면 P가 해결되고 새 문제가 없다"
  - ㉡ 전 라운드 결론을 전제로 쓰지 않는다. 검증 스크립트를 새로 써서 독립 재확인한다
  - ㉢ 실측 수치에는 채널 포인트, 프레임 수, max_iter를 반드시 병기한다. 조건 미기재 수치는 절반이 재현되지 않았다
  - ㉣ 심각도는 조건을 붙여 적는다 ("HIGH(2SD 구현 시)", "CRITICAL(batch가 정수 0일 때)"). 단순 강등은 시한 결함의 성질을 지운다. 기준표의 결과 축과 트리거 축을 섞지 않는다
  - ㉤ 처방은 독립이 아니다. 각각 유효해도 함께 넣으면 갈릴 수 있으니 상호작용을 따로 판정하고 적용 순서를 정한다
  - ㉥ 라벨과 수정 순서는 별개다. 조용히 틀린 수치가 hang보다 실질 피해가 크다
- ㉯ 거짓 양성의 공통 원인 5
  - ㉠ 동명이물: 개정본과 본체에 같은 이름의 파일이 있어 "삭제가 허위"라고 오판
  - ㉡ 소실 판정 전 git 미확인: `git ls-files`로 추적 중이고 재생성 경로가 살아 있는 자산을 "소실"로 보고
  - ㉢ 트리거 범위 과대: 유발값이 정수 0 하나뿐인 hang을 "batch <= 0 전부"로 서술
  - ㉣ 발동 조건 과대 서술: 정확 조건의 부분집합만 참인데 "정수배면 전부"로 일반화
  - ㉤ 도달 경로 오인: 사람이 개명해야만 도달하는 경로를 자동 경로처럼 서술
- ㉰ 처방 채택 전 점검 4 (부작용으로 고쳐진 처방에서 얻음): 같은 함수를 쓰는 다른 소비자, 로더와 포맷 제약, 본체 수치 보존, 다른 처방과의 상호작용

## 사용 방법

- ㉮ 언제: 리뷰 검증 라운드(Round 3)를 운영할 때, 리뷰 보고를 받아 처방을 채택할 때
- ㉯ 어떻게: 검증자 지시문에 ㉮ 여섯을 넣는다. 보고를 읽을 때 ㉯ 다섯을 점검표로 돌려 거짓 양성을 먼저 거른다. 채택 직전 ㉰ 넷을 확인한다
- ㉰ 주의: 원본 C++와 "다르다"는 것만으로는 결함 근거가 아니다. 원본이 받는 입력을 거부하거나 원본에 없는 통일을 만드는 처방은 기각한다
- 관련 문서
  - [20260808_prescriptions-revised-for-side-effects.md](../trials/20260808_prescriptions-revised-for-side-effects.md)
  - [20260806_rejected-unification-and-relaxation.md](../trials/20260806_rejected-unification-and-relaxation.md)
  - [20260808_equivalence-verification-methods.md](20260808_equivalence-verification-methods.md)
