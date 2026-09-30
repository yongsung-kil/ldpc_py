### arxiv:1008.4177v2 - LDPC Codes from Latin Squares Free of Small Trapping Sets (2010, IEEE Trans. Information Theory (submitted))

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.7~0.8 |
| 부호length | 155~4381 |
| 연판정 | 무관 |
| 핵심기여 | Latin square 기반 순열행렬 구조 부호 + Trapping Set Ontology로 유해 trapping set을 배제해 error-floor 낮춤 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | column-weight-3 고정 저rate 부호 + BSC/Gallager A-B 기준 TSO라 NAND 고rate QC-LDPC(z=32, wt17)와 구조 불일치 |
| 추가확인 | 우리 고rate QC-LDPC의 절대적 harmful trapping set/absorbing set 목록에 동일한 forbidden-subgraph 배제법 적용 가능 여부 |

> 총평: error-floor 저감을 위한 trapping-set-free 부호구성 이론은 개념적으로 가치 있으나, wt-3 저rate·비QC 구조라 우리 고rate QC-LDPC에 직접 이식은 어려움.

### B. 알고리즘 요약

1. GF(q)의 덧셈군 Cayley table로 정의한 Latin square에서 순열행렬 집합 `M`을 만들고, 이 순열행렬들이 행렬연산 하에서 GF(q)와 동형인 체를 이룸을 보임 (`f: Q → 순열행렬`).
2. 문제: 유한길이 고rate 부호에서 girth만 키워서는 error-floor를 지배하는 유해 trapping set을 제거 못함 (rate penalty 큼).
3. 채널/디코더 모델: BSC + Gallager A/B (부분적으로 fixed set으로 조합적 특성화), 그리고 SPA. all-zero codeword 대칭성 가정.
4. 핵심기법1: parity check matrix `H=f(W)`가 4-cycle이 없을 필요충분조건 = cross-addition constraint `w_i1,j1 + w_i2,j2 = w_i1,j2 + w_i2,j1` (girth ≥ 6 보장).
5. 이 식은 순열행렬 곱이 다시 `M`의 원소가 되므로, 두 행이 2개 이상 공통 1을 갖는 조건을 대수적 등식으로 환원 (RC constraint 자동화).
6. 핵심기법2: Trapping Set Ontology(TSO) - Gallager A/B용 fixed set(trapping set) DB + 부모/자식(successor) 위상관계로 유해도 순위화.
7. 구현 디테일: PEG류 progressive check-and-select 알고리즘(Algorithm 1)으로 지정 collection의 forbidden subgraph를 회피하며 Tanner graph 축조.
8. 유해도 결정: (4,4) trapping set을 successor 생성 여부로 분할해 각각 SPA 복호 성공률 `χ_i(ε)` 비교 → (6,2){1},(5,3){2},(8,2) 등이 유해함을 실험적으로 판정.
9. 결과: C1(155,64) 3-error 정정, C5(3165,2554,R=0.8), C6/C7 등 girth-8 wt-3 부호가 PEG·array-masking QC·lattice 부호보다 error-floor 낮음(BSC·AWGNC 모두).
10. 한계: HW 미설계, 순수 시뮬(FER)만, wt-3 저rate·BSC 최적화 고정, non-QC 순열구조라 고rate NAND QC-LDPC와 직접 정합 안 됨.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Latin square 순열행렬 부호 구성 / H-matrix | ecc_top.cpp `Load_PCM()` | 부호구조 로드에 대응하나 우리는 QC circulant 고정, non-QC 구조 도입은 재검증 부담 큼 |
| trapping-set-free 부호로 error-floor 개선 | 대응 없음 | 우리 부호는 특정 QC-LDPC 고정, forbidden-subgraph 최적화 파이프라인 부재 |
| SPA 복호 성공률 기반 유해도 분석 | decoder.cpp `LDPC_Decoder()` | 개념적 참고(우리는 min-sum 근사이므로 SPA 결과 직접 이식 불가) |
| progressive Tanner graph 축조(Algorithm 1) | 대응 없음 | 코드 생성 툴 부재(코드베이스는 고정 H-matrix 시뮬레이터) |

적용 가치: **낮음** — error-floor 저감 이론은 유익하나 wt-3 저rate·non-QC·BSC 최적화라 고rate binary QC-LDPC(z=32) 코드베이스에 직접 떼어 쓰기 어렵고, 우리 특정 부호에 대한 재검증 부담이 큼.

### D. JSON 블록

```json
{
  "id": "arxiv:1008.4177v2",
  "title": "LDPC Codes from Latin Squares Free of Small Trapping Sets",
  "year": 2010,
  "venue": "IEEE Trans. Information Theory (submitted)",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "기타",
  "code_rate": "0.7~0.8",
  "code_length": "155~4381",
  "soft_quant": "무관",
  "key_contribution": "Latin square 기반 순열행렬 구조 부호 + Trapping Set Ontology로 유해 trapping set 배제해 error-floor 낮춤",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "column-weight-3 고정 저rate 비QC 부호 + BSC/Gallager A-B 기준 TSO라 NAND 고rate QC-LDPC(z=32)와 구조 불일치",
  "todo_check": "우리 고rate QC-LDPC의 harmful trapping/absorbing set에 동일 forbidden-subgraph 배제법 적용 가능 여부"
}
```
