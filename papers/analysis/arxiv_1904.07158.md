### arxiv:1904.07158v1 - Efficient Search and Elimination of Harmful Objects in Optimized QC SC-LDPC Codes (2019, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | SC-LDPC |
| 부호rate | 0.51~0.71 |
| 부호length | 155~301 |
| 연판정 | 무관 |
| 핵심기여 | edge-spreading 트리탐색(MIHAO)으로 QC-SC-LDPC의 유해객체(AS/트래핑셋) 다중도 최소화 |
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
| 추천도 | 하 |
| 한계,주의 | SC-LDPC(convolutional) 구성 전용, sliding-window BP 가정 — 고정 binary block QC-LDPC(Prime ECC)와 구조 불일치 |
| 추가확인 | MIHAO를 block QC-LDPC의 lifting/shift 설계에 직접 적용 가능한지(SC 구조 제거 시) |

> 총평: QC-SC-LDPC의 error-floor 개선용 구성법으로 이론·시뮬만, block QC-LDPC 기반 Prime ECC에는 구조가 달라 직접 이식 곤란.

### B. 알고리즘 요약

1. 대상 코드: QC-LDPC block code(exponent matrix `P`, m×n circulant, lifting `N`)로부터 edge spreading으로 유도한 QC-SC-LDPC(`H[0,∞]`), 예제 rate 2/5~4/7, `L=155~301`.
2. 문제: 반복 BP 복호가 Tanner graph의 유해객체(stopping/trapping/absorbing set, pseudocodeword)에 갇혀 특히 error-floor 영역 성능이 저하됨.
3. 기존 한계: 기존 edge-spreading 최적화는 특정 구조·소형 memory에만 국한되고 다수 후보를 사전 배제하여 최적해를 놓침.
4. 핵심 기법: memory `ms`인 `(ms+1)`-ary spreading matrix `B`(벡터 `b`)로 block code의 edge를 convolutional 구조로 펼침.
5. 핵심 정리(Lemma 2): block-cycle이 spreading 후에도 존재할 필요충분조건은 해당 `B` 부분행렬 `Bλ`가 사이클 조건식 (1)을 정수 위에서 만족하는 것 — 사이클 검사만으로 유해객체 다중도 예측.
6. 지표: node당 평균 block-cycle 수 `Eλ`, 평균 absorbing set 수 `E(a,b)`를 block-cycle 분포 `DL,Λ`로부터 계산.
7. 탐색: MIHAO(트리탐색) — 루트=all-zero `B`, `l`번째 tier=비영 항목 `l`개, 부모보다 유해객체 다중도를 줄이는 자식만 유지하고 나쁜 후보는 backtrack.
8. 구현: `edge_spread`, `count_elimin_objects`, `count_harmful_objects` 함수로 재귀 greedy 탐색(최적 보장 없음, 정지기준=backtrack/tier 수).
9. 결과: array/Tanner code 벤치마크에서 문헌 대비 낮은 유해객체 다중도(예 `E(3,3)` 감소), random search 대비 3.5~8.2배 speed up, BER(AWGN, BPSK, SW decoder W=5(ms+1), 100 iter) 개선.
10. 한계: HW 미설계, AWGN 시뮬만, block QC-LDPC이 아닌 SC(convolutional) 구조 전용, gate/throughput 수치 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| edge-spreading으로 QC-SC 부호 구성 | 대응 없음 (Prime ECC는 block QC-LDPC 고정) | SC-LDPC 구조라 부호 로드 구조와 불일치 |
| 유해객체(AS/트래핑셋) 최소화 설계 | ecc_top.cpp `Load_PCM()` | H-matrix 설계 레이어에 개념적 연관, 재검증 부담 큼 |
| block-cycle/사이클 조건식 기반 최적화 | 대응 없음 | shift 설계 최적화 아이디어만 간접 참고 |

적용 가치: **낮음** — SC-LDPC(convolutional) 전용 구성법이고 HW/디코더 이득이 없어 block binary QC-LDPC인 Prime ECC에 떼어 쓰기 어렵다.

### D. JSON 블록

```json
{
  "id": "arxiv:1904.07158v1",
  "title": "Efficient Search and Elimination of Harmful Objects in Optimized QC SC-LDPC Codes",
  "year": 2019,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "SC-LDPC",
  "code_rate": "0.51~0.71",
  "code_length": "155~301",
  "soft_quant": "무관",
  "key_contribution": "edge-spreading 트리탐색(MIHAO)으로 QC-SC-LDPC의 유해객체(AS/트래핑셋) 다중도 최소화",
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
  "recommend": "하",
  "caveat": "SC-LDPC(convolutional) 구성 전용, sliding-window BP 가정 — 고정 binary block QC-LDPC(Prime ECC)와 구조 불일치",
  "todo_check": "MIHAO를 block QC-LDPC의 lifting/shift 설계에 직접 적용 가능한지(SC 구조 제거 시)"
}
```
