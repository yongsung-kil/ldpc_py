### arxiv:2502.16408v1 - Decision-tree decoders for general quantum LDPC codes (2025, arXiv quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | qLDPC용 Decision Tree Decoder(DTD): 결함을 하나씩 추가해 syndrome height 하한으로 트리를 가지치기, 최소무게 정정 보장 provable 디코더 + BP-DTD heuristic |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 양자 stabilizer/CSS 코드(color/bivariate bicycle) 타깃, logical action matrix A·syndrome height 개념이 classical binary NAND LDPC에 없음 |
| 추가확인 | 없음 (BP는 min-sum 서브루틴이나 상위 디코더가 qLDPC 전용이라 이식 대상 아님) |

> 총평: 양자 LDPC(qLDPC)/FT 회로용 최소무게 결정트리 디코더로, min-sum BP를 보조로 쓰나 문제구조(syndrome height, logical operator)가 NAND binary LDPC와 달라 이식성 하.

### B. 알고리즘 요약

1. 대상: check matrix `H`(희소)와 logical action matrix `A`로 정의되는 일반 qLDPC 코드/FT 회로 디코딩 — classical과 달리 `A`가 항등이 아님.
2. 문제: (i)범용 qLDPC (ii)최소무게 보장 (iii)poly(w) 최악시간을 모두 만족하는 디코더 부재; MaxSAT는 (ii) 되나 느리고, MWPM/union-find는 (i) 안 됨.
3. 핵심: Decision Tree Decoder(DTD) — syndrome `σ`에서 불만족 check의 이웃 fault를 하나씩 추가해 부분정정 경로(결정트리)를 탐색, `HF=σ`가 되면 종료.
4. Explore 서브루틴의 cost 함수가 알고리즘을 결정: breadth-first(느림) / syndrome-height oracle(`h(σ)`, 이상적).
5. 핵심식: `h(σ)=min_{F|HF=σ} w(F)` (syndrome height). 자식 syndrome에 대해 `h(σ'')≥h(σ')-w_j`, 최대 감소 branch가 최소무게 정정.
6. Provable 디코더(Height-bound DTD): 계산 가능한 `h(σ)` 하한(neighborhood bound)으로 cost `C=w(F)+h_min(σ)` 산정해 트리 가지치기, 최소무게 보장.
7. BP 정제: min-sum belief propagation을 tie-breaking에 사용해 탐색 효율↑ (`µ_{i→j}=(-1)^{σ_i}·∏sign·min|µ|`, LPR 가중치 `w_j=log((1-p_j)/p_j)`).
8. Heuristic 디코더(BP-DTD): BP로 DT 노드 cost 추정 후 depth-first 탐색, 비균일 fault 확률(회로 잡음) 수용, 최소무게 보장 없음.
9. 결과: color/bivariate bicycle 코드에서 median으로 weight-w 오류에 `w`개 노드만 탐색; gross code 회로잡음(p=1e-3)에서 BP-DTD가 BP-OSD보다 정확·빠름.
10. 한계: 순수 시뮬(FPGA는 향후 언급뿐), 양자 stabilizer/토폴로지 코드 특화, classical binary LDPC/NAND 실험 전무.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| min-sum BP 서브루틴 | decoder.cpp CNU_Update_New_Mag() | min1/min2·sign은 유사하나 우리 이미 보유, 신규성 없음 |
| Decision Tree/syndrome-height 탐색 | 대응 없음 | 반복 message-passing이 아닌 트리 탐색+logical action, NAND 디코더와 이질적 |
| logical action matrix A / stabilizer 등가 | 대응 없음 | classical binary LDPC에 A=항등이라 해당 개념 없음 |

적용 가치: 낮음 — 양자 qLDPC/FT 회로용 최소무게 디코더로, min-sum BP만 공통이나 그마저 이미 보유(§3), 상위 결정트리 알고리즘은 NAND binary QC-LDPC에 이식 대상이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2502.16408v1",
  "title": "Decision-tree decoders for general quantum LDPC codes",
  "year": 2025,
  "venue": "arXiv quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "qLDPC용 Decision Tree Decoder(DTD): syndrome height 하한으로 트리 가지치기, 최소무게 정정 보장 provable 디코더 + BP-DTD heuristic",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "양자 stabilizer/CSS 코드(color/bivariate bicycle) 타깃, logical action matrix A·syndrome height 개념이 classical binary NAND LDPC에 없음",
  "todo_check": "없음 (BP는 min-sum 서브루틴이나 상위 디코더가 qLDPC 전용이라 이식 대상 아님)"
}
```
