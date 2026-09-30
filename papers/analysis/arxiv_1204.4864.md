### arxiv:1204.4864v1 - Tight lower bound of consecutive lengths for QC-LDPC codes with girth twelve (2012, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호length | 449~ (예시: 2694 이상, step 6) |
| 부호rate | 미상 |
| 연판정 | 무관 |
| 핵심기여 | (3,L) QC-LDPC 부호의 shift matrix가 주어졌을 때 girth 12를 보장하는 CPM 크기의 tight lower bound를 수학적으로 증명 |
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
| 한계,주의 | column weight 3(=(3,L)) 고정 구조에 한정된 순수 수학적 증명, 실제 디코딩 성능·HW 검증 전혀 없음 |
| 추가확인 | Prime ECC의 실제 H-matrix가 (3,L) 구조인지, girth 최적화가 실용적 이득으로 이어지는지 별도 확인 필요 |

> 총평: girth-12 QC-LDPC 존재성/구성법에 대한 순수 이론적 증명으로, 디코더·HW·NAND와 무관한 조합론적 결과이며 Prime ECC 이식 가치는 낮음.

### B. 알고리즘 요약

1. 대상 부호: (3,L) QC-LDPC, shift matrix `S`(2×L)와 CPM 크기 `X`로 정의되는 parity-check matrix `H_X`, 길이 `N=XL`.
2. 풀려는 문제: girth-12(최대 girth) (3,L) QC-LDPC의 "consecutive length"(연속된 CPM 크기 전 구간에서 girth 12 보장) 존재성이 선행연구([8])에서 열린 문제로 남아 있었음.
3. 핵심 가정: 임의의 shift matrix `S`로 정의된 일반 (3,L) QC-LDPC, HW/채널 모델은 다루지 않음(순수 조합론).
4. shift matrix의 원소로부터 `A=max(p1,j)`, `B=max(p2,j)`, `C=max(p1,j-p2,j)`, `D=max(p2,j-p1,j)` 정의, 이를 조합한 `T1..T6`(예: `T1=2A+D`, `T5=A+B+D`)과 `P'=max{T1,...,T6}`.
5. 핵심 결과(Theorem 1): 어떤 정수 `Q`에서 `g(H_Q)=12`이면, `P>P'`인 모든 `P`에 대해 `g(H_P)=12`이고 `P=P'`에서는 `g(H_P)<12`(즉 `P'`가 tight lower bound).
6. 증명은 두 Lemma로 구성: Lemma1(`P>P'`이면 4/6/8/10-cycle 부재를 모듈러 산술 부등식으로 반증), Lemma2(`P=P'`이면 항상 8- 또는 10-cycle 존재 구성).
7. 부수 트릭: mod 연산이 걸린 순환 방정식을 LHS/RHS 모두 non-negative인 정규형으로 변환해 "P가 두 값보다 크면 mod 없이도 등식 성립 → 모순" 형태로 각 case를 소거.
8. 학습/최적화 없음. 예시로 simulated annealing 기반 shift matrix 탐색(3x6, girth-12 for Q=393)만 부수적으로 사용.
9. 결과: 예시 shift matrix로 `P'=488`(2×244+1=449) 도출, 길이 2694부터 시작해 step 6의 연속 girth-12 (3,6) QC-LDPC 무한 집합 제시, 기존 최단 girth-12 (3,6) 코드(O'Sullivan, length 2874)보다 짧은 코드 다수 포함.
10. 한계: column weight 3 고정 및 girth 12(최대 girth) 특수 케이스에만 적용되는 순수 존재성 증명, 실제 오류정정 성능·디코더 알고리즘·HW 구현은 전혀 다루지 않음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| girth-12 shift matrix 존재성 증명 | `ecc_top.cpp` `Load_PCM()` | H-matrix 로드 대상이지만 Prime ECC는 고rate/degree 17 구조라 (3,L) column weight 3 특화 결과와 직접 무관 |
| consecutive length 구성법 | (대응 없음) | 순수 조합론적 존재성 증명, 코드 생성 알고리즘·모듈 형태 아님 |
| 디코더/HW | (대응 없음) | 논문에 디코더·HW 내용 전혀 없음 |

적용 가치: **낮음** — 순수 수학적 girth 존재성 증명으로 Prime ECC의 실제 부호(고rate, degree 17, non-(3,L)) 및 디코더/HW 어느 레이어와도 직접 연결되지 않음.

### D. JSON 블록

```json
{
  "id": "arxiv:1204.4864v1",
  "title": "Tight lower bound of consecutive lengths for QC-LDPC codes with girth twelve",
  "year": 2012,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": "미상",
  "code_length": "449~",
  "soft_quant": "무관",
  "key_contribution": "(3,L) QC-LDPC 부호의 shift matrix가 주어졌을 때 girth 12를 보장하는 CPM 크기의 tight lower bound를 수학적으로 증명",
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
  "caveat": "column weight 3(=(3,L)) 고정 구조에 한정된 순수 수학적 증명, 실제 디코딩 성능·HW 검증 전혀 없음",
  "todo_check": "Prime ECC의 실제 H-matrix가 (3,L) 구조인지, girth 최적화가 실용적 이득으로 이어지는지 별도 확인 필요"
}
```
