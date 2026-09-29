---
summary: 채널 모델 3종(rber, fixed_error, strong_error)의 산식과 출력 dict, 디코딩 모드 정합 3층
tags: [channel, rber, strong-error]
sources: [src/channel.py:1-21, src/channel.py:24-40, src/channel.py:43-68, src/channel.py:71-88, src/channel.py:91-135, src/channel.py:138-149, src/run.py:504-530, src/decoder.py:230-232]
last_verified: 2026-09-30
---

## 무엇을 하는가

- ㉮ `src/channel.py`가 송신 codeword(all-zero)에 에러를 넣어 디코더 입력 dict를 만든다. C++ 원본의 채널 모드 3종에 대응한다 (`src/channel.py:1-7`)
- ㉯ 출력은 `{"mode", "hd", "sd", "cc"}`. `hd`는 (B, N_b, z) uint8 read bit, `sd`는 2SD와 3SD의 strong 플래그, `cc`는 3SD의 very 플래그 (`:9-11`)

## 어떻게 도는가

- ㉮ 레지스트리 `CHANNELS`와 지원 모드 `CHANNEL_MODES` (`src/channel.py:138-149`)

| 채널 | C++ 대응 | 지원 모드 | 포인트 값 |
|---|---|---|---|
| rber | MODE_CH_RBER | HD, 2SD, 3SD | RBER p (0 < p < 0.5) |
| fixed_error | MODE_CH_FIXED_ERROR | HD | 프레임당 에러 bit 수 E |
| strong_error | MODE_CH_STRONG_ERROR | 2SD | E와 SER, SCR |

- ㉯ rber (`:43-68`)
  - ㉠ `dev_from_rber(p)`: snr = qfunc_inv(p)^2 / 2, dev = sqrt(1 / (2 snr)) (`:37-40`). `qfunc_inv` 계수는 C++와 같다 (`:24-34`)
  - ㉡ bpsk = 1 - 2 cw, cwr = bpsk + N(0, dev), hd = (cwr < 0) (`:50-52`)
  - ㉢ SD: `llr_mag = |2 cwr / var|`, th_k = 2 r_offset_k / var. `_R_OFFSET`는 2SD (0.35,), 3SD (0.15, 0.35, 0.55) (`:21`, `:56-57`)
  - ㉣ 2SD: 임계 하나, sd = (llr_mag >= th[0]). 3SD: `th1, th2, th3 = th`로 풀어 sd = (llr_mag >= th2), cc = (llr_mag >= th3) 또는 (llr_mag < th1) (`:58-67`). 3SD 조합: sd=1,cc=1 very strong, sd=1,cc=0 normal strong, sd=0,cc=0 normal weak, sd=0,cc=1 very weak (`:11`)
- ㉰ fixed_error (`:78-88`): HD 전용. `_rand_positions`가 `argpartition`으로 프레임마다 정확히 E개 위치를 뽑아 flip (`:71-75`). 뽑힌 집합만 균일하고 내부 순서는 무작위가 아니다
- ㉱ strong_error (`:91-135`): 2SD 전용. e2 = round(E `*` SER) (에러 중 strong), c2 = round((N - E) `*` SCR) (정정 중 strong), c1 = N - E - c2. sd 초기값 1 (`:113-117`)
  - ㉠ rand_vals의 argpartition으로 에러 위치 E개 (`:119-122`)
  - ㉡ 에러 위치를 `permuted`로 행별 셔플한 뒤 앞 e2개만 strong으로 남기고 나머지를 weak (`:124-126`)
  - ㉢ 에러 위치를 2.0으로 막은 rand_masked에서 하위 c1개를 weak (`:129-133`)
  - ㉣ 원본의 부분 Fisher-Yates와 구간 슬라이스와 통계 등가. 균일 순열의 앞 k개는 균일 부분집합과 분포가 같다 (`:98-103`)
- ㉲ 모드 정합 3층: `_check_channel_mode`가 측정 전 전 채널 (`src/run.py:504-512`, 호출 `:519`, `:568-569`), 채널 함수의 `mode` 인자 검사 (`src/channel.py:46-47`, `:80-81`, `:104-105`), 디코더 `_read_channel_input`의 채널 dict mode 검사 (`src/decoder.py:230-232`)
- ㉳ 난수는 numpy Generator (`:16`). 쇼트닝과 펑처링 없음 전제 (`:15`)

## 쓰는 법

- ㉮ 디코딩 모드는 LLR matrix 파일명이 정하므로 채널 type을 고를 때 지원 모드를 맞춘다. fixed_error는 HD 파일, strong_error는 2SD 파일과만 짝이 된다
- ㉯ strong_error는 `channels.fixed_error` 공간의 E와 `strong_ratios`의 SER, SCR를 함께 쓴다
- ㉰ 새 채널 추가는 교체 지점이 아니다. `CHANNELS`, `CHANNEL_MODES`, run 검증을 함께 고친다
- ㉱ `_rand_positions` 결과를 구간 슬라이스로 나눠 쓰지 않는다 (집합만 균일)

## 관련 문서

- ㉮ [결정: strong_error 2단계 추출](../decisions/20260807_strong-error-two-stage-extraction.md)
- ㉯ [잘못된 패턴: 집합 균일과 순서 균일](../assets/20260806_set-uniform-vs-order-uniform.md)
- ㉰ [channels 섹션과 실험 루프](20260930_channels-section-and-experiment-loop.md)
- ㉱ [SD region 매핑과 Pre 단계](20260930_sd-region-and-pre-stage.md)
- ㉲ [결정: seed 하나에서 파생하는 난수 스트림](../decisions/20260807_single-seed-derived-streams.md)
