---
summary: 논문 아이디어를 교체 지점 하나만 재정의해 붙이고, 무효과 조건 일치와 유효 재정의 차이의 두 방향으로 검증한 뒤 on/off 비교하는 절차
type: pattern
tags: [paper-idea, replacement-point, procedure, verification]
date: 2026-08-13
last_verified: 2026-09-30
---

## 내용

교체 지점이란 본체 `src/decoder.py`의 `BaseDecoder`가 원본 C++ 함수 경계를 따라 따로 떼어 둔 메서드 6개다. 본체는 고치지 않고 자식 클래스에서 그중 하나만 재정의한다.

- 1. 사전 준비: 논문의 delta를 한 문장으로 적고 실물 C++ 이식 지점을 식별한다 (예: `decoder.cpp`의 `CNU_Update_New_Mag()`). 논문 아카이브(형제 저장소)의 stage5 산출물(pseudocode, impl, integration_patch, verification_plan)이 있으면 확인한다
- 2. 베이스 회귀 확인: 실험 직전에 refactor가 있었으면 그 직전 커밋을 worktree로 꺼내 같은 조건으로 돌려 수치 완전 일치를 먼저 확인한다
- 3. 양식 복사: `workspace/_template/`(run.py, config.json, README.md)를 새 실험 폴더로 복사하고 `decoder.py`를 추가한다
- 4. 재정의: `BaseDecoder`를 상속해 교체 지점 6개(`_is_edge_clear_iter`, `_column_order`, `_c2v_reconstruct`, `_vn_decide`, `_vnu_quantize`, `_cnu_update`) 중 하나만 재정의한다. 인자 목록은 부모와 같게 둔다. 파라미터는 우선 클래스 속성으로 전달하고 config 통로(checker 허용 키 확장, setup 전달)는 별도 작업으로 미룬다
- 5. 주입: `run.py`의 `DECODER_CLASS`를 그 클래스로 지정한다. config에는 디코더 선택 키가 없다
- 6. 무효과 조건 일치: 재정의가 아무 효과도 내지 않는 파라미터(예: 클리핑 상한이 레벨 최대와 같은 (7,7))로 돌려 `workspace/base_run/`과 수치 완전 일치를 확인한다. 이것이 구현 동등성 증거다
- 7. 유효 재정의 차이: 효과가 있는 파라미터로 돌려 FER나 BER이 base_run과 달라지는 것을 확인한다. 이것이 주입 반영 증거다 (예: 동점 비반전 `NoTieFlipDecoder`)
- 8. on/off 비교: seed, 채널, 포인트, `frames_per_batch`를 같게 두고 base_run(off)과 실험(on)의 `fer_{label}.csv`와 summary.txt 결과 줄을 대조한다. 안전성 체크리스트 네 줄은 본체 무변경, base_run 재정의 0개 유지, 재정의 함수 인자 동일, 비교 조건 동일
- 9. 기록: 결과, 판정, 한계를 실험 폴더 README 표에 적는다. toy 상대 비교면 절대 성능 판단 불가를 명시한다

최소 코드 조각:

```python
# workspace/{실험}/decoder.py
from src.decoder import BaseDecoder

class MyDecoder(BaseDecoder):
    def _vn_decide(self, sum_t):
        return sum_t < 0        # 예: 동점을 반전하지 않는 변형
```

```python
# workspace/{실험}/run.py
from decoder import MyDecoder
DECODER_CLASS = MyDecoder
```

## 사용 방법

- ㉮ 언제: 논문이나 제안의 delta를 처음 붙일 때. 새 상태 배열이나 iteration 구조 변경이 필요한 기법은 이 절차에 맞지 않는다 (`../../docs/profile/replacement_points.md` 3절)
- ㉯ 주의: `_cnu_update`는 제자리 갱신 규칙을 지킨다. `_vnu_quantize`가 비정수 raw를 만들면 `_uniform_saturate`도 함께 재정의한다. 증분 갱신 상태에 값 변형을 넣기 전에 읽기 시점 교체 지점이 있는지 본다
- ㉰ 이 사본의 제약: 6단계부터 실행이 막혀 있다. 사유는 [20260930_testbed-copy-vs-original-layout.md](../tech/20260930_testbed-copy-vs-original-layout.md), 해결 방향은 [20260930_variant-decoder-run-path.md](../decisions/20260930_variant-decoder-run-path.md) (판정요청 대기)
- ㉱ 근거 위치: 교체 지점 표지는 `src/decoder.py:136-220`의 docstring 첫 줄 `[교체 지점: ...]`, 주입 사슬은 `workspace/_template/run.py:24-33`과 `src/run.py:780-795`
- 관련 문서
  - ㉠ [20260807_replacement-point-cpp-function-boundary.md](../decisions/20260807_replacement-point-cpp-function-boundary.md)
  - ㉡ [20260930_replacement-points-six.md](../tech/20260930_replacement-points-six.md)
  - ㉢ [20260930_variant-decoder-run-path.md](../decisions/20260930_variant-decoder-run-path.md)
  - ㉣ [20260813_minsum-dual-clip-trial.md](../trials/20260813_minsum-dual-clip-trial.md)
  - ㉤ [20260813_refactor-regression-by-worktree.md](20260813_refactor-regression-by-worktree.md)
  - ㉥ [20260807_fixed-input-array-regression.md](20260807_fixed-input-array-regression.md)
  - ㉦ [20260813_clip-at-reconstruct-not-stored-state.md](20260813_clip-at-reconstruct-not-stored-state.md)
