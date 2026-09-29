---
summary: edge 메시지 양자화를 bit 수(`edge_resolution_bits`)와 최대값(`edge_max_value`) 두 축으로 나누고, 기본은 C++ 3-bit 레벨 {7,5,3,1}, th는 레벨값과 같으며, 최대값을 키우면 채널 LLR도 같은 배율로 키운다
status: Accepted
tags: [quantization, config, edge]
date: 2026-08-13
commit: 0394b81 (시험장 사본에 포함)
source: README.md:224; _pm/DONE.md:37-77; src/llr_matrix.py:60-89; workspace/_template/config.json
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 기존 `num_bits` 하나는 레벨 수와 최대값 `2^(n-1)-1`이 묶여 있어 C++ 3-bit의 "최대 7을 4레벨로 벌린" 배치 {7,5,3,1}을 표현하지 못했다
  - ㉡ 채널 LLR 대비 edge 메시지의 무게(최대값)와 해상도(레벨 수)는 별개의 실험 축이다
- ㉯ 거부한 대안
  - ㉠ `num_bits` 하나로 묶어 두기
  - ㉡ th를 별도 튜닝값으로 받기
- ㉰ 이유
  - ㉠ C++는 th가 LLR matrix의 튜닝 데이터라 고정 배치 규칙이 없다. 간격 1에서 th = `[top..1]`이던 저장소 균일 경로의 자연 확장으로 th = 레벨값을 사용자가 결정했다 (`src/llr_matrix.py:65-68`)
- ㉱ 결과로 생긴 규칙
  - ㉠ 레벨 수 = `2^(bits-1)`, 간격 step = `(max+1) / 레벨 수`, max부터 내림차순. 예: (3, 7) → {7,5,3,1}, (3, 15) → {15,11,7,3} (`src/llr_matrix.py:60-89`)
  - ㉡ `edge_max_value`는 `2^n-1` 꼴이어야 하고 `레벨 수 - 1` 미만이면 에러
  - ㉢ 간격 1이면 `uniform_edge_mag`와 같은 `[top..1, 1]`, 간격 2 이상이면 최소 레벨은 `step-1`
  - ㉣ `use_default_edge_quantization`(기본 true)이면 bits 3, max 7. false면 `edge_quantization` 블록을 읽는다. `num_bits`와 `internal_quantize` 키는 폐기
  - ㉤ `edge_max_value`를 키우면 `channel_llr_*`도 같은 배율로 키운다. 안 키우면 복호가 무너지는 스케일 효과를 실측했다
  - ㉥ 로더의 균일 판별을 `[n..1]` 패턴에서 등차 감소 패턴으로 일반화해 벌린 레벨 파일도 왕복 복원한다. 생성 파일명에 `max{값}` 표기 추가
- ㉲ 비용
  - ㉠ 간격 2 이상 레벨은 `has_uniform_levels`가 False라 O(1) 등가식 대신 캐스케이드로 간다
  - ㉡ 3-bit 파일과 균일 경로가 아닌 넓은 레벨의 SD 시딩은 3-bit 상수로 떨어지며 의도인지 미확인이다

## 하위 링크

- [../tech/20260930_uniform-llr-matrix-synthesis](../tech/20260930_uniform-llr-matrix-synthesis.md): 레벨 생성식과 저장 왕복의 현행 코드
- [../tech/20260807_flip-condition-ch-le-7dv](../tech/20260807_flip-condition-ch-le-7dv.md): 최대값과 채널 LLR 배율이 반전 가능 조건에 미치는 영향
- [20260809_uniform-min-level-one](20260809_uniform-min-level-one.md): 간격 1 배치의 최소 레벨 결정
- [20260813_config-slots-and-flags](20260813_config-slots-and-flags.md): 같은 날 확정된 config 구조 (플래그가 양자화 블록을 고른다)
