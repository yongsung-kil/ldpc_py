### arxiv:2512.02941v1 - Pseudocodewords of Quantum, Quasi-Cyclic, and Spatially-Coupled LDPC Codes: A Fundamental Cone Perspective (2025, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 성분코드로부터 합성된 코드의 pseudocodeword를 fundamental cone의 곱 구조·생성함수로 특성화 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 LP/graph-cover 이론(fundamental cone 구조 분석)뿐, 디코더·HW·NAND 실험 전무 |
| 추가확인 | pseudocodeword 열거가 QC-LDPC error-floor(trapping-set) 진단에 실무적으로 쓸 수 있는지 |

> 총평: LP 디코딩 pseudocodeword의 fundamental cone 곱 구조를 CSS/QC/SC-LDPC에 적용한 순수 이론 논문으로 NAND binary QC-LDPC ECC 이식 가치는 낮음.

### B. 알고리즘 요약

1. 대상은 binary linear code의 LP 디코딩과 graph-cover 디코딩에서 나타나는 pseudocodeword 구조 분석(부호 rate/length는 특정하지 않음).
2. 문제: iterative/LP 디코더는 pseudocodeword 때문에 codeword가 아닌 vertex로 수렴해 실패할 수 있어, 이를 parity-check matrix `H` 표현과 연결해 이해하려 함.
3. 모델: relaxed polytope `R(H) = ∩_j poly(C(Row_j(H)))`와 fundamental cone `K(H) = {v∈R≥0^n : Row_j(H)·v ≥ 2h_{ji}v_i}` 정의(Def 6).
4. 핵심 정리(Thm 7): `p∈P(H)` (graph-cover pseudocodeword) ⇔ `p∈K(H)` 이고 `Hp^T=0 mod 2`.
5. 블록 결합 정리: 행 적층 시 `K(H)=∩K(H_ℓ)` (Lemma 8), 블록대각 시 `K/P/생성함수`가 곱으로 분해(Thm 9), 열 결합 시 곱이 부분집합으로 포함(Thm 10).
6. 생성함수 `f_H(x)=Σ_{p∈P(H)} x^p`로 pseudocodeword 집합을 다변수 다항식으로 압축 표현(cycle code의 edge zeta function 관점 확장).
7. 양자 적용(4.1): stabilizer code를 label code(A(S), N(S))로 환원, CSS `H=diag(H1,H2)`에 Thm 9 적용해 `P(H)=P(H1)×P(H2)`.
8. QC 적용(4.2): 순환 구조를 이용, `K(H)`가 circulant 블록 `K(J_{j,i})`의 곱을 포함(Cor 18), quasi-cyclic shift가 LP 성공/실패에 무관(Thm 21).
9. 결과: Steane code(7,4,3 Hamming 기반) 예에서 Polymake로 42 edge·96 vertex 계산, redundant 저중량 dual 행 추가로 non-codeword pseudocodeword 제거하는 알고리즘 제시.
10. 한계: 전면 이론(HW·시뮬·BER 없음), MDPC/BIKE·기타 Q-LDPC 적용은 open problem으로 남김.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| LP/graph-cover pseudocodeword 이론 | 대응 없음 | Prime ECC는 min-sum 메시지 패싱 기반, LP 디코더 미구현 |
| QC-LDPC circulant 블록 구조 분석 | ecc_top.cpp `Load_PCM()` | H-matrix 구조 참조 접점이나 이론뿐이라 이식 실익 없음 |
| redundant 행 추가로 LP 성능 개선 | 대응 없음 | LP 디코더 전제라 min-sum 파이프라인에 무관 |
| fundamental cone/생성함수 열거 | 대응 없음 | pseudocodeword 열거는 error-floor 진단 도구일 뿐 디코더 로직 아님 |

적용 가치: **낮음** — LP·graph-cover 순수 이론이며 Prime ECC의 min-sum 디코더/HW 어디에도 직접 이식할 코드 레이어가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2512.02941v1",
  "title": "Pseudocodewords of Quantum, Quasi-Cyclic, and Spatially-Coupled LDPC Codes: A Fundamental Cone Perspective",
  "year": 2025,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "성분코드로부터 합성된 코드의 pseudocodeword를 fundamental cone의 곱 구조·생성함수로 특성화",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 LP/graph-cover 이론(fundamental cone 구조 분석)뿐, 디코더·HW·NAND 실험 전무",
  "todo_check": "pseudocodeword 열거가 QC-LDPC error-floor(trapping-set) 진단에 실무적으로 쓸 수 있는지"
}
```
