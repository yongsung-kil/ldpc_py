### arxiv:1701.05686v1 - High Rate LDPC Codes from Difference Covering Arrays (2017, arXiv math.CO)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | regular |
| 부호rate | 0.742~0.899 |
| 부호length | 132~870 |
| 연판정 | 무관 |
| 핵심기여 | difference covering array/pseudo-orthogonal Latin square로 모든 n에 존재하는 길이 4n^2-2n regular LDPC 구성, rate·최소거리 명시식 제공 |
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
| 한계,주의 | 순수 조합론 구성법으로 BER/디코더/HW 전무, QC 구조 아님(cyclic PBIBD 기반), 최소거리 6(n홀수)/4(n짝수)로 작음 |
| 추가확인 | 이 구성이 QC-LDPC 형태로 변환 가능한지, girth-6·d=6이 error-floor에 주는 실측 영향 |

> 총평: DCA/pseudo-orthogonal Latin square 기반의 순수 이론 부호구성법(math.CO)으로 디코더·HW·성능 실험이 전무하고 최소거리도 6 이하 — NAND용 고rate QC-LDPC에 직접 이식 가치는 낮음.

### B. 알고리즘 요약

1. difference covering array `DCA(k,2n;2n)`(cyclic group `Z_2n` 기반)로부터 regular binary LDPC 부호를 조합론적으로 구성하는 방법.
2. 풀려는 문제: BIBD/Latin square 기반 기존 구성은 존재 차수가 소수거듭제곱 등으로 제한되어 고rate·유연 길이 부호를 얻기 어려움.
3. 핵심 모델: RC-constraint(임의 두 행/열 내적 <=1) 만족 -> Tanner graph girth >= 6 보장.
4. 핵심 기법 1단: `DCA*(3,2n;2n)`(식 (1)의 `x(j,g)`)로 2n-1개 starter block을 orbit 전개해 resolvable cyclic `PBIBD(6n,3)`(lambda<=1) 생성.
5. 의미: PBIBD의 pair-occurrence lambda<=1이 곧 열/행 내적 조건이 되어 short cycle 부재를 수식으로 보장.
6. 핵심 기법 2단: PBIBD incidence matrix를 `H`(크기 `6n x (4n^2-2n)`, col weight `gamma=3`, row weight `rho=2n-1`)로 삼아 부호 정의.
7. 부수: pseudo-orthogonal Latin square와의 동치 연결(Theorem 3.1)로 구성을 재해석, 증명 보조.
8. 이론 결과: `rank(H)=6n-2` 증명 -> rate `= (4n^2-8n+2)/(4n^2-2n)`, 최소거리 `d=6`(n홀수)/`4`(n짝수) 명시.
9. 수치: rate가 n=8에서 0.808, n=15에서 0.899 (길이 240~870) — 기존 조합론 부호보다 훨씬 짧은 길이로 rate>=0.8 달성.
10. 한계: 디코더/복호 성능/BER 시뮬 전무, HW 없음, QC 구조 아님, d<=6로 정정능력 자체는 작음.

### C. Prime ECC 관련 모듈 핀포인트

대상이 `code-design`이므로 C섹션(디코더 성능)은 전부 N/A. 참고용 모듈 대응만 표기.

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| DCA/PBIBD 기반 H-matrix 구성 | ecc_top.cpp `Load_PCM()` | H-matrix 로드 지점이나 우리는 QC(base+circulant) 고정 — 구조 자체가 상이 |
| regular(gamma=3, rho=2n-1) 부호구조 | 대응 없음 | Prime ECC는 VN degree 17급 고rate QC-LDPC, gamma=3 sparse와 불일치 |
| girth-6 / 최소거리 이론 보증 | 대응 없음 | 부호설계 이론이며 우리 코드에 대응 함수 없음 |

**적용 가치**: 낮음 — 순수 조합론 부호구성 이론으로 QC 구조도, 디코더/HW도 없고 col weight 3·d<=6이 NAND용 고rate QC-LDPC 스펙과 맞지 않아 이식 대상이 아니다.

### D. JSON 블록

```json
{
  "id": "arxiv:1701.05686v1",
  "title": "High Rate LDPC Codes from Difference Covering Arrays",
  "year": 2017,
  "venue": "arXiv math.CO",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "regular",
  "code_rate": "0.742~0.899",
  "code_length": "132~870",
  "soft_quant": "무관",
  "key_contribution": "difference covering array/pseudo-orthogonal Latin square로 모든 n에 존재하는 길이 4n^2-2n regular LDPC 구성, rate·최소거리 명시식 제공",
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
  "caveat": "순수 조합론 구성법으로 BER/디코더/HW 전무, QC 구조 아님(cyclic PBIBD 기반), 최소거리 6(n홀수)/4(n짝수)로 작음",
  "todo_check": "이 구성이 QC-LDPC 형태로 변환 가능한지, girth-6·d=6이 error-floor에 주는 실측 영향"
}
```
