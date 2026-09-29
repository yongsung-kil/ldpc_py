---
summary: refactor 직전 커밋을 git worktree로 꺼내 같은 조건으로 실행하고 HEAD와 수치 완전 일치를 확인하는 회귀 절차. 기준 커밋 선택 함정 포함
type: pattern
tags: [regression, worktree, refactor, baseline]
date: 2026-08-13
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/done/20260813_minsum_dual_clip/20260813_minsum_dual_clip.md:34-41`, `docs/profile/constraints.md:116`
- ㉮ 목적: refactor가 여러 커밋에 걸쳐 있을 때 "베이스가 그동안 바뀌지 않았다"를 실행으로 보장한다. 논문 아이디어 실험은 이 확인 뒤에 시작한다
- 절차
  - 1. 기준 커밋을 고른다. refactor 묶음의 바로 앞 커밋이다 (2026-08-13 사례: refactor 4건 직전 커밋 하나)
  - 2. `git worktree add <폴더> <기준 커밋>`으로 별도 폴더에 꺼낸다. 현재 작업 트리는 건드리지 않는다
  - 3. 두 트리에서 기준 실험(`workspace/base_run/`)을 같은 config, 같은 seed, 같은 `frames_per_batch`로 돌린다
  - 4. 채널 포인트마다 FER, BER, avg_decoding_iteration을 대조한다. 통과 기준은 완전 일치다 (사례: fixed_error 두 포인트 전부 일치)
  - 5. summary.txt의 `code commit` 줄로 어느 실행이 어느 커밋인지 기록한다
  - 6. `git worktree remove <폴더>`로 정리한다
- ㉯ 기준 커밋 선택 함정
  - ㉠ 너무 오래된 실행과 비교하면 의도된 변경이 결함처럼 보인다. 2026-08-10 실행(FER 1.0)과 달랐던 원인은 성공 판정을 information 구간만 검사하도록 바꾼 커밋과 post-FEC BER 기준을 바꾼 커밋이었다
  - ㉡ 비교 전에 두 커밋 사이의 판정 규칙 변경을 `git log`로 확인한다. 판정 규칙이 바뀌었으면 그 커밋 뒤를 기준으로 잡는다
  - ㉢ 수치가 다르면 "결함"으로 단정하기 전에 커밋 이력으로 차이를 설명할 수 있어야 한다

## 사용 방법

- ㉮ 언제: 논문 아이디어 실험 직전, 여러 커밋에 걸친 refactor 뒤. 단일 커밋 refactor는 고정 입력 회귀로 충분하다
- ㉯ 어떻게: 위 절차 1~6. 결과 기록에는 채널 포인트, 프레임 수, max_iter를 병기한다
- ㉰ 주의: 이 사본에서는 실험 폴더의 `python run.py`가 동작하지 않으므로 각 트리의 루트에서 `python -m src.run <config>`로 돌린다
- 관련 문서
  - [20260807_fixed-input-array-regression.md](20260807_fixed-input-array-regression.md)
  - [20260808_equivalence-verification-methods.md](20260808_equivalence-verification-methods.md)
  - [20260813_minsum-dual-clip-trial.md](../trials/20260813_minsum-dual-clip-trial.md)
