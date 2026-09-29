---
summary: min1/min2가 증분 갱신되는 CN 저장 상태에는 값 변형을 넣지 않고, C2V를 읽어 내는 시점(`_c2v_reconstruct`)에 변형을 건다
type: pattern
tags: [replacement-point, cnu, clipping, state]
date: 2026-08-13
last_verified: 2026-09-30
---

## 내용

- ㉮ 문제: 논문의 클리핑 위치는 C++ `CNU_Update_New_Mag()`(min1/min2 확정 직후)이고 Python 대응은 `_cnu_update`다. 그런데 이 시뮬레이터는 CN 상태(min1, min2, min1_pos, check_sum, edge_sgn)를 remove old 후 insert new로 증분 갱신한다 (`src/decoder.py:197-220`). 저장값을 클리핑하면 다음 column 처리의 remove old가 원래 값을 찾지 못해 상태가 오염된다
- ㉯ 선택: `_c2v_reconstruct`(C++ C2V_Cal 대응, `src/decoder.py:150-157`)에서 `min1_row`를 P로, `min2_row`를 Q로 클리핑한 뒤 기존 선택식(자신이 min1 위치면 min2, 아니면 min1)을 그대로 쓴다. 논문 식에 대입하기 직전에 클리핑하는 것과 등가다
- ㉰ 지킨 경계
  - ㉠ 정수 클리핑이라 `_uniform_saturate` 등가 조건(비정수 메시지 금지)을 유지한다
  - ㉡ P, Q의 도메인은 edge magnitude 레벨 도메인(기본 3-bit {7,5,3,1}, 상한 7)이다
  - ㉢ `_cnu_update`의 제자리 갱신 규칙(반환값 미사용, `src/decoder.py:202-203`)에 손대지 않는다
- ㉱ 일반화: 상태를 누적 갱신하는 교체 지점에 값 변형을 넣기 전에, 같은 값을 읽어 쓰는 등가한 읽기 시점 교체 지점이 있는지 먼저 본다. 있으면 그쪽에 건다

## 사용 방법

- ㉮ 언제: CN 메시지 크기에 상한, 오프셋, 스케일을 거는 min-sum 변형(클리핑, offset min-sum, normalized min-sum)을 붙일 때
- ㉯ 어떻게: `_c2v_reconstruct`를 재정의해 `min1_row`, `min2_row`를 변형한 뒤 부모와 같은 선택식으로 C2V를 만든다. 변형이 정수를 벗어나면 `_vnu_quantize`와 `_uniform_saturate`의 등가 조건을 함께 본다
- ㉰ 주의: 무효과 파라미터(상한이 레벨 최대와 같은 값)로 돌려 `workspace/base_run/`과 수치 완전 일치를 먼저 확인한다. 실험 구현 파일(`workspace/minsum_dual_clip/decoder.py`)은 이 사본에 없어 태스크 문서 서술 기준이다
- 관련 문서
  - ㉠ [20260930_cnu-min1-min2-update.md](../tech/20260930_cnu-min1-min2-update.md)
  - ㉡ [20260930_replacement-points-six.md](../tech/20260930_replacement-points-six.md)
  - ㉢ [20260813_minsum-dual-clip-trial.md](../trials/20260813_minsum-dual-clip-trial.md)
  - ㉣ [20260813_paper-idea-single-override-procedure.md](20260813_paper-idea-single-override-procedure.md)
  - ㉤ `../../docs/profile/replacement_points.md`
