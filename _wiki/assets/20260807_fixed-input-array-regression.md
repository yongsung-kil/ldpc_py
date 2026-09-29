---
summary: 리팩토링 전에 고정 seed 결과를 저장하고 뒤에 같은 조건으로 재실행해 배열 단위 완전 일치를 확인하는 회귀 방법. 실행 폴더 비교와 주입 검증의 통과 기준 포함
type: pattern
tags: [regression, fixed-seed, refactor]
date: 2026-08-07
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/done/20260807_가독성리팩토링/20260806_가독성리팩토링.md:88-94`, `_pm/done/20260810_workspace전환/20260810_workspace전환.md:44-51`, `_pm/done/20260809_2SD3SD구현/20260809_2SD3SD구현.md:42-44`, `docs/profile/constraints.md:116`, `docs/profile/overview.md:20`
- ㉮ 원리: 같은 seed와 같은 `frames_per_batch`면 채널 난수와 복호 경로가 결정적이라 결과 배열이 비트 단위로 같아야 한다. 로직 무변경의 증거는 "통계가 비슷하다"가 아니라 "배열이 같다"
- 절차 4단계
  - 1. 리팩토링 전에 고정 seed로 기준 결과를 저장한다. 예: 채널 2종(fixed_error, rber) 각 32프레임의 success 배열과 decode_success_iteration 배열, 또는 매트릭스 2개와 채널 2종에 16프레임씩의 decode 결과 배열
  - 2. 리팩토링 후 같은 seed, 같은 config로 재실행해 배열 단위 완전 일치를 확인한다
  - 3. 채널 3종(fixed_error, rber, strong_error) end-to-end 정상 동작을 확인한다
  - 4. `python -m py_compile`로 전 파일 통과를 확인한다
- ㉯ 실행 폴더 비교 (실행 구조를 바꿨을 때): 두 실행 폴더의 로그 CSV 전부와 `fer_{label}.csv`, summary.txt 결과 줄을 대조한다. 허용되는 차이는 경과시간 열뿐이다. 모드 확장(2SD/3SD 추가) 때는 HD 경로가 파일 로드와 균일 생성 둘 다 수정 전과 완전 일치해야 한다
- ㉰ 주입 검증은 반대다: 변형 디코더(예: 동점 비반전 재정의)를 `DECODER_CLASS`로 넣었을 때 BER이 기준선과 "달라져야" 통과다. 같으면 재정의가 반영되지 않은 것이다
- ㉱ 잘못된 패턴 3
  - ㉠ 회귀 기준을 저장하지 않고 리팩토링에 착수한다 (비교 대상이 사라진다)
  - ㉡ 경과시간 열까지 일치를 요구한다 (항상 실패한다)
  - ㉢ 배치 크기를 바꾼 채 수치를 비교한다 (배치 크기는 수치 재현 조건이라 정당한 차이가 난다)
- ㉲ 적용 이력: 가독성 리팩토링, 교체 지점 분리, 함수 추출, 이름 변경, 캐스케이드 일반화, 2SD/3SD 추가, workspace 전환 전부 이 방법으로 로직 무변경을 확인했다. 자동화된 테스트 파일은 저장소에 없다

## 사용 방법

- ㉮ 언제: 기존 경로를 건드리는 모든 변경 전. 새 기능 추가도 기존 경로를 지나면 먼저 기준 산출물을 남긴다
- ㉯ 어떻게: 프레임 수는 16~32면 충분하다. 채널 포인트는 성공과 실패가 섞이는 값을 고른다 (전부 성공이나 전부 실패면 차이가 보이지 않는다)
- ㉰ 주의: 결과 파일을 비교하려면 `python -m src.run <config>`로 실행 폴더를 만들고 CSV를 대조한다. 판정 규칙이 바뀐 커밋을 사이에 두면 일치하지 않는 것이 정상이다 (worktree 회귀 문서의 함정 참조)
- 관련 문서
  - [20260808_equivalence-verification-methods.md](20260808_equivalence-verification-methods.md)
  - [20260813_refactor-regression-by-worktree.md](20260813_refactor-regression-by-worktree.md)
  - [20260807_single-seed-derived-streams.md](../decisions/20260807_single-seed-derived-streams.md)
