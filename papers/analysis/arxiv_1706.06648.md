### arxiv:1706.06648v1 - Pseudocodeword-Free Criterion for Codes with Cycle-Free Tanner Graph (2017, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | cycle-free 표현이 가능한 부호에서 geometrically perfect(=pseudocodeword-free) parity-check matrix를 완전 특성화 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | cycle-free Tanner graph를 허용하는 부호(=정정능력 제한적, [3]) 전용 이론으로 실전 고rate LDPC와 무관 |
| 추가확인 | 없음 (순수 조합론/그래프 이론 결과) |

> 총평: cycle-free 표현 가능한 특수 부호류에 대한 pseudocodeword 구조의 순수 이론 특성화로, NAND용 실전 QC-LDPC 이식 가치 없음.

### B. 알고리즘 요약

1. 대상은 **binary linear code**를 parity-check matrix `H`로 표현하고, 그 Tanner graph `T(H)`상의 message-passing / LP 디코딩을 다룬다.
2. 풀려는 문제: cycle이 LDPC 성능 저하의 주범으로 여겨지나, cycle-free 표현이 가능한 부호에서는 cycle이 redundant row에만 있으면 성능에 무해함을 규명.
3. 핵심 개념은 graph cover에서 나오는 **pseudocodeword** `PC(H)` 와, 그 집합이 codeword의 비음 정수결합과 정확히 일치할 때의 **geometrically perfect** 성질.
4. `PC(H)`는 fundamental cone `K(H)`와 `Hp^T = 0 (mod 2)` 조건으로 특성화된다 (Koetter et al. Thm 2.8 인용).
5. 저자는 이를 국소화한 **p-satisfy** 개념(Def 3.1: 비음/짝수합/한 원소가 나머지 합 이하)을 도입해 Tanner graph만으로 pseudocodeword를 판정 가능하게 함 (Prop 3.2).
6. 핵심 정리 Theorem 3.5: cycle-free 표현을 갖는 부호 `C`에서, `H`가 geometrically perfect ⟺ redundant row들을 제거해 cycle-free 표현을 얻을 수 있다.
7. 증명은 tree인 `T(H')`에서 pivotal row를 찾아 값 `2d`/`2` 할당으로 반례 pseudocodeword를 구성 (Lemma 3.3, Prop 3.4의 row weight 부등식 활용).
8. 학습/최적화 절차 없음 (조합론적 증명).
9. 결과: 두 예제(Example 4.1, 4.2)로 정리 예시. 특히 small cycle이 있어도 tree 부분그래프가 지배하면 geometrically perfect일 수 있음을 보임.
10. 한계: cycle-free 표현 가능 부호(정정능력 본질적으로 제한적)에만 적용, HW·시뮬·수치성능 전무.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| pseudocodeword / geometrically perfect 이론 | 대응 없음 | cycle-free 부호 전용 순수 이론, 우리 고rate QC-LDPC와 무관 |
| parity-check matrix 표현/redundant row | ecc_top.cpp Load_PCM() | H-matrix 로드 지점이나, 본 이론은 cycle-free 부호에만 성립 |
| LP/iterative 디코딩 수렴 논의 | decoder.cpp LDPC_Decoder() | 개념적 배경일 뿐 min-sum 이터레이션 개선 기여 없음 |
```

마지막에 한 문장으로 **적용 가치**: `낮음` — cycle-free Tanner graph를 허용하는 제한적 부호류 전용 이론이라 error-floor가 실전 이슈인 고rate QC-LDPC(cycle 불가피)에 이식할 수 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1706.06648v1",
  "title": "Pseudocodeword-Free Criterion for Codes with Cycle-Free Tanner Graph",
  "year": 2017,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": null,
  "code_length": null,
  "soft_quant": "무관",
  "key_contribution": "cycle-free 표현이 가능한 부호에서 geometrically perfect(pseudocodeword-free) parity-check matrix를 완전 특성화 (Theorem 3.5)",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "cycle-free Tanner graph를 허용하는 부호(정정능력 제한적)에만 성립, 실전 고rate LDPC와 무관",
  "todo_check": "없음 (순수 조합론/그래프 이론 결과)"
}
```
