### arxiv:1403.0804v1 - Double Cylinder Cycle codes of Arbitrary Girth (2014, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 1/10~1/5 |
| 부호length | 450~3500 |
| 연판정 | 무관 |
| 핵심기여 | column-weight 2인 cycle LDPC의 mother matrix H(a,b,c)와 block-structure graph(BSG)로 최대 achievable girth를 이론적으로 결정 |
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
| 한계,주의 | column-weight 2 cycle code는 rate가 매우 낮고(1/10~1/5) 최소거리가 로그 증가에 그쳐 NAND ECC급 고rate와 무관 |
| 추가확인 | 없음 |

> 총평: column-weight 2 cycle LDPC의 girth 최대화 구성법·이론 논문으로, 저rate·순수 그래프이론 결과라 고rate binary QC-LDPC(NAND) 이식 가치 없음.

### B. 알고리즘 요약

1. 대상은 column-weight 2인 cycle LDPC 코드(QC-LDPC의 특수 클래스)로, 각 열에 비영 원소가 정확히 2개.
2. 기존 Gholami-Esmaeili의 cylinder-type BC-LDPC 코드보다 동일 girth에서 더 높은 rate를 갖는 mother matrix를 구성하는 것이 목표.
3. block-structure graph(BSG(H))라는 새 그래프 표현을 도입해 mother matrix H의 순환치환 블록 간 관계를 방향성 라벨 간선으로 표현.
4. `(a,b,c)-double-cylinder LDPC (DC-LDPC)` 코드의 mother matrix `H(a,b,c)`를 정의, design rate는 `R = 1/(a+c)`.
5. `gmax`(최대 achievable girth)는 `b ≥ ⌈(a-1)/(c+1)⌉+2`일 때 `8(a+c)`, 아니면 `4(bc+b+a-1)`로 정리(Theorem 2.5).
6. 증명은 BSG(H) 상에서 폐쇄보행(closed walk) 체인 `P1P2P3P2⁻¹P1⁻¹P2P3⁻¹P2⁻¹`의 길이를 계산해 girth 상한을 도출.
7. 여러 (a,b,c) 조합에 대한 최대 girth 표(Figure 2)를 제공, 실제 mother matrix로부터 shift sequence를 찾아 특정 girth·length의 DC-LDPC 코드 예시 표(Table 1)를 제시.
8. 최적화/학습 절차 없음, 순수 조합론적 구성.
9. 결과는 rate 1/10~1/5, length 450~3500대의 다양한 girth(20~75) 코드 예시로, 기존 구성 대비 girth per rate가 개선됨을 표로 제시.
10. 한계: HW 설계 없음, 시뮬레이션/BER 성능 검증 없음(순수 girth 이론), column-weight 2 cycle code 자체가 저rate·성능 제약 큰 클래스.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Column-weight 2 cycle LDPC mother matrix 구성 | 대응 없음 | Prime ECC는 고rate(~0.9) QC-LDPC(VN degree 17)로 column-weight 2 cycle code와 구조·rate가 전혀 다름 |
| BSG(H) girth 최대화 이론 | `ecc_top.cpp` `Load_PCM()` | H-matrix 설계 단계에 이론적으로 참고 가능하나 low-rate 특화라 실질 적용성 낮음 |

적용 가치: **낮음** — 저rate column-weight 2 cycle code의 girth 이론으로, Prime ECC의 고rate QC-LDPC 부호설계와 rate·구조가 근본적으로 달라 이식 실익 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1403.0804v1",
  "title": "Double Cylinder Cycle codes of Arbitrary Girth",
  "year": 2014,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": "1/10~1/5",
  "code_length": "450~3500",
  "soft_quant": "무관",
  "key_contribution": "column-weight 2인 cycle LDPC의 mother matrix H(a,b,c)와 block-structure graph(BSG)로 최대 achievable girth를 이론적으로 결정",
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
  "caveat": "column-weight 2 cycle code는 rate가 매우 낮고(1/10~1/5) 최소거리가 로그 증가에 그쳐 NAND ECC급 고rate와 무관",
  "todo_check": "없음"
}
```
