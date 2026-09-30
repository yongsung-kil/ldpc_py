### arxiv:1808.05258v1 - Edge Coloring Technique to Remove Small Elementary Trapping Sets from Tanner Graph of QC-LDPC Codes with Column Weight 4 (2018, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | column weight 4 QC-LDPC의 exponent matrix에서 특정 6/8-cycle을 회피하면 (5,b)/(6,b)/(7,4) 소형 ETS가 제거됨을 edge-coloring으로 증명 |
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
| 한계,주의 | fully connected (∞ 없는) exponent matrix·column weight 4 한정, girth 6/8뿐 - BER/error-floor 시뮬 없이 순수 그래프이론 충분조건만 제시 |
| 추가확인 | Prime ECC 부호(VN degree 17, column weight≠4)에 해당 조건 적용 불가 - 자사 QC 구성법에 6/8-cycle 회피 규칙을 재유도할 수 있는지 확인 필요 |

> 총평: 소형 ETS 제거로 error-floor를 낮추는 QC-LDPC 부호설계 이론이나 column weight 4에 특화되고 HW·BER 검증이 없어, Prime ECC 부호 재설계 시 참고용으로 이식가치 중간.

### B. 알고리즘 요약

1. 대상: `(4,n)`-regular QC-LDPC 부호, exponent matrix `B=[bij]`, CPM 크기 `N`(lifting degree), fully connected(∞ 원소 없음).
2. 풀려는 문제: error floor를 유발하는 소형 elementary trapping set(ETS, degree-1/2 check만 포함)을 부호설계 단계에서 제거 - 기존 PEG 기반 ETS-free 부호는 대부분 column weight 3에 국한.
3. 핵심 도구 1: cycle 존재 조건 `Σ(b_{mi,ni} − b_{mi,ni+1}) ≡ 0 mod N` (Fossorier[12]) - girth `g`를 얻으려면 `k<g/2`에 대해 이 식을 회피.
4. 핵심 도구 2: ETS의 VN graph(degree-1 check 제거, degree-2 check를 간선으로) 위 edge-coloring; fully connected QC-LDPC에서 `(a,b)` ETS 존재 ⇔ VN graph가 `m`-edge-coloring 가능 (Proposition 1, Vizing 정리 기반).
5. girth 6: `6-cycle{1,2,3}`과 `6-cycle{1,2,4}`(exponent matrix 행 조합에서 나오는 6-cycle) 회피 → VN graph에 4-edge-coloring 불가 → `(5,4)` ETS 제거 (Lemma 1).
6. 연쇄 결과: `(5,4)` 제거 시 `(6,0)` 제거(Lemma 2), 동일 조건으로 `(6,2)`도 제거(Lemma 3); 종합해 `(5,b) b≤4`, `(6,b) b≤2` free (Theorem 3).
7. girth 8: 최소 ETS인 `(7,4)`의 VN graph가 완전이분그래프 `K3,4` 하나뿐임을 차수열 분석으로 증명(Proposition 3).
8. `(7,4)` 제거 조건: 첫 행 2회+둘째 행 1회 이상 쓰는 3개 행에서 나오는 8-cycle 회피 → `K3,4`가 4-edge-coloring 불가 (Theorem 4).
9. 결과: Table I에 girth 6(n=5,6,7; N=13,18,21)·girth 8(N=41,63,91) exponent matrix 예시 제공. 탐색공간 축소 위해 column weight 3 기존 수치결과 활용.
10. 한계: 충분조건(그래프이론 증명)만 - BER/error-floor 곡선·복호 시뮬·HW 없음, column weight 4 및 fully connected에 국한.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| exponent matrix 6/8-cycle 회피 → ETS 제거 부호설계 | ecc_top.cpp Load_PCM() | H-matrix/PCM 로드부에서 부호구조 결정, ETS-free 조건은 오프라인 부호설계에 반영 |
| girth/사이클 조건으로 error-floor 개선 | 대응 없음 | Prime ECC는 복호기(min-sum) 중심, 부호 사이클/ETS 최적화 툴은 코드베이스에 없음 |
| 소형 ETS 제거로 복호 실패율 감소 | decoder.cpp LDPC_Decoder() | 복호 성능(error-floor)에 간접 영향이나 알고리즘 변경 아님(부호 자체 변경) |
```

적용 가치: **중간** - error-floor 저감 부호설계 이론으로 유효하나 column weight 4·fully connected 한정이고 Prime ECC 부호(VN degree 17)와 구조가 달라 조건 재유도가 필요하며 HW/BER 검증이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1808.05258v1",
  "title": "Edge Coloring Technique to Remove Small Elementary Trapping Sets from Tanner Graph of QC-LDPC Codes with Column Weight 4",
  "year": 2018,
  "venue": "arXiv cs.IT",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": null,
  "soft_quant": "무관",
  "key_contribution": "column weight 4 QC-LDPC의 exponent matrix에서 특정 6/8-cycle을 회피하면 (5,b)/(6,b)/(7,4) 소형 ETS가 제거됨을 edge-coloring으로 증명",
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
  "caveat": "fully connected (∞ 없는) exponent matrix·column weight 4 한정, girth 6/8뿐 - BER/error-floor 시뮬 없이 순수 그래프이론 충분조건만 제시",
  "todo_check": "Prime ECC 부호(VN degree 17, column weight≠4)에 해당 조건 적용 불가 - 자사 QC 구성법에 6/8-cycle 회피 규칙을 재유도할 수 있는지 확인 필요"
}
```
