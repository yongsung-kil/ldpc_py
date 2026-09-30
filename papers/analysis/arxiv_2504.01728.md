### arxiv:2504.01728v1 - Linear Time Iterative Decoders for Hypergraph-Product and Lifted-Product Codes (2025, arXiv preprint / cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 600~1054 |
| 연판정 | 무관 |
| 핵심기여 | HP/LP 양자부호의 stabilizer-induced TS와 classical TS를 특성화하고, 구성 classical LDPC 디코더로부터 병렬 TS-회피 BF/min-sum 디코더를 도출해 error-floor 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | 부분 |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | HP/LP 양자 CSS 부호(qubit degeneracy/QTS) 전용, depolarizing 채널·완전 syndrome 가정, HW·soft-read 없음 |
| 추가확인 | "classical LDPC의 TS-회피 디코더를 곱부호에 상속" 및 VV/CC 교대 스케줄 아이디어가 고전 binary LDPC min-sum error-floor 대책으로 유효한지 |

> 총평: 양자 HP/LP 부호의 trapping-set 회피 디코더 설계 논문으로 NAND binary LDPC 직접 이식은 불가하나, "부호 구조에서 TS 열거→bias 조정으로 회피"라는 디코더 다이버시티 방법론만 개념 참고 가치.

### B. 알고리즘 요약

1. 대상은 양자 LDPC(QLDPC)의 HP(hypergraph-product)/LP(lifted-product) CSS 부호, 채널은 depolarizing(확률 p), syndrome 완전(circuit-level 아님) 가정.
2. 풀려는 문제: iterative MP 디코더가 QLDPC에서 error floor 높음 - 원인은 (1) stabilizer-induced TS(QTS)와 (2) 구성 classical 부호에서 상속된 classical TS.
3. 핵심 모델: HP 부호는 두 classical Tanner 그래프의 곱 `HX=[H1⊗I | I⊗H2^T]`, `HZ=[I⊗H2 | H1^T⊗I]`, LP는 이를 circulant lifting(`WX,WZ`)으로 일반화.
4. TS 분석: bit-flipping 디코더로 stabilizer generator(및 그 선형결합)가 유도하는 subgraph에서 VV-type/CC-type 변수노드 대칭 때문에 오류추정이 진동(Lemma 1,2).
5. 핵심 도구: 체크노드를 생략하고 unsatisfied check 수를 셀 수 있는 concise representation + Brook 정리 기반 labeling(property 1~3)으로 최대 4개 generator 결합 subgraph가 TS임을 증명(Theorem 1).
6. QTS 회피 디코더(Algorithm 2): VV-type과 CC-type 변수노드를 같은 iteration에 동시 갱신하지 않고 교대 갱신 → dv,dc 홀수(>2)면 stabilizer-induced 오류 전부 정정(Theorem 2), 짝수차수는 랜덤 flip 보정.
7. LP 확장: lifting이 base graph의 TS 구조를 보존(Lemma 4,5)하므로 HP 결론이 LP로 이월; 곱연산으로 classical TS가 다수 복제(Lemma 6,7).
8. 디코더 다이버시티(Section VII): D1은 QTS 회피용 교대 스케줄 min-sum, 나머지는 classical TS별로 bias `b(e)` 조정한 min-sum, 병렬 실행 후 최소 Hamming weight 추정 채택.
9. 결과: `[[1054,140,20]]` LP 부호에서 디코더 5개(QTS 1 + classical TS 4, 각 20 iter) 병렬로 normalized min-sum(100 iter) 대비 error floor 대폭 개선; `[[600,40,20]]`는 logical error rate 약 1자릿수 감소.
10. 한계: syndrome 완전 가정(circuit-level noise 미포함, future work), HW 미설계, depolarizing 시뮬만.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| min-sum 디코더 갱신규칙 | decoder.cpp `LDPC_Decoder()`, `CNU_Update_New_Mag()` | Min-Sum 자체는 이미 보유, VV/CC 교대 스케줄(Dual-Update 유사) 개념만 부분 참고 |
| bias/normalization 조정 | decoder.cpp `LDPC_Decoder()` | edge별 bias로 TS 회피, Prime ECC의 적응형 LLR 테이블과 개념 유사하나 양자 TS 전용 |
| HP/LP 곱부호 H-matrix 구성 | ecc_top.cpp `Load_PCM()` | 양자 CSS 곱부호라 binary QC-LDPC 로더와 개념 불일치, 직접 이식 불가 |
| stabilizer-induced/classical TS 열거 | 대응 없음 | Prime ECC는 QC-LDPC 고정, TS 열거·다이버시티 디코더 미보유 |

적용 가치: **낮음** — 양자 HP/LP CSS 부호의 degeneracy(QTS) 전용 디코더로 HW 미설계·depolarizing 시뮬뿐이라 NAND binary QC-LDPC 직접 이식 요소는 없다. TS 회피 디코더 다이버시티 방법론만 원리 수준 참고.

### D. JSON 블록

```json
{
  "id": "arxiv:2504.01728v1",
  "title": "Linear Time Iterative Decoders for Hypergraph-Product and Lifted-Product Codes",
  "year": 2025,
  "venue": "arXiv preprint (cs.IT)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "600~1054",
  "soft_quant": "무관",
  "key_contribution": "HP/LP 양자부호의 stabilizer-induced TS와 classical TS를 특성화하고, 구성 classical LDPC 디코더로부터 병렬 TS-회피 BF/min-sum 디코더를 도출해 error-floor 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "부분",
  "latency": "개선",
  "recommend": "하",
  "caveat": "HP/LP 양자 CSS 부호(qubit degeneracy/QTS) 전용, depolarizing 채널·완전 syndrome 가정, HW·soft-read 없음",
  "todo_check": "classical LDPC의 TS-회피 디코더를 곱부호에 상속 및 VV/CC 교대 스케줄 아이디어가 고전 binary LDPC min-sum error-floor 대책으로 유효한지"
}
```
