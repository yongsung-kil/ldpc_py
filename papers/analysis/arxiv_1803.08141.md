### arxiv:1803.08141v1 - Efficient Search of QC-LDPC Codes with Girths 6 and 8 and Free of Elementary Trapping Sets with Small Size (2018, arXiv cs.IT / TCOMM draft)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 차분행렬 D/DD 기반 지수행렬 충분조건으로 girth 6/8 (3,n)-정규 QC-LDPC를 소형 ETS-free로 구성 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | 컬럼웨이트 3 (γ=3) 전용, 순수 구성 이론이며 BER/error-floor 실측·시뮬 없음, 소형 ETS 제거는 간접 근거 |
| 추가확인 | Prime ECC의 VN degree 17·고rate 구조에 γ=3 방식이 맞지 않음; 실제 부호에 조건 적용 시 lifting degree(N=2n(n-1)) 급증 여부 |

> 총평: γ=3 QC-LDPC의 error-floor(ETS) 제거를 위한 순수 조합 구성법. 이론은 견고하나 Prime ECC의 고차수·고rate 부호와 스펙 불일치가 커 직접 이식은 제한적.

### B. 알고리즘 요약

1. 대상은 CPM(circulant permutation matrix) 기반 fully-connected `(3, n)`-정규 QC-LDPC로, 지수행렬 `B`(3×n, 원소 `bij ∈ {0..N-1}`)와 lifting degree `N`으로 부호가 완전 기술된다.
2. 문제: girth만 높여서는 error-floor를 지배하는 소형 ETS(elementary trapping set, degree-1 CN 위주 `b/a<1`)를 제거하기 어렵다.
3. 핵심 도구는 Fossorier의 사이클 조건 식(2): `Σ(b_{mi,ni} - b_{mi,ni+1}) = 0 mod N` 이면 길이 `2k` 사이클 존재.
4. 이를 3×n 행렬에서 다루기 쉽게 차분행렬 `D`(행 간 차)와 `DD`(D의 두 열 차)를 정의해 사이클 조건을 재표현한다.
5. Girth 6: `DD`가 각 행에 반복·영(0) 원소가 없고 `2×DD ≠ 0 mod N`이면 (4,0),(4,2) ETS-free (Theorem 1). (5,1) ETS는 CPM 정의상 자동으로 없음.
6. Girth 6 lifting degree 하한: `N ≥ n²-n` (Corollary 1).
7. Girth 8: 특정 8-cycle 집합(edge label {u,v,u,v},{u,w,u,w},{u,v,u,w})을 제거하면 6-cycle까지 자동 제거되며 `a≤8, b≤3` ETS-free (Theorem 2, Lemma 1·2).
8. Girth 8 lifting degree 하한: `N = 2n(n-1)` (Corollary 2). 첫 행·열을 all-zero로 고정해 탐색공간 축소.
9. 결과: `4≤n≤9` 범위 최단길이 지수행렬을 Table I(girth6)·Table II(girth8)로 명시 (예 n=6 girth8 N=31).
10. 한계: 오직 이론적 구성/증명이며 디코더·BER·error-floor 시뮬이나 HW 구현이 전혀 없고, 컬럼웨이트 3에 한정.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 지수행렬/차분행렬 기반 QC-LDPC 부호 구성 | ecc_top.cpp `Load_PCM()` (H-matrix/PCM 로드) | 부호설계 레이어에 닿으나 Prime ECC는 QC-LDPC 고정, 재검증 부담 큼 |
| ETS 제거로 error-floor 개선 | 대응 없음 (디코더 후처리/수렴추적은 `corner.cpp`이나 부호구성과 별개) | 부호단 error-floor 보증은 디코더 코드와 직접 대응 없음 |
| 사이클/girth 제어 | 대응 없음 | Prime ECC 프로파일에 부호 구성·girth 최적화 모듈 없음 |

적용 가치: **낮음** — γ=3·고정 (3,n) 구조가 Prime ECC의 고rate·VN degree 17 QC-LDPC와 스펙이 크게 달라, 조건식만 참고 가능하고 부호 자체 이식은 부적합.

### D. JSON 블록

```json
{
  "id": "arxiv:1803.08141v1",
  "title": "Efficient Search of QC-LDPC Codes with Girths 6 and 8 and Free of Elementary Trapping Sets with Small Size",
  "year": 2018,
  "venue": "arXiv cs.IT (IEEE TCOMM draft)",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "차분행렬 D/DD 기반 지수행렬 충분조건으로 girth 6/8 (3,n)-정규 QC-LDPC를 소형 ETS-free로 구성",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "컬럼웨이트 3(γ=3) 전용, 순수 구성 이론이며 BER/error-floor 실측·시뮬 없음",
  "todo_check": "Prime ECC 고rate·VN degree 17 구조에 γ=3 방식 부적합; 조건 적용 시 lifting degree 급증 여부 확인"
}
```
