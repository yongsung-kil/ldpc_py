### arxiv:1701.06218v1 - On Advisability of Designing Short Length QC-LDPC Codes Using Perfect Difference Families (2017, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.51~0.97 |
| 부호length | 57~3960 |
| 연판정 | 무관 |
| 핵심기여 | PDF/QPDF + column dispersion technique(CDT)로 girth6 유지하며 short-cycle 수를 점진 조절해 waterfall/error-floor 균형 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 부호구성법(BER는 short-cycle 통계에 의존), 특정 QC-LDPC(z=32) 고정된 Prime ECC에 재설계·재검증 부담 큼 |
| 추가확인 | Prime ECC의 고rate high-degree(VN17) 부호에는 dv=3,4 저차수 구성이 부적합할 수 있음 |

> 총평: girth6 QC-LDPC를 PDF기반으로 구성하고 cycle수로 waterfall을 미세조정하는 이론/시뮬 논문 - HW·디코더 개선 없고 부호설계 이식 부담 커 가치 낮음.

### B. 알고리즘 요약

1. 대상은 CPM(circulant permutation matrix) 기반 binary QC-LDPC의 short~moderate length 부호설계, AWGN·SP(Sum-Product) 디코딩, rate `t-1/t` (t=block 수).
2. 문제: 최단길이 QC-LDPC는 girth·degree 고정 시 `dmin`이 낮아지는데, 낮은 `dmin`을 무엇으로 보상해 BER를 낮출지가 미해결.
3. 핵심 관찰: 고정 파라미터에서 Tanner graph의 short simple cycle 수(길이 4·6·8·10 multiplicity)가 평균보다 높으면 waterfall이 더 가팔라진다.
4. Construction 1: perfect/quasi-perfect difference family `(v,k,1)` PDF/QPDF의 block을 exponent matrix로 써서 girth6인 1-level Type-k(k=3,4) CPM-QC-LDPC 생성, lifting `N>=v`.
5. 핵심 식: cycle 존재조건 `sum(P_{m_i n_i} - P_{m_i n_{i+1}}) = 0 mod N` (식4). inevitable cycle = N과 무관하게 항상 0이 되는 cycle.
6. Construction 2 (CDT, column dispersion): exponent 벡터를 m조각으로 분산해 m-level Type-L* 부호로 변환, `g*>=g`, `d*min>=dmin` 보장(Proposition 1) — girth·dmin 유지하며 rate/short-cycle 재조정.
7. 부수 트릭: masking matrix 곱셈(CM* 부호)으로 short-cycle 수를 더 낮춰 error-floor 억제.
8. 최적화: PDF/QPDF는 Skolem sequence·graceful prism labeling으로 생성, `dmin`은 MAGMA로 계산.
9. 결과: 예 (546,273) C1*는 length6 cycle 3276개로 [29]대비 sharp waterfall이나 error-floor 존재, CDT 적용 C3*는 cycle 감소로 error-floor 개선; BER 10^-8~10^-9까지 시뮬로 다수 기존부호(WiMAX/PEG/array/algebraic) 대비 우위.
10. 한계: HW·디코더 설계 전무, SP 디코딩·AWGN 시뮬만, NAND soft-read/양자화 미고려, 저차수(dv=3,4) 부호에 한정.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| PDF/CDT 기반 H-matrix 구성 | ecc_top.cpp Load_PCM() | 부호구조를 새로 생성해야 하나 Prime ECC는 특정 QC-LDPC(z=32,VN17) 고정이라 이식 부담 큼 |
| SP(Sum-Product) 디코딩 가정 | 대응 없음 | Prime ECC는 min-sum 기반, full-tanh SP는 미대응 |
| cycle수 기반 waterfall/error-floor 분석 | decoder.cpp LDPC_Decoder() (성능 관측 대상일 뿐) | 부호설계 지표이며 디코더 알고리즘 변경 아님 |
```

적용 가치: **낮음** - 순수 저차수 QC-LDPC 구성법으로, min-sum·고rate·고차수(VN17) 고정된 Prime ECC에 떼어 쓰기엔 부호 재설계·재검증 부담이 크고 HW·soft-read 이점이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1701.06218v1",
  "title": "On Advisability of Designing Short Length QC-LDPC Codes Using Perfect Difference Families",
  "year": 2017,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": "0.51~0.97",
  "code_length": "57~3960",
  "soft_quant": "무관",
  "key_contribution": "PDF/QPDF + column dispersion technique로 girth6 유지하며 short-cycle 수를 점진 조절해 waterfall/error-floor 균형",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 부호구성법(BER는 short-cycle 통계 의존), 특정 QC-LDPC 고정된 Prime ECC에 재설계·재검증 부담 큼",
  "todo_check": "Prime ECC의 고rate high-degree(VN17) 부호에는 dv=3,4 저차수 구성이 부적합할 수 있음"
}
```
