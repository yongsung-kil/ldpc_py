### arxiv:1202.1060v1 - A Non-Disjoint Group Shuffled Decoding for LDPC Codes (2012, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5~0.67 |
| 부호length | 504~816 |
| 연판정 | soft-4bit+ |
| 핵심기여 | CN을 겹치는(non-disjoint) 그룹으로 나누어 인접 서브이터레이션 간 정보 전달을 늘려 수렴속도를 높인 shuffled BP 스케줄링 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | Sum-Product(tanh) 기반 GA 분석이며 min-sum HW로의 정량적 이식 효과 미검증 |
| 추가확인 | 겹침비율 r과 그룹수 G가 임의 선택(random)이라 실제 HW 스케줄러의 group 재구성 오버헤드 미검토 |

> 총평: CN 그룹 간 오버랩을 두는 shuffled 스케줄링으로 동일 복잡도에서 수렴속도 개선을 보이나, HW 미설계·구형 regular 코드 시뮬 수준이라 이식성은 중간.

### B. 알고리즘 요약

1. 대상은 이진 (504,252)/(816,544) regular LDPC, dc=6, BIAWGN 채널에서 BPSK 전송.
2. 기존 disjoint group shuffled BP(GSBP)는 CN을 겹치지 않는 그룹으로 나눠 그룹별 순차 메시지 전달을 수행하나 그룹 간 정보 전달량이 제한적.
3. 채널은 AWGN, 초기 LLR `L_n = 2y_n/σ²`로 정의되는 표준 BP 모델을 가정.
4. 핵심 기법은 CN을 `r`(오버랩 비율)만큼 겹치는 non-disjoint 그룹으로 분할: `k`번째 그룹은 이전 그룹에서 `r·N_G`개, 나머지 CN 풀에서 `(1-r)·N_G`개를 취함.
5. 오버랩된 CN(Class-b)은 이전 서브이터레이션에서 갱신된 메시지를 다시 전달해 연결도(CoCSG, `ℓ`)를 키우며, `ℓ`가 클수록 더 많은 정보가 다음 서브이터레이션으로 전파됨.
6. CN을 Class-a/b/c/d 4종으로 나누고 Gaussian Approximation(GA)으로 각 클래스 평균 LLR `μ_c` 갱신식(식 6~17)을 유도해 수렴 거동을 해석적으로 추적.
7. 부수 트릭은 없음(순수 스케줄링 변경, 양자화/HW 최적화 언급 없음).
8. 최적화 절차는 GA 기반 이론 해석과 시뮬 병행이며 별도 학습(GA/NN) 없음.
9. 결과: BER 10⁻⁵에서 NDGSBP가 표준 BP 대비 0.2dB, GSBP 대비 0.08dB 이득; 동일 SNR에서 필요 반복수도 BP/GSBP보다 적음(표 I, 예: dv=3/dc=6 BP 422회 → NDGSBP(G=36) 196회).
10. 한계: HW 설계 없이 알고리즘·GA 분석·시뮬뿐이며, 그룹 오버랩 위치는 무작위 선택이라 코드 구조를 고려한 최적화는 미제시.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Non-disjoint group shuffled 스케줄링 | `decoder.cpp` `LDPC_Decoder()` 이터레이션 루프 | 서브이터레이션 그룹 순서/오버랩 로직을 이터레이션 루프에 삽입 가능하나 현재 Dual-Update 스케줄과는 다른 방식 |
| CN/VN 메시지 갱신 (tanh 기반 sum-product) | `decoder.cpp` `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | Prime ECC는 min-sum 기반이라 tanh 연산 자체는 대응 없음, 그룹 스케줄 아이디어만 이식 가능 |
| GA 기반 수렴 분석 | 대응 없음 | 시뮬레이터는 bit-exact HW 모사이며 GA 해석 도구는 없음 |

> 적용 가치: 낮음. CN 그룹 오버랩 스케줄링 아이디어 자체는 min-sum 디코더 이터레이션 루프에 원론적으로 이식 가능하나, 이미 Prime ECC가 보유한 Dual-Update 스케줄과 중복되는 개념이고 본 논문은 tanh 기반 GA 분석·구형 regular 코드 시뮬뿐이라 HW 이식 근거가 약함.

### D. JSON 블록

```json
{
  "id": "arxiv:1202.1060v1",
  "title": "A Non-Disjoint Group Shuffled Decoding for LDPC Codes",
  "year": 2012,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": null,
  "code_length": "504~816",
  "soft_quant": "soft-4bit+",
  "key_contribution": "CN을 겹치는(non-disjoint) 그룹으로 나누어 인접 서브이터레이션 간 정보 전달을 늘려 수렴속도를 높인 shuffled BP 스케줄링",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "중",
  "caveat": "Sum-Product(tanh) 기반 GA 분석이며 min-sum HW로의 정량적 이식 효과 미검증",
  "todo_check": "겹침비율 r과 그룹수 G가 임의 선택(random)이라 실제 HW 스케줄러의 group 재구성 오버헤드 미검토"
}
```
