---
summary: run_fer_point의 배치 루프와 종료 조건, FER와 post_fec_ber와 avg_decoding_iteration 산식, 진행 줄, 반환 dict, FER CSV 열
tags: [sim, fer, metrics]
sources: [src/sim.py:21-26, src/sim.py:29-70, src/sim.py:86-92, src/sim.py:95-167, src/sim.py:170-182]
last_verified: 2026-09-30
---

## 무엇을 하는가

- ㉮ `run_fer_point`가 한 채널 조건(한 포인트)의 FER를 잰다. 배치 단위로 채널 생성과 복호를 반복하고 프레임 에러 수 또는 프레임 수로 끝낸다 (`src/sim.py:29-167`)
- ㉯ 결과는 dict 하나. `save_csv`가 포인트 결과 목록을 FER CSV로 쓴다 (`:170-182`)

## 어떻게 도는가

- ㉮ 시그니처 (`src/sim.py:29-32`): `run_fer_point(code, channel_fn, decoder, random_generator, max_frame_errors=50, max_frames=20000, frames_per_batch=128, print_progress=False, log=None, progress_label="", progress_interval_frames=100, summary_path=None)`
- ㉯ 최소 가드 (`:58-70`): 정수 4개는 1 이상 (frames_per_batch가 0이면 무한 대기). log 항목은 `LOG_ITEMS` 부분집합 (오타 검출)
- ㉰ 루프 (`:95-120`)
  - ㉠ `while frames < max_frames and errors < max_frame_errors`. batch = min(frames_per_batch, 남은 프레임)
  - ㉡ `decoder.decoder_main(channel_fn(batch, rng), log=)`로 batch 프레임을 한 번에 복호
  - ㉢ 집계: errors += 실패 수, 성공 프레임의 수렴 iteration 합, 정보 구간 잔여 에러 bit 합, `np.add.at(iter_hist, decode_success_iteration, 1)` (실패는 [0])
  - ㉣ log가 있으면 iteration별 합(active, csw, bit_err, bit_err_by_dv). fail_detail이면 (frames + k, final_err_bits, final_csw, final_err_by_dv) 튜플을 쌓는다
- ㉱ 지표 (`:139-149`)

| 지표 | 산식 |
|---|---|
| fer | errors / frames |
| post_fec_ber | 정보 구간 잔여 에러 bit 합 / (frames `*` K) |
| avg_decoding_iteration | (성공 프레임 수렴 iteration 합 + errors `*` max_iter) / frames |
| fps | frames / 경과 초 |
| ips | 합산 iteration / 경과 초 |

- ㉲ 진행 줄 (`:121-137`): `progress_interval_frames`마다 `e/fr = errors/frames fer = ... ber = ... avg_iter = ... (f/s, it/s, elapsed hh:mm:ss)`. 콘솔 `\r` 갱신은 `sys.stdout.isatty()`일 때만 (`:86`). summary.txt는 시작 시 파일 크기를 offset으로 잡고 (`:92`) `_rewrite_file_tail`로 꼬리를 교체하며 (`:21-26`, `:135`) 끝나면 결과 줄로 대체한다 (`:164-166`)
- ㉳ 반환 dict 키 (`:142-161`): frames, errors, fer, post_fec_ber, avg_decoding_iteration, sec, fps, ips, iter_hist, summary_line. log 시 iteration_totals {active_frames, csw_sum, bit_err_sum, bit_err_by_dv_sum}. fail_detail 시 fail_frame_details
- ㉴ FER CSV 열 (`save_csv`, `:170-182`)

| 열 | 뜻 | 형식 |
|---|---|---|
| param | 포인트 값 | 그대로 |
| fer | 프레임 에러율 | 6e |
| post_fec_ber | 정보 bit 기준 잔여 BER | 6e |
| frames | 측정 프레임 수 | 정수 |
| errors | 프레임 에러 수 | 정수 |
| avg_decoding_iteration | 프레임당 평균 복호 iteration | 3f |
| sec | 경과 초 | 1f |

## 쓰는 법

- ㉮ 종료 조건: `max_frame_errors`는 통계 신뢰, `max_frames`는 상한. 낮은 FER 구간은 max_frames를 키운다
- ㉯ `frames_per_batch`는 속도와 메모리 조절용이지만 같은 seed 수치 재현에는 이 값까지 같아야 한다
- ㉰ 실패 프레임은 max_iter로 세므로 `avg_decoding_iteration`은 FER가 높을수록 max_iter에 가깝다
- ㉱ 파일로 리다이렉트하면 진행 줄 없이 결과 줄만 남는다. 진행은 summary.txt 꼬리에서 본다
- ㉲ 직접 호출할 때 `channel_fn(batch, rng)`는 `channel.py` 출력 dict를 돌려줘야 한다

## 관련 문서

- ㉮ [결정: 평균 iteration 정의와 summary 실시간 갱신](../decisions/20260810_avg-iteration-and-realtime-summary.md)
- ㉯ [실행 폴더와 출력 파일](20260930_run-dir-and-output-files.md)
- ㉰ [channels 섹션과 실험 루프](20260930_channels-section-and-experiment-loop.md)
- ㉱ [genie 판정과 배치 압축](20260930_genie-check-and-batch-compress.md)
- ㉲ [디코더 단계 함수와 상태](20260930_decoder-stages-and-state.md)
