---
summary: 원본에 없는 값(메시지 크기 0)을 균일 레벨에 도입하자 공명 붕괴, min1 점유, -0.0 부호 소실 세 증상이 한 뿌리에서 나왔다
type: antipattern
tags: [quantization, edge-mag, min-sum]
date: 2026-08-08
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/tasks/20260808_review/종합보고.md`, `_pm/tasks/20260808_review/r3_round3_lv2_verification/team_a_verification.md`

### ㉮ 증상 (리뷰 시점 사실, 2026-08-08)

- ㉠ 공명 붕괴: 균일 레벨을 `[top..0]`으로 잡은 상태에서 채널 LLR `ch`가 `top`과 같으면 iteration 1에서 `sum_t`가 정확히 0이 되고, 그 0이 레벨 0으로 살아남아 CN(check node)을 침묵시켰다. FER 1.0으로 경고 없이 완주. 인접 `ch` 값은 정상이라 스윕 중 함정
- ㉡ min1 점유: 크기 0 메시지가 `<=` 비교로 항상 min1 자리를 차지해 그 CN이 한 edge만 빼고 0을 내보내고, 그 한 edge는 근거 없는 RESET(최대 확신)을 받았다. 워터폴 FER 1.2배에서 1.9배 악화
- ㉢ `-0.0` 부호 소실: `sgn * 0`이 `-0.0`이 되고 `(x < 0)` 판정이 양수로 읽었다. FER와 BER는 기본 column 순서에서 불변이었지만 CSW 계열 로그가 전 행 틀렸다

### ㉯ 원인

- C++는 압축 V 도메인(0이 정상 상태)과 EDGE 도메인(C2V 최소 1)이 분리되어 있다. Python이 둘을 `edge_mag` 하나로 합치면서 EDGE 도메인에 없던 0이 들어왔다

### ㉰ 점검 항목

- ㉠ 원본 레벨 집합에 없는 값(특히 0)을 도입하지 않는다. 도입해야 하면 최솟값 비교 연산과 부호 표현에 미치는 영향을 먼저 본다
- ㉡ 부호를 부동소수점 곱으로 실어 나르지 않는다. 부호와 크기를 따로 두거나 `np.signbit`을 쓴다
- ㉢ "복호 결과 불변"이라는 주장에는 조건(기본 스케줄)을 붙인다. 순서가 바뀌는 스케줄에서는 갈렸다
- ㉣ 스윕에서 특정 한 점만 붕괴하면 공명을 의심한다

### ㉱ 현재 코드 (수리된 위치)

- ㉠ `uniform_edge_mag(top)`이 `[top..2,1,1]`을 만든다. 최소 레벨 1 (`src/llr_matrix.py:51-57`)
- ㉡ 균일 등가식 `_uniform_saturate`가 `max(min(|raw|, top), 1)`로 하한을 1로 막는다 (`src/decoder.py:189-195`)
- ㉢ 레벨 분리 뒤 간격 2 이상이면 최소 레벨은 `step-1`이라 여전히 0이 없다 (`src/llr_matrix.py:72, 85-89`)
- ㉣ 0이 사라져 `-0.0`이 생기지 않으므로 signbit 처방은 넣지 않았다. `new_sgn = (vnu_out < 0)`이 그대로다 (`src/decoder.py:410`)

## 사용 방법

- 언제: 양자화 레벨 집합, 포화 상한과 하한, 특수값(0, -1)을 원본과 다르게 잡으려 할 때
- 어떻게: 새 값이 들어갈 연산을 셋으로 나눠 본다. ㉠ 최솟값과 정렬 비교 ㉡ 부호 곱과 부호 판정 ㉢ 합이 정확히 0이 되는 조건. 하나라도 걸리면 원본 도메인 구분을 먼저 되살린다
- 주의: 증상 하나를 고치는 처방(예: signbit)을 뿌리 처방(레벨 최소 1)과 함께 넣으면 서로 갈릴 수 있다. 뿌리를 먼저 정하고 나머지 처방의 필요를 다시 본다

관련 문서
- [20260809_uniform-min-level-one.md](../decisions/20260809_uniform-min-level-one.md)
- [20260930_vnu-quantize-cascade.md](../tech/20260930_vnu-quantize-cascade.md)
- [20260807_flip-condition-ch-le-7dv.md](../tech/20260807_flip-condition-ch-le-7dv.md)
- [20260808_prescriptions-revised-for-side-effects.md](../trials/20260808_prescriptions-revised-for-side-effects.md)
