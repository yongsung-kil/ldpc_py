---
summary: VNU 출력 |raw|를 th 캐스케이드로 edge_mag 레벨에 양자화하는 규칙, 균일 레벨 등가식이 성립하는 조건 (정수 raw), raw == 0일 때의 부호 규칙
tags: [decoder, vnu, quantization]
sources: [src/decoder.py:116-117, src/decoder.py:164-187, src/decoder.py:189-195, src/decoder.py:405-411, src/llr_matrix.py:51-57, src/llr_matrix.py:220-226, src/llr_matrix.py:388-400, docs/차이.md:38]
last_verified: 2026-09-30
---

## 하는 일

VNU (variable node unit, 변수 노드 연산부)가 낸 값 `raw = sum_t - vnu_in`을 임계값 th 목록과 견줘 edge_mag 레벨 (3-bit 기본 {7, 5, 3, 1}) 하나로 바꾼다. 레벨은 고정이고, iteration과 CSW에 따라 바뀌는 것은 th와 ch 값이다. 균일 레벨이면 같은 결과를 상수 시간 식으로 낸다.

## 동작 방식

- ㉮ 입력 (`src/decoder.py:405-408`): raw는 float32이며 포화가 없다 (`:407`). vnu_in은 부호 결정용. th는 `cur_th[:, dv_idx, :]` (F, th_len)로 프레임별 현재 row의 dv별 값
- ㉯ 캐스케이드 (`:173-181`): `mag_in = |raw|`. mag를 `edge_mag[-1]`로 시작해 k를 (len - 2)에서 0까지 내려가며 `mag_in >= th[:, k]`면 `edge_mag[k]`로 덮어쓴다. 결과는 가장 위 (작은 k)의 참 조건이 이긴다. C++ elif 체인과 같다: 3-bit에서 `>= th1 → 7`, 아니고 `>= th2 → 5`, 아니고 `>= th3 → 3`, 그 외 1 (`docs/차이.md:38`)
- ㉰ 비단조 th (`src/decoder.py:169`, `src/llr_matrix.py:220-226`): th가 내림차순이 아니어도 C++와 같은 캐스케이드 의미로 소비한다. 지시함수 합 (`Σ(|raw| >= th_k)`)으로 구현하면 내림차순 전제라 비단조에서 조용히 갈린다. 로더는 `th_nonmonotonic`을 세우고 경고만 낸다. 거부하면 원본이 받는 파일을 못 읽는다
- ㉱ 부호 (`src/decoder.py:182-186`): `raw > 0`이면 +1, 아니면 -1. `raw == 0`이면 vnu_in의 부호를 쓴다 (`vnu_in > 0`이면 +1). 반환은 `sgn * mag` (`:187`), VN 정렬
- ㉲ 균일 등가식 (`src/decoder.py:175-176`, `:189-195`): `_uniform_levels` (`llr_matrix.has_uniform_levels`를 생성자에서 읽음, `src/decoder.py:117`)가 True면 `_uniform_saturate(mag_in) = max(min(|raw|, edge_mag[0]), 1)`. 정수 raw에서 캐스케이드 (th [top..1], edge_mag [top..2, 1, 1])와 완전히 같다. 비정수 raw에서는 캐스케이드가 내림 동작이라 등가가 아니다
- ㉳ 균일 판정 (`src/llr_matrix.py:388-400`): restart 없음, `edge_mag == uniform_edge_mag(th_len)`, 전 row의 th가 [th_len..1] 연속 정수. 파일명이 아니라 값으로 정한다. 간격 2 이상 레벨 (예 {15, 11, 7, 3})은 False라 캐스케이드로 간다
- ㉴ 최소 레벨 1 (`src/llr_matrix.py:51-57`): `uniform_edge_mag(top) = [top..2, 1] + [1]`. C++도 C2V 크기 0을 내보내지 않는다. 마지막 두 항이 1인 것은 레벨 수 = th 수 + 1 제약 때문

## 쓰는 법

- ㉮ 재정의가 비정수 raw를 만들면 (offset min-sum, normalized min-sum, damping) `_uniform_saturate`도 함께 재정의하거나 캐스케이드 경로를 쓴다 (`src/decoder.py:192-194`)
- ㉯ 인스턴스 바인딩 금지: `__init__`에서 `self._vnu_quantize = ...`로 바꾸면 자식 재정의가 조용히 무시된다. 본체는 별도 함수와 조건부 호출 (`src/decoder.py:175-177`)로 되어 있다
- ㉰ 부호를 부동소수점 곱으로 실어 나르지 않는다. 최소 레벨 1이라 `-0.0` 문제는 없지만, 레벨 0을 도입하면 부호 소실과 min1 점유가 되살아난다
- ㉱ 디버그: `llr_matrix.summary()`가 "th 비단조 주의"를 붙이면 캐스케이드 순서로 읽히고 있다는 뜻이다. 의도한 값인지 파일을 본다
- ㉲ 속도: 캐스케이드는 th 개수만큼 `np.where`를 돈다. 균일 n-bit에서 th가 많을수록 등가식의 이득이 크다

## 관련 문서

- ㉮ [../decisions/20260809_uniform-min-level-one.md](../decisions/20260809_uniform-min-level-one.md): 최소 레벨 1 결정
- ㉯ [20260930_uniform-llr-matrix-synthesis.md](20260930_uniform-llr-matrix-synthesis.md): 균일 레벨 생성과 역판별
- ㉰ [20260930_replacement-points-six.md](20260930_replacement-points-six.md): `_vnu_quantize` 시그니처
- ㉱ [20260930_syndrome-aided-column-step.md](20260930_syndrome-aided-column-step.md): 호출 위치
- ㉲ [../assets/20260808_replacement-point-contract-protection.md](../assets/20260808_replacement-point-contract-protection.md): 등가 조건 명시와 인스턴스 바인딩 금지
- ㉳ [../assets/20260808_zero-level-not-in-original.md](../assets/20260808_zero-level-not-in-original.md): 레벨 0의 세 증상
- ㉴ [../trials/20260806_rejected-unification-and-relaxation.md](../trials/20260806_rejected-unification-and-relaxation.md): 비단조 th 거부가 기각된 경위
