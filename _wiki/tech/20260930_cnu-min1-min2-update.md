---
summary: CN 상태 (min1, min2, min1_pos, check_sum, edge_sgn)의 remove old, insert new 갱신 규칙과 C2V 메시지 재구성
tags: [decoder, cnu, min-sum]
sources: [src/decoder.py:150-157, src/decoder.py:197-220, src/decoder.py:271-275, src/decoder.py:294-314, src/decoder.py:342-349, docs/차이.md:37, docs/차이.md:43-44]
last_verified: 2026-09-30
---

## 하는 일

CN (check node, 검사 노드)마다 들어온 메시지 전부를 저장하지 않고 최솟값 둘 (min1, min2)과 min1의 위치, 부호 합, edge별 부호만 둔다. 새 메시지가 오면 옛 기여를 빼고 (remove old) 새 값을 넣는다 (insert new). C2V (check to variable, 검사 노드에서 변수 노드로) 메시지는 이 상태에서 읽는 시점에 재구성한다.

## 동작 방식

- ㉮ CN 상태 5필드 (`src/decoder.py:271-275`)

| 배열 | 축 | dtype | 초기값과 뜻 |
|---|---|---|---|
| min1, min2 | (B, M_b, z) | float32 | RESET = edge_mag[0]. 첫째, 둘째 최솟값 (EDGE 도메인) |
| min1_pos | (B, M_b, z) | int32 | -1. min1을 낸 edge 인덱스 |
| check_sum | (B, M_b, z) | uint8 | 0. 들어온 부호의 XOR 누적 |
| edge_sgn | (B, E, z) | uint8 | 0. edge별 마지막 부호 |

- ㉯ `_c2v_reconstruct` (`:150-157`): `check_out = min2 if min1_pos == edge else min1` (`:155`), `sign = syndrome ^ check_sum ^ edge_sgn` (`:156`), 반환은 ±check_out (CN 정렬, roll 전, `:157`)
- ㉰ `_cnu_update(edge, edge_clear, new_sgn, new_mag, row_blk, min1, min2, min1_pos, check_sum, edge_sgn)` (`:197-220`)
  - ㉠ `RESET = edge_mag[0]` (`:204`). row_blk 슬라이스에서 cur_min1, cur_min2, cur_pos를 읽는다 (`:205-207`)
  - ㉡ remove old (edge_clear가 아닐 때만, `:208-212`): `check_sum ^= edge_sgn[edge]`, 자신이 min1이었으면 min1 ← min2, min2 ← RESET
  - ㉢ insert new (`:213-220`): `is_new_min1 = new_mag <= cur_min1`, `is_new_min2 = new_mag <= cur_min2`. min2 = RESET (새 min1이면) 또는 new_mag (새 min2면) 또는 cur_min2. min1과 min1_pos 갱신, `check_sum ^= new_sgn`, `edge_sgn[edge] = new_sgn`
- ㉱ HW 특성 재현 (`:200-202`, `docs/차이.md:37`): 새 min1이 들어오면 기존 min1을 min2로 내리지 않고 RESET으로 둔다. 비교는 `<=`
- ㉲ 제자리 갱신: 받은 배열을 직접 고치고 반환값은 쓰이지 않는다 (`src/decoder.py:202-203`)
- ㉳ edge_clear=True인 호출 두 곳: restart 클리어 직후 iteration은 edge_clear 플래그가 `src/decoder.py:342-349`에서 정해지고 그 값으로 `src/decoder.py:412`에서 부른다. SD Pre 단계 호출은 `src/decoder.py:310`. 두 곳 다 옛 기여가 없으니 remove old를 건너뛴다
- ㉴ 등가 확인 (`docs/차이.md:43-44`): C++는 V 코드 {3,2,1,0}으로 저장 후 EDGE 값으로 변환하고 py는 EDGE 값을 직접 저장한다 (단조 일대일). min1_pos 초기값 -1은 클리어 직후 min1 = min2 = RESET이라 결과에 영향이 없다

## 쓰는 법

- ㉮ normalized min-sum이나 offset min-sum은 `_c2v_reconstruct`를 재정의해 읽는 시점에 건다. 저장 상태 (min1, min2)를 변형하면 증분 갱신이 누적 오차를 만든다
- ㉯ `_cnu_update`를 재정의할 때도 받은 배열을 제자리에서 고친다. `new_sgn`은 uint8이라는 dtype 계약을 지킨다 (`src/decoder.py:410`)
- ㉰ column 중복 방문은 remove old를 두 번 태워 min1을 잃는다. `_column_order` 재정의 시 각 column은 한 iteration에 한 번만
- ㉱ 디버그: `min1_pos == -1`인 CN은 클리어 뒤 아직 메시지를 받지 않은 것이다

## 관련 문서

- ㉮ [20260930_replacement-points-six.md](20260930_replacement-points-six.md): 교체 지점 시그니처와 경계
- ㉯ [20260930_syndrome-aided-column-step.md](20260930_syndrome-aided-column-step.md): 호출 위치와 roll 규약
- ㉰ [20260930_table-row-select-and-restart.md](20260930_table-row-select-and-restart.md): Edge Clear
- ㉱ [../assets/20260813_clip-at-reconstruct-not-stored-state.md](../assets/20260813_clip-at-reconstruct-not-stored-state.md): 읽기 시점 변형 패턴
- ㉲ [../assets/20260808_replacement-point-contract-protection.md](../assets/20260808_replacement-point-contract-protection.md): dtype 계약
- ㉳ [../../docs/차이.md](../../docs/차이.md)
