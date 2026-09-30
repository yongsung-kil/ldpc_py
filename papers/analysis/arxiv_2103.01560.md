### arxiv:2103.01560v1 - Efficient Encoding Algorithm of Binary and Non-Binary LDPC Codes Using Block Triangulation (2021, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | encoder |
| 부호종류 | irregular |
| 부호rate | 미상 |
| 부호length | 1000~5000 |
| 연판정 | 무관 |
| 핵심기여 | 패리티부를 행·열 순열로 저가중 대각 부분행렬을 가진 블록삼각행렬로 변환, 블록 후진대입으로 인코딩 복잡도 감소(비이진 cycle code는 linear time) |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 없음 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 인코딩 복잡도(곱셈/덧셈 카운트) 이론이며 HW 미설계, 비이진 이득이 주효과·이진 이득은 장부호에서만 |
| 추가확인 | Prime ECC는 dual-diagonal 인코딩 고정이라 임의 H 전처리 순열 기반 방식과 정합 어려움 |

> 총평: 임의 LDPC H-matrix의 인코딩 복잡도 감소 이론 논문으로, dual-diagonal 인코딩 고정인 NAND 고정 QC-LDPC에는 이식 가치 낮음.

### B. 알고리즘 요약

1. 대상: binary/non-binary irregular LDPC 부호의 인코딩 알고리즘(EA), non-binary는 `F_q`(예 `F_8`), 실험 code length n=1000~5000.
2. 문제: generator matrix `G`는 sparse H여도 dense → 인코딩 복잡도 `O(n^2)`로 sum-product 복호보다 비쌈, 인코딩이 병목.
3. 핵심: 열순열로 `H=(H_P|H_I)` 분리 후 `H_P p^T = -H_I u^T` 를 풀되, `H_P`를 행·열 순열(`PHQ`)만으로 저가중 대각블록을 가진 블록삼각행렬 `H`로 변환(복호성능 불변).
4. 블록삼각행렬 대각블록 `F_i`를 가능한 한 대각(diagonal) 또는 cycle 행렬로 만들어, 블록 후진대입(block back-substitution)으로 파트별 `F_i p_i^T = b_i^T` 순차 해결.
5. 복잡도 이득 근거: 대각/cycle 블록 하나당 곱셈이 각각 `m_i`, `3m_i-1`로 ATM(gap δ의 `Φ^{-1}` 포함)보다 낮아 `wt(D)+wt(K)`만큼 절감.
6. 전처리(Preprocessing): 반복 알고리즘으로 Sub-step (a)대각/(b)cycle/(c)small-ATM/(d)large-ATM 추출, SBBD(singly bordered block-diagonalization)와 associated-graph cycle 검출 사용.
7. cycle 행렬 해법: `Cω^T=b^T`를 곱셈 `3k-1`·덧셈 `2(k-1)`로 해결(기존 [10]의 `4k-3`보다 개선).
8. 이론성질: 입력이 proper non-binary cycle code면 출력이 HZ-EA와 일치 → 제안 EA는 HZ-EA의 일반화, non-binary cycle code에서 `O(n)` linear time.
9. 결과: 수치실험(E8/E2 각 100개)에서 non-binary는 곱셈 최소, binary는 n≥2000 장부호에서 RU-EA·K-EA보다 낮은 덧셈(예 n=5000 α=17473 vs Kaji 24119); 단부호는 LU-factorization 변형으로 개선.
10. 한계: 순수 인코딩 복잡도(연산 카운트) 이론, HW 미설계, 이진 단부호에서는 K-EA에 열세, soft/BER 등 복호성능 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 인코딩 알고리즘(블록삼각화 전처리+후진대입) | encoder.cpp `LDPC_encoder_4KB()`, `Generate_PCM_encoding()` | Prime ECC는 dual-diagonal 인코딩 고정, 임의 H 순열 방식과 상이 |
| 부호 PCM 생성/열 재배치 | encoder.cpp `Column_Reordering_Dual_Update()` | 열순열 개념은 유사하나 목적(dual-update)·구조 다름 |
| non-binary cycle 행렬 처리 | 대응 없음 | Prime ECC는 binary 전용, GF(q) 무관 |
| H-matrix 로드 | ecc_top.cpp `Load_PCM()` | H 자체는 고정 QC-LDPC, 전처리 순열 재설계 부담 큼 |

적용 가치: **낮음** — Prime ECC의 인코더는 dual-diagonal로 고정되어 이미 linear-time 인코딩이 가능하고, 이 논문의 주 이득은 non-binary 및 임의 irregular H 대상이라 binary 고정 QC-LDPC에 떼어낼 실익이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2103.01560v1",
  "title": "Efficient Encoding Algorithm of Binary and Non-Binary LDPC Codes Using Block Triangulation",
  "year": 2021,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "encoder",
  "code_type": "irregular",
  "code_rate": "미상",
  "code_length": "1000~5000",
  "soft_quant": "무관",
  "key_contribution": "패리티부를 행·열 순열로 저가중 대각 부분행렬을 가진 블록삼각행렬로 변환, 블록 후진대입으로 인코딩 복잡도 감소(비이진 cycle code는 linear time)",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "없음",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 인코딩 복잡도(곱셈/덧셈 카운트) 이론이며 HW 미설계, 비이진 이득이 주효과·이진 이득은 장부호에서만",
  "todo_check": "Prime ECC는 dual-diagonal 인코딩 고정이라 임의 H 전처리 순열 기반 방식과 정합 어려움"
}
```
