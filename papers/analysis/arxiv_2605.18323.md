### arxiv:2605.18323v1 - Existence and Counting Bounds for High-Memory Spatially-Coupled Codes via the Combinatorial Nullstellensatz (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | Combinatorial Nullstellensatz와 Alon–Füredi 정리로 SC-LDPC protograph edge-spreading의 4-cycle/6-cycle 제거를 위한 memory 하한과 feasible assignment 개수의 존재/카운팅 bound를 도출 |
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
| 한계,주의 | 순수 비구성적(nonconstructive) 결과로 실제 구성 알고리즘이 제시되지 않으며 fully-connected base graph에 한정됨 |
| 추가확인 | 후속 preprint에서 제공한다는 CLLL/MT bound와의 상세 비교(동일 저자 [33])가 이식성 판단에 참고될 수 있는지 |

> 총평: 대수적 조합론 기반의 순수 이론 논문으로 HW/디코더/NAND와 무관하며 Prime ECC 이식 가치는 낮음.

### B. 알고리즘 요약

1. Type-I SC-LDPC 코드는 (γ,κ) fully-connected base matrix `H`를 m+1개 component matrix `{H0,...,Hm}`로 분할(edge-spreading)해 구성하며, 분할 패턴은 partition matrix `P(i,j)=l`로 기록된다.
2. 문제의식: 유한 길이 SC-LDPC 성능은 Tanner graph의 짧은 harmful cycle(4-cycle, 6-cycle 등)에 좌우되는데, 기존 CLLL/Moser-Tardos 기반 구성적 프레임워크는 bound가 느슨하다.
3. 채널/노이즈 모델 없이 순수 조합론적 문제로 환원: cycle 활성화 조건 `Σ P(ik,jk) = Σ P(ik,jk+1)`을 다변수 다항식의 vanishing 조건으로 인코딩.
4. 핵심 기법 1단: Combinatorial Nullstellensatz(그리드 형태, Lemma 2)를 적용해 각 cycle의 다항식 `l_c(x)`들의 곱 `L_T*(x)`가 그리드 위에서 0이 아닐 충분조건을 도출.
5. 핵심 식 `m ≥ mt ≥ W_H^hit`(Theorem 1) — cycle hitting set의 최대 edge load(`W_H^hit`)보다 큰 memory면 모든 harmful structure를 깨는 edge-spreading이 존재.
6. 확장: 4-cycle 전부 제거 시 `m ≥ (γ-1)(κ-1)`(girth≥6, Corollary 2), 4·6-cycle 동시 제거 시 `m ≥ (γ-1)(γ-2)(κ-1)(κ-2)+(γ-1)(κ-1)`(girth≥8, Corollary 3).
7. 구현 디테일: `P(i,j)=ij`라는 명시적(explicit) 할당으로 4-cycle bound를 실제 달성 가능함을 증명(Remark 1).
8. 최적화 절차: Alon–Füredi 정리(Lemma 3, 4)를 이용해 조건을 만족하는 edge-spreading assignment의 개수 하한(Theorem 2, Corollary 4)을 도출.
9. 결과: 3×5 base graph 예제에서 제안 bound는 m=8인 반면 CLLL/MT는 각각 m=35, m=37 필요 — 동일 조건에서 feasible assignment 수는 최대 10^13배 차이.
10. 한계: 비구성적(nonconstructive) 결과이며 실제 코드 탐색 알고리즘 미제공, fully-connected base graph로 한정, trapping/absorbing set 등 더 큰 구조로의 확장은 future work.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| protograph edge-spreading / partition matrix 설계 | `ecc_top.cpp` `Load_PCM()` | Prime ECC는 특정 QC-LDPC H-matrix 고정이며 SC-LDPC 자체가 아니어서 직접 적용 불가 |
| cycle-hitting-set 기반 memory bound | 대응 없음 | Prime ECC는 non-coupled QC-LDPC이며 memory/coupling 개념 없음 |
| 4-/6-cycle 제거 존재·카운팅 정리 | 대응 없음 | 이론적 존재성 증명일 뿐 실제 H-matrix 생성 알고리즘 없음 |

적용 가치: **낮음** — SC-LDPC(convolutional coupling) 전용 이론 결과이며 Prime ECC는 non-coupled QC-LDPC 고정 부호이므로 부호설계 레이어조차 직접 대응되지 않고, 구성 알고리즘도 제공되지 않아 실이식 불가.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.18323v1",
  "title": "Existence and Counting Bounds for High-Memory Spatially-Coupled Codes via the Combinatorial Nullstellensatz",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "Combinatorial Nullstellensatz와 Alon–Füredi 정리로 SC-LDPC protograph edge-spreading의 4-/6-cycle 제거 memory 하한과 feasible assignment 개수 bound 도출",
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
  "caveat": "비구성적 결과로 실제 구성 알고리즘 미제공, fully-connected base graph에 한정",
  "todo_check": "동일 저자 후속 preprint의 CLLL/MT bound 상세 비교가 이식성 판단에 추가 참고될 수 있는지"
}
```
