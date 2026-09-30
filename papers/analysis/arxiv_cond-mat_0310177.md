### arxiv_cond-mat_0310177v1 - The polynomial error probability for LDPC codes (2003, arXiv cond-mat.stat-mech)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | regular |
| 부호rate | 미상 |
| 부호length | 50~10000 |
| 연판정 | 무관 |
| 핵심기여 | diagrammatic power-counting으로 앙상블 평균 block error의 다항항(atypical poor code 기여) 정확 평가 + short-loop 제거 linear-time expurgation 알고리즘 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 통계역학 이론(ML/MPM/TS 앙상블 평균, BSC 가정), QC 구조·HW·soft-read·BP 실복호 성능 전부 미다룸; `regular (2,d)` 부호는 나쁘다고 명시 |
| 추가확인 | short-loop 제거(swap) 알고리즘이 실제 QC-LDPC/구조적 부호에 girth 향상 도구로 유효한지, BP 실복호 error-floor와의 상관 |

> 총평: 앙상블 평균 block-error의 다항 스케일링을 diagram으로 유도하고 short-loop expurgation을 제안한 이론 논문. NAND용 특정 QC-LDPC 부호설계·복호·HW와 거리가 멀어 이식성 하.

### B. 알고리즘 요약

1. 대상: regular `(c,d,N)` LDPC 앙상블(N 메시지비트, `L=cN/d` 체크), BSC(flip rate `p`), ML 복호 위주(MPM/TS는 부록 B).
2. 문제: 앙상블 평균 block error `P_B`는 지수항(typical 부호)과 다항항(atypical poor 부호)의 합 → 저노이즈에서도 poor 부호가 O(1) 에러를 유발하는 다항 기여를 SM 관점에서 정량화·억제하려 함.
3. 핵심 아이디어: 낮은 codeword weight `w(x)` 발생을 bipartite graph의 "most dangerous diagram"(sub-graph) 출현과 1:1 대응시킴. admissible diagram = 각 edge가 `V_f`로부터 짝수 링크 수신.
4. power counting: `n_v`개 vertex·`n_e`개 edge diagram의 출현확률 `~ N^{n_v-(n_v c - n_e)}`. 최대화 조건 `n_e-(c-1)n_v` → 지배 diagram 식별.
5. 핵심 결과 스케일: `P_f(n_v*) ~ N^{n_v*(1-c/2)}` (식5). `c=2`면 `N^0`이라 무한 diagram → `P_B~O(1)` (즉 regular (2,d) 부호는 block-error 기준 매우 나쁨, 이후 `2<c<d` 가정).
6. 앙상블 정의: MB(다중링크 허용)=MLL-1, NML(다중링크 금지)=MLL-2, MLL-ℓ(길이 ℓ 미만 loop 전면 제거). 각각 `P_f` 폐형식(식7~10) 유도.
7. loop 통계: 기약 ℓ-loop 개수는 Poisson분포 `P_ℓ(k)≈λ_ℓ^k/k! e^{-λ_ℓ}`, `λ_ℓ=((c-1)(d-1))^ℓ/(2ℓ)` (식14). ℓ-loop(monopartite)=2ℓ-cycle(bipartite).
8. expurgation: MB 앙상블에서 length<ℓ loop 제거 시 축소인자 `exp(-Σλ_l)`=O(1). Gallager 이상적 expurgation(인자 1/2)보다 큰(sub-optimal) 앙상블.
9. 실용 알고리즘: (a) O(N) random regular code 생성 (b) walk 성장으로 ℓ-loop 탐지(vertex당 O(1)) (c) vertex/edge swap으로 loop 제거(loop당 typ. O(1)) → 전체 linear-time. `(3,4,10^4)` 시뮬에서 Poisson 이론과 일치, 다만 `~log N` 길이 loop는 제거 불가.
10. 한계: HW·QC 구조·soft-read 없음. BP 실복호가 아닌 ML/MPM/TS 앙상블 평균 이론. 다항항은 typical(지수) 성능과 별개.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| short-loop expurgation(부호 girth 개선) | ecc_top.cpp `Load_PCM()` | 부호 로드 지점이나 우리 QC-LDPC는 circulant 구조 고정 → random-swap expurgation 직접 적용 불가 |
| ML/MPM 앙상블 평균 error 이론 | 대응 없음 | Prime ECC는 특정 확정 부호 + min-sum 실복호. 앙상블 평균 이론은 부호 선정 근거로만 간접 참고 |
| loop/diagram 기반 error-floor 분석 | 대응 없음 | trapping-set/HW error-floor 대책 아님, BSC-ML 이론 |

적용 가치: **낮음** — regular 랜덤 앙상블 대상 순수 이론이며 QC-LDPC 구조 부호설계·min-sum 복호·HW·soft-read와 접점이 약하다. short-loop 회피의 일반 원칙만 참고 가치.

### D. JSON 블록

```json
{
  "id": "arxiv:cond-mat/0310177v1",
  "title": "The polynomial error probability for LDPC codes",
  "year": 2003,
  "venue": "arXiv cond-mat.stat-mech",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "regular",
  "code_rate": "미상",
  "code_length": "50~10000",
  "soft_quant": "무관",
  "key_contribution": "diagrammatic power-counting으로 앙상블 평균 block error 다항항 정확 평가 + short-loop 제거 linear-time expurgation",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 통계역학 이론(ML/MPM/TS 앙상블 평균, BSC), QC·HW·soft-read·BP 실복호 미포함; regular (2,d)는 나쁘다고 명시",
  "todo_check": "swap 기반 short-loop 제거가 구조적 QC-LDPC girth 향상에 유효한지, BP error-floor 상관"
}
```
