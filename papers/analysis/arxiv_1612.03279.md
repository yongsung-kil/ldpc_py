### arxiv:1612.03279v1 - Graph Based Linear Error Correcting Codes (2016, Albanian J. Math.)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | regular |
| 부호rate | 0.33~0.83 |
| 부호length | 25~2401 |
| 연판정 | 무관 |
| 핵심기여 | Ustimenko-Woldar 대수 그래프를 유한체 대신 유한환 Zn/Zn²로 변형해 girth≥6 sparse bi-regular LDPC 부호 구성 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 그래프 이론 구성법, HW·디코더·양자화 논의 전무, 저rate/소규모 부호(N≤2401), BER 곡선은 그림에만 존재 |
| 추가확인 | 없음 (구성법 자체가 특정 QC-LDPC 고정 구조와 무관, 재검증 부담 큼) |

> 총평: 대수 그래프 기반 LDPC 부호 구성 이론 논문으로 NAND binary QC-LDPC ECC 이식 가치는 매우 낮음.

### B. 알고리즘 요약

1. 목표: Tanner 그래프 기반으로 sparse·bi-regular·short-cycle(C4) 없는 LDPC 부호를 대수 그래프로부터 구성.
2. 문제: 좋은 error-correcting 성질과 높은 rate를 동시에 만족하는 구성적 방법 필요.
3. 사용 그래프: Ustimenko-Woldar family `F(Fq, Fq²)` — bipartite, girth≥8, bi-regularity `(q, q²)`, |P|=q⁴ points, |L|=q⁵ lines.
4. 핵심 변형: 유한체 `Fq` 대신 유한환 `Zn, Zn²`와 modulo 연산 사용 → `F(Zn, Zn²)`, 모든 `n≥2`에 대해 정의 가능(소수 거듭제곱 제약 제거).
5. 인접행렬 `A=[[0,H],[Hᵀ,0]]`에서 H를 부호의 parity-check matrix로 사용, 라인=코드워드 비트, 점=parity check.
6. rate 공식: 방식1은 `RC=(n-1)/n`, 방식2(좌표 제한으로 bi-degree 축소)는 `RC=(r-n)/n`으로 조절.
7. bi-degree 축소는 girth를 높이지만 rate를 낮추고 disconnected 될 수 있어 한 component만 사용.
8. 규칙적(regular) LDPC 부호 산출 — H의 모든 열 weight 동일.
9. 결과: AWGN 채널 시뮬레이션으로 [243,162], [1024,768], [2000,1375] 등 부호의 BER 측정, 기존 D(n,q) 그래프 기반 부호보다 나은 정정 성질 주장(그림 3~5).
10. 한계: 순수 구성법으로 디코더/HW/양자화 설계 없음, 부호 크기 작고 rate 낮음, 성능 수치는 그림에만 존재.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 그래프 기반 H-matrix 구성 | ecc_top.cpp `Load_PCM()` | Prime ECC는 특정 QC-LDPC(circulant) 고정, 이 대수 그래프 구성은 QC 구조와 무관해 이식 부담 큼 |
| bi-regular sparse 부호설계 | 대응 없음 | QC-LDPC circulant 구조가 아니어서 base+shift 표현으로 매핑 불가 |
| 디코더 | 대응 없음 | 논문은 "기존 디코더 사용"만 언급, 신규 복호 기법 없음 |

적용 가치: **낮음** — NAND용 고rate binary QC-LDPC와 구조·rate·규모가 모두 어긋나고 HW/디코더 기여가 전무하다.

### D. JSON 블록

```json
{
  "id": "arxiv:1612.03279v1",
  "title": "Graph Based Linear Error Correcting Codes",
  "year": 2016,
  "venue": "Albanian Journal of Mathematics",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "regular",
  "code_rate": null,
  "code_length": "25~2401",
  "soft_quant": "무관",
  "key_contribution": "Ustimenko-Woldar 대수 그래프를 유한환 Zn/Zn²로 변형해 girth≥6 sparse bi-regular LDPC 부호 구성",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 그래프 이론 구성법, HW·디코더·양자화 논의 전무, 저rate/소규모 부호, BER은 그림에만 존재",
  "todo_check": "없음 (특정 QC-LDPC 고정 구조와 무관, 재검증 부담 큼)"
}
```
