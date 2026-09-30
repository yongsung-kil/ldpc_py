---
summary: QCCode의 H 파일 형식(Ref-C), edge 배열 구성(column 우선), QC 연결의 roll 규약, syndrome 계산
tags: [pcm, qc-ldpc, h-matrix]
sources: [src/pcm.py:1-19, src/pcm.py:24-46, src/pcm.py:49-82, src/pcm.py:85-92, src/pcm.py:94-118, src/decoder.py:396, src/decoder.py:409]
last_verified: 2026-09-30
---

## 하는 일

- ㉮ `QCCode`가 QC-LDPC 부호를 base matrix (M_b, N_b)와 lifting 크기 z로 표현한다. base 값 -1은 zero block, 그 외는 circulant shift s (0 <= s < z) (`src/pcm.py:3`)
- ㉯ 파일은 Ref-C(원본 C++ `Load_PCM`) 포맷 하나만 읽고 쓴다 (`:7-8`)

## 동작 방식

- ㉮ 파일 형식 (`src/pcm.py:7-18`)
  - ㉠ 줄 순서: `N_b M_b` / `J K` (최대 column degree, 최대 row degree) / `z` / 빈 줄 / M_b행 x N_b열 shift 행렬
  - ㉡ 주석 없음. 행렬 M_b `*` N_b개 값 뒤는 무시한다 (행렬이 2벌 들어 있어도 첫 벌만)
  - ㉢ 구 포맷('#' 주석과 'M_b N_b z' 헤더) 지원은 제거됐다 (2026-08-06)
- ㉯ `load` (`:58-82`): 첫 줄이 정수 2개가 아니면 에러 (`:67-69`). 값 개수가 M_b `*` N_b 미만이면 에러 (`:74-75`). 앞 M_b `*` N_b개만 사용 (`:76`). 헤더 J, K보다 실제 degree가 크면 에러 (`:78-81`). `save` (`:49-55`)는 같은 형식으로 쓴다
- ㉰ 생성자 (`:24-46`)
  - ㉠ shift >= z면 에러 (`:28-29`). N = N_b `*` z, M = M_b `*` z, K = N - M, rate = K / N (`:33-36`)
  - ㉡ edge는 `np.lexsort((rows, cols))`로 column 우선 정렬 (`:38-39`). `edge_row`, `edge_col`, `edge_shift`는 (E,) (`:40-42`)
  - ㉢ `col_edges[j]`는 column block j의 edge 인덱스 (`:44`). `row_deg`, `col_deg` (`:45-46`)
- ㉱ roll 규약 (`:4-5`): edge (i, j, s)에서 CN block i의 lane k는 VN block j의 lane (k + s) mod z와 연결. VN 정렬 v를 CN 정렬로 `np.roll(v, -s)`, CN 정렬 c를 VN 정렬로 `np.roll(c, +s)`. 디코더가 같은 규약을 쓴다 (`src/decoder.py:396`, `:409`)
- ㉲ `syndrome(bits)` (`:85-92`): edge마다 `syn[i] ^= roll(bits[j], -s)`. 입력 (..., N_b, z), 반환 (..., M_b, z)
- ㉳ 전제: column block은 DV 내림차순 배치 (`:18`). 코드 검사는 없다. genie 판정의 정보 구간이 앞쪽 N_b - M_b 블록이라 어긋나면 잘못된 구간을 본다

## 쓰는 법

- ㉮ H 파일은 `Input/H_matrix/`에 두고 config `H_matrix: {"dir", "file"}`로 가리킨다. 로드 결과는 실행 요약의 `code`, `col degree`, `row degree` 줄로 확인한다
- ㉯ 새 H-matrix를 만들 때 column block을 DV 내림차순으로 재배열한 뒤 저장한다
- ㉰ LLR matrix의 dv 구간이 H의 모든 column degree를 덮어야 한다. 못 덮으면 에러 (기준은 H-matrix)
- ㉱ `count_cycles4()` (`:94-110`)로 길이 4 사이클 수를, `summary()` (`:112-118`)로 치수 요약을 본다

## 관련 문서

- ㉮ [genie 판정과 배치 압축](20260930_genie-check-and-batch-compress.md)
- ㉯ [syndrome-aided column 처리](20260930_syndrome-aided-column-step.md)
- ㉰ [LLR_MATRIX 파일 형식과 로더](20260930_llr-matrix-file-format-and-loader.md)
- ㉱ [결정: genie 판정과 all-zero codeword](../decisions/20260730_genie-check-and-all-zero-codeword.md)
- ㉲ 프로파일 [constraints](../../docs/profile/constraints.md)
