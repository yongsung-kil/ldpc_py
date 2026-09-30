### arxiv:1504.06416v1 - On the Minimum Distance of Array-Based Spatially-Coupled Low-Density Parity-Check Codes (2015, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | array-based SC-LDPC 코드의 최적 minimum distance에 대한 q-무관 상한을 m=3,4,5에 대해 증명하고 cutting vector exhaustive search로 실제 값을 표로 제시 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 조합론적 minimum distance 분석이며 저자 스스로 반복복호 성능은 absorbing set이 지배적이라 명시, ML복호 맥락에서만 의미 있다고 함 |
| 추가확인 | 해당 없음 |

> 총평: array LDPC의 순수 이론적 최소거리 상한/exhaustive search 논문으로 디코더·HW·NAND 이식 요소 전무.

### B. 알고리즘 요약

1. 대상 코드: array LDPC C(q,m) — q는 홀수 소수, m≤q, quasi-cyclic 구조(식 (1)), 각 열은 (x, x+y, ..., x+(m-1)y) mod q 형태(식 (3)).
2. 문제의식: 반복복호 성능은 absorbing set이 지배하지만, ML복호 관점에서는 minimum distance가 중요 성능지표가 되므로 array-based SC-LDPC의 최적 minimum distance 특성을 규명하고자 함.
3. 채널/모델 가정 없음 — 순수 조합론(코드 구조) 분석, 확률적 채널 모델 미사용.
4. 핵심 기법: cutting vector ζ=(ζ0,...,ζm-1)로 H(q,m)을 H0, H1로 분할해 spatially-coupled parity-check matrix H(q,m,L,ζ)를 구성(식 (4)).
5. 핵심 식: `dopt(q,m) = lim_{L→∞} max_ζ d(q,m,L,ζ)` — 최적 minimum distance를 coupling length 무한대에서 모든 cutting vector에 대한 최대값으로 정의.
6. Template support matrix와 column group index 시퀀스의 range 개념을 도입해 특정 weight의 codeword가 모든 q≥q0에서 존재함을 증명(Lemma 1–3, Theorem 1–4).
7. 부수 트릭: template support matrix는 [10]의 알고리즘으로 탐색해 발견, 증명은 codeword를 cyclic shift하여 column section 내로 이동시키는 논증 사용.
8. 최적화 절차: 작은 q(m=3,4,5)에 대해 모든 cutting vector에 대한 exhaustive search 수행(Proposition 1로 탐색공간 축소).
9. 결과: m=3, q≥13에서 dopt=6; m=4, q≥31에서 dopt=10; m=5, q≥59에서 dopt=12. q=53에서 특정 cutting vector로 dmin=14까지 증가 확인(Table III).
10. 한계: 반복복호(BP) 성능과 무관한 순수 조합론적 지표, HW/디코더 설계 없음, m=5의 일반 상한 증명은 미완(q>79는 10 또는 12로 추정만).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| array-based SC-LDPC 부호 구성/minimum distance 이론 | 대응 없음 | Prime ECC는 특정 QC-LDPC H-matrix 고정 사용, array code 구성법이나 SC-LDPC 구조 자체를 다루지 않음 |
| cutting vector 최적화 | 대응 없음 | 부호 구성 단계 이론이며 디코더/인코더 구현과 무관 |

> 적용 가치: 낮음 — 순수 이론적 minimum distance 분석으로 디코더/HW/NAND 실무 요소가 전무하며 Prime ECC의 어떤 모듈과도 직접 대응되지 않음.

### D. JSON 블록

```json
{
  "id": "arxiv:1504.06416v1",
  "title": "On the Minimum Distance of Array-Based Spatially-Coupled Low-Density Parity-Check Codes",
  "year": 2015,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "array-based SC-LDPC 코드의 최적 minimum distance에 대한 q-무관 상한을 m=3,4,5에 대해 증명하고 cutting vector exhaustive search로 실제 값을 표로 제시",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 조합론적 minimum distance 분석이며 저자 스스로 반복복호 성능은 absorbing set이 지배적이라 명시, ML복호 맥락에서만 의미 있다고 함",
  "todo_check": "해당 없음"
}
```
