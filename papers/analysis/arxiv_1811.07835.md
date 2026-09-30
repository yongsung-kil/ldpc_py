### arxiv:1811.07835v2 - Neural Belief-Propagation Decoders for Quantum Error-Correcting Codes (2018, arXiv quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.125~0.2 |
| 부호length | 129~256 |
| 연판정 | 무관 |
| 핵심기여 | BP를 심층신경망으로 매핑해 trainable weight/bias 학습, error degeneracy 반영 loss로 quantum LDPC 복호정확도 최대 3자릿수 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | quantum stabilizer(Pauli) 코드 전용 + full-tanh Sum-Product NN 디코더 → NAND binary min-sum HW와 무관, degeneracy는 고전 ECC에 없음 |
| 추가확인 | 없음 (NN 디코더·quantum degeneracy loss는 Prime ECC 대응 모듈 없음) |

> 총평: quantum LDPC(toric/bicycle/hypergraph-product)용 학습형 NBP 디코더로, NN 전면 대체 + quantum degeneracy 전용이라 NAND binary LDPC ECC 이식 가치 없음.

### B. 알고리즘 요약

1. 시스템: quantum LDPC 코드(toric `[[·]]`, bicycle `[[256,32]]` r=0.125, hypergraph-product `[[129,28]]` r~0.2)의 복호. syndrome `s = He mod 2`에서 error `e` 추정.
2. 문제: 표준 BP는 quantum 코드에서 부정확 — "error degeneracy"(stabilizer 차이만 나는 오류는 동일 작용) 때문에 고전 BP loss가 부적합.
3. 모델: Pauli 오류를 `2N`-bit symplectic 표현, stabilizer 코드 PCM `H`. 성공 조건은 `e_inf == e`가 아니라 `e_tot = e + e_inf`가 stabilizer group 소속.
4. 핵심 기법: BP 반복식 (1)~(3)을 신경망으로 매핑, trainable weight `w`·bias `b` 도입 (식 4~6). 비선형 `a(x)=log(tanh(x/2))`, 표준 BP는 모든 파라미터=1인 특수경우.
5. 식 의미: full Sum-Product 형태 `μ_{c→v}` 업데이트에 학습 가중치를 곱해 quantum 코드의 short-cycle/degeneracy로 인한 BP 편향을 보정.
6. 확장: degeneracy 반영 loss `L = Σ f(Σ H⊥·M·[e + σ(μ)])` (식 8), parity를 미분가능 `f(x)=|sin(πx/2)|`로 대체해 gradient 학습 가능.
7. 구현 디테일: residual connection, cycle별 loss 평균, toric의 주기성 활용한 weight-sharing(CNN filter 유사), `tanh⁻¹` 인자 truncation `ε=1e-4`.
8. 학습: TensorFlow backprop, minibatch당 120 error pattern(6개 physical error rate ∈[0.01,0.05]), ~10000 minibatch, `lr`=1e-4~2e-4.
9. 결과: toric/bicycle/hypergraph-product 모두 logical error rate 최대 3자릿수 개선, threshold 발생 조짐, 다른 code size로 전이(transfer) 가능.
10. 한계: HW 미설계, 시뮬만, quantum stabilizer 코드 전용(degeneracy는 고전 ECC에 없음), NN 전면 대체 디코더.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| NBP(학습형 BP) 디코더 전체 | 대응 없음 | NN/딥러닝 디코더 + full-tanh Sum-Product는 min-sum HW 구조와 대응 없음 |
| degeneracy 반영 loss / stabilizer | 대응 없음 | quantum Pauli/stabilizer 전용, binary NAND ECC에 개념 없음 |
| BP 반복식(C2V/V2C) | `decoder.cpp` `LDPC_Decoder()`, `C2V_Cal()` | 형식만 유사하나 quantum·NN·tanh 기반이라 실질 이식 불가 |

적용 가치: **낮음** — quantum LDPC용 학습형 NN 디코더로, Prime ECC의 binary min-sum HW 디코더에 이식할 요소(quantum degeneracy loss·trainable full-SP)가 대응 없음.

### D. JSON

```json
{
  "id": "arxiv:1811.07835v2",
  "title": "Neural Belief-Propagation Decoders for Quantum Error-Correcting Codes",
  "year": 2018,
  "venue": "arXiv quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": "0.125~0.2",
  "code_length": "129~256",
  "soft_quant": "무관",
  "key_contribution": "BP를 심층신경망으로 매핑해 trainable weight/bias 학습, error degeneracy 반영 loss로 quantum LDPC 복호정확도 최대 3자릿수 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "quantum stabilizer(Pauli) 코드 전용 + full-tanh Sum-Product NN 디코더로 NAND binary min-sum HW와 무관",
  "todo_check": "없음 (NN 디코더·quantum degeneracy loss는 Prime ECC 대응 모듈 없음)"
}
```
