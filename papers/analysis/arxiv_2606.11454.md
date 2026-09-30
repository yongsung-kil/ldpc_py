### arxiv:2606.11454v1 - Lifted Gabidulin Construction for LDPC Representations of Finite Geometry Codes (2026, arXiv (cs.IT))

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.4~0.99 |
| 부호length | 8~1024 |
| 연판정 | soft-4bit+ |
| 핵심기여 | finite geometry code의 dense incidence matrix를 pencil 기반으로 sparsify하는 문제를 lifted Gabidulin code로 명시적으로 해결 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | non-binary 대수구조(Gabidulin/rank-metric code, GF(q) 기반) 기반 구성법이라 binary QC-LDPC 이식에 근본적 제약 |
| 추가확인 | 특정 finite geometry(AG/PG) 부호가 Prime ECC의 고rate QC-LDPC 구조와 얼마나 호환 가능한지 |

> 총평: FG code용 sparse PCM 구성법(pencil selection + lifted Gabidulin)으로 이론적으로 흥미롭지만, 특정 대수적 부호족(Reed-Muller/FG code) 및 rank-metric code 기반이라 NAND 고전 binary QC-LDPC로의 이식성은 낮음.

### B. 알고리즘 요약

1. Finite geometry (FG) code: affine/projective geometry의 point-flat incidence matrix를 parity-check matrix로 쓰는 고전 대수적 부호(µ=0이면 4-cycle-free, µ≥1이면 dense+많은 4-cycle).
2. 문제: incidence matrix가 µ≥1일 때 dense하고 4-cycle이 많아 BP 디코딩에 부적합, 기존 PCRB 탐색 기반 sparsification은 blocklength 커지면 계산량 폭발.
3. 핵심 관찰: `pencil` (공통 µ-flat Π를 포함하는 모든 (µ+1)-flat 집합 `G(Π)`)을 이용하면 AVN(auxiliary variable node) 1개 추가로 cycle-free parity-check row block(PCRB) 생성 가능.
4. Pencil selection 문제: disjoint pencil들의 kernel `Π_1,...,Π_B`을 골라 (P1) 행 재사용 없음, (P2) `rank_F2(H_p)=rank_F2(H)` 만족.
5. 핵심 정리(Thm 1,2): pencil disjoint 조건이 kernel subspace 간 거리 `d_S(W_i,W_j)≥4` 조건으로 환원됨(affine은 예외조건 (5-2) 추가).
6. Constant-dimension subspace code로 kernel을 뽑기 위해 rank-metric MRD code인 `lifted Gabidulin code` 사용, `(n,n-1,2)` Gabidulin code를 lifting해 거리 조건 충족.
7. 구현 디테일: affine 기하에서는 offset `b(A)`를 zero/linear/nonlinear로 탐색해 rank 보존조건(P2) 만족시켜야 함(Thm 3: q>2에서 zero offset은 P2 실패).
8. 최적화 절차: length 1024까지 모든 AG/PG 부호에 대해 offset map을 경험적으로 탐색하여 rank 보존을 전수 검증(Table I, II).
9. 결과: 4개 FG code(길이 128~585)에서 flooding BP 디코딩 시 error floor 없음, BLER 10^-7에서 대응 5G LDPC 대비 약 0.5dB 이득.
10. 한계: HW 미설계, 순수 시뮬(이론+수치검증) 결과이며 non-binary 대수구조(GF(q), q>2 포함) 기반이라 binary 전용 코드베이스 이식엔 제약.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Finite geometry code 부호설계 (H-matrix 구성) | `ecc_top.cpp` `Load_PCM()` | FG code는 QC-LDPC와 무관한 별도 대수구조라 직접 대응 어려움, 참고용 |
| flooding BP 디코딩 (min-sum 아님, sum-product 계열 언급 없음) | `decoder.cpp` `LDPC_Decoder()` | 디코더 알고리즘 자체는 표준 BP로 새로운 기여 없음 |
| lifted Gabidulin 기반 pencil selection (부호구조 결정) | 대응 없음 | non-binary rank-metric code 기반 구성법으로 대응 모듈 없음 |
| AVN 삽입을 통한 sparse PCM 생성 | 대응 없음 | Prime ECC는 이미 고정된 QC-LDPC PCM 사용, AVN 개념 대응 없음 |
```

적용 가치: 낮음 — FG code(Reed-Muller/affine·projective geometry code)라는 특정 대수적 부호족의 sparse PCM 구성 이론이며, non-binary rank-metric(Gabidulin) 코드에 의존해 Prime ECC의 고정 binary QC-LDPC 구조와 직접 접점이 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2606.11454v1",
  "title": "Lifted Gabidulin Construction for LDPC Representations of Finite Geometry Codes",
  "year": 2026,
  "venue": "arXiv (cs.IT)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "8~1024",
  "soft_quant": "soft-4bit+",
  "key_contribution": "finite geometry code의 dense incidence matrix를 pencil 기반으로 sparsify하는 문제를 lifted Gabidulin code로 명시적으로 해결",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "non-binary 대수구조(Gabidulin/rank-metric code, GF(q) 기반) 기반 구성법이라 binary QC-LDPC 이식에 근본적 제약",
  "todo_check": "특정 finite geometry(AG/PG) 부호가 Prime ECC의 고rate QC-LDPC 구조와 얼마나 호환 가능한지"
}
```
