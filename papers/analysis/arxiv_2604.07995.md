### arxiv:2604.07995v1 - Belief Propagation Convergence Prediction for Bivariate Bicycle Quantum Error Correction Codes (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 기타 |
| 부호length | 72~360 |
| 부호rate | 미상 |
| 연판정 | 무관 |
| 핵심기여 | Bivariate Bicycle 양자 LDPC 코드에서 defect count mod w 연산 하나로 BP 수렴 여부를 사전 예측해 OSD 후처리 필요 여부를 O(1)로 판단 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 양자 안정자 코드(quantum stabilizer code)의 hyperedge parity check 및 measurement error 모델에 특화되어 있어 고전 binary NAND LDPC의 syndrome 구조와 근본적으로 다름 |
| 추가확인 | classical binary LDPC에서 유사한 "column weight 기반 defect divisibility" 구조가 존재하는지(트래핑셋/조기종료 판별 응용 가능성) 여부 |

> 총평: 양자 LDPC(BB code)의 BP+OSD 파이프라인에서 OSD 스킵 여부를 사전 예측하는 기법으로, NAND classical binary LDPC 이식 관점에서는 대상 코드 구조(quantum stabilizer, hyperedge, measurement error)가 전혀 달라 적용 가치가 낮음.

### B. 알고리즘 요약

1. 대상은 IBM Bivariate Bicycle(BB) 양자 오류정정 코드([[144,12,12]] Gross code 등)로, parity check matrix가 hyperedge를 포함해 MWPM이 아닌 BP+OSD로 복호한다.
2. 문제: BP가 수렴할지 여부는 기존에는 BP를 끝까지 돌려봐야만 알 수 있어, 실패 시 OSD(`O(n^3)` Gaussian elimination)로 인한 지연이 크다.
3. 채널/노이즈 모델: phenomenological noise (data error + measurement error), 코드의 column weight `w`(각 데이터 큐빗이 정확히 `w`개 stabilizer를 활성화)를 핵심 구조로 사용.
4. 핵심 기법: syndrome defect count `mod w`가 0이면 BP 수렴 가능성이 매우 높고(≤0.001에서 100%), 0이 아니면 실패 확률 90%+ — `defect_count mod w = |m| mod w`(Proposition 1)로 measurement error 개수에만 의존함을 증명.
5. 핵심 식의 의미: data error는 항상 `w`의 배수만큼 defect를 만들므로, mod-w 값은 measurement error 존재 여부의 지표가 되고 BP는 measurement error를 모델링하지 못해 실패한다.
6. 확장: false positive(모드-0인데 BP 실패)의 원인은 (a) `|m|≥w` measurement error 누적, (b) weight-2 데이터 에러 클러스터가 만드는 4-cycle 트래핑셋 — 후자가 저노이즈에서 지배적(`O(p^2)`).
7. 구현: `predict_convergence(syndrome, w) = syndrome.sum() % w == 0` 한 줄, 추가 연산 오버헤드 없음.
8. 별도 학습/최적화 절차는 없음(구조적 증명 기반, 파라미터 튜닝 없음).
9. 결과: p=0.001에서 mod-3 AUC=0.995(다른 syndrome feature 대비 압도적), 65%의 syndrome에서 OSD 완전 스킵 가능, false positive rate가 `O(p^2.05)`로 스케일링(Proposition 2 일치).
10. 한계: 양자 stabilizer code 전용(hyperedge, measurement error 개념 자체가 classical binary LDPC에 없음), w=4 코드에서는 AUC 0.762로 급락하며 non-degenerate BB code에만 적용, HW 미설계(FPGA 프로젝션만 언급).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BP 수렴 사전예측(mod-w) | 대응 없음 | Prime ECC는 classical binary QC-LDPC이며 measurement error/hyperedge 개념이 없어 defect mod-w 판정 자체가 성립하지 않음 |
| BP+OSD 파이프라인, OSD 스킵 라우팅 | 대응 없음 | Prime ECC는 min-sum + partial/full CRC 조기종료 구조(`partial_CRC.cpp`)이며 OSD(Gaussian elimination) 후처리 자체가 없음 |
| min-sum BP의 4-cycle 트래핑셋(frustrated loop) | `decoder.cpp` `LDPC_Decoder()`, `CNU_Update_New_Mag()` | 짧은 사이클로 인한 sign oscillation 현상 자체는 min-sum 계열 디코더 일반론과 일부 겹치나, 논문의 핵심 기여(mod-w 예측)와는 무관 |

> 적용 가치: 낮음 — 논문의 핵심 기법(defect count mod w 기반 BP 수렴 예측)이 quantum stabilizer code의 구조적 특성(hyperedge, measurement error, column weight w)에 전적으로 의존하며, classical binary NAND LDPC의 syndrome/디코더 구조에는 대응 개념이 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2604.07995v1",
  "title": "Belief Propagation Convergence Prediction for Bivariate Bicycle Quantum Error Correction Codes",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "72~360",
  "soft_quant": "무관",
  "key_contribution": "Bivariate Bicycle 양자 LDPC 코드에서 defect count mod w 연산 하나로 BP 수렴 여부를 사전 예측해 OSD 후처리 필요 여부를 O(1)로 판단",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "양자 안정자 코드의 hyperedge parity check 및 measurement error 모델에 특화되어 고전 binary NAND LDPC 구조와 근본적으로 다름",
  "todo_check": "classical binary LDPC에서 유사한 column weight 기반 defect divisibility 구조가 트래핑셋/조기종료 판별에 응용 가능한지 확인"
}
```
