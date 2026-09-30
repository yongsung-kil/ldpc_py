### arxiv:2003.01998v5 - Neural Enhanced Belief Propagation on Factor Graphs (2020, arXiv/AISTATS 2021)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 96 |
| 연판정 | soft-4bit+ |
| 핵심기여 | Graph Neural Network(FG-GNN)를 매 BP 반복마다 결합해 메시지를 보정하는 하이브리드 디코더(NEBP)로 non-Gaussian(bursty) 채널에서 표준 sum-product BP 대비 BER 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | GNN(MLP+GRU) 전면 결합형 sum-product 디코더로 학습 파라미터·부동소수 연산 다수 필요, NAND ASIC HW 이식에 부적합하며 부호도 (96,48) 소형 예시로 실용 rate/length 검증 없음 |
| 추가확인 | bursty 채널 가정이 NAND read-noise(retention/read-disturb 등)와 통계적으로 부합하는지 미검증, 표준 AWGN에서는 성능 이득이 사실상 없음(σb=0에서 BP와 유사) |

> 총평: GNN을 결합한 신경망 강화 BP 디코더로 non-Gaussian 채널 강건성을 목표로 한 순수 알고리즘/이론 논문. binary min-sum 계열이 아닌 학습 기반 접근으로 Prime ECC(bit-exact HW min-sum 시뮬레이터)와 구조적 이질성이 커 이식 가치 낮음.

### B. 알고리즘 요약

1. LDPC 부호는 factor graph 상 belief propagation(BP, sum-product)의 특수 사례로 다뤄지며, 실험에서는 David MacKay의 "96.3.963" 코드(`n=96`, `k=48`)를 사용.
2. 문제: 표준 BP/LDPC는 채널이 정확히 알려진(주로 Gaussian) 경우에만 최적이며, 실제로는 채널 분포가 불확실하거나 non-Gaussian(bursty noise)일 때 성능이 저하됨.
3. 채널 모델: `r_i = x_i + z_i + p_i*w_i` (기본 AWGN `z_i~N(0,σc²)`에 확률 `ρ=0.05`로 큰 노이즈 `w_i~N(0,σb²)`가 추가되는 bursty channel, Gilbert 1960/Kim et al. 2018 기반).
4. 핵심 기법: Graph Neural Network를 factor graph용으로 확장한 FG-GNN을 정의, 매 BP 반복 후 BP 메시지(`µ̃_f→x`, `µ̃_x→f`)를 FG-GNN 입력으로 넣어 2회 GNN 반복 후 메시지를 보정하는 하이브리드 알고리즘 NEBP(Neural Enhanced BP) 제안.
5. 핵심 식: `µ_f→x^(t+1) = µ̃_f→x^t · f_s(M_f→x^t) + f_u(M_f→x^t)` — GNN 임베딩 `M_f→x`로부터 스칼라 배율(`f_s`)과 가산 보정(`f_u`)을 학습해 BP 메시지를 보정, `f_u=0`이면 순수 BP와 동일.
6. 확장/보조: singleton factor(채널 사전확률)로 가는 메시지와 일반 factor 메시지를 별도 MLP로 처리, 학습은 `Loss = L(x_gt, p̂(x)) + R`로 binary cross-entropy + `f_u` 정규화 항(BP에 가깝게 유도).
7. 구현 디테일: 전 과정 20 iteration, Adam optimizer(lr=2e-4), hidden feature 32, 활성함수 SeLU, node update는 2-layer MLP + GRU. NAND HW 친화적 양자화/근사 없음(부동소수 학습망 그대로).
8. 학습 절차: SNR={0,1,2,3,4}dB, `σb~U(0,5)`에서 다양한 조합으로 데이터 생성해 지도학습, 검증 정확도로 조기종료.
9. 결과: bursty noise가 커질수록(σb>0) NEBP가 표준 LDPC/FG-GNN/LDPC-bursty 대비 가장 낮은 BER 달성, σb=0(순수 AWGN)에서는 표준 LDPC와 유사한 성능으로 수렴(큰 개선 없음).
10. 한계: 소형 부호(96,48) 시뮬레이션만 수행, HW 구현·게이트카운트·throughput 전무. 통신 채널(bursty interference) 대상이며 NAND 특유의 read-noise/retention 모델과 직접 연결되지 않음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BP(sum-product) 메시지 업데이트 | `decoder.cpp` `LDPC_Decoder()`, `C2V_Cal()` | Prime ECC는 min-sum(HW 근사)만 사용, full sum-product는 미지원이라 개념적 대응만 가능 |
| GNN(FG-GNN) 기반 메시지 보정 | 대응 없음 | NN/딥러닝 디코더는 프로파일 §6에서 "대응 없음"으로 명시된 항목, ASIC bit-exact 시뮬레이터와 이질적 |
| VN/CN 반복 스케줄(iteration 구조) | `decoder.cpp` `LDPC_Decoder()` 이터레이션 루프 | 반복 구조 자체는 유사하나 신경망 결합 로직은 이식 불가 |
| bursty 채널 모델(가우시안+간헐적 큰 노이즈) | `channel.cpp` | NAND의 AWGN/RBER/fixed-error 모델과 다른 통신 특화 노이즈 모델, 직접 대응 낮음 |

적용 가치: **낮음** — NN 전면 결합형 BP 디코더로 프로파일의 "NN/딥러닝 디코더는 대응 없음" 판정 기준에 정확히 해당하며, 검증도 소형 통신 부호의 시뮬레이션에 그침.

### D. JSON 블록

```json
{
  "id": "arxiv:2003.01998v5",
  "title": "Neural Enhanced Belief Propagation on Factor Graphs",
  "year": 2020,
  "venue": "arXiv/AISTATS 2021",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": "96",
  "soft_quant": "soft-4bit+",
  "key_contribution": "Graph Neural Network(FG-GNN)를 매 BP 반복마다 결합해 메시지를 보정하는 하이브리드 디코더(NEBP)로 non-Gaussian(bursty) 채널에서 표준 sum-product BP 대비 BER 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "GNN(MLP+GRU) 전면 결합형 sum-product 디코더로 학습 파라미터·부동소수 연산 다수 필요, NAND ASIC HW 이식에 부적합하며 부호도 (96,48) 소형 예시로 실용 rate/length 검증 없음",
  "todo_check": "bursty 채널 가정이 NAND read-noise(retention/read-disturb 등)와 통계적으로 부합하는지 미검증, 표준 AWGN에서는 성능 이득이 사실상 없음(σb=0에서 BP와 유사)"
}
```
