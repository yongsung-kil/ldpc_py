### arxiv:2112.01647v1 - Explicit Abelian Lifts and Quantum LDPC Codes (2021, arXiv cs.DS)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호rate | 미상 |
| 부호length | 미상 |
| 부호종류 | QC-LDPC |
| 연판정 | 무관 |
| 핵심기여 | abelian (H,ℓ)-lift로 near-Ramanujan 확장그래프를 explicit 구성, Panteleev-Kalachev qLDPC 및 quasi-cyclic LDPC를 derandomize |
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
| 한계,주의 | 확장그래프 explicit 구성(trace power/DFS 인코딩)이 본체, 복호기·유한길이 BER·HW 전무, 양자/circulant size 이론 결과 |
| 추가확인 | derandomize된 circulant size 제어가 실제 QC-LDPC 부호행렬 설계에 활용 가능한지 (실용화 여지) |

> 총평: QC-LDPC/qLDPC 부호 구성에 쓰이는 확장그래프의 explicit(비무작위) 구성을 다루는 순수 그래프이론·부호이론 논문으로, NAND binary LDPC 디코더/HW 이식 관점의 실체가 없어 이식가치 낮음.

### B. 알고리즘 요약

1. 대상: base expander `G0`에 abelian 군 `H⊆Sym(ℓ)`의 `(H,ℓ)`-lift로 얻는 `d`-정규 확장그래프의 explicit(결정론적 다항시간) 구성.
2. 문제: 기존 near-Ramanujan lift 구성(MOP20의 2-lift)은 큰 lift size `ℓ`에서 walk counting이 붕괴, qLDPC/quasi-cyclic 부호의 explicit화가 미해결.
3. 모델: signed non-backtracking operator `Bs(χ)`의 spectral radius `ρ(Bs)`를 trace power method로 bound → 확장성 판정.
4. 핵심기법: singleton-free hike(닫힌 walk) 개수를 DFS traversal history로 압축 인코딩하는 새 counting으로 큰 `ℓ`까지 spectral bound 유지.
5. 핵심 식: `ρ(Bs)^{2k} ≤ tr((Bs*)^k Bs^k)`, hike 개수를 `(√(d-1))^{2k}` 규모로 억제해 `λ(G) ≤ 2√(d-1)+ε` 달성.
6. 확장: exact-exponential regime(`ℓ=exp(Θ(n))`)은 Bilu-Linial의 expander mixing lemma 역을 이용한 간단 증명(Thm 1.3).
7. 구현 디테일: ε-biased distribution(Jalan-Moshkovitz)으로 random signing을 derandomize, degree-2 정점 압축으로 near-Ramanujan 확보.
8. 최적화: 학습 없음, 순수 조합론·스펙트럼 논증.
9. 결과(Corollary 1.5): explicit quasi-cyclic LDPC(circulant size ~`N/polylog`), explicit qLDPC(distance `Ω(N/log N)`, dim `Ω(log N)`) — 유한길이 시뮬/BER 없음.
10. 한계: 부호 구성용 그래프의 explicit화가 전부 — 복호기·HW·유한길이 성능·양자화 없음, cs.DS 이론 논문.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| abelian lift 확장그래프 구성 | 대응 없음 | Ramanujan/Cayley 그래프 이론, 우리 고정 QC 구조 `Load_PCM()`과 무관 |
| quasi-cyclic LDPC 부호 도출 (corollary) | `ecc_top.cpp` `Load_PCM()` (원거리) | QC-LDPC 부호행렬 개념만 공유, circulant size 제어는 이론적 |
| qLDPC / CSS 부호 | 대응 없음 | 양자 부호, binary QC-LDPC ECC와 무관 |
| trace power / DFS 인코딩 증명 | 대응 없음 | 순수 스펙트럼 분석, 복호·HW 무관 |

적용 가치: **낮음** — 부호 구성에 쓰이는 확장그래프의 explicit 구성이라는 상위 이론이며, NAND binary QC-LDPC의 부호설계→디코더→HW 어느 레이어에도 떼어 쓸 구체 기법이 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2112.01647v1",
  "title": "Explicit Abelian Lifts and Quantum LDPC Codes",
  "year": 2021,
  "venue": "arXiv cs.DS",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": "미상",
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "abelian (H,ℓ)-lift로 near-Ramanujan 확장그래프를 explicit 구성, Panteleev-Kalachev qLDPC 및 quasi-cyclic LDPC를 derandomize",
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
  "caveat": "확장그래프 explicit 구성(trace power/DFS 인코딩)이 본체, 복호기·유한길이 BER·HW 전무, 양자/circulant size 이론 결과",
  "todo_check": "derandomize된 circulant size 제어가 실제 QC-LDPC 부호행렬 설계에 활용 가능한지 (실용화 여지)"
}
```
