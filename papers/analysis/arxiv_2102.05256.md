### arxiv:2102.05256v1 - Proximal Decoding for LDPC-coded Massive MIMO Channels (2021, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5 |
| 부호length | 204 |
| 연판정 | 무관 |
| 핵심기여 | code-constraint 다항식을 정규화항으로 쓰는 proximal gradient 기반 근사 MAP 복호(gradient step + code-proximal step) — massive MIMO에서 MMSE+BP 대비 약 3dB 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | 부분 |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | massive MIMO(채널행렬 A) 검출·복호 결합 전용 — memoryless NAND엔 이점 소멸(gradient step이 A^T(As-y) 기반). γ,ω 튜닝 민감, HW 미설계 |
| 추가확인 | code-proximal step(GDBF류 penalty gradient)만 memoryless AWGN LDPC에 떼어내 min-sum 대비 이득이 있는지 |

> 총평: MIMO 검출과 LDPC 복호를 proximal gradient로 통합한 최적화형 복호 — massive MIMO 채널행렬 의존이 핵심이라 memoryless NAND QC-LDPC 이식성은 낮음.

### B. 알고리즘 요약

1. 시스템: LDPC-coded massive MIMO(`y=Ax+w`, Kronecker 상관 채널), QPSK→실수 BPSK 등가, (3,6)-regular LDPC `n=204, m=102`(rate 0.5).
2. 풀려는 문제: memoryless 가정의 BP는 채널메모리/MIMO 검출에 비자명 — 검출+복호를 하나의 최적화로 풀고자 함.
3. 핵심 가정: prior를 `p(x)∝exp(-γh(x))`로 두면 `γ→∞`에서 코드워드 집합 delta로 수렴 → 근사 MAP `argmin[L(x;y)+γh(x)]`.
4. 핵심 기법: code-constraint 다항식 `h(x)=Σ(xj²-1)² + Σ(∏_{j∈A(i)}xj -1)²`(bipolar+parity, SOS형, `h≥0` 등호⟺코드워드)를 정규화항으로 사용.
5. 핵심 식: proximal 반복 `r=s-ω∇L`, `s=Pγ(r)=r-γ∇h(r)` — ISTA의 code 버전. code-proximal operator가 pull-in property로 코드워드로 끌어당김.
6. 확장: MIMO 특화 gradient `∇L∝Aᵀ(As-y)`, box projection `Πη`(η=1.5)로 수치 불안정(∇h 발산) 억제.
7. 구현 디테일: `∇h` 계산이 `Q(i)=∏xj` 기반 O(n+k), LDPC면 O(n)로 BP와 동급 복잡도.
8. 학습 가능성: 모든 subprocess가 미분가능 → deep unfolding으로 γ,ω 튜닝 가능(future work).
9. 결과: ρ=0.4에서 BER=1e-4 기준 MMSE+BP 대비 약 3dB 이득, MMSE 대비 수렴 빠름·saturated error 낮음.
10. 한계: massive MIMO 검출 전용(A 행렬 의존), HW/throughput/양자화 없음, γ 선택에 성능 민감(γ=0.05 heuristic).

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| proximal/code-proximal 반복 복호 | decoder.cpp LDPC_Decoder() | 복호 루프 위치는 대응하나 gradient기반 최적화라 min-sum 메시지패싱과 알고리즘 이질적 |
| code-constraint 다항식 ∇h (parity penalty gradient) | decoder.cpp CNU_Update_New_Mag() | CN 연산에 대응 개념이나 GDBF류 실수 gradient — HW min-sum과 부정합 |
| gradient step Aᵀ(As-y) (MIMO 검출) | 대응 없음 | Prime ECC는 memoryless NAND 채널 — MIMO 채널행렬 검출 단계 없음 |
| soft LLR / 초기값 y | channel.cpp Set_LLR_Th() | 입력 soft값 개념 대응뿐, NAND soft-read 양자화 논의 없음 |
```

적용 가치: **낮음** — proximal decoding의 이득이 MIMO 채널행렬 `A`와의 결합 검출에서 나오며 memoryless NAND에선 그 핵심이 소멸. code-proximal(GDBF penalty) 부분만이 이론적 후보이나 실수 gradient라 min-sum HW와 이질적이고 HW 미설계.

### D. JSON 블록

```json
{
  "id": "arxiv:2102.05256v1",
  "title": "Proximal Decoding for LDPC-coded Massive MIMO Channels",
  "year": 2021,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.5,
  "code_length": "204",
  "soft_quant": "무관",
  "key_contribution": "code-constraint 다항식 정규화 기반 proximal gradient 근사 MAP 복호, massive MIMO에서 MMSE+BP 대비 약 3dB 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "부분",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "massive MIMO 검출·복호 결합 전용 — memoryless NAND엔 이점 소멸(gradient step이 Aᵀ(As-y) 기반), γ·ω 튜닝 민감, HW 미설계",
  "todo_check": "code-proximal step(GDBF류 penalty gradient)만 memoryless AWGN LDPC에 떼어내 min-sum 대비 이득이 있는지"
}
```
