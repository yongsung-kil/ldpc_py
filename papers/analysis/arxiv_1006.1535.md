### arxiv:1006.1535v1 - Tree-structure Expectation Propagation for Decoding LDPC codes over Binary Erasure Channels (2010, arXiv/ISIT-class preprint)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5 |
| 부호length | 512~4096 |
| 연판정 | 무관 |
| 핵심기여 | BP가 멈추면 degree-2 체크노드에서 pair-wise marginal 제약을 부과해 계속 복호하는 TEP 알고리즘 (BP와 동일 복잡도로 BEC capacity 상향) |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | N/A |
| latency | 동등 |
| 추천도 | 하 |
| 한계,주의 | BEC 소실채널 전용 peeling/EP 복호 — NAND의 BSC/AWGN soft LLR min-sum과 채널·메시지 모델이 근본적으로 다름, degree-2 체크노드 병합은 QC-LDPC의 순차 그래프 조작이라 HW 병렬 min-sum과 부정합 |
| 추가확인 | irregular 확장은 [10]에 있음; TEP의 "정체 후 재출발" 아이디어가 BSC/AWGN post-processing(예: error-floor bit-flip)로 일반화 가능한지 |

> 총평: BEC 전용 BP 개선 복호기(TEP). 정체 시 degree-2 체크노드 병합으로 MAP에 근접하나, NAND soft min-sum과 채널·복호 모델 상이 → 이식성 낮음.

### B. 알고리즘 요약

1. 대상: BEC(소실확률 `ε`) 상 regular LDPC(`λ(x)=x^2`, `ρ(x)=x^5`, 즉 (3,6) rate-1/2) 복호. 코드길이 `n=2^i` (i=9~12).
2. 문제: 유한/순환 그래프에서 BP는 degree-1 체크노드가 소진되면 멈춤 — BP capacity `0.4294` < MAP capacity `0.48815`. Maxwell 복호는 MAP 달성하나 추정변수 수에 지수 복잡도.
3. 핵심 기법(TEP): BP가 멈춘 잔여 그래프 `TBP`에서 **degree-2 체크노드**를 골라 변수노드 하나+엣지 2개 제거, 남은 변수에 나머지 체크노드 재연결(parity 1이면 반전). 제거변수는 남은 변수 복호 시 확정.
4. 메커니즘: degree-2 체크의 두 변수가 degree-3 체크도 공유하면, 제거 후 degree-1 체크노드가 생성되어 BP 재시작 가능 → 정체 탈출.
5. 복잡도: 매 iteration 체크1+변수1 제거로 **BP와 동일**(추정변수 수에 무관), Maxwell의 지수 복잡도 회피. EP의 tree-structured 근사(pair-wise marginal 제약)에서 유래.
6. 분석: DD(degree distribution) 진화를 Stage A(변수쌍이 다른 체크 미공유)/Stage B(항상 공유, `pB(t)=1`)로 나눠 미분방정식(식12~17)으로 기술, `n→∞` 극한 해석.
7. 핵심식: `r1(x)=λ(x)[x-1+ρ(1-λ(x))]` — BP가 멈추는 지점 `xBP` 판정; TEP는 Stage A에서 평균 좌차수 `a(t)`가 지수증가해 `pB→1` 도달.
8. 결과(점근): (3,6) regular에서 `ε_TEP ≥ 0.4315 > ε_BP=0.4294` (하한, 실제는 더 큼).
9. 결과(유한길이): n=512~4096 WER에서 TEP가 항상 BP를 상회(100 샘플 평균).
10. 한계: BEC 전용, HW 미설계, irregular 확장·엄밀 capacity는 후속 논문[10]에 위임.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BP/peeling 복호 루프 (BEC) | decoder.cpp `LDPC_Decoder()` | Prime ECC는 soft LLR min-sum 반복복호 — BEC peeling과 메시지·채널 모델 상이 |
| degree-2 체크노드 병합 그래프 조작 | 대응 없음 | Prime ECC는 고정 QC-LDPC에 병렬 min-sum, 동적 그래프 축약 미지원 |
| BP 정체 후 재시작 post-processing | 대응 없음 | 개념적으로만 error-floor 대책과 유사, BEC 전용이라 직접 대응 없음 |

적용 가치: **낮음** — TEP는 BEC 소실채널 전용 BP 개선 복호기로, NAND의 BSC/AWGN soft-decision min-sum 파이프라인(병렬, LLR 기반)과 채널·메시지·HW 모델이 달라 직접 이식 불가.

### D. JSON 블록

```json
{
  "id": "arxiv:1006.1535v1",
  "title": "Tree-structure Expectation Propagation for Decoding LDPC codes over Binary Erasure Channels",
  "year": 2010,
  "venue": "arXiv (cs.IT)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.5,
  "code_length": "512~4096",
  "soft_quant": "무관",
  "key_contribution": "BP가 멈추면 degree-2 체크노드에서 pair-wise marginal 제약을 부과해 계속 복호하는 TEP 알고리즘 (BP와 동일 복잡도로 BEC capacity 상향)",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "N/A",
  "latency": "동등",
  "recommend": "하",
  "caveat": "BEC 소실채널 전용 peeling/EP 복호 — NAND의 BSC/AWGN soft LLR min-sum과 채널·메시지 모델이 근본적으로 다름, degree-2 체크노드 병합은 순차 그래프 조작이라 HW 병렬 min-sum과 부정합",
  "todo_check": "irregular 확장은 [10]; TEP의 '정체 후 재출발' 아이디어가 BSC/AWGN post-processing(error-floor bit-flip)로 일반화 가능한지"
}
```
