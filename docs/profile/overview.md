---
title: 프로젝트 개요
tags: [profile, overview]
---
# 프로젝트 개요

> onboard 스킬이 채웠다 (최초 2026-09-30). 코드가 바뀌면 이 문서를 먼저 고친다. 경로는 저장소 루트 기준이고 `파일:줄`은 그 파일의 줄 번호다.

## 1. 한 문장 정체성

QC-LDPC(quasi-cyclic low-density parity-check, 순환 시프트 블록 구조의 저밀도 패리티 검사 부호) 복호 기법을 on/off 상대 비교하기 위한 Python 프레임 배치 시뮬레이터. 원본 C++ 시뮬레이터의 syndrome-aided quantized min-sum 디코더를 재현하고, 디코더 변형은 본체를 고치지 않고 교체 지점 함수만 재정의해 붙인다.

## 2. 문제 정의

| 항목 | 값 | 근거 (파일:줄) |
|---|---|---|
| 입력 | ㉮ H-matrix 파일 (Ref-C 헤더 형식: `N_b M_b` / `J K` / `z` / 빈 줄 / M_b×N_b shift 행렬). 기준 치수 M_b=18, N_b=147, z=256, N=37,632 bit, K=33,024 bit. 저장소의 두 번째 예시 `matrix_sel_1.txt`는 M_b=15, N_b=145, N=37,120, K=33,280<br>㉯ LLR 테이블 파일 (DAO LLR_MATRIX 텍스트 형식, 모드 HD/2SD/3SD는 파일명으로 판별, 마지막 row의 iter_end가 max_iter)<br>㉰ 실험 설정 JSON (H-matrix와 LLR 경로, 채널 종류와 포인트, 프레임 수, 로그 항목, 출력 폴더) | `src/pcm.py:7-18`, `README.md:222`, `workspace/matrix_sel_1_HD/_probe/260818_225547_probe/summary.txt:6`, `src/llr_matrix.py:11-19, 162`, `src/run.py:17-80` |
| 출력 | 실행 폴더 `output.dir/YYMMDD_HHMMSS_{label}/`에 ㉮ config 사본 ㉯ summary.txt (커밋 해시, 실험 요약, 포인트별 결과 줄) ㉰ `{csv_prefix}_{label}.csv` (param, fer, post_fec_ber, frames, errors, avg_decoding_iteration, sec) ㉱ 로그 CSV 3종 (iteration별 CSW와 bit 에러, 수렴 히스토그램, 실패 프레임 상세) ㉲ 사용한 LLR 파일 사본 ㉳ fer_curves.png | `src/run.py:715-733`, `src/run.py:736-777`, `src/sim.py:170-182` |
| 성능 지표 | ㉮ FER(frame error rate, 프레임 에러율) = 실패 프레임 / 전체 프레임<br>㉯ post_fec_ber (복호 후 정보 비트 에러율) = 정보 구간 잔여 에러 bit 합 / (frames × K)<br>㉰ avg_decoding_iteration = (성공 프레임 수렴 iteration 합 + 실패 프레임 수 × max_iter) / frames<br>㉱ 보조: iter_hist (iteration별 성공 수), fer_vs_iter ("max_iter를 k로 줄였다면"의 FER) | `src/sim.py:139-149`, `src/run.py:656-677` |
| 평가 방법 | 기준 실험(`workspace/base_run/`, 재정의 없는 BaseDecoder)과 변형 디코더 실험을 같은 config와 seed로 돌려 FER 커브를 비교한다. C++와의 절대 FER 일치는 보장하지 않으며 상대 비교 전용이다. 같은 seed로 수치를 재현하려면 `frames_per_batch`까지 같아야 한다 | `README.md:4, 215`, `workspace/base_run/README.md:5-9`, `README.md:120-121` |

## 3. 실행 환경

| 항목 | 값 | 근거 (파일:줄) |
|---|---|---|
| 언어 | Python (14파일, `src/` 8모듈 약 2,200줄). 서드파티는 numpy(필수)와 matplotlib(그림 저장에만) | `requirements.txt:1-2`, `src/run.py:694-696` |
| 빌드 | 없음. `pip install -r requirements.txt`만 | `README.md:19-23` |
| 실행 | 저장소 루트에서 `python -m src.run <config.json 경로>` (디코더는 BaseDecoder 고정). 원래 배치에서는 실험 폴더에서 `python run.py [config...]`이지만, 이 사본은 폴더 이름이 `ldpc_py`라 런처가 찾는 `2_LDPC_base/src`가 없어 `SystemExit`로 끝난다 (2026-09-30 실행 확인) | `src/run.py:780-791`, `workspace/base_run/run.py:11-17` |
| 시뮬레이터 또는 합성 도구 | 해당 없음 (소프트웨어 시뮬레이터 자체) | |
| 테스트 | 없음 (`tests/` 폴더와 pytest 설정 없음). 관습은 ㉮ `workspace/test/`로 파이프라인 동작 확인 ㉯ 같은 seed 수치 완전 일치 회귀 비교 | `workspace/test/README.md:7-8`, `docs/차이.md:23`, `_pm/TODO.md:21` |

확인한 동작 환경 (2026-09-30): Python 3.11.7, numpy 1.26.4, matplotlib 3.10.7. 최소 버전 문구는 코드에 없고, API 사용처로 Python 3.7 이상, numpy 1.20 이상으로 추정한다 (`src/run.py:608-615`의 `subprocess.run(capture_output=, text=)`, `src/channel.py:125`의 `Generator.permuted`).

## 4. 폴더 지도

| 폴더 | 역할 |
|---|---|
| `src/` | 본체 코드 8모듈: `pcm`(부호와 H 파일), `encoder`(all-zero 임시), `channel`(채널 3종), `llr_matrix`(LLR 테이블 로더와 합성), `decoder`(BaseDecoder), `sim`(포인트 측정 루프), `run`(설정 검증, 구성, 실험 루프, 출력, CLI), `__init__`(공개 API) |
| `workspace/` | 실험 폴더. `_template/`(새 실험 복사 원본), `base_run/`(기준선), `test/`(파이프라인 점검), `matrix_sel_1_HD/`와 `matrix_sel_1_HD_fixed/`(특정 H-matrix 실험). 각 폴더에 `run.py`, `config.json`, README |
| `Input/H_matrix/` | H-matrix 파일 (`example_18x147_z256.qc`, `matrix_sel_1.txt`). 저장소의 파일은 예시이고 평가 대상은 외부에서 넣는다 |
| `Input/LLR/` | DAO LLR_MATRIX 파일 (HD_0, HD_1, 2SD_toy0, 3SD_toy0, HD_matrix_sel_1) |
| `docs/` | `차이.md`(C++ 원본 대비 로직 차이), `profile/`(이 프로파일), `adr/`(설계 결정), `explore/`(탐색 결과) |
| `_pm/` | 작업 관리 (TODO, DONE, tasks, done) |
| 루트 | `README.md`(설정 스키마, 채널 모델, 확정 결정 기록의 정본), `requirements.txt`, `__init__.py` |

## 5. 이 프로젝트에서 "교체 지점"이란

`src/decoder.py`의 `BaseDecoder`를 상속한 자식 클래스에서 메서드 하나를 재정의하는 것이 교체 단위다. 본체가 원본 C++ 함수 경계를 따라 6개 메서드를 따로 떼어 두었고(`_is_edge_clear_iter`, `_column_order`, `_c2v_reconstruct`, `_vn_decide`, `_vnu_quantize`, `_cnu_update`), 실험 폴더 `run.py`의 `DECODER_CLASS` 한 곳이 자식 클래스를 주입한다 (`src/decoder.py:40-46, 136-220`, `workspace/_template/run.py:24-28`). 상세는 [replacement_points.md](replacement_points.md).
