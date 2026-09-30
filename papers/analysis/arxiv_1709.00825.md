### arxiv:1709.00825v1 - Lower bounds on the lifting degree of single-edge and multiple-edge QC-LDPC codes by difference matrices (2017, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 16~156 |
| 연판정 | 무관 |
| 핵심기여 | difference matrix `D`,`DD` 도입으로 girth 6/8/10/12 조건과 lifting degree 하한을 유도, 탐색 복잡도 축소 |
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
| 한계,주의 | girth/lifting-degree 순수 조합론 결과, BER·디코더·HW 검증 전무, 소길이 예제뿐 |
| 추가확인 | 없음 (정정능력·복호성능 언급 없음) |

> 총평: QC-LDPC exponent matrix의 girth 최적화·lifting degree 하한을 difference matrix로 다루는 순수 부호설계 이론으로, 고rate NAND ECC의 특정 QC-LDPC를 대체할 이식 가치는 낮음.

### B. 알고리즘 요약

1. 대상은 base(protograph) matrix를 CPM으로 lifting한 **single-edge/multiple-edge QC-LDPC** 부호이며, `N`=lifting degree, exponent matrix `B=[Bij]`로 표현.
2. 풀려는 문제: girth를 키우면서 최단 길이(=최소 `N`)를 얻는 QC-LDPC 구성의 탐색 복잡도가 Fossorier's Lemma로는 너무 큼.
3. 핵심 도구는 **difference matrix** `D` (행 간 exponent 차) 와 `DD` (D 원소쌍 차, 크기 `C(m,2)×C(n,2)`) 두 행렬 (Def 1,2).
4. 핵심 기법 1: cycle 존재조건(식(3))을 `D`,`DD` 언어로 재서술 — 4-cycle-free ⟺ `DD`에 zero 없음(Cor 1), 6/8/10-cycle 조건을 Lemma 1~6·Theorem 1,3로 특성화.
5. 핵심 식: 8-cycle-free ⟺ `2DD` zero 없음 + `DD` 중복 없음 + 4×4 submatrix `Dij0−Di'j1−Di''j2−Di'''j3≠0` (Theorem 1).
6. 핵심 결과 2: 첫 행·열이 all-zero인 exponent matrix에서 8-cycle 부재가 (첫 행 관련) 6-cycle 부재를 보장(Cor 3,4) → girth 10 탐색 시 3×3 submatrix 검사 생략.
7. 부수 결과: girth 10 lifting degree 하한 `N ≥ 2·C(n,2)·C(m,2)+1` 로 기존 [8]보다 `C(m,2)/(m-1)`배 개선, girth 12는 `N≥|A|+C(m,2)n(n-1)+1`.
8. multiple-edge girth 6 하한 `N=max{A,B,C}` (Thm 6) 을 최초로 해석적으로 유도, tightness를 예제로 확인.
9. 결과(수치): (3,7)/(3,8) girth-10 부호를 `N=145/211`로 문헌값 159/219보다 축소, girth-10 non-isomorphic 부호 개수도 [2]보다 많음(n=5:4, n=6:2). 예제 부호 길이는 16~156.
10. 한계: 순수 조합론/그래프 이론, BER·디코더·gate count·HW 없음, 정정능력·복호성능 논의 없음.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| exponent/H-matrix 구성 (difference matrix 기반) | ecc_top.cpp Load_PCM() | H-matrix 로드 지점이나 우리 부호는 이미 고정, 재구성·재검증 부담 큼 |
| girth/lifting-degree 최적화 | 대응 없음 | 부호설계 이론 전용, 우리 QC-LDPC base+shift 고정과 무관 |
| CPM base matrix (base+shift) 표현 | ecc_data.h PCM_b (base+shift) | 표현 방식은 유사하나 논문은 저길이 girth 예제에 국한 |
```

마지막에 한 문장으로 **적용 가치**: `낮음` — Prime ECC는 이미 특정 고rate QC-LDPC를 고정(§4 부호설계 이식 난이도 높음)하고 있고, 본 논문은 저길이 girth 최적화 구성법·lifting degree 하한 이론이라 디코더/HW/복호성능 개선에 직접 닿지 않는다.

### D. JSON 블록

```json
{
  "id": "arxiv:1709.00825v1",
  "title": "Lower bounds on the lifting degree of single-edge and multiple-edge QC-LDPC codes by difference matrices",
  "year": 2017,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "16~156",
  "soft_quant": "무관",
  "key_contribution": "difference matrix D,DD 도입으로 girth 6/8/10/12 조건과 lifting degree 하한 유도 및 탐색 복잡도 축소",
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
  "caveat": "girth/lifting-degree 순수 조합론 결과, BER·디코더·HW 검증 전무, 소길이 예제뿐",
  "todo_check": "없음 (정정능력·복호성능 언급 없음)"
}
```
