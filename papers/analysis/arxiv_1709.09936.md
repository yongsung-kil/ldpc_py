### arxiv:1709.09936v1 - A Branch-and-Cut Algorithm to Design LDPC Codes without Small Cycles in Communication Systems (2017, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 20~1000 |
| 연판정 | 무관 |
| 핵심기여 | girth 목표를 만족하는 (J,K)-regular LDPC H-matrix 생성을 정수계획(MIP)+branch-and-cut으로 정식화, 최적성 보장 |
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
| 한계,주의 | BSC 가정, offline 부호설계 최적화만 - BER·디코더·HW 검증 전무, (3,6) n≤1000 소규모 실험 |
| 추가확인 | 없음 (QC-LDPC 아닌 일반 (J,K)-regular, NAND 고rate와 무관) |

> 총평: small cycle 없는 LDPC H-matrix 생성을 MIP branch-and-cut으로 최적 해결하는 부호설계 최적화 논문으로, BSC·저rate·offline 설정이라 NAND 고rate QC-LDPC 디코더/HW에 이식 가치는 낮음.

### B. 알고리즘 요약

1. 대상은 채널 BSC(flip 확률 `p`)에서 쓰는 일반 (J,K)-regular / irregular binary LDPC 부호(`H` 크기 `m×n`, `m=n-k`), 예제는 (3,6)-regular, `n=20~1000`, rate 0.5.
2. 풀려는 문제: Tanner graph의 small cycle이 정정능력을 해치므로 목표 girth `T` 이상을 보장하는 `H`를 heuristic(PEG 등)이 아닌 **최적성 보장** 방식으로 구성.
3. 핵심 모델: `Xij`(H 원소)를 이진 결정변수로 하는 정수계획 GFM/MDD — girth 위배 cycle마다 `sum Xij ≤ |C|-1` 제약(식(4)), MDD는 목표 차수 편차 최소화.
4. 핵심 기법: cycle 제약이 지수개이므로 cutting-plane으로 추가하는 **branch-and-cut** (Alg.1); 정수해 분리는 DFS로 cycle 탐색(Alg.2), 분수해 분리는 undirected Bellman-Ford 음-cycle 검출(Alg.3).
5. 핵심 식: 분수해에서 mean-cost cycle `sum Xij/|C|`를 `-Xij-μ` 비용으로 반복 갱신하며 최소 mean-cost cycle을 찾아 위배 cut 생성.
6. 개선 1: 대칭성(=`(n!)(m!)`개 동형해) 제거를 위한 변수 고정(Alg.4, basic/extended), extended 고정이 cycle을 만들지 않음을 증명(Prop.4).
7. 개선 2: cycle-region(ρ(i,j))에 근거한 valid inequality(Prop.5)와 `n` 하한(Prop.3: T=8이면 n≥70 등) 유도.
8. 개선 3: PEG를 변수고정 초기해에서 시작하도록 수정해 초기 upper bound 제공(Alg.6, `O(|V||E|+|E|^2)`).
9. 결과(수치): CPLEX 12.6.2로 (3,6) 27 인스턴스 중 BC4가 19개 최적해, 13개는 해당 (J,K) 부호 부재 증명; PEG 대비 17개 개선. BER·성능곡선 없음.
10. 한계: BSC 가정, offline 부호설계 최적화만 다루며 디코더·gate count·throughput·HW 및 정정능력 실측 전무.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| girth 목표 H-matrix 생성(MIP) | ecc_top.cpp Load_PCM() | H-matrix 로드 지점이나 우리 부호는 QC-LDPC 고정, 재구성·재검증 부담 큼 |
| small cycle 제거(부호설계) | 대응 없음 | offline MIP 부호설계 이론, 디코더/HW 알고리즘에 닿지 않음 |
| PEG 초기해/차수분포 | 대응 없음 | 일반 (J,K)-regular 대상, 우리 base+shift QC 구조와 상이 |
```

마지막에 한 문장으로 **적용 가치**: `낮음` — 일반 (J,K)-regular LDPC를 BSC·offline 설정에서 MIP로 설계하는 부호설계 최적화라, 이미 특정 고rate QC-LDPC를 고정한 Prime ECC의 디코더/HW/복호성능 개선에 직접 이식할 수 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1709.09936v1",
  "title": "A Branch-and-Cut Algorithm to Design LDPC Codes without Small Cycles in Communication Systems",
  "year": 2017,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": "20~1000",
  "soft_quant": "무관",
  "key_contribution": "girth 목표를 만족하는 (J,K)-regular LDPC H-matrix 생성을 정수계획(MIP)+branch-and-cut으로 정식화, 최적성 보장",
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
  "caveat": "BSC 가정, offline 부호설계 최적화만 - BER·디코더·HW 검증 전무, (3,6) n<=1000 소규모 실험",
  "todo_check": "없음 (QC-LDPC 아닌 일반 (J,K)-regular, NAND 고rate와 무관)"
}
```
