---
summary: strong_error 채널은 에러 위치 E개를 먼저 뽑고 그중 round(E*SER)개를 strong으로 배정하는 2단계 추출이다. 원본의 균일 순열 슬라이스와 통계적으로 등가다
status: Accepted
tags: [channel, sampling, equivalence]
date: 2026-08-07
commit: 0394b81 (시험장 사본에 포함)
source: _pm/done/20260807_리뷰후속수정/20260807_리뷰후속수정.md:16, 41-49, src/channel.py:71-75, 91-135, docs/profile/constraints.md:43
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - 2026-08-06 딥 리뷰 F1: 옛 구현은 `_rand_positions`(argpartition) 결과를 앞부분 strong, 뒷부분 weak으로 구간 슬라이스했다
  - argpartition은 뽑힌 집합만 균일하고 내부 순서는 introselect 잔여라 균일하지 않다. 실측에서 strong 위치가 특정 column block에 극단 편향됐다 (카이제곱 약 244만, 자유도 146)
  - 원본 C++ `rand_sel_ep`는 부분 Fisher-Yates로 균일 순열을 만들고 앞부분을 [strong 에러 | weak 에러 | weak 정상]으로 잘라 쓴다
- ㉯ 거부한 대안
  - ㉠ 원본처럼 부분 Fisher-Yates 순열을 Python으로 재현한 뒤 슬라이스
  - ㉡ argpartition 결과를 그대로 슬라이스 (편향, 옛 구현)
  - ㉢ 공용 `_rand_positions` 안에 셔플을 넣기 (fixed_error의 비트 단위 재현성이 깨진다)
- ㉰ 이유 (사용자 제안 2026-08-07, 등가성 논증)
  - 균일 순열의 앞 k개는 "크기 k의 균일 부분집합"과 분포가 같다. 따라서 순서 무작위성 요구 자체가 사라지고 집합 균일성만 있으면 된다
  - 절차: ㉠ N개 중 에러 위치 E개를 argpartition으로 뽑는다 ㉡ 에러 E개를 행별 독립 셔플(`permuted(axis=1)`)한 뒤 앞 e2 = round(E*SER)개를 strong, 나머지를 weak으로 ㉢ 정정 비트는 에러 위치를 막은 같은 난수의 여집합에서 하위 c1개를 weak으로
  - 비용은 프레임당 E개 셔플과 채널 생성 1회분 이내. 디코딩 대비 미미하다
- ㉱ 결과로 생긴 규칙과 비용
  - `_rand_positions`는 집합 전체를 같은 방식으로 쓰는 경우 전용이다. 구간 슬라이스로 나눠 쓰지 않는다 (`src/channel.py:71-75` docstring)
  - fixed_error 경로는 무수정이라 기존 결과의 비트 단위 재현성이 유지된다
  - `permutation`과 `shuffle`은 전 행에 같은 순열을 적용하므로 `permuted`를 대체하지 못한다
  - 재사용 틀: 샘플링을 다시 설계할 때는 원본 절차의 분포를 정의하고 새 절차가 같은 분포를 만드는지 보인다. 검증 도구는 블록 카이제곱 분포 검정

## 하위 링크

- [../assets/20260806_set-uniform-vs-order-uniform.md](../assets/20260806_set-uniform-vs-order-uniform.md): 집합 균일과 순서 균일이 다르다는 antipattern
- [../tech/20260930_channel-models.md](../tech/20260930_channel-models.md): 채널 3종의 산식과 strong_error 구현 위치
- [20260807_single-seed-derived-streams.md](20260807_single-seed-derived-streams.md): 난수 스트림 파생과 재현 조건
