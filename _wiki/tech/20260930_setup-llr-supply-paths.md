---
summary: setup이 H-matrix를 읽은 뒤 LLR matrix를 파일 로드 또는 균일 합성 후 저장 후 로드로 공급하는 두 경로, 생성 파일명, 단일 로더
tags: [setup, llr-matrix, uniform]
sources: [src/run.py:20-45, src/run.py:322-339, src/run.py:393-446, src/run.py:469-470, src/run.py:764-768, src/llr_matrix.py:230, src/llr_matrix.py:286]
last_verified: 2026-09-30
---

## 하는 일

- ㉮ `setup(config, decoder_class)`가 H-matrix를 로드하고, LLR matrix를 준비하고, 디코더를 만든다 (`src/run.py:393-446`)
- ㉯ LLR matrix 공급은 두 경로지만 읽는 곳은 `LLRMatrix.load` 한 곳이다. 균일 합성도 파일로 저장한 뒤 같은 로더로 읽는다

## 동작 방식

- ㉮ H-matrix: 파일이 없으면 `FileNotFoundError`. 이 함수는 생성하지 않는다 (`src/run.py:403-404`). `QCCode.load` (`:405`)
- ㉯ 경로 1, 파일 로드 (`use_input_llr_matrix` true, `:406-411`): 지정 파일의 존재만 확인한다. 모드는 파일명이, max_iter는 파일의 마지막 iter_end가 정한다. config의 `mode`, `max_iter`는 읽지 않는다 (`:31-34`)
- ㉰ 경로 2, 균일 합성 (`use_input_llr_matrix` false, `:412-440`)
  - ㉠ 입력: `mode`, `max_iter`, `channel_llr_{mode}`, `dv_max = code.col_deg.max()`, 레벨은 기본 (bits 3, max 7) 또는 `edge_quantization` 두 값 (`:413-422`)
  - ㉡ `LLRMatrix.make_internal_uniform_matrix(...)`로 합성 (`:423-429`, `src/llr_matrix.py:286`)
  - ㉢ `output.dir/_generated/` 아래에 저장 (`src/run.py:430-439`). 파일명 `LLR_MATRIX_{mode}_uniform_{bits}bit_max{max}_ch{값-값}_dv{dv_max}_iter{max_iter}.txt`. 파일명의 uniform은 사람이 만든 파일이 아니라는 표시이고 레벨 인식은 th 값 패턴으로 한다 (`src/run.py:24-27`)
  - ㉣ 파일명에 dv_max가 들어가므로 H 로드 뒤에야 확정된다 (`:338-339`)
- ㉱ 공통: `LLRMatrix.load(path)` (`:441`, `src/llr_matrix.py:230`). 실제 파일 경로를 `config["decoder"]["_used_llr_matrix_path"]`에 남겨 `report`가 실행 폴더에 사본을 저장한다 (`:442`, `:764-768`)
- ㉲ 디코더 생성: `decoder_class(code, llr_matrix=llr_matrix)`. None이면 `BaseDecoder` (`:443-445`)

## 쓰는 법

- ㉮ 실물 LLR 파일: `use_input_llr_matrix: true`, `llr_matrix: {"dir", "file"}`. 파일명에 `LLR_MATRIX_HD_`처럼 모드가 들어 있어야 한다
- ㉯ 균일 매트릭스로 빠른 점검: `use_input_llr_matrix: false`, `mode`, `max_iter`, `channel_llr_{mode}`를 채운다. edge 레벨을 바꾸려면 `use_default_edge_quantization: false`와 `edge_quantization` 두 값
- ㉰ `channel_llr_*`와 `edge_max_value`는 같은 배율로 키운다 (`workspace/_template/config.json:33-34`)
- ㉱ 어느 경로였는지는 summary.txt의 `LLR matrix` 줄로 확인한다. "파일 로드" 또는 "균일 생성 후 로드"와 실제 파일명이 찍힌다 (`src/run.py:469-472`)
- ㉲ 자식 디코더의 생성자는 `(code, llr_matrix=)` 꼴을 유지한다

## 관련 문서

- ㉮ [LLR_MATRIX 파일 형식과 로더](20260930_llr-matrix-file-format-and-loader.md)
- ㉯ [균일 LLR matrix 합성과 저장 왕복](20260930_uniform-llr-matrix-synthesis.md)
- ㉰ [결정: 균일 LLR은 파일 생성 후 로드](../decisions/20260808_uniform-llr-file-then-load.md)
- ㉱ [결정: edge 양자화를 bit 수와 최대값으로 분리](../decisions/20260813_edge-quantization-bits-max-split.md)
- ㉲ [run.py main 흐름](20260930_run-main-flow.md)
