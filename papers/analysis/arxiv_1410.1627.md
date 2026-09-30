### arxiv:1410.1627v1 - New Results on the Pseudoredundancy (2014, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | value assignment 기법으로 특정 k차원 이진 선형부호(반복/확장 좌표, shortened subcode, constant-weight 부호 등)의 pseudocodeword redundancy 상한/정확값을 유도 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | LP(linear-programming) decoding 이론 프레임에서의 순수 대수적 증명뿐, 실제 min-sum/BP 디코더나 구체적 QC-LDPC 구성과 무관 |
| 추가확인 | LP decoding pseudoweight 개념이 실제 사용 중인 min-sum 디코더 성능과 어떻게 연결되는지 불명확 |

> 총평: LP decoding 이론틀의 pseudoredundancy 상한을 다루는 순수 수학 논문으로, NAND binary QC-LDPC 실무 이식 가치는 거의 없음.

### B. 알고리즘 요약 (10줄 내외)

1. 대상은 일반 이진 선형부호 `[n,k,d]`이며 LP(linear programming) decoding 하에서의 pseudocodeword/pseudoweight 이론을 다룸 (BP iterative decoding과도 부분적으로 연관).
2. 풀려는 문제: 특정 부호의 pseudoredundancy `ρ(C)` (최소 pseudoweight가 최소 Hamming distance `d`와 같아지는 parity-check 행렬의 최소 행 수)를 결정하거나 상한을 구하는 것.
3. 핵심 가정/모델: fundamental cone `K(H)` 상의 pseudocodeword `x`에 대해 BEC/AWGNC/BSC/max-fractional 4종 pseudoweight를 정의하고 `wmin(H) ≤ d(C)`를 이용.
4. 핵심 기법 1단: Chen-Kløve의 value assignment `m(p): PG(k-1,q) → N`를 이용해 생성행렬 G의 컬럼(반복 가능)을 사영공간의 점으로 표현.
5. 핵심 식 `wmaxfrac(x) = (Σxi)/max(xi)`; 컬럼 반복(`m(p)` 증가)으로 얻은 확장부호의 pseudoredundancy가 원부호 대비 `ρ(C') ≤ ρ(C) + (n'-n)`으로 상한됨을 증명 (정리 3).
6. 확장 기법 2단: shortened subcode `C_I'`의 pseudoredundancy 상한 `ρ(C_I') ≤ ρ(C) + (n-|I'|)` (정리 5), subcode-complete 부호 판정 조건(정리 6) 도출.
7. 부수 기법: representing-set(대표점 집합)의 independent/dependent 여부로 k차원 부호를 분류, 각 경우 parity-check 행렬을 block-diagonal 구조로 명시적 구성.
8. 학습/최적화 절차 없음 - 순수 조합론적/대수적 증명(Tanner graph cycle-free 여부 분석 포함).
9. 결과: constant-weight 부호에 대해 `ρ(C) ≤ n + (2^k-1)(2^(k-1)-4)/3` 상한 도출, 특정 k차원 부호에 대해 `ρ(C) = n-k` (하한과 일치하는 exact값) 증명. 예제(k=6,t=3 등)로 non-cycle-free 부호에서도 성립함을 검증.
10. 한계: 순수 이론/증명뿐이며 시뮬레이션·HW·실제 채널 실험 전혀 없음. 다루는 부호가 특수 구성(simplex code 반복, representing-set 조건 만족 등)에 국한되어 실용 QC-LDPC 설계에 직접 적용하기 어려움.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| LP decoding pseudoredundancy 이론 | 대응 없음 | Prime ECC는 min-sum BP 디코더이며 LP decoding 미사용 |
| value assignment 기반 부호 구성 | 대응 없음 | QC-LDPC(base+shift) 구성과 무관한 일반 선형부호 이론 |
| Tanner graph cycle-free 분석 | 대응 없음 | 구체적 H-matrix 설계 도구(`ecc_top.cpp` `Load_PCM()`)와 연결점 없음 |
```

적용 가치: `낮음` — LP decoding 이론 틀의 순수 수학적 pseudoredundancy 증명으로, min-sum 기반 binary QC-LDPC HW 이식과 직접적 접점이 없음.

### D. JSON 블록 (DB 적재용)

```json
{
  "id": "arxiv:1410.1627v1",
  "title": "New Results on the Pseudoredundancy",
  "year": 2014,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "value assignment 기법으로 특정 k차원 이진 선형부호의 pseudocodeword redundancy 상한/정확값을 유도",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "LP decoding 이론 프레임에서의 순수 대수적 증명뿐, 실제 min-sum/BP 디코더나 구체적 QC-LDPC 구성과 무관",
  "todo_check": "LP decoding pseudoweight 개념이 실제 사용 중인 min-sum 디코더 성능과 어떻게 연결되는지 불명확"
}
```
