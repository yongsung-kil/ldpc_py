### arxiv:0912.4995v3 - 1-State Error-Trellis Decoding of LDPC Convolutional Codes Based on Circulant Matrices (2010, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | SC-LDPC |
| 부호rate | 0.33 |
| 부호length | 미상 |
| 연판정 | hard-1bit |
| 핵심기여 | check matrix를 두 submatrix로 분할, 한쪽으로 error-trellis 구성 + 다른쪽 syndrome-subsequence를 side info로 써 1-state trellis에서 ML/M-algorithm 복호 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | trellis(Viterbi/M-algorithm) 기반 convolutional code 복호 - min-sum 반복 message-passing과 완전히 다른 패러다임, binary QC-LDPC 블록 디코더에 이식 불가 |
| 추가확인 | 없음 (패러다임 불일치로 이식 대상 아님) |

> 총평: LDPC convolutional code의 error-trellis 복호 복잡도를 줄이는 순수 이론 논문으로, NAND binary QC-LDPC iterative 디코더와 무관.

### B. 알고리즘 요약

1. 대상은 `GF(2)` 상의 `(n, n-m)` convolutional code로, 크기 `m×n`의 canonical check matrix `H(D)`와 그 syndrome former `H^T(D)`로 정의된다.
2. 문제: Tanner et al.의 circulant(monomial entry) LDPC convolutional code는 constraint length `ν`가 커서 error-trellis 기반 복호가 비현실적 → 복잡도 축소 필요.
3. 핵심 기법 1단: `H^T(D)`를 두 submatrix `(H1^T, H2^T)`로 수직 분할하고, `H1^T`만으로 degenerate error-trellis를 구성한다.
4. 일부 check 조건이 빠져 원래 없던 error path가 생기지만, `H2^T`로 계산한 syndrome-subsequence `{ζk^(2)}`를 side information으로 써 불일치 path를 제거하면 ML error path를 정확히 복원(Proposition 1, Corollary 1/2).
5. 복잡도(Proposition 3/4): survivor 총수와 compare-and-select 횟수는 `2^ν`로, 기존 원 trellis 복호와 본질적으로 동일(불일치 path 제거 비용만 추가).
6. 핵심 기법 2단: monomial entry 특성상 어느 한 row를 골라 각 entry의 인자 `D^l`을 factor-out하면 submatrix가 all-1이 되어 **1-state error trellis**가 얻어진다((7)의 예).
7. 부수 관찰: 1-state trellis의 state 우도가 all-zero state와 0이 많은 state에 집중(likelihood-concentration)됨을 crossover 확률 `ε`로 유도(TABLE I, `ε≤0.01`에서 합 >0.99).
8. 이 특성을 이용해 syndrome test를 통과한 path 중 weight 최소 `M(≤2^ν)`개만 survivor로 남기는 **M-algorithm** 기반 sub-optimal 복호를 제안.
9. 결과: (3,1) 예제에서 4 survivor로 ML 복호 재현, M-algorithm으로는 매우 작은 degradation으로 복잡도 축소(선행연구 [11]: `M≈√S`가 점근 최적).
10. 한계: HW 미설계, BSC(hard) 소형 손계산 예제와 확률표뿐(시뮬/실측 없음), convolutional code 전용 trellis 복호라 블록 QC-LDPC message-passing과 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| error-trellis / M-algorithm 복호 | 대응 없음 | trellis(Viterbi/list) 복호는 min-sum 반복 message-passing과 다른 패러다임 |
| LDPC convolutional code(circulant) 구조 | 대응 없음 | 우리는 block QC-LDPC 고정, convolutional/SC 구조 미대응 |
| syndrome-subsequence side info | 대응 없음 | trellis 복호 전용 보조정보, 디코더 루프에 대응 없음 |
| 복잡도 축소(survivor 수 `2^ν`) | 대응 없음 | trellis state 복잡도로 decoder.cpp 반복 복잡도와 무관 |

적용 가치: **낮음** — convolutional LDPC의 error-trellis(Viterbi/M-algorithm) 복호 복잡도 이론으로, NAND용 binary QC-LDPC 블록 min-sum 디코더와 접점이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:0912.4995v3",
  "title": "1-State Error-Trellis Decoding of LDPC Convolutional Codes Based on Circulant Matrices",
  "year": 2010,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "SC-LDPC",
  "code_rate": 0.33,
  "code_length": "미상",
  "soft_quant": "hard-1bit",
  "key_contribution": "check matrix를 두 submatrix로 분할해 한쪽으로 error-trellis 구성, 다른쪽 syndrome-subsequence를 side info로 활용하여 1-state trellis에서 ML/M-algorithm 복호로 복잡도 축소",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "trellis(Viterbi/M-algorithm) 기반 convolutional code 복호로 min-sum 반복 message-passing과 다른 패러다임, binary QC-LDPC 블록 디코더에 이식 불가",
  "todo_check": "없음 (패러다임 불일치로 이식 대상 아님)"
}
```
