---
summary: 파일 없이 균일 간격 edge 레벨과 전 dv 공통 ch로 그룹 1개 LLR matrix를 합성해 저장하고 같은 로더로 읽으며, th 값 패턴으로 레벨을 되찾는 규칙
tags: [llr-matrix, uniform, edge-quantization, synthesis]
sources: [src/llr_matrix.py:51-57, src/llr_matrix.py:60-89, src/llr_matrix.py:92-120, src/llr_matrix.py:285-316, src/llr_matrix.py:318-344, src/llr_matrix.py:388-400, src/run.py:412-441, src/decoder.py:117, src/decoder.py:175-176, src/decoder.py:189-195, workspace/_template/config.json:31-45]
last_verified: 2026-09-30
---

## 하는 일

`use_input_llr_matrix: false`일 때 `LLRMatrix.make_internal_uniform_matrix`가 균일 배치 레벨과 전 dv(column degree) 공통 ch(채널 LLR 크기)로 매트릭스를 만들고 DAO(decoder auto optimizer) 포맷으로 저장한 뒤 `load`로 읽는다. 디코더는 파일 로드 경로 하나만 탄다. 레벨 판별은 파일명이 아니라 th 값 패턴이다.

## 동작 방식

- 1. 간격 1 레벨 `uniform_edge_mag(top) = [top, ..., 2, 1] + [1]` (`src/llr_matrix.py:51-57`). 최소 레벨 1 (C++가 C2V 크기 0을 내보내지 않는 방향). 마지막 두 항이 1인 이유는 레벨 수 = th 수 + 1 제약
- 2. 레벨 배치 `edge_quantization_levels(bits, max)` (`:60-89`): 레벨 수 = `2^(bits-1)` (`:80`). max는 `2^n-1` 꼴 (`:78-79`), `max >= 레벨 수 - 1` (`:81-84`). `step = (max+1) // 레벨 수` (`:85`). step 1이면 (`uniform_edge_mag(max)`, th [max..1]) (`:86-87`). 아니면 `edge_mag = range(max, 0, -step)`, `th = edge_mag[:-1]` (`:88-89`). th = 레벨값 (사용자 결정 2026-08-13)

| bits, max | edge_mag | th | 최소 레벨 |
|---|---|---|---|
| 3, 7 (기본) | {7,5,3,1} | {7,5,3} | 1 (C++ 3bit와 동일) |
| 3, 15 | {15,11,7,3} | {15,11,7} | step-1 = 3 |
| 4, 7 | {7,6,5,4,3,2,1,1} | {7,...,1} | 1 |

- 3. 합성 `make_internal_uniform_matrix(bits, max, channel_llr, max_iter, dv_max, mode)` (`:285-316`): ch는 스칼라면 region 수만큼 반복, 리스트면 길이 = region 수 (`:303-309`). values = ch + th (`:310`). row 1개 (csw -1, iter 1..max_iter, floor -1) (`:312`). dv 구간 [1, dv_max] 하나, 그룹 1개 ITER, restart 없음, max_value = max(max, ch 값) 반복, min_value 0 (`:314-316`)
- 4. 저장 `save(path)` (`:318-344`): 로더가 읽는 형식 그대로 탭 구분, 빈 줄 삽입, 전부 정수
- 5. `setup`이 합성 결과를 `output.dir/_generated/`에 저장한 뒤 같은 `LLRMatrix.load`로 읽는다 (`src/run.py:412-441`). 경로와 파일명 규칙은 [20260930_setup-llr-supply-paths.md](20260930_setup-llr-supply-paths.md)
- 6. 로드 시 역판별 `_detect_uniform_edge_mag` (`src/llr_matrix.py:92-120`): restart 0 (`:99`), 첫 row 첫 dv의 th가 공차 d(1 이상) 등차 감소 (th 1개면 홀수, `:102-110`), 마지막 항 = 2d-1 (`:111-112`), 전 row 전 dv의 th 동일 (`:113-119`) → `edge_mag = th + [max(d-1, 1)]` (`:120`). 아니면 None (3-bit 기본)
- 7. `has_uniform_levels` (`src/llr_matrix.py:388-400`): restart 없음, edge_mag == `uniform_edge_mag(th_len)`, 전 row th == [th_len..1]이면 True. 디코더가 생성자에서 한 번 읽어 (`src/decoder.py:117`) `_uniform_saturate` 등가식 `max(min(|raw|, top), 1)`을 쓴다 (`:175-176`, `:189-195`). step 2 이상 레벨(예 {15,11,7,3})은 False라 캐스케이드로 간다

## 쓰는 법

- ㉮ config: `use_input_llr_matrix: false`, `mode`, `max_iter`, `channel_llr_{mode}` (전 dv 공통, 강한 region부터, 길이 = region 수), `use_default_edge_quantization` (false면 `edge_quantization.edge_resolution_bits`와 `edge_max_value`). 설명 정본은 `workspace/_template/config.json:31-45`
- ㉯ 스케일: `edge_max_value`를 키우면 `channel_llr_*`도 같은 배율로 키운다 (`config.json:33-34`). 안 키우면 복호가 무너진다 (반전 조건 문서 참조)
- ㉰ 균일 모드는 dv별 ch 차등을 표현하지 못한다 (특성). dv 차등은 파일 경로로 한다
- ㉱ 검증: 합성 → save → load 왕복에서 필드와 디코딩 결과 동일 확인이 관례. 생성 파일은 `_generated/`에 남고 사용 사본은 실행 폴더에 저장된다 (`output.save_llr_matrix`)
- ㉲ 주의: 생성 파일을 개명해 `uniform`을 빼도 값 패턴으로 레벨을 되찾는다. 반대로 `uniform`이 든 이름인데 패턴이 아니면 에러다

## 관련 문서

- decisions [20260808_uniform-llr-file-then-load.md](../decisions/20260808_uniform-llr-file-then-load.md), [20260813_edge-quantization-bits-max-split.md](../decisions/20260813_edge-quantization-bits-max-split.md), [20260809_uniform-min-level-one.md](../decisions/20260809_uniform-min-level-one.md)
- assets [20260809_antipattern-filename-decides-semantics.md](../assets/20260809_antipattern-filename-decides-semantics.md), [20260808_zero-level-not-in-original.md](../assets/20260808_zero-level-not-in-original.md), [20260808_equivalence-verification-methods.md](../assets/20260808_equivalence-verification-methods.md)
- tech [20260930_llr-matrix-file-format-and-loader.md](20260930_llr-matrix-file-format-and-loader.md), [20260930_setup-llr-supply-paths.md](20260930_setup-llr-supply-paths.md), [20260930_vnu-quantize-cascade.md](20260930_vnu-quantize-cascade.md), [20260807_flip-condition-ch-le-7dv.md](20260807_flip-condition-ch-le-7dv.md)
- profile `../../docs/profile/techniques.md`
