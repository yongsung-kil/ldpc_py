### arxiv:2603.25824v1 - Exploiting the Degrees of Freedom: Multi-Dimensional Spatially-Coupled Codes Based on Gradient Descent (2026, arXiv (cs.IT), ISIT'24 확장판)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | SC-LDPC |
| 부호rate | 0.60~0.82 |
| 부호length | 3250~210250 |
| 연판정 | 무관 |
| 핵심기여 | MD-SC 코드의 relocation 확률분포를 gradient-descent로 최적화해 short cycle/6-6,6-8,8-8 concatenation(흡수집합 전구체)을 최소화 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | Prime ECC는 binary QC-LDPC(non-SC) 고정 H-matrix라 SC 특유의 partitioning/relocation/lifting 3단 구조 자체가 대응 불가 |
| 추가확인 | 부호설계(H-matrix) 재검증 부담이 크다는 프로파일 §4 판단과 일치하는지 재확인 필요 |

> 총평: SC/MD-SC 코드의 흡수집합 감소를 위한 확률적 FL 최적화 이론 논문으로 알고리즘적으로 정교하나 대상이 spatially-coupled 구조 전용이라 Prime ECC(고정 QC-LDPC, non-SC)에는 이식 난이도가 매우 높음.

### B. 알고리즘 요약

1. 시스템: circulant-based SC 코드(파라미터 γ,κ,z,L,m)를 M개 복사해 relocation으로 연결한 multi-dimensional SC(MD-SC) 코드, rate 0.60~0.82, length 3.25k~210k, AWGNC 채널 시뮬.
2. 문제: MD-SC 설계 자유도(m, M)가 커질수록 short cycle/absorbing set 최소화를 위한 조합 탐색공간이 지수적으로 커져 기존 방식으로 다루기 어려움.
3. 핵심 가정: base matrix `Hg`는 all-one, 채널은 AWGN, 검출대상은 cycle-6/8 및 그 concatenation(6-6, 6-8, 8-8)으로 흡수집합(absorbing/trapping set)의 전구체.
4. 핵심 기법 1단(MD-GRADE): 확률분포행렬 `P`(각 원소 `p_i,j`는 base matrix의 1이 i번째 component/j번째 auxiliary matrix에 배정될 확률)를 정의하고, 기대 cycle-6/8 개수 `N6(p_con)`, `N8(p_con)`를 `P`의 다항식(coupling polynomial `f(X,Y;P)`)으로 표현.
5. KKT 조건으로 국소최적 `P`의 해 형태를 유도(`f^3(X,Y)f^2(X^-1,Y^-1)` 계수 균등화 조건, 식 14/19)하고 gradient descent로 반복 갱신.
6. 확장(2단): 임의 서브그래프(object)의 characteristic polynomial 일반이론을 세우고, 특히 두 short cycle의 VN-CN-VN concatenation(6-6/6-8/8-8)까지 목적함수에 포함해 고립 cycle보다 실제 흡수집합에 가까운 구조를 직접 타깃.
7. 구현 디테일: 다차원 convolution을 FFT 기반으로 가속(O(N log N)), `force()` 함수로 매 반복 후 확률 벡터를 feasible set(행합=p*)에 재투영.
8. 최적화 절차: MD-GRADE(GD)로 얻은 국소최적 `P`를 초기값 삼아 Gibbs sampling 기반 MCMC(Metropolis-Hastings형) FL 최적화기로 실제 정수 relocation matrix `M`을 탐색.
9. 결과: MD Code 1은 문헌([31]) 대비 cycle-6 63% 감소(9,078→3,366), GD-GD 코드는 GD-UNF/UNF-UNF 대비 FER 최대 2.81 orders of magnitude 개선(오차마루 제거).
10. 한계: 인코더/디코더 HW 설계 없음(순수 이론+FL 최적화+AWGN 시뮬), SC 코드 특유의 3단(partitioning/lifting/relocation) 구조에 종속적이라 일반 QC-LDPC로 일반화 불명확.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 부호설계(MD-SC partitioning/relocation/lifting) | `ecc_top.cpp` `Load_PCM()` | 이식 난이도 높음(§4) - Prime ECC는 SC 구조 자체가 없는 고정 QC-LDPC라 대응 불가에 가까움 |
| 디코딩(sum-product, AWGNC) | `decoder.cpp` `LDPC_Decoder()` | Prime ECC는 min-sum 기반이라 sum-product 자체는 대응 없음, 이터레이션 루프만 형식적 유사 |
| HW/양자화/파이프라인 | (해당 없음) | 논문에 HW 설계·양자화 논의 전무 |

> 적용 가치: 낮음 - SC/MD-SC 코드 전용 부호설계 이론이며 Prime ECC는 non-SC 고정 QC-LDPC라 partitioning/relocation 개념 자체가 이식 불가에 가깝고, HW/디코더 개선도 다루지 않음.

### D. JSON 블록

```json
{
  "id": "arxiv:2603.25824v1",
  "title": "Exploiting the Degrees of Freedom: Multi-Dimensional Spatially-Coupled Codes Based on Gradient Descent",
  "year": 2026,
  "venue": "arXiv (cs.IT), ISIT'24 확장판",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "SC-LDPC",
  "code_rate": "0.60~0.82",
  "code_length": "3250~210250",
  "soft_quant": "무관",
  "key_contribution": "MD-SC 코드의 relocation 확률분포를 gradient-descent로 최적화해 short cycle/6-6,6-8,8-8 concatenation(흡수집합 전구체)을 최소화",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "Prime ECC는 binary QC-LDPC(non-SC) 고정 H-matrix라 SC 특유의 partitioning/relocation/lifting 3단 구조 자체가 대응 불가",
  "todo_check": "부호설계(H-matrix) 재검증 부담이 크다는 프로파일 §4 판단과 일치하는지 재확인 필요"
}
```
