### arxiv:2111.03654v2 - Asymptotically Good Quantum and Locally Testable Classical LDPC Codes (2022, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 0~0.5 (classical), 0~1 (quantum) |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 비아벨군 lifted product로 asymptotically good qLDPC 및 constant-rate/locality LTC 존재 증명 |
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
| 한계,주의 | 순수 존재성 증명(asymptotic), non-binary Fq/양자 CSS 중심, HW·복호기·유한길이 성능 전무 |
| 추가확인 | binary F2 특수화 시 유한길이 QC-LDPC 부호로 실용화 가능한지 (후속 연구 필요) |

> 총평: qLDPC 추측을 증명한 이론적 이정표지만 NAND binary QC-LDPC ECC 이식 관점에서는 순수 구성법·존재성 증명에 그쳐 이식가치 없음.

### B. 알고리즘 요약

1. 대상은 constant rate·locality·거리를 갖는 classical LTC와 asymptotically good qLDPC 부호로, 비아벨군 `G` 위 lifted product 구성 `A ⊗_G B*`로 얻는다.
2. 문제: qLDPC 추측(constant rate·distance `d=Θ(n)`)과 c³-추측(classical LTC)이 오랫동안 미해결이었다.
3. 모델: (co)chain complex와 Tanner code를 homological algebra로 통합, `∂1∘∂2=0`인 3-term complex `C`에서 classical `ker ∂2`와 quantum CSS `Q(∂1,∂2*)`를 정의.
4. 핵심기법: 두 expander code `T(Γ;h)`, `T(Γ;h')`를 group algebra `R=F_qG` 위 tensor product로 lifting, `Γ`는 Ramanujan Cayley graph의 double-cover `Cay2(G,S)`.
5. 핵심 개념: `product-expansion`(local 코드쌍의 견고한 확장성)이 성립해야 거리 하한이 보장 — random linear code 쌍이 w.h.p. 이 성질을 만족함을 증명.
6. 확장: locally minimal (co)chain 개념을 local coefficient system을 가진 고차원 복합체로 일반화해 거리 하한/local testability 증명.
7. 구현 디테일: base graph `B_w`(bouquet)/`D_w`에 voltage assignment로 `G`-lift 생성, 비아벨 `G`(예 `PSL2(F_q)`)가 abelian 상한 회피에 필수.
8. 최적화: 별도 학습 없음, 순수 조합론적/스펙트럼 논증.
9. 결과: Theorem 1(classical LTC `[n, Rn, Θ(n)]`, `R∈(0,1/2)`), Theorem 2(qLDPC `⟦n, Rn, Θ(n)⟧`, `R∈(0,1)`) 존재성 증명. 유한길이 시뮬/BER 없음.
10. 한계: 순수 asymptotic 존재성 증명 — 복호기(bit-flip/small-set-flip은 언급뿐), HW, 유한길이 성능, 양자화 전무.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| lifted product 부호 구성 (`A ⊗_G B*`) | 대응 없음 | 비아벨군/양자 CSS 구성으로 binary QC-LDPC `Load_PCM()`과 무관 |
| classical LTC / product-expansion | 대응 없음 | local testability는 NAND ECC 복호와 무관 |
| expander/Tanner code 부호구조 | 대응 없음 | Ramanujan Cayley graph 기반, 우리 고정 QC 구조와 상이 |
| small-set-flip / bit-flip 복호 (언급) | 대응 없음 (`decoder.cpp` min-sum과 상이) | 논문은 복호기를 다루지 않음(추측 수준) |

적용 가치: **낮음** — 양자·non-binary·asymptotic 존재성 이론으로 NAND binary QC-LDPC의 부호설계→디코더→HW 어느 레이어에도 떼어 쓸 실체가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2111.03654v2",
  "title": "Asymptotically Good Quantum and Locally Testable Classical LDPC Codes",
  "year": 2022,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": "0~0.5(classical)/0~1(quantum)",
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "비아벨군 lifted product로 asymptotically good qLDPC 및 constant-rate/locality LTC 존재 증명",
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
  "caveat": "순수 존재성 증명(asymptotic), non-binary Fq/양자 CSS 중심, HW·복호기·유한길이 성능 전무",
  "todo_check": "binary F2 특수화 시 유한길이 QC-LDPC 부호로 실용화 가능한지 (후속 연구 필요)"
}
```
