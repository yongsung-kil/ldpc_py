### arxiv:2503.14058v1 - Strongly regular generalized partial geometries and associated LDPC codes (2025, arXiv preprint / math.CO)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | regular |
| 부호rate | 0.875 |
| 부호length | 648 |
| 연판정 | 무관 |
| 핵심기여 | grade-r 강정규 일반화 부분기하(SRPG)를 정의하고 PG(2,q)/PG(3,q) 이차곡면으로 구성해 최소거리/차원/girth 하한을 갖는 정규 binary LDPC 부호 유도 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 조합론적 구성법(QC/circulant 구조 아님), q=3 단일 사례만 BER 비교, HW/양자화/스케줄 언급 전무 |
| 추가확인 | SRPG incidence 행렬이 NAND용 고rate QC-LDPC로 재구성 가능한지(circulant lifting 가능 여부) |

> 총평: 유한기하 기반 정규 LDPC 구성법 논문으로 이론적 최소거리/girth 하한이 강점이나 QC-LDPC 구조·HW·soft-read가 없어 NAND Prime ECC 이식성은 낮음.

### B. 알고리즘 요약

1. 대상은 유한기하(부분기하)에서 유도한 정규 binary LDPC 부호, 채널은 AWGN, 디코더는 sum-product(최대 1000 iter).
2. 풀려는 문제: partial geometry / (α,β)-geometry를 일반화해 더 넓은 구조에서 좋은 최소거리·girth 하한을 갖는 구조적 LDPC 부호를 만드는 것.
3. 핵심 정의: grade-r 강정규 일반화 부분기하 `SRPG(s,t;α1,...,αr;λ,µ)` — 임의 점-블록 쌍에서 결합 점 수가 `{α1,...,αr}` 중 하나, 점그래프가 강정규.
4. 구성 1: PG(2,q)의 conic(이차곡선)으로 `(P1,C1)` incidence 행렬 `M1` (`(q-1)^2 x (q-1)^2`), grade-3 `PG(q-3,q-3;q-5,q-4,q-3)` 얻음.
5. 구성 2: PG(3,q)의 hyperbolic quadric로 `(L1,H1)` incidence 행렬 `M2` (`q^4 x q^4(q^2-1)`), `PG(q-1,q(q^2-1)-1;q-2,q-1,q)`.
6. LDPC 부호 `C(M)`는 `(s+1,t+1)`-정규, 차원은 `n - rank2(M)`; 강정규그래프 고유값 `k,u1,u2`로 `MM^T` 스펙트럼 유도.
7. 최소거리: Tanner의 bit/parity-oriented 고유값 하한(식 10,11)을 `s,t,λ,µ,∆`로 표현(Theorem 4.2).
8. 2-rank: Brouwer의 p-rank 결과로 `rank2(M)` 하한 도출, `M2`는 MAGMA로 q=3,5,7에서 81/625/2401 확인 후 `q^4` 추측.
9. girth: `αi≥2`면 girth 6 존재, 6-cycle 개수 정확히 `ns(s+1)(λ-s+1)/6` (Theorem 4.5).
10. 결과/한계: q=3 `SRPG(2,23;1,2,3;27,30)`의 (3,24)-정규 부호(rate 0.875, 길이 648)가 동길이 랜덤부호보다 BER 낮음. HW 미설계, 시뮬 1건, 양자화·병렬화 언급 없음.

### C. Prime ECC 관련 모듈 핀포인트

대상이 `code-design`이므로 C섹션 디코더 성능 항목은 해당 없음. 모듈 대응만 참고.

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SRPG incidence 행렬 = H-matrix 구성 | ecc_top.cpp `Load_PCM()` | H-matrix 로더에 닿지만 QC/circulant 구조 아니어서 base+shift 형식과 불일치 |
| 최소거리/girth 하한 이론 | 대응 없음 | Prime ECC는 QC-LDPC 고정, 유한기하 구성법 미보유 |
| sum-product 디코딩 | decoder.cpp `LDPC_Decoder()` | Prime ECC는 min-sum 채택(full-tanh SP 미보유), 직접 대응 없음 |

적용 가치: **낮음** — 유한기하 순수 구성법으로 QC-LDPC 형식·HW·soft-read가 없어 NAND binary QC-LDPC 파이프라인에 떼어 쓸 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2503.14058v1",
  "title": "Strongly regular generalized partial geometries and associated LDPC codes",
  "year": 2025,
  "venue": "arXiv preprint (math.CO)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "regular",
  "code_rate": 0.875,
  "code_length": "648",
  "soft_quant": "무관",
  "key_contribution": "grade-r 강정규 일반화 부분기하(SRPG)를 정의하고 PG(2,q)/PG(3,q) 이차곡면으로 구성해 최소거리/차원/girth 하한을 갖는 정규 binary LDPC 부호 유도",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 조합론적 구성법(QC/circulant 구조 아님), q=3 단일 사례만 BER 비교, HW/양자화/스케줄 언급 전무",
  "todo_check": "SRPG incidence 행렬이 NAND용 고rate QC-LDPC로 재구성 가능한지(circulant lifting 가능 여부)"
}
```
