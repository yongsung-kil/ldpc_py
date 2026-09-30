### arxiv:1403.6090v1 - Column Weight Two and Three LDPC Codes with High Rates and Large Girths (2014, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.24~0.9 |
| 부호length | 21~7620 |
| 연판정 | 무관 |
| 핵심기여 | broken diagonal pair 기반 조합론적 구성으로 girth-12 column-weight t(3~20) cycle code와 이를 확장한 girth-6 column-weight-3 LDPC 부호를 제시 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 대수적 구성/BER 시뮬 논문으로 디코더·HW·NAND 채널(soft-read, RBER) 관점 전혀 없음 |
| 추가확인 | 시뮬 그래프(Fig.3)의 정확한 BER/Eb-N0 수치는 그림뿐이라 본문 서술 없어 확인 불가 |

> 총평: girth-12/6 cycle/column-weight-3 QC-LDPC 부호의 대수적 구성법 논문으로 고전 부호 이론적 기여이나 HW/디코더/NAND 채널 요소가 전무해 Prime ECC 이식 가치가 낮음.

### B. 알고리즘 요약

1. m×m 체스판형 정사각 격자 `Lm`에서 대각선(diagonal)들의 흑백 컬러링으로 cycle code(column weight-2 LDPC)의 parity-check 행렬을 구성한다.
2. 문제의식: 기존 girth-12 cycle code 구성(cage graph, Singer perfect difference set 등)은 임의 row-weight에 대해 결정적 구성이 어렵거나 최소 길이가 크다.
3. 핵심 가정/모델: `Lm(p)`를 "broken diagonal pair"로 정의하고, `(m,t)-vector` `v=(v1,...,vt)`로 t개의 broken diagonal을 결합해 incidence matrix `Hm(v)`를 만든다(각 vi는 홀수, m 미만).
4. 핵심 기법: Theorem 1에서 `(vk1+vk2)-(vk3+vk4) ∈ {0,±m}` 조건이 성립하면 `g(Hm(v))=12`(8-cycle 회피)임을 증명, 이를 만족하는 v를 찾는 탐색 알고리즘(Algorithm, 단계별 후보 집합 `Ak` 갱신) 제시.
5. 구성된 `Hm(v)`는 rate `r=1-(m-1)/(t⌊m/2⌋)`이며, row-weight `t=q+1`(q는 소수거듭제곱)일 때 Gallager bound를 달성하는 최소 길이를 얻는다(Table I, t=3~20).
6. 확장 기법: cycle code `Hm(v)`에 t개의 행을 추가한 `Mm(v)`로 girth-6 column-weight-3 LDPC 부호 구성(Lemma 3.1: 4-cycle 회피에 최소 t개 행 필요함을 증명), rate `r'=1-(t+m-1)/(t⌊m/2⌋)`.
7. 부수 트릭: `Hm(v)`/`Mm(v)`는 base matrix로 사용해 quasi-cyclic(QC) lifting 시 girth를 최소 36(column weight 2) 또는 20(column weight 3)까지 보장 가능(Kim et al. girth 확장 정리 인용).
8. 학습/최적화 절차 없음 — Algorithm은 조합적 탐색(exhaustive search 유사)으로 조건을 만족하는 v 벡터를 결정적으로 찾는 방식.
9. 결과: 구성된 column-weight-3 QC-LDPC 부호(예: C3(3,2731;girth12~18), C3(4,1500;girth12~16))가 Steiner Triple System(STS(9))·정수격자(L3×5) 기반 부호 대비 AWGN 채널 BER 곡선에서 현저히 우수(Fig.3, 정량 수치는 그림에만 존재).
10. 한계: 순수 이론적/시뮬레이션(AWGN) 결과만 제시하며 디코더 알고리즘, HW 구현, 복잡도, NAND 채널 특성(soft-read, RBER) 관련 논의가 전혀 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| girth-12/6 cycle/column-weight-3 QC-LDPC 부호 구성(H-matrix 대수적 생성) | `ecc_top.cpp` `Load_PCM()` | H-matrix 구조 자체를 교체해야 하므로 이식 난이도 높음(프로파일 §4 "부호설계" 항목) |
| QC lifting을 통한 girth 보장 | 대응 없음 | Prime ECC는 특정 QC-LDPC(base+circulant, N_b=129) 고정, base matrix 재설계는 재검증 부담 큼 |
| AWGN BER 시뮬레이션(디코더/HW 무관) | 대응 없음 | 디코딩 알고리즘 자체를 다루지 않음(단순 성능 검증용) |

> 적용 가치: **낮음** — 순수 대수적 H-matrix 구성법 논문으로 Prime ECC의 고정 QC-LDPC 구조 교체는 재검증 부담이 크고(§4 "부호설계=높음"), 디코더/HW 개선 요소가 전혀 없어 이식 실익이 낮음.

### D. JSON 블록

```json
{
  "id": "arxiv:1403.6090v1",
  "title": "Column Weight Two and Three LDPC Codes with High Rates and Large Girths",
  "year": 2014,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": "0.24~0.9",
  "code_length": "21~7620",
  "soft_quant": "무관",
  "key_contribution": "broken diagonal pair 기반 조합론적 구성으로 girth-12 column-weight t(3~20) cycle code와 이를 확장한 girth-6 column-weight-3 LDPC 부호를 제시",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 대수적 구성/BER 시뮬 논문으로 디코더·HW·NAND 채널(soft-read, RBER) 관점 전혀 없음",
  "todo_check": "시뮬 그래프(Fig.3)의 정확한 BER/Eb-N0 수치는 그림뿐이라 본문 서술 없어 확인 불가"
}
```
