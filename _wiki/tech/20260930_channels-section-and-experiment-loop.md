---
summary: channels 섹션의 정규화 규칙, 채널 x 포인트 측정 루프, 포인트별 난수 스트림 파생, stop_below_fer 동작
tags: [channels, experiment-loop, rng]
sources: [src/run.py:158-180, src/run.py:183-247, src/run.py:515-545, src/run.py:548-600, workspace/_template/config.json:83-99]
last_verified: 2026-09-30
---

## 무엇을 하는가

- ㉮ `_check_channels`가 channels 섹션을 `[{"type", "points", ...}]` 리스트로 정규화한다. `type`이 측정할 채널을 고르고 값 공간은 자리를 미리 만들어 둔다 (`src/run.py:183-247`)
- ㉯ `run_experiment`가 채널마다, 포인트마다 `run_fer_point`를 불러 결과를 모은다. 난수는 seed 하나에서 포인트별로 파생한다 (`:548-600`)

## 어떻게 도는가

- ㉮ channels 정규화 (`src/run.py:183-247`)
  - ㉠ `type`은 문자열 또는 문자열 리스트. 같은 type 중복 금지 (`:200-201`). `CHANNELS`에 등록된 이름만 허용 (`:202-206`)
  - ㉡ 값 공간 `rber`, `fixed_error`는 존재하면 전부 `_check_channel_values`로 검사 (`:207-211`, `:158-180`): 스칼라는 리스트로, 비어 있거나 null이면 에러, rber는 `0 < p < 0.5` 실수, 그 외는 0 이상 정수. `int(1e6 * 값)`이 겹치면 에러 (같은 난수 스트림으로 중복 측정되고 로그 CSV 파일명이 덮이므로)
  - ㉢ `strong_ratios`는 `{SER, SCR}` 객체이고 각각 0 이상 1 이하 (`:212-223`)
  - ㉣ 공간 공용: `fixed_error` 공간은 fixed_error와 strong_error type이 함께 소비 (`:233-238`). strong_error는 `strong_ratios`도 필수 (`:239-245`)
  - ㉤ 결과: `[{"type", "points", (strong_error면 "SER", "SCR")}]`
- ㉯ 실험 루프 (`src/run.py:548-600`)
  - ㉠ 측정 전 전 채널의 모드 호환을 `_check_channel_mode`로 확인 (`:568-569`). 포인트마다 `_make_channel_fn`에서도 한 번 더 부른다 (`:519`)
  - ㉡ 채널 라벨 = `type` (`:577`). 같은 라벨이 있으면 `_2`, `_3` 접미사 (`:578-583`). 라벨은 CSV 파일명에 쓰인다
  - ㉢ 포인트마다 `np.random.default_rng([seed, channel_index, int(1e6 * point)])` (`:586`). 포인트 간, 채널 간 독립이고 같은 seed면 재현
  - ㉣ `_make_channel_fn` (`:515-530`): `generate_message` → `encode`(all-zero 임시) → `CHANNELS[type](code, cw, point, rng, mode=, **extra)`. strong_error는 `scr`, `ser`를 extra로 넘긴다
  - ㉤ `run_fer_point` 호출 뒤 `point_result["param"] = point` (`:588-595`)
  - ㉥ `stop_below_fer`가 있고 측정 FER가 그 값 미만이면 그 채널의 남은 포인트를 중단한다. 다음 채널은 계속 (`:597-598`)
  - ㉦ 반환 `[(라벨, [point_result, ...]), ...]`
- ㉰ 진행 줄의 포인트 표기 `_point_label` (`:533-545`): fixed_error `E=`, rber `rber=`, strong_error `E=, SCR=, SER=`

## 쓰는 법

- ㉮ config 꼴 (`workspace/_template/config.json:83-99`): `"type"`은 `"fixed_error"` 또는 `["fixed_error", "rber"]`, 값 공간은 `"rber": [...]`, `"fixed_error": [...]`, `"strong_ratios": {"SER", "SCR"}`
- ㉯ 채널을 바꿀 때 값 공간은 그대로 두고 `type`만 바꾼다
- ㉰ 같은 seed 수치 재현 조건: seed, 채널 순서(channel_index), 포인트 값, `frames_per_batch`가 같아야 한다. 채널 순서를 바꾸면 스트림이 달라진다
- ㉱ rber 포인트를 소수점 7자리 이상으로 촘촘히 두면 `int(1e6 * 값)` 충돌로 config 검증에서 막힌다
- ㉲ 여러 포인트를 낮은 FER 쪽으로 늘어놓을 때 `stop_below_fer`로 남은 포인트를 자동 생략한다

## 관련 문서

- ㉮ [채널 모델 3종](20260930_channel-models.md)
- ㉯ [한 포인트 측정 루프와 지표](20260930_fer-point-loop-and-metrics.md)
- ㉰ [config 검증 규칙](20260930_config-validation-rules.md)
- ㉱ [결정: seed 하나에서 파생하는 난수 스트림](../decisions/20260807_single-seed-derived-streams.md)
- ㉲ [잘못된 패턴: 공유 난수와 배치 크기 의존](../assets/20260808_shared-rng-batch-dependence.md)
