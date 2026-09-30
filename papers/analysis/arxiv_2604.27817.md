### arxiv:2604.27817v1 - High-Girth Regular Quantum LDPC Codes from Square-Base Hypergraph Products via CPM Lifts (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 0(design rate, 실제rate는 매우 낮음 예: 62/28800≈0.0022) |
| 부호length | 98~28800 |
| 연판정 | 무관 |
| 핵심기여 | 정방행렬 base matrix 기반 CSS hypergraph-product 양자 LDPC 코드에서 regularity/rank deficiency/short-cycle 배제 조건을 이론적으로 규명하고, CPM lift로도 제거 불가능한 orthogonality-forced Tanner 8-cycle 존재를 증명 |
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
| 추천도 | 하 |
| 한계,주의 | CSS(양자 안정자) 코드 전용 구성법으로 X/Z 두 parity check matrix의 직교성(commutation) 제약이 핵심이며, 이는 classical binary LDPC에 대응 개념이 없음. 설계 quantum rate가 0(rank deficiency로만 rate 확보)이라 NAND ECC의 고rate 요구와도 맞지 않음 |
| 추가확인 | girth-8 배제를 위한 row/column overlap≤1 및 6-cycle 배제 조건(Lemma 3), CPM lift의 voltage-sum 기반 short-cycle 제어 기법 자체는 classical QC-LDPC protograph 설계에서도 일반적으로 쓰이는 기법인지 대조 필요 |

> 총평: 양자 CSS 코드의 hypergraph-product 구성에서 rank deficiency와 girth 조건을 정교하게 분석한 이론 논문으로, 부호설계가 X/Z 직교성이라는 양자 특유 제약에 근본적으로 묶여 있어 NAND classical binary QC-LDPC 이식 관점의 적용 가치는 낮음.

### B. 알고리즘 요약

1. 대상은 CSS(Calderbank-Shor-Steane) hypergraph-product(HGP) 양자 LDPC 코드로, 정방 이진 base matrix `B (s×s)`로부터 `H_X = [B⊗I_s | I_s⊗B^T]`, `H_Z = [I_s⊗B | B^T⊗I_s]` 두 parity check matrix를 구성하며 이들은 항상 `H_X H_Z^T=0`(직교) 성질을 만족한다.
2. 풀려는 문제: quantum LDPC는 X/Z check matrix가 서로 commute해야 하는 제약 때문에 classical irregular LDPC처럼 degree distribution을 자유롭게 최적화할 수 없고, regular/high-girth 유한장 코드 설계 조건이 명확히 규명되지 않았었다.
3. 핵심 모델: base matrix `B`의 rank 결핍(`corank c_B = s - rank(B)`)이 논리 큐빗 수 `k=2c_B^2`를 결정하며, 설계 quantum rate `R_des=0`(전부 rank deficiency로만 rate 확보).
4. 핵심 정리(Theorem 2): `B`가 정방 `w`-regular이면 HGP 코드는 `(d_v,d_c)=(w,2w)`-regular이 되고, CPM lift도 이 degree를 보존한다.
5. 핵심 식의 의미: `Lemma 3`은 `B`의 Tanner graph에 4-cycle/6-cycle이 없으면 HGP 코드에도 없음을 보장하는 충분조건(행/열 쌍이 공통 1을 최대 1개만 공유)이며, `Theorem 5/Corollary 6`은 CSS 직교성 제약이 오히려 `N_8(B)=s^2·C(w,2)^2`개의 Tanner 8-cycle을 모든 CPM lift에서 강제로 남긴다는 것을 증명(즉 CPM lift로는 girth 10 이상 불가능).
6. 확장(Theorem 7): lift 크기 `P`를 키워도 `n=m_X+m_Z`인 square HGP에서는 lift 후 논리 큐빗 수가 base 코드의 `k` 이상으로 보장됨(`k̂≥k`).
7. 부수 트릭: 유한기하 incidence 구조(Fano plane, generalized quadrangle W(2)/W(3), projective plane PG(2,3))를 이용해 정규성·저rank·짧은사이클 배제를 동시에 만족하는 구체적 base matrix 예시 제작(랜덤 로컬서치 예시도 1개 포함).
8. 학습/최적화 절차: CPM lift의 shift 값은 CSS 직교성(선형 congruence)과 목표 short-cycle 배제(비선형 congruence) 제약을 만족하는 랜덤 kernel walk로 탐색(uniform sampler 아님).
9. 결과: [[28800,62]] girth-8 (3,6)-regular 코드가 depolarizing p=0.1402에서 2.993×10^8회 시행 중 실패 0회(Wilson 95% 상한 1.28×10^-8), degeneracy-aware BP + OSD-lite 후처리 사용.
10. 한계: 거리(distance) 인증 미완료(잔여 syndrome이 nonzero인 실패만 관측되어 최소거리 상한을 제공 못함), 설계 quantum rate가 0(실제 rate도 예시에서 0.002 수준으로 매우 낮음), HW 미설계·시뮬레이션뿐.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| HGP 기반 CSS 부호구조(H_X, H_Z 직교 구성) | 대응 없음 | quantum stabilizer code 전용 구성이며 Prime ECC는 단일 binary QC-LDPC PCM만 사용, X/Z 이중 check 직교성 개념 자체가 없음 |
| Tanner girth 확대를 위한 4-cycle/6-cycle 배제 조건 (Lemma 3) | `ecc_top.cpp` `Load_PCM()` | classical QC-LDPC의 short-cycle 배제 설계 원칙(행/열 쌍 공통 1 최대 1개)은 일반론적으로 유사하나, 본 논문은 CSS 직교성 제약 하의 특수 사례이며 H-matrix 설계는 Prime ECC에서 특정 QC-LDPC 고정이라 이식 난이도 높음 |
| CPM(circulant permutation matrix) lift, voltage-sum 기반 cycle 제어 | `ecc_top.cpp` `Load_PCM()` | Prime ECC도 QC-LDPC(base+circulant shift)이므로 CPM lift 개념 자체는 구조적으로 겹치나, 본 논문의 shift 설계는 CSS 직교 제약 해소가 목적이라 binary 단일 PCM에는 직접 적용할 필요가 없음 |

> 적용 가치: 낮음 — 논문의 핵심 기여(CSS 직교성 제약 하 rank deficiency 및 강제 8-cycle 분석)가 양자 안정자 코드 특유의 X/Z 이중 구조에 근본적으로 의존하며, classical binary NAND QC-LDPC는 단일 PCM 설계 문제라 해당 제약이 존재하지 않음.

### D. JSON 블록

```json
{
  "id": "arxiv:2604.27817v1",
  "title": "High-Girth Regular Quantum LDPC Codes from Square-Base Hypergraph Products via CPM Lifts",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": 0.0022,
  "code_length": "98~28800",
  "soft_quant": "무관",
  "key_contribution": "정방행렬 base matrix 기반 CSS hypergraph-product 양자 LDPC 코드에서 regularity/rank deficiency/short-cycle 배제 조건을 규명하고 CPM lift로도 제거 불가능한 orthogonality-forced Tanner 8-cycle 존재를 증명",
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
  "recommend": "하",
  "caveat": "CSS 양자 안정자 코드 전용 구성법으로 X/Z 두 parity check matrix 직교성 제약이 핵심이며 classical binary LDPC에는 대응 개념이 없고, 설계 quantum rate가 0으로 NAND ECC의 고rate 요구와도 부합하지 않음",
  "todo_check": "girth-8 배제 조건(Lemma 3) 및 CPM lift voltage-sum 기법이 classical QC-LDPC protograph 설계 기법과 어느 정도 중복되는지 대조 필요"
}
```
