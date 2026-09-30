### arxiv:2001.07464v2 - Pruning Neural Belief Propagation Decoders (2020, ISIT/arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.5 |
| 부호length | 128 |
| 연판정 | soft-4bit+ |
| 핵심기여 | Tanner graph 가중치 크기 기반으로 iteration별 overcomplete parity-check 행렬의 CN을 pruning하여 저복잡도로 near-ML 성능 확보 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | 부분 |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | RM/BCH급 dense parity-check 코드와 CCSDS 짧은 LDPC(length 128) 대상 실험뿐, NAND급 QC-LDPC(수천~수만 bit, high-rate) 확장성 미검증 |
| 추가확인 | 학습(Adam/Tensorflow) 기반 오프라인 최적화 결과를 실제 QC-LDPC circulant 구조에 어떻게 매핑할지, iteration마다 다른 H를 쓰는 것이 HW 파이프라인과 호환되는지 |

> 총평: neural network로 학습한 overcomplete parity-check pruning을 통한 waterfall 개선 기법이나, 짧은 코드·소프트 실수 가중치·오프라인 학습 의존이라 고rate QC-LDPC HW 이식은 재검증 부담이 큼.

### B. 알고리즘 요약

1. 짧은 선형 블록코드(RM, CCSDS LDPC length 128 rate 0.5)에 대해 overcomplete parity-check 행렬 `Hoc`로 weighted BP(WBP) 디코딩을 수행.
2. 문제: 표준 BP는 dense parity-check(BCH/RM)나 짧은 코드에서 ML 대비 성능 열화가 크고, WBP도 초기 `Hoc` 선택에 성능이 크게 좌우됨.
3. 가정: 채널은 AWGN, all-zero codeword로 학습 가능한 대칭 채널/디코더를 전제.
4. 핵심 기법: CN마다 가중치를 tie(`w_c^(ℓ)`)한 WBP를 학습 후, `w_c^(ℓ)` 크기가 작은 CN을 순차적으로 pruning하여 iteration `ℓ`마다 다른 parity-check 행렬 `H_ℓ`을 구성.
5. CN 업데이트 `λ_c→v = 2 w_c^(ℓ) tanh^-1(Π tanh(λ/2))`에서 `w_c^(ℓ)→0`이면 해당 CN 기여가 사실상 제거됨 — 이를 명시적 pruning으로 전환.
6. 학습-pruning을 번갈아 반복(gradient descent → 최소 가중치 CN 제거 → 재학습)하여 목표 복잡도/성능까지 축소.
7. Decoder 변형 3종: D1(최적 H+가중치 유지), D2(최적 H+가중치 모두 1, 즉 conventional BP), D3(H+iteration/edge별 untied 가중치).
8. 손실함수는 soft bit-error-rate 기반 multi-loss(`Γ~`, 식 12-13), Adam optimizer로 최적화.
9. 결과: RM(3,7)에서 ML 대비 0.27dB, CCSDS LDPC(rate 0.5, length 128)에서 ML 대비 1.5dB, conventional BP 대비 0.5~0.6dB 개선(동일 CN evaluation 수 기준).
10. 한계: 알고리즘/시뮬 수준(HW 미설계), 짧은 코드(length ≤128, RM은 32~128) 위주, iteration마다 다른 H를 사용하는 구조가 QC-LDPC HW 파이프라인에 그대로 적용되는지 불명.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| WBP CN/VN 업데이트 (가중치 tanh 기반) | `decoder.cpp` `LDPC_Decoder()`, `C2V_Cal()` | Prime ECC는 min-sum 기반이라 full-tanh WBP는 알고리즘 계열이 다름 |
| iteration별 다른 parity-check 행렬(H_ℓ) 사용 | `ecc_top.cpp` `Load_PCM()` | 고정 QC-LDPC PCM 구조와 상충, 이식 난이도 높음 |
| 학습 기반 CN pruning(가중치 최적화) | 대응 없음 | Prime ECC는 min-sum + 고정 HW 구조, NN 학습 파이프라인 없음 |
| 오버컴플리트 parity-check 초기화 | 대응 없음 | Prime ECC는 단일 H-matrix(base+circulant) 고정 |

> 적용 가치: 낮음 — full-tanh 기반 WBP·NN 학습 pruning 계열로 Prime ECC의 min-sum/고정 QC-LDPC HW 구조와 이질적이며, 짧은 코드(≤128bit) 실험이라 NAND급 고rate QC-LDPC로의 확장 근거가 부족함.

### D. JSON 블록

```json
{
  "id": "arxiv:2001.07464v2",
  "title": "Pruning Neural Belief Propagation Decoders",
  "year": 2020,
  "venue": "ISIT/arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": 0.5,
  "code_length": 128,
  "soft_quant": "soft-4bit+",
  "key_contribution": "Tanner graph 가중치 크기 기반으로 iteration별 overcomplete parity-check 행렬의 CN을 pruning하여 저복잡도로 near-ML 성능 확보",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "부분",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "RM/BCH급 dense parity-check 코드와 CCSDS 짧은 LDPC(length 128) 대상 실험뿐, NAND급 QC-LDPC(수천~수만 bit, high-rate) 확장성 미검증",
  "todo_check": "학습 기반 오프라인 최적화 결과를 실제 QC-LDPC circulant 구조에 어떻게 매핑할지, iteration마다 다른 H를 쓰는 것이 HW 파이프라인과 호환되는지"
}
```
