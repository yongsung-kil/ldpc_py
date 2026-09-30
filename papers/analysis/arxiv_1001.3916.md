### arxiv:1001.3916v1 - Girth-12 Quasi-Cyclic LDPC Codes with Consecutive Lengths (2010, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5 |
| 부호length | 2358~3000+ |
| 연판정 | 무관 |
| 핵심기여 | 한 girth-12 (3,L) 코드에서 연속 길이(LP)의 girth-12 QC-LDPC 코드군을 유도하는 구성 정리 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 저rate(0.5) column-weight-3 (3,6) 코드 전용, NAND 고rate ECC와 스펙 불일치, HW 미설계 |
| 추가확인 | 확장(다른 P) 시 dmin(=24) 보존 여부는 미해결(open problem) |

> 총평: girth-12 (3,6) QC-LDPC 연속 길이 구성의 순수 이론 논문으로, Prime ECC의 고rate binary QC-LDPC와 rate/구조가 맞지 않아 이식 가치 낮음.

### B. 알고리즘 요약

1. 대상: circulant permutation matrix 기반 `(3,L)` QC-LDPC 코드, exponent matrix `E`(3행×L열, 1행 전부 0)로 표현, 길이 `N = XL`.
2. 문제: 기존 girth-12 구성(Tanner (3,5), O'Sullivan)은 지원 가능한 코드 길이가 제한적 — 임의 연속 길이의 girth-12 코드를 얻고 싶다.
3. 핵심 결과(Theorem 1): 어떤 `HQ`가 girth-12이고 `p1,v < p2,v`(Cond.2), `p2,x - p2,y ≠ p1,x`(Cond.3)를 만족하면, `P ≥ 2·p2,x + 1`인 모든 정수 P에 대해 `HP`도 girth-12.
4. 증명: 길이 4/6/8/10 cycle이 `HP`에 존재한다고 가정하면 그 방정식이 `mod Q`에서도 성립 → `HQ`의 girth-12에 모순. 4가지 case(A~D)로 완결.
5. 하한의 타이트함: `i=k=0, j=l=x`로 두면 `2·p2,x`에서 8-cycle이 생김 → `2·p2,x`가 girth-12 보장 임계 하한임을 보임.
6. 예시: greedy + simulated annealing으로 row-weight-6 exponent matrix `E`(원소 max = 224) 발견. `P=393`이면 (3,6) girth-12, 길이 2358. Theorem 1로 `N=6P (P≥448)` 임의 길이 구성 가능.
7. 최단 길이: 기존 최단 O'Sullivan 2874 대비, 본 코드군은 2688 이상 연속 길이 → 더 짧은 30개 member code 포함.
8. 성능: `P=449, 500` (rate 0.5) 코드를 PEG-LDPC와 sum-product(최대 80 iter) 비교 — 첫 코드 BER=1e-5에서 0.1dB 미만 열화, 둘째는 열화 없음.
9. 최소거리: girth-12 (3,L) 코드는 `dmin ≥ 14` 보장, 개선 impulse method로 `P=393, 500` 모두 `dmin = 24`(3,L에서 최대치) 확인.
10. 한계: rate 0.5 (3,6) 코드에 국한, HW 미설계, 확장 시 dmin 보존 여부 open problem.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| girth-12 (3,L) QC-LDPC exponent matrix 구성 | ecc_top.cpp `Load_PCM()` (H-matrix 로드) | 구성법 자체가 다른 rate/degree 대상이라 직접 적용 불가 |
| circulant permutation 기반 PCM 표현 | ecc_data.h `PCM_b` (base+shift) | 표현 형식은 동일하나 우리는 고rate·고degree 고정 |
| sum-product 복호 성능 비교 | 대응 없음 (Prime ECC는 min-sum) | 논문은 SPA 시뮬, 디코더 기여 없음 |

마지막 적용 가치: **낮음** — 저rate(0.5) column-weight-3 girth-12 구성 이론으로, Prime ECC의 고rate·고degree binary QC-LDPC 스펙과 맞지 않고 디코더/HW 기여가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1001.3916v1",
  "title": "Girth-12 Quasi-Cyclic LDPC Codes with Consecutive Lengths",
  "year": 2010,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": 0.5,
  "code_length": "2358~3000+",
  "soft_quant": "무관",
  "key_contribution": "한 girth-12 (3,L) 코드에서 연속 길이의 girth-12 QC-LDPC 코드군을 유도하는 구성 정리",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "저rate(0.5) column-weight-3 (3,6) 코드 전용, NAND 고rate ECC와 스펙 불일치, HW 미설계",
  "todo_check": "확장(다른 P) 시 dmin(=24) 보존 여부는 미해결(open problem)"
}
```
