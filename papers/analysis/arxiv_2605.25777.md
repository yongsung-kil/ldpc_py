### arxiv:2605.25777v1 - Best-First Ordered Statistics Decoding of Quantum LDPC Codes (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 72~288 |
| 연판정 | soft-4bit+ |
| 핵심기여 | null-space generator의 XOR 조합을 cost 오름차순으로 탐색하는 Best-First OSD(BF-OSD)를 제안하고, BP를 수렴까지 돌리지 않고 소수 iteration 후 바로 OSD를 호출하는 방식으로 OSD-CS 대비 1/100 query budget으로 동등 성능 달성 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | Quantum CSS code(BB codes) 전용 실험이며 syndrome decoding(코드워드 아닌 오류패턴+논리연산자 동치) 문제; classical LDPC 적용 시 OSD 자체의 높은 계산복잡도(Gaussian elimination, O(r^2 N))가 NAND 실시간 디코더에 부담 |
| 추가확인 | Prime ECC의 조기종료(Partial CRC) 실패 시 fallback post-processing으로 BF-OSD 스타일의 best-first null-space 탐색이 실현 가능한 복잡도인지, min-sum 근사 하에서의 성능(논문도 future work로 명시) |

> 총평: OSD 탐색 순서를 cost 기반 best-first로 개선하고 BP 수렴 조건 없이 소수 iteration만으로 결합하는 디코더 후처리 아이디어로, quantum 전용이지만 OSD 자체는 classical LDPC의 error-floor 대책으로 general하여 이식 검토 여지가 있음(단 GE 기반 OSD의 HW 복잡도가 관건).

### B. 알고리즘 요약

1. 대상은 QLDPC(CSS, Bivariate Bicycle codes) 코드이며 full circuit-level noise 하에서 syndrome decoding을 수행, 표준 파이프라인은 BP 실패 시에만 OSD를 호출하는 cascade 구조.
2. 풀려는 문제: 기존 OSD-w/OSD-CS는 사전에 정해진 저신뢰 비트 부분집합만 brute-force 열거해 비효율적이고, circuit-level noise에서는 Tanner graph에 4-cycle이 많아 BP가 수렴하지 못해 conditional invocation이 비효율적.
3. 핵심 가정: circuit-level fault는 spatio-temporal decoding matrix `H_dec`로 모델링되며 동일 (syndrome, logical effect) tuple을 갖는 fault는 병합(`p(d,ℓ)=Σp_f`), degeneracy로 인해 stabilizer 차이만 나는 오류는 모두 등가.
4. 핵심 기법 1단: OSD-0로 `H_dec`의 열을 LLR 기준 정렬 후 Gaussian Elimination으로 pivot/free set을 나누고 `E_base`를 구함(`H_dec·E_base=s`), 이는 matroid 이론상 최소비용 pivot을 선택하는 greedy 최적해(Appendix Theorem 1로 증명).
5. 핵심 식: 해공간은 `{e: H_dec·e=s} = E_base ⊕ ker(H_dec)`인 affine coset이며, free column마다 null-space generator `g_j`를 만들고 cost `cost(e)=Σ_{i:e_i=1}|Λ_i|`를 최소화할 조합을 탐색.
6. 핵심 기법 2단(BF-OSD): generator들의 XOR 조합(부분집합 T⊆F)을 priority queue 기반 best-first search로 비용 증가 순 탐색, 자식 비용은 증분(incremental) 계산, query budget Q 소진 시 종료(anytime, Q→2^k에서 coset ML과 일치).
7. 구현 디테일: BP를 수렴까지 돌리지 않고 소수 iteration만 수행(flooding 대신 serial/sequential schedule 사용해 동일 복잡도로 정보 전파 가속), confidence-based column ordering(pre-flip으로 모든 LLR을 비음수화)이 OSD-0 baseline 품질을 개선.
8. 별도 학습 절차 없음(고정 알고리즘, 탐색 순서만 재설계).
9. 결과: 5종 BB code(`[[72,12,6]]`~`[[288,12,18]]`)에서 p=10^-3 circuit-level noise 하 pL이 BP+OSD-CS 베이스라인과 대등(예: `[[144,12,12]]`에서 2.38×10^-7 vs 2×10^-7)하면서 query budget은 1/100 수준으로 감소.
10. 한계: quantum syndrome decoding 전용 실험(순수 시뮬레이션, HW 미설계)이며 min-sum 근사 하 성능, column ordering의 영향 등은 future work로 남김; OSD의 GE 기반 복잡도(`O(r²N)`)는 실시간 HW 디코더에는 부담.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BP 소수 iteration 후 OSD 호출(조건부 대신 항상 호출) | `decoder.cpp` `LDPC_Decoder()` 이터레이션 루프 | Prime ECC의 조기종료(Partial CRC)와 유사한 "언제 fallback을 호출할지" 설계 문제이나, OSD 자체가 min-sum 반복 대신 GE 기반이라 구조가 다름 |
| BF-OSD (best-first null-space coset 탐색) | 대응 없음 | Prime ECC는 min-sum 반복 디코더로 OSD/GE 기반 list-decoding 모듈이 없음; error-floor 대책으로 신규 도입 시 별도 HW 블록 필요 |
| serial(sequential) BP schedule | `decoder.cpp` `LDPC_Decoder()`, Dual-Update 스케줄 | Prime ECC도 이미 Dual-Update(parity even/odd 교대) 스케줄을 보유해 개념적으로 유사하나 논문의 sequential update는 전체 순차 방식으로 세부 구현 상이 |
| confidence-based column ordering / LLR pre-flip | `channel.cpp` `Set_LLR_Th()`, `decoder.h` `Get_VNU_*` | LLR 부호/크기 기반 정렬 개념은 참고 가능하나 Prime ECC는 quantization 테이블 기반이라 직접 대응은 아님 |

적용 가치: **중간** — Quantum QLDPC 전용 실험이지만 OSD는 classical LDPC error-floor 대책으로도 잘 알려진 기법이며, "BP 조기 중단 + post-processing 호출" 설계 철학은 Prime ECC의 조기종료·post-processing 방향과 유사함. 다만 OSD/GE 자체가 min-sum 반복 HW 구조와 이질적이라 실제 이식은 알고리즘 차용 수준(HW 재설계 필요)에 그침.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.25777v1",
  "title": "Best-First Ordered Statistics Decoding of Quantum LDPC Codes",
  "year": 2026,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "72~288",
  "soft_quant": "soft-4bit+",
  "key_contribution": "null-space generator XOR 조합을 cost 오름차순으로 탐색하는 Best-First OSD(BF-OSD) 제안, BP 수렴 대기 없이 소수 iteration 후 항상 OSD 호출해 OSD-CS 대비 1/100 query budget으로 동등 성능 달성",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "중",
  "caveat": "Quantum CSS(BB codes) syndrome decoding 전용 실험이며 OSD의 Gaussian elimination 기반 복잡도(O(r^2 N))가 NAND 실시간 HW 디코더에는 부담",
  "todo_check": "Prime ECC의 Partial CRC 실패 후 fallback으로 BF-OSD 스타일 best-first 탐색이 실현 가능한 HW 복잡도인지, min-sum 근사 하 성능(논문 future work)"
}
```
