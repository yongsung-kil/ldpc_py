### arxiv:1801.08811v1 - Constructing LDPC Codes from Partition and Latin-Style Splicing (2018, arXiv/IEEE Commun. Lett.-style)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 0.51~0.67 |
| 부호length | 2048~5184 |
| 연판정 | 무관 |
| 핵심기여 | 짧은 base PCM을 Latin square 기반 partition·splicing으로 결합해 girth 비감소(g(H)≥g(H0)) 보장하며 더 긴 QC-LDPC 생성 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | 순수 부호구성법(SPA 50-iter 시뮬만), HW·디코더 성능 분석 없음, 특정 H-matrix 고정된 Prime ECC엔 재검증 부담 큼 |
| 추가확인 | Prime ECC의 z=32·N_b=129 고rate 구조에 splicing 적용 시 rate/degree 분포 및 error-floor 실측 필요 |

> 총평: girth 보존형 QC-LDPC 확장 구성법으로 이론적 우아함은 있으나, 순수 code-design이고 고rate NAND 부호로의 직접 이식·재검증 부담이 커 참고 수준.

### B. 알고리즘 요약

1. 대상은 QC-LDPC(P×P circulant 배열, exponent matrix `E0`+CPM 크기 `P`), 짧은 base code로부터 더 긴 code 구성.
2. 문제: 짧은 code에서 girth를 유지하며 더 긴 code를 얻는 일반적 방법이 드물다(기존 [3][4][5]은 제약적).
3. 핵심: base PCM `H0`(m×n array)를 N개의 non-overlapping masking matrix `Mk`로 분할(합이 all-one), order N Latin square `A=[a_i,j]`로 재배열해 mPN×nPN PCM `H` 생성(Equ.1).
4. exponent 버전: `E = [E0 ⊗˜ M_{a_i,j}]`, 연산 `x⊗˜0=∞, x⊗˜1=x`로 정의(Equ.2).
5. Theorem 1: `g(H) ≥ g(H0)` — H의 임의 cycle이 H0의 동일 길이 cycle에 대응하므로 girth 비감소 보장(핵심 정리).
6. row/column weight 분포와 designed rate는 `H0`와 동일하게 보존됨.
7. 특수화: `A=[i−j mod N]`이면 spatially coupled LDPC의 base matrix로 환원(일반화 관계).
8. partition 옵션 3종: diagonal(D), triangle(T), Hamming-like(H) — H는 컬럼을 최대한 distinct하게.
9. 결과: GCD base(girth-8, 성능 나쁨)로부터 girth≥8 code 생성, PS-H code가 GCD·quad.-cong.·QC-PEG보다 우수(최소무게 codeword 소거로 error floor 완화), (2048,1046)·(5184,3484) 등, BI-AWGN+SPA 50-iter.
10. 한계: HW·디코더 latency·복잡도 분석 전무, non-binary/soft-read 고려 없음, 성능은 특정 예제 시뮬에 국한.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Latin-splicing 기반 H-matrix 구성 | ecc_top.cpp `Load_PCM()` | base PCM 확장으로 새 QC-LDPC 로드 가능하나 고정 구조 재검증 부담 |
| exponent matrix / QC 구조 | ecc_top.cpp `Load_PCM()` | E0→E 확장이 z=32·circulant 규격과 정합 필요 |
| girth/성능(error-floor) 개선 | 대응 없음 | 부호설계 단계 효과, 디코더 코드에 직접 대응 함수 없음 |

적용 가치: **낮음** — 순수 QC-LDPC 구성법이라 부호설계(`Load_PCM`) 레이어에만 닿고, Prime ECC의 고정 고rate H-matrix 교체·재검증 비용이 커 실이식 가치는 제한적.

### D. JSON

```json
{
  "id": "arxiv:1801.08811v1",
  "title": "Constructing LDPC Codes from Partition and Latin-Style Splicing",
  "year": 2018,
  "venue": "arXiv (cs.IT) / IEEE Commun. Lett.-style Letter",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": "0.51~0.67",
  "code_length": "2048~5184",
  "soft_quant": "무관",
  "key_contribution": "짧은 base PCM을 Latin square 기반 partition·splicing으로 결합해 girth 비감소(g(H)>=g(H0)) 보장하며 더 긴 QC-LDPC 생성",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "순수 부호구성법(SPA 50-iter 시뮬만), HW·디코더 성능 분석 없음, 고정 H-matrix 재검증 부담 큼",
  "todo_check": "Prime ECC의 z=32·N_b=129 고rate 구조에 splicing 적용 시 rate/degree 분포 및 error-floor 실측 필요"
}
```
