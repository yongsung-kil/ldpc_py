---
summary: 실행 폴더 구조와 거기 남는 파일(summary.txt, CSV 4종, LLR 사본, PNG)의 열 정의, 로그 항목의 C++ 대응과 용도
tags: [output, logging, csv]
sources: [src/run.py:64-77, src/run.py:113-114, src/run.py:603-618, src/run.py:621-712, src/run.py:715-733, src/run.py:736-777, src/sim.py:170-182]
last_verified: 2026-09-30
---

## 무엇을 하는가

- ㉮ 실행마다 `{output.dir}/{YYMMDD_HHMMSS}_{label}/` 폴더 하나에 config 사본, summary.txt, FER CSV, 켠 로그 CSV, LLR 사본, 그림을 남긴다 (`src/run.py:71-77`)
- ㉯ `create_run_dir`가 측정 전에 폴더와 summary 머리를 만들고, `run_experiment`가 측정 중 summary 꼬리를 갱신하며, `report`가 종료 후 나머지를 저장한다

## 어떻게 도는가

- ㉮ `create_run_dir` (`src/run.py:715-733`): label은 `output.label`, 없으면 첫 채널 type (`:720`). `config.json` 사본 (`:725`). summary.txt 머리는 `run:`, `code commit:`, `start:`, 빈 줄, 실험 요약 불릿, 빈 줄 (`:726-732`)
- ㉯ `code commit` (`:603-618`): `git rev-parse --short HEAD`. 미커밋 변경이 있으면 `+dirty`. git이 없거나 실패면 "(git 없음)"
- ㉰ `report` (`:736-777`)가 쓰는 파일

| 파일 | 조건 | 열 | 근거 |
|---|---|---|---|
| `{csv_prefix}_{label}.csv` | 항상 | param, fer, post_fec_ber, frames, errors, avg_decoding_iteration, sec | `src/sim.py:170-182` |
| `log_iter_{label}_p{param}.csv` | csw_per_iter, bit_err_per_iter, bit_err_by_dv 중 하나 이상 | iter, active_frames, csw_mean, bit_err_mean, bit_err_{dv라벨}_mean (켠 열만). 평균 = 합 / max(active, 1). 행은 활성 프레임이 있는 마지막 iteration까지 | `src/run.py:627-653` |
| `log_iter_hist_{label}_p{param}.csv` | iter_histogram 또는 fer_vs_iter | iter, success_at_iter, fer_if_max_iter_k (= 1 - 누적 성공 / frames) | `src/run.py:656-677` |
| `log_fail_{label}_p{param}.csv` | fail_frame_detail | frame, final_err_bits, final_csw, err_{dv라벨} | `src/run.py:680-689` |
| 사용한 LLR 파일 사본 | `save_llr_matrix` true | 원본 파일 그대로 | `src/run.py:764-768` |
| `fer_curves.png` | fer_curve_png | 라벨별 FER 곡선 | `src/run.py:769-775` |

- ㉱ dv 라벨은 `dv{from}` 또는 `dv{from}-{to}` (`:621-624`). JSON log 키와 디코더 항목 이름의 대응은 `_LOG_TO_ITEM` (`:113-114`): csw_per_iter → csw, bit_err_per_iter → bit_err, bit_err_by_dv → bit_err_by_dv, fail_frame_detail → fail_detail
- ㉲ PNG (`:692-712`): matplotlib 지연 import, Agg 백엔드, 로그 y축. 에러 0 포인트는 0.5/frames를 흰 역삼각형 상한 마커로 찍는다. 저장에 실패해도 측정 결과는 보존된다 (`:771-775`)
- ㉳ 로그 항목의 C++ 대응과 용도

| 항목 | C++ 로그 대응 | 용도 |
|---|---|---|
| csw_per_iter | `m_log_CSW`, `m_log_CSW_auto` | 수렴 궤적, CSW 그룹 임계 튜닝 |
| bit_err_per_iter | `m_log_bit_err` | restart 효과 |
| bit_err_by_dv | `m_log_bit_err_col` 축약판 | 특정 dv 고착 진단 |
| iter_histogram | `m_log_iter_histogram_tot` | max_iter 여유 판단 |
| fer_vs_iter | (py 고유) | "max_iter를 k로 줄였다면"의 FER를 한 실행에서 산출 |
| fail_frame_detail | corner 추적 축약판 | error floor와 trapping set 1차 진단 |
| fer_curve_png | (py 고유) | FER 곡선 그림 |

## 쓰는 법

- ㉮ 로그는 `log.enabled`가 상위 스위치다. false면 items가 true여도 전부 꺼진다. 켜면 속도 비용이 든다
- ㉯ 실행 식별은 summary.txt의 `run:`과 `code commit:` 줄. `+dirty`면 실행 코드가 커밋과 다를 수 있다
- ㉰ 실행 폴더 비교: 로그 CSV는 완전 일치, FER CSV는 `sec` 열만 다르면 같은 결과로 본다
- ㉱ 로그 CSV 파일명에 `param`이 들어가므로 같은 채널의 포인트 값이 `int(1e6*값)`에서 겹치면 config 검증이 막는다
- ㉲ 후순위 로그 7종(bit_err_by_col, table_row_history 등)은 미구현. 재개 자료는 trial 문서에 있다

## 관련 문서

- ㉮ [결정: 분석 로그 핵심 세트](../decisions/20260806_analysis-log-core-set.md)
- ㉯ [결정: 평균 iteration 정의와 summary 실시간 갱신](../decisions/20260810_avg-iteration-and-realtime-summary.md)
- ㉰ [시도: 후순위 로그 항목](../trials/20260807_deferred-log-items.md)
- ㉱ [잘못된 패턴: 선택 산출물이 필수 기록 앞에서 죽는다](../assets/20260808_optional-output-before-required-record.md)
- ㉲ [한 포인트 측정 루프와 지표](20260930_fer-point-loop-and-metrics.md)
- ㉳ [run.py main 흐름](20260930_run-main-flow.md)
