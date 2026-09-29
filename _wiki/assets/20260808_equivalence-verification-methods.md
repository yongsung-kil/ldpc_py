---
summary: 등가 구현을 검증할 때 고르는 방법 9종 (스칼라 전수 대조, 비트 단위 회귀, 바이트 대조, 저장 로드 왕복, 분포 검정, 저장소 무수정 실증, 자동 검증 묶음, AST 대조, 무효과 조건 일치)
type: pattern
tags: [verification, equivalence, regression]
date: 2026-08-08
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/done/20260806_review/r4_round2_lv1_fix_review/report.md:13-17, 40`, `_pm/tasks/20260808_review/r2_round2_lv2_analysis/report.md:37-43`, `_pm/TODO.md:20-21`, `_pm/DONE.md:31`, `docs/profile/constraints.md:118`
- 방법 9종 (무엇을 증명하는지와 실제 쓰인 사례)
  - 1. 스칼라 레퍼런스 전수 대조: 원본 C++ 산술을 스칼라 함수로 옮겨 적고 벡터 구현과 전 입력 조합을 대조한다. 벡터화가 산술을 바꾸지 않았음을 증명한다. VNU 양자화 캐스케이드에서 조합 약 1,000건과 무작위 20만 건 불일치 0
  - 2. 고정 seed 비트 단위 회귀: 수정 전후 채널 출력 배열과 난수 생성기 잔여 상태까지 같은지 본다. "통계 단위 동일"과 "비트 단위 동일"을 구분해 적는다
  - 3. 산출물 바이트 대조: 리팩토링 전후 실행 폴더 산출물을 바이트로 비교한다. 로그 항목 조합 16가지 전수. 출력 경로 변경에 쓴다
  - 4. 저장/로드 왕복: 균일 매트릭스를 합성하고 `save()` 뒤 `load()`해 헤더와 row 필드(12조합에 19필드씩)가 같은지, 왕복 전후 디코딩 결과 배열이 같은지, 커밋 파일과 재생성본이 바이트와 md5로 같은지 본다. 로더, 세이버, 판별 규칙(균일 패턴)을 바꿀 때마다
  - 5. 분포 검정: 위치 선택 함수에 블록 카이제곱 검정과 원문 전사 대량 시행(60만 회) 순열 균일성 검정. 샘플링 재설계에 쓴다
  - 6. 저장소 무수정 실증: 검증용 동작 변형은 서브클래스 재정의나 monkey-patch로, 산출물은 scratchpad에, 끝날 때 `git status`를 기준선과 대조한다. 리뷰 검증이 코드를 오염하지 않았음을 보인다
  - 7. 자동 검증 묶음: 설정 검증, sim 가드, strong_error 통계, 캐스케이드 등가, `_validate`, 디코더 경로, 회귀로 나눈 51건. 다만 이 테스트 파일은 이 사본에 없다 (`docs/profile/constraints.md:118`). 구성만 재사용한다
  - 8. AST 대조: 주석, docstring, 문자열만 고치는 대량 수정(줄표 일괄 수리 22파일 149건)은 수정 전후 파이썬 AST(abstract syntax tree, 추상 구문 트리)를 비교해 로직 무변경을 확인한다. 예외 문구 같은 문자열 리터럴 변경은 따로 본다. 기계 치환 후유증(부분문자열 오염)은 AST가 잡지 못하므로 grep 검사를 병행한다
  - 9. 무효과 조건 일치: 변형 디코더를 무효과 파라미터(예: 클리핑 상한을 레벨 최대와 같게)로 돌려 기준선과 수치 완전 일치를 확인한다. 이것이 재정의 구현의 동등성 증거다

## 사용 방법

- ㉮ 고르는 기준
  - ㉠ 산술 함수 하나를 바꿨다: 1
  - ㉡ 난수 소비 경로를 바꿨다: 2와 5
  - ㉢ 출력 구조나 실행 경로를 바꿨다: 3
  - ㉣ 파일 포맷 로더나 세이버를 바꿨다: 4
  - ㉤ 텍스트만 바꿨다: 8
  - ㉥ 교체 지점 재정의를 새로 만들었다: 9, 그다음 유효 재정의로 수치가 달라지는지
- ㉯ 실측 수치를 적을 때는 채널 포인트, 프레임 수, max_iter를 병기한다
- ㉰ 주의: 방법 7의 테스트 파일이 없으므로 "자동 검증 통과"를 현재 상태의 근거로 인용하지 않는다. 필요하면 구성을 따라 새로 만든다
- 관련 문서
  - [20260807_fixed-input-array-regression.md](20260807_fixed-input-array-regression.md)
  - [20260813_refactor-regression-by-worktree.md](20260813_refactor-regression-by-worktree.md)
  - [20260813_paper-idea-single-override-procedure.md](20260813_paper-idea-single-override-procedure.md)
  - [20260808_rewrite-not-patch-positive-rules.md](../decisions/20260808_rewrite-not-patch-positive-rules.md)
