### arxiv:1403.4405v1 - Absorbing Set Analysis and Design of LDPC Codes from Transversal Designs over the AWGN Channel (2014, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.76~0.92 |
| 부호length | 841~2209 |
| 연판정 | 무관 |
| 핵심기여 | Transversal design(cyclic MOLS 기반) QC-LDPC 부호의 absorbing set을 조합론적으로 완전분류하고, scale factor/Galois field 선택으로 소형 harmful absorbing set을 제거해 error-floor를 낮추는 부호설계법 |
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
| 한계,주의 | 특정 대수구조(cyclic MOLS/transversal design)에 종속된 H-matrix 구성법으로 기존 QC-LDPC(base matrix+circulant shift)에 그대로 이식 불가, 재설계 부담 큼 |
| 추가확인 | column weight 3/4(및 5) 예시뿐이므로 Prime ECC의 실제 VN degree(17, HCU 비대칭 구조)에 이 absorbing-set 제거 전략이 확장 가능한지 |

> 총평: absorbing-set 기반 error-floor 최적화 부호 구성법으로 정정능력 개선 근거(시뮬레이션)는 있으나, 특정 대수 구조 종속이라 기존 고정 QC-LDPC 부호에 이식하기는 어려움.

### B. 알고리즘 요약

1. 대상은 cyclic-structured MOLS(mutually orthogonal Latin squares)로부터 구성한 quasi-cyclic transversal design(TD) LDPC 부호, column weight `k=3,4(,5)`, block length `N=q^2`, rate `R ≥ (q-k+2)/q` (AWGN, SPA 디코딩).
2. 문제의식: AWGN 채널 SPA 디코딩에서 error-floor의 주원인인 absorbing set(특히 fully/elementary absorbing set)을 제거해 error-floor 성능을 개선하려는 것.
3. 채널/디코더 모델: 표준 AWGN + standard sum-product algorithm(SPA), 최대 2000(분류 시뮬) 또는 50 iteration(성능 비교).
4. 핵심 기법 1단: `(a,b)` absorbing set을 조합론적 "absorbing set candidate"(set system + t-colouring)로 정의하고, 열거 알고리즘(`Classification(k,t)`)으로 column weight 3, 4에서 발생 가능한 모든 소형 후보를 완전 열거.
5. 핵심 식: absorbing set 발생 조건을 Galois field `F_q` 위의 선형방정식계 `Ep=0`(scale factor `α_i` 종속)로 표현(Theorem 6) → symbolic Gaussian elimination으로 특정 `(α_i, F_q)` 선택 시 방정식계가 해를 갖지 못하게 만들어 absorbing set을 원천 배제.
6. 확장 기법: elimination constraint(`C1~C28`, 예: `ωq=2`, `α1+α2=0` 등)를 도출해, 이를 만족하는 scale factor 조합을 선택하면 특정 크기의 (fully) absorbing set이 코드에서 원천적으로 발생하지 않음을 증명.
7. 부수 트릭: MOLS를 reduced form(`β_i=1`)으로 정규화해 탐색공간을 축소하고, 서로 다른 scale factor 집합이 동일 부호로 귀결되는 동치관계(Theorem 5)로 중복 탐색 제거.
8. 최적화 절차: 별도 학습 없이 조합론적 완전탐색 + symbolic elimination(트리 기반 case analysis)으로 최적 scale factor·Galois field 선택을 결정론적으로 도출.
9. 결과: `[841,0.76]`, `[1681,0.9]`, `[2209,0.92]` 등 부호에서 good/bad scale factor 선택 간 BER 수 자릿수 차이(10^-4~10^-9 영역까지 waterfall 유지) 관찰, PEG/Zhang/Vasic 구성법 대비 우수한 error-floor.
10. 한계: 순수 알고리즘/시뮬레이션 수준(HW 미설계), 특정 대수구조(cyclic MOLS)에 종속된 H-matrix 구성이라 임의의 고정 QC-LDPC 부호에는 이 방법론을 직접 적용할 수 없음.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| absorbing set 제거를 통한 error-floor 최적화 부호 구성 | `ecc_top.cpp` `Load_PCM()` | H-matrix 자체를 재설계하는 방법론이나 Prime ECC의 QC-LDPC(base+circulant)는 이 MOLS 기반 구성과 상이해 재검증 부담 큼 |
| SPA(standard sum-product) 디코딩 | 대응 없음 | Prime ECC는 min-sum 기반이라 tanh 기반 SPA와 직접 대응 없음 |
```

적용 가치: `낮음` — error-floor 개선이라는 목표는 Prime ECC 관심사와 일치하나, 특정 대수구조(MOLS/transversal design) 종속 H-matrix 구성법이라 기존 고정 QC-LDPC 코드베이스에 이식하려면 부호 자체를 재설계해야 함(§4 "부호설계" 난이도 `높음`에 해당).

### D. JSON 블록

```json
{
  "id": "arxiv:1403.4405v1",
  "title": "Absorbing Set Analysis and Design of LDPC Codes from Transversal Designs over the AWGN Channel",
  "year": 2014,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": "0.76~0.92",
  "code_length": "841~2209",
  "soft_quant": "무관",
  "key_contribution": "Transversal design(cyclic MOLS 기반) QC-LDPC 부호의 absorbing set을 조합론적으로 완전분류하고, scale factor/Galois field 선택으로 소형 harmful absorbing set을 제거해 error-floor를 낮추는 부호설계법",
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
  "caveat": "특정 대수구조(cyclic MOLS/transversal design)에 종속된 H-matrix 구성법으로 기존 QC-LDPC(base matrix+circulant shift)에 그대로 이식 불가, 재설계 부담 큼",
  "todo_check": "column weight 3/4(및 5) 예시뿐이므로 Prime ECC의 실제 VN degree(17, HCU 비대칭 구조)에 이 absorbing-set 제거 전략이 확장 가능한지"
}
```
