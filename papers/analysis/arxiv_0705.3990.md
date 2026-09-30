### arxiv:0705.3990v2 - Interior Point Decoding for Linear Vector Channels (2007/2008, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 204 |
| 연판정 | soft-4bit+ |
| 핵심기여 | LDPC MLD를 fundamental polytope 위 convex 최적화로 완화한 interior point decoding 제안, ISI/partial response 등 memory 있는 채널에서 joint MPD 대비 우수한 BER·throughput 달성 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | 부분 |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | ISI/partial response(memory 있는 채널) 전용 설계이며 순수 memoryless NAND 채널에는 해당 없음. HW 미설계, gradient/Hessian/Cholesky/Jacobi 등 부동소수점 수치최적화 기반이라 NAND HW 대비 이질적 |
| 추가확인 | built-in min-sum(부분)이 표준 normalized min-sum과 어떻게 다른지, NAND에 memory 채널 요소(예: inter-cell interference)가 있다면 응용 가능성 |

> 총평: ISI/partial-response 채널을 위한 convex-optimization 기반 신개념 디코더로 이론적 가치는 있으나, 순수 memoryless NAND 채널·binary QC-LDPC HW와는 채널모델·연산구조가 근본적으로 달라 이식 가치가 낮음.

### B. 알고리즘 요약

1. 채널모델: linear vector channel `r = Ax + b + z` (A: interference matrix, ISI/partial response(PR) 채널 포함), 시뮬은 n=204, m=102, wc=3, wr=6 regular LDPC + PR 채널(dicode, 1-D, EPR4, long-tail δ=16 등).
2. 문제: 기존 joint message-passing decoder(BCJR+min-sum)는 memory가 긴 채널(δ 큰 PR)에서 계산량이 폭발적으로 증가해 적용 어려움 — memory 채널용 새로운 저복잡도 디코더 필요.
3. 핵심 가정: MLD `argmin_{x∈C} d(Ax+b, r)`를 Feldman의 fundamental polytope `P` 위로 완화(relax)한 convex 최적화 문제(relaxed MLD)로 재정의.
4. 핵심 기법: interior point algorithm(barrier function 방식)으로 merit function `ψ(x)=t·f(x)+B(x)` (f=거리목적함수, B=log-barrier `-Σln(-θ_i)`)를 최소화, outer loop에서 t를 점진적으로 키움.
5. `θ_i` (parity constraint 위반도)를 O(w_r) 시간에 계산하는 feasibility check(Lemma 3)로 탐색점이 항상 polytope 내부(P*)에 머물도록 보장 — 이 식이 매 iteration 실행가능성 판정의 핵심.
6. 확장 기법: 근사 gradient(O(w_r·n))와 근사 Hessian(O(w_r·n), Newton법)을 이용해 exact gradient의 O(2^wr·n) 비용을 회피, Newton 방식이 gradient descent보다 적은 iteration으로 수렴.
7. 구현 디테일: PR채널에서 Hessian은 대역(Toeplitz) 구조를 가져 Cholesky 분해(O(n)) 또는 Jacobi/under-relaxation 반복법(병렬화 가능)으로 Newton 방정식을 O(n)에 해결. inner loop 후 built-in normalized min-sum(dumping factor κ≈0.7~0.9)으로 secondary decoding 수행.
8. 최적화 절차: outer loop마다 (1) inner loop(gradient/Newton) 반복, (2) built-in min-sum으로 codeword 검증, (3) parity 만족 시 종료, 아니면 t := αt로 증가.
9. 결과: 1-D 채널에서 Newton(5,5)이 joint MPD 대비 BER 1e-4에서 1.5dB 이득, throughput은 소프트웨어 구현 기준 Newton+Cholesky 1715 blocks/sec vs joint MPD 359 blocks/sec(약 4.8배). EPR4 채널에서는 반대로 joint MPD가 1.8dB 우세.
10. 한계: memoryless AWGN이 아닌 ISI/PR(memory) 채널 전용 정식화이며, HW 구현·게이트카운트 없음(소프트웨어 시뮬 throughput만 제시), 채널 계수에 따라 성능이 크게 갈림(EPR4에서 열세).

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Interior point / convex 최적화 디코딩 전체 | 대응 없음 | Prime ECC는 message-passing(min-sum) 구조로 gradient/Hessian/Newton 기반 최적화 프레임워크 자체가 없음 |
| built-in normalized min-sum(secondary decoding) | decoder.cpp `CNU_Update_New_Mag()` | 이미 보유한 normalized/scaled min-sum과 유사 개념이나 논문에서는 보조 역할일 뿐 |
| ISI/partial response 채널 모델 | channel.cpp `Set_R_Offset()` | Prime ECC는 AWGN/RBER/fixed-error 채널만 지원, memory 있는 ISI 채널 미지원 (대응 미흡) |
```

> 적용 가치: 낮음 — ISI/partial-response(memory 채널) 전용 convex-optimization 디코더로, NAND의 memoryless binary QC-LDPC HW 구조(min-sum 기반 bit-exact 파이프라인)와 연산모델이 근본적으로 다르며 HW 검증도 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:0705.3990v2",
  "title": "Interior Point Decoding for Linear Vector Channels",
  "year": 2007,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": 204,
  "soft_quant": "soft-4bit+",
  "key_contribution": "LDPC MLD를 fundamental polytope 위 convex 최적화로 완화한 interior point decoding 제안, ISI/partial response 등 memory 있는 채널에서 joint MPD 대비 우수한 BER·throughput 달성",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "부분",
  "latency": "개선",
  "recommend": "하",
  "caveat": "ISI/partial response(memory 있는 채널) 전용 설계이며 순수 memoryless NAND 채널에는 해당 없음. HW 미설계, gradient/Hessian/Cholesky/Jacobi 등 부동소수점 수치최적화 기반이라 NAND HW 대비 이질적",
  "todo_check": "built-in min-sum(부분)이 표준 normalized min-sum과 어떻게 다른지, NAND에 memory 채널 요소(예: inter-cell interference)가 있다면 응용 가능성"
}
```
