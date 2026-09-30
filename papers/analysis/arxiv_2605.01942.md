### arxiv:2605.01942v1 - Combinatorial Analysis of Dyadic and Quasi-Dyadic Codes (2026, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 8~64 |
| 연판정 | 무관 |
| 핵심기여 | dyadic/quasi-dyadic 행렬의 TBC-walk 기반 4/6/8-cycle 계수 및 forbidden-set PEG 구성으로 girth·단주기 최소화 (CSS QLDPC 대상) |
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
| 한계,주의 | 양자 CSS(QLDPC) 전용 구성법·순수 조합론, dyadic lift는 girth≤8 상한(all-one 프로토그래프), NAND binary LDPC와 무관 |
| 추가확인 | dyadic-PEG의 forbidden-set/cycle-count 아이디어가 우리 QC-LDPC(원형 shift) 구성에 재사용 가능한지 정도만 참고 |

> 총평: 양자 CSS 부호를 위한 dyadic 행렬 조합론·girth 분석 논문으로 NAND binary QC-LDPC 디코더/HW 이식과는 사실상 무관, 이식성 하.

### B. 알고리즘 요약

1. 대상은 CSS 조건 `HZHX^T=0`을 만족해야 하는 양자 LDPC(QLDPC)이며, dyadic 행렬(`Dx,y=D0,x+y`, `N=2^ℓ`)의 가환환·재귀 블록 구조를 부호 설계 기판으로 활용한다.
2. 문제: 반복복호 성능은 Tanner 그래프의 단주기(4/6/8-cycle)와 absorbing set에 좌우되는데, 기존 quasi-dyadic CSS 구성(Construction 3.11)은 girth가 필연적으로 4에 갇혀 성능이 나쁘다.
3. 핵심 대응: lifted Tanner 그래프의 cycle을 프로토그래프의 tailless-backtrackless-closed(TBC) walk로 대응시키고, 블록 인접행렬 거듭제곱 `A^m`의 permutation-shift 라벨로 실제 cycle 여부를 판정한다.
4. dyadic/quasi-dyadic 모두에 대해 4-cycle(Thm 4.15/4.18), 6-cycle, 8-cycle 개수 `N4,N6,N8`의 명시적 계수 공식·알고리즘(Alg 1)을 유도한다.
5. 의미: 이 cycle 수가 단순 기술량이 아니라 부호 구성의 제약·목적함수가 된다.
6. dyadic-aware PEG: 인덱스별 forbidden set `F^{g,N}_a`(선택 시 girth≤g가 되는 shift 집합)를 배제하며 edge를 순차 배치, 최대 girth 확보 후 불가하면 target girth를 6→4로 낮춘다(Alg 2).
7. Alg 3은 여기에 각 선택마다 g-cycle 수 `Ng`를 최소화하는 shift를 고르는 cycle-minimization 단계를 추가한다.
8. dyadic이 한 개 1을 signature에 넣으면 `N-1`개 edge가 동시 생성되어 full lift 대비 PEG 구성 복잡도가 `O(mn)`에서 크게 감소.
9. absorbing set: `m×1`/`1×n`/동일 dyadic 배열 등 boundary case에서 완전이분 성분(`K_{m,n}`)이 생겨 (a,0)-absorbing set이 명시적으로 열거됨(과다 발생 layout 식별).
10. 결과: BP 시뮬(Roffe LDPC 툴)에서 girth를 못 올려도 4-cycle 수를 288→96 등으로 줄이면 상당한 복호 gain. 한계: HW 미설계·양자 CSS 전용·시뮬 proof-of-concept 수준, dyadic lift girth 상한 8.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| dyadic/quasi-dyadic 부호 구성 (CSS/QLDPC) | 대응 없음 | 양자 CSS 전용 구조, 우리 binary QC-LDPC와 부호 클래스 다름 |
| TBC-walk 기반 cycle 계수 | 대응 없음 (부호설계 계층, ecc_top.cpp Load_PCM() 밖) | QC-LDPC cycle 분석 개념은 유사하나 dyadic 전용, 코드 대응 함수 없음 |
| forbidden-set dyadic-PEG 구성 | ecc_top.cpp Load_PCM() (H-matrix 로드만) | 우리 H-matrix는 고정, 구성 알고리즘 자체는 이식 대상 아님 |
| absorbing set / girth 분석 | 대응 없음 | error-floor 분석 개념뿐, 우리 디코더/부호에 직접 대응 함수 없음 |
| BP 복호 (Sum-Product 계열) | decoder.cpp LDPC_Decoder() (우리는 Min-Sum) | 논문은 full-BP, 우리는 min-sum 근사 — 알고리즘 상이 |
```

적용 가치: **낮음** — 양자 CSS/dyadic 전용 부호설계·조합론 논문으로, NAND binary QC-LDPC 디코더·HW·부호설계 어느 계층에도 떼어 쓸 실체가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.01942v1",
  "title": "Combinatorial Analysis of Dyadic and Quasi-Dyadic Codes",
  "year": 2026,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "8~64",
  "soft_quant": "무관",
  "key_contribution": "dyadic/quasi-dyadic 행렬의 TBC-walk 기반 4/6/8-cycle 계수 및 forbidden-set PEG 구성으로 girth·단주기 최소화 (CSS QLDPC 대상)",
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
  "caveat": "양자 CSS(QLDPC) 전용 구성법·순수 조합론, dyadic lift는 girth<=8 상한, NAND binary LDPC와 무관",
  "todo_check": "dyadic-PEG의 forbidden-set/cycle-count 아이디어가 우리 QC-LDPC 구성에 재사용 가능한지 정도만 참고"
}
```
