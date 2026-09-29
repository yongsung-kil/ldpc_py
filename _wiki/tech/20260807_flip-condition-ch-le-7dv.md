---
summary: 반전 불가 조건 `ch > dv*top`의 유도, 클리핑 일반형 `Q + (dv-1)*P`, 레벨 0 시절의 공명 조건, 스케일 인사이트, 알려진 위반 상태, dv별 사망 경계 판단 절차
tags: [flip-condition, channel-llr, trapping, clipping]
sources: [src/decoder.py:21-22, src/decoder.py:116, src/decoder.py:155-157, src/decoder.py:159-162, src/decoder.py:204, src/decoder.py:382-398, src/llr_matrix.py:51-57, Input/LLR/LLR_MATRIX_HD_0.txt:5, Input/LLR/LLR_MATRIX_HD_0.txt:20, Input/LLR/LLR_MATRIX_HD_0.txt:24, Input/LLR/LLR_MATRIX_HD_1.txt:19, Input/LLR/LLR_MATRIX_HD_1.txt:21, docs/profile/constraints.md:21, docs/profile/constraints.md:49, _pm/TODO.md:29-31, _pm/DONE.md:3-16, _pm/tasks/20260808_review/r3_round3_lv2_verification/team_a_verification.md:64-95, workspace/_template/config.json:31-34]
last_verified: 2026-09-30
---

## 무엇을 하는가

VN(variable node) 판정 `sum_t = ch + Σ C2V`에서 ch(채널 LLR 크기)는 항상 + 부호라, 한 column의 ch가 C2V(check-to-variable 메시지) 합의 최대치를 넘으면 그 column은 어떤 iteration에서도 반전되지 않는다 (trapping). 3-bit 기본에서 반전 가능 조건은 `ch <= 7*dv` (dv는 column degree)다. 이 문서는 조건의 유도, 클리핑 일반형, 스케일 인사이트, 위반 상태, 판단 절차를 모은다.

## 어떻게 도는가

- ㉮ 유도: `sum_t = ch + Σ vnu_in`이고 ch는 항상 + (`src/decoder.py:21-22`, `:382-388`), 반전은 `sum_t <= 0` (`:159-162`). C2V 크기 상한은 `edge_mag[0]` = top (`:116`, `:204`, 3-bit에서 7). dv개 C2V가 전부 반대 부호 최대여도 `sum_t >= ch - dv*top`이므로 `ch > dv*top`이면 반전이 없다. 경계는 초과다. `ch = dv*top`은 sum_t가 0에 닿을 수 있고 동점 반전으로 반전된다 (`team_a_verification.md:91-95`)
- ㉯ 클리핑 일반형: `_c2v_reconstruct`가 min1 또는 min2를 돌려주므로 (`src/decoder.py:155-157`) min1 상한 P, min2 상한 Q로 클리핑하면 dv column의 최대 extrinsic은 edge 하나가 min2(Q), 나머지 dv-1개가 min1(P)인 `Q + (dv-1)*P`다. 이것이 ch보다 작으면 반전 불능 (`_pm/DONE.md:10-11`). 무클립은 P = Q = top이라 `dv*top`
- ㉰ 공명 조건 (레벨 0이 있던 시절): 균일 레벨 [top..0]에서 `ch = k*top`이고 `|k| <= dv-1`, `k ≡ dv-1 (mod 2)`인 dv가 있으면 iteration 1에서 raw = 0이 레벨 0으로 살아남아 CN(check node)을 침묵시켰다. 예시 부호에서는 k=1(ch = top)만 파국이고 bit 수와 무관했다 (`team_a_verification.md:72-83`). 균일 최소 레벨을 1로 올려 해소 (`src/llr_matrix.py:51-57`, 2026-08-09). ch = 1도 파국이며 이것은 남는다 (`_pm/tasks/20260808_review/r3_round3_lv2_verification/team_a_verification.md:88-90`)
- ㉱ 스케일 인사이트 (2026-08-14): edge 상한과 ch는 같은 배율이다 (`docs/profile/constraints.md:21`, `workspace/_template/config.json:33-34`). 상한 15에 균일 ch=8(headroom)이면 무클립이 붕괴(FER 1.0)하고 클리핑 (4,8)이 0/256으로 복구한다. ch=16(balanced)이면 무클립이 건강하고 (4,8)은 사망한다 (`_pm/DONE.md:14-16`). 클리핑은 실효 edge 상한을 ch 스케일에 맞추는 조정으로 읽힌다
- ㉲ 알려진 위반 상태: 토이 파일 `Input/LLR/LLR_MATRIX_HD_0.txt`와 `HD_1.txt`의 dv=2 열 ch=28 > 14 (`HD_0.txt:5, 20, 24`, `HD_1.txt:19, 21`, `docs/profile/constraints.md:49`). 같은 파일의 dv=4 ch=10, dv=3 ch=13은 조건을 지킨다. 조치 없음 (예시 데이터 특성, 2026-08-09). 파라미터 수정 시점에 함께 처리한다 (`_pm/TODO.md:29-31`). 코드 검사는 없다
- ㉳ 유래: 2026-08-03 낮은 dv의 ch가 메시지 최대 이상이면 trapping 발견 → 2026-08-07 LLR 최적화 탐색 범위 규칙으로 등재 → 2026-08-09 SD 토이 파일 작성 시 준수 → 2026-08-14 클리핑 실험 원인 규명에서 일반형으로 확장

## 쓰는 법

- 사망 경계 판단 절차 (dv별)
  - 1. 실행 폴더 summary.txt의 `col degree` 분포에서 지배 dv를 찾는다
  - 2. LLR 파일 row의 dv별 ch를 읽는다. 먼저 summary.txt `LLR matrix` 줄로 실제 탄 경로가 파일 로드인지 균일 생성인지 확인한다
  - 3. (P, Q)마다 `Q + (dv-1)*P`를 계산해 dv별 생존 여부 표를 만든다 (무클립은 `7*dv`). 예: dv=4, ch=10이면 (2,3)은 9로 사망, (2,5)는 11로 생존
  - 4. `log.items.bit_err_by_dv`를 켜서 `log_iter_*.csv`의 `bit_err_dv{..}_mean` 열로 어느 dv가 고착인지 실측 대조한다. 무클립에서 이미 위반인 열(dv=2 ch=28)은 on/off 차이 원인에서 뺀다
- ㉮ LLR 최적화나 토이 파일 작성 때 dv별 `ch <= top*dv`를 탐색 범위 상한으로 둔다
- ㉯ 균일 경로에서 `edge_max_value`를 바꾸면 `channel_llr_*`를 같은 배율로 바꾼다
- ㉰ 주의: 원인 서술에 인용하는 ch 값은 실험이 실제로 탄 경로의 값이어야 한다 (균일 경로 값을 파일 경로 실험에 인용한 오류가 있었다). 공급자가 준 참고값은 문서에 적지 않는다

## 관련 문서

- decisions [20260809_fer-one-no-action-example-data.md](../decisions/20260809_fer-one-no-action-example-data.md), [20260813_edge-quantization-bits-max-split.md](../decisions/20260813_edge-quantization-bits-max-split.md), [20260809_uniform-min-level-one.md](../decisions/20260809_uniform-min-level-one.md)
- trial [20260813_minsum-dual-clip-trial.md](../trials/20260813_minsum-dual-clip-trial.md)
- assets [20260814_fix-misquoted-cause-with-logged-values.md](../assets/20260814_fix-misquoted-cause-with-logged-values.md), [20260814_slot-config-and-pq-scan.md](../assets/20260814_slot-config-and-pq-scan.md), [20260808_zero-level-not-in-original.md](../assets/20260808_zero-level-not-in-original.md)
- tech [20260930_syndrome-aided-column-step.md](20260930_syndrome-aided-column-step.md), [20260930_uniform-llr-matrix-synthesis.md](20260930_uniform-llr-matrix-synthesis.md), [20260930_run-dir-and-output-files.md](20260930_run-dir-and-output-files.md)
- profile `../../docs/profile/constraints.md`
