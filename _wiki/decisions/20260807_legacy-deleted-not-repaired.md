---
summary: legacy 복호 경로와 구 자산은 수리하지 않고 삭제한다 (git 이력으로 복구). plan.md도 삭제하고 결정 기록만 README로 옮겼으며, README 상시 최신 의무는 두지 않는다
status: Accepted
tags: [cleanup, legacy, documentation]
date: 2026-08-07
commit: 2e600ea (원본 저장소, 구 코드 삭제 커밋)
source: _pm/DONE.md (2026-08-07 개정본 본체 반영, 가독성 리팩토링, 딥 리뷰 후속 수정), _pm/done/20260807_리뷰후속수정/20260807_리뷰후속수정.md:19, 22-23, 64-77, 85, _pm/done/20260807_가독성리팩토링/20260806_가독성리팩토링.md:96-100, _pm/tasks/20260808_review/종합보고.md:72, 74-79, 106, _pm/TODO.md:14-15, 27
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - 개정본 decoder에 matrix 경로 외 legacy 경로 셋(two_set 스케줄, column_wise 경로, llr_profile 모드의 signed LLR 경로)이 남아 있었다. 데이터 파일이 없어 사실상 미사용
  - 2026-08-06 딥 리뷰 F4~F7이 본체 반영 때 파손될 구 자산(examples, mpi_runner, llr/ 등)을 열거했다. F14는 genie 동점 처리가 경로마다 다르다고 지적했는데 Round 3에서 "legacy는 C++ 대응 원문이 없어 '다르다'가 결함 근거가 못 된다"로 판정됐다
  - 2026-08-09 종합보고: 구 코드 삭제 커밋이 `llr_tables.py`를 빠뜨렸고, `llr_tune`의 LLR 후보 비교 절차는 대체가 없다. `docs/plan.md`는 머리 단서가 낡은 정보를 보증하고 포맷 서술이 현행과 어긋났다. README 여러 곳이 코드와 어긋났다
- ㉯ 거부한 대안
  - ㉠ 구 자산을 새 구조에 맞게 수리
  - ㉡ legacy 경로를 이름만 정리하고 남기기, 또는 주석과 문서화로 잠정 처리
  - ㉢ 아카이브 폴더에 보존
  - ㉣ `llr_tune` 탐색 절차를 되살리거나 TODO에 올리기
  - ㉤ plan.md를 계획 문서로 유지
  - ㉥ 코드 변경마다 README를 최신으로 유지하는 의무
- ㉰ 이유
  - C++ 대응 원문이 없는 경로는 유지 근거가 약하다. legacy를 지우면 F14의 경로 간 차이는 자연 소멸한다 (사용자 확정 2026-08-07)
  - git 이력이 복구 수단이라 아카이브 폴더가 필요 없다
  - 사문 모듈 주석에 있던 구 하드웨어 참고값은 보존하지 않는다 (사용자 확인 2026-08-09). 앞서 llr_profile 제거의 선행 조건으로 걸었던 문서 이관을 되돌린 것이다
  - 결정 기록은 README "확정 결정 기록" 절에 있으면 충분하다. 상세 경위는 `_pm/DONE.md`와 git이 담당한다
  - README는 지금 고칠 수 있는 사실 오류만 바로 수리한다. 이후 지식 정본은 `docs/profile/` 다섯 문서로 옮겨졌고 "코드가 바뀌면 프로파일을 먼저 고친다"가 현행 규칙이다
- ㉱ 결과로 생긴 규칙과 비용
  - 디코더는 syndrome-aided matrix 단일 경로. 동점 반전 `sum_t <= 0` 하나만 남았다
  - `mpi_runner`는 새 구조 기준으로 다시 설계한다 (TODO 잔류). 병렬 경로는 현재 없다
  - LLR 후보 여러 개를 같은 조건으로 견주는 절차는 저장소에 없다. 필요해지면 그때 구현한다
  - 삭제 전에 그 경로만 갖고 있던 참고값이 있으면 문서로 옮길지 먼저 묻는다
  - plan.md 참조 7곳을 정리했다. 이 사본의 `_pm/TODO.md:6`에는 옛 참조가 하나 남아 있다

## 하위 링크

- [../trials/20260806_rejected-unification-and-relaxation.md](../trials/20260806_rejected-unification-and-relaxation.md): legacy 경로가 있어서 생긴 genie 동점 통일 처방과 그 기각
- [20260808_rewrite-not-patch-positive-rules.md](20260808_rewrite-not-patch-positive-rules.md): 같은 날 확정된 문장 규칙과 이력물 보존
- [../../README.md](../../README.md): 확정 결정 기록 절 (plan.md에서 이관)
- [../../docs/profile/constraints.md](../../docs/profile/constraints.md): 변경 금지 대상과 이력물 보존 항목
