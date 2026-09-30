### arxiv:2310.12556v1 - An Efficient Algorithm for Counting Cycles in QC and APM LDPC Codes (2023, Iranian Journal of Science (preprint))

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 0.67 |
| 부호length | 1296~1944 |
| 연판정 | 무관 |
| 핵심기여 | base matrix만으로 CPM-size 무관하게 임의 길이 사이클을 열거하는 재귀 카운팅 알고리즘 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | N/A |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 부호 성능·디코더가 아닌 순수 사이클 열거 도구, error-floor 개선 자체는 미제공 |
| 추가확인 | 우리 QC-LDPC H-matrix 설계·검증 파이프라인에 사이클 분포 분석 보조도구로 쓸지 여부 |

> 총평: 디코더/HW와 무관한 순수 사이클 카운팅 알고리즘으로 Prime ECC 런타임 이식 대상은 아니며, H-matrix 설계 단계 오프라인 분석 보조도구로만 제한적 가치.

### B. 알고리즘 요약

1. 대상: (Type-I) QC-LDPC 및 APM-LDPC (CPM/APM으로 lift한 protograph 부호)의 Tanner graph 사이클 분포 계산 (부호 설계용 조합론).
2. 문제: 기존 사이클 카운팅은 행렬곱 기반이라 lifting degree(CPM-size) `m`에 복잡도가 종속되고 길이도 `2g-2`까지만 셀 수 있어 대형 부호에 비효율적.
3. 모델: `2l`-사이클을 base matrix의 TBC(tailless backtrackless closed) walk에 대응시키고, slope vector `S`·shift vector `A` 기반 modular 방정식(Thm 3.1/3.2)으로 사이클 존재 판정.
4. 기법1 (allowable chain 분류): base graph의 non-isomorph cycle-chain만 열거 (Def 3.6 isomorph 관계, `b→(L)`,`b←(L)` k-adic 표현으로 고속 중복 제거).
5. 핵심식: 각 allowable `2l`-cycle chain 하나가 Tanner graph에서 `r = m/n(L)`개의 실제 사이클에 대응 (Thm 3.17), `n(L)`은 subchain 반복 횟수.
6. 기법2 (APM 확장): shift vector가 all-one이 아닌 APM-LDPC로 재귀 확장 (`δ→,t`,`δ↑,t` 점화식, Lemma 3.3 allowability 조건).
7. 구현: base matrix를 열 단위(column-by-column)로 `B(e)` 부분설계에 대해 재귀 열거 (Algorithm 4.1), C# 구현.
8. 학습/최적화: 없음 (결정론적 열거 알고리즘).
9. 결과: IEEE 802.11 rate-2/3 (1296,432)/(1944,648) 부호에서 `N4~N12` 카운팅을 0.046/0.048초에 완료 ([25] 대비 약 10~20배 빠름), (3,4) girth-12 CPM-100 부호 사이클 분포 산출.
10. 한계: 순수 이론/열거 도구 — 디코더·HW·정정성능 개선 없음, 복잡도는 base graph 크기·`bmax`·`l`에 다항적이나 `l` 증가 시 급증.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC-LDPC base matrix / 사이클 분포 분석 | `ecc_top.cpp` `Load_PCM()` (H-matrix 구조) | 우리 PCM의 girth·short-cycle 오프라인 진단 보조에만 간접 관련 |
| 사이클 카운팅 알고리즘 자체 | 대응 없음 | 런타임 디코더/인코더 경로 밖, 코드베이스에 대응 모듈 없음 |
| APM-LDPC 구성 | 대응 없음 | Prime ECC는 binary QC-LDPC(CPM) 고정, APM 미사용 |

적용 가치: **낮음** — 디코더·HW·정정성능과 무관한 부호 설계용 사이클 열거 도구로, Prime ECC 런타임에 이식할 요소가 없고 기껏해야 H-matrix 설계 검증의 외부 보조도구 수준.

### D. JSON 블록

```json
{
  "id": "arxiv:2310.12556v1",
  "title": "An Efficient Algorithm for Counting Cycles in QC and APM LDPC Codes",
  "year": 2023,
  "venue": "Iranian Journal of Science (preprint)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": 0.67,
  "code_length": "1296~1944",
  "soft_quant": "무관",
  "key_contribution": "base matrix만으로 CPM-size 무관하게 임의 길이 사이클을 열거하는 재귀 카운팅 알고리즘",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "N/A",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "부호 성능·디코더가 아닌 순수 사이클 열거 도구, error-floor 개선 자체는 미제공",
  "todo_check": "우리 QC-LDPC H-matrix 설계·검증 파이프라인에 사이클 분포 분석 보조도구로 쓸지 여부"
}
```
