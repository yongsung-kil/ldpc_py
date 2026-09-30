### arxiv:2105.03462v1 - Necessary and Sufficient Girth Conditions for Tanner Graphs of Quasi-Cyclic LDPC Codes (2021, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.4 |
| 부호length | 1225~13545 |
| 연판정 | 무관 |
| 핵심기여 | protograph QC-LDPC의 girth 6~12 필요충분조건을 HHᵀ 부분행렬(C_H) 성질로 유도, lifting exponent를 손으로도 계산 가능한 고속 알고리즘 제시, pre-lifting으로 girth 14 구성 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | 부호설계(H 구성)만 다루고 디코더·HW 미설계, 예시가 (2,nv)·(3,nv)-regular 완전연결 protograph·저rate(R≈0.4) 중심 |
| 추가확인 | Prime ECC의 고rate(~0.9) QC-LDPC/펑처링·비대칭 degree(VN 17, HCU) 구조에 girth 조건 적용 시 최소 lifting factor N과 z=32 정합성 |

> 총평: QC-LDPC girth 필요충분조건과 고속 lifting-exponent 알고리즘을 준 부호설계 이론으로, error-floor 개선 관점에서 참고 가치 있으나 고rate NAND QC-LDPC 재설계·재검증 부담 존재.

### B. 알고리즘 요약

1. 대상: protograph-based binary QC-LDPC, base matrix를 N×N circulant permutation `x^r`로 lifting; 예시 (2,nv)·(3,nv)-regular 완전연결 protograph, R≈2/5, length 1225~13545.
2. 문제: Tanner graph의 짧은 cycle(작은 girth)이 BP 상관·trapping/absorbing set·error-floor·최소거리 상한 저하를 유발 → 큰 girth가 필요.
3. 핵심 연결: girth(H)를 `B_n(H)=(HHᵀ)^⌊n/2⌋ H^(n mod 2)`로 특징화(Thm 1), girth(H)>2g ⟺ `B_t(H)△B_{t-2}(H)=0`.
4. (2,nv) 경우: 순열합 `C21=∏PᵢᵀQᵢ`에 대해 `girth(H)=2·girth(C21)` — H의 cycle이 훨씬 작은 N×N 행렬 cycle과 1:1 대응.
5. (3,nv) 경우: `CH`(3N×3N, `HHᵀ=nvI+CH`) 부분행렬로 girth>4/6/8/10/12를 각각 `CH^k△(...)=0` 형태 필요충분조건으로 환원(Thm 6).
6. 의미: 성긴 조건집합이라 lifting exponent `i_l, j_l` 선택을 "forbidden set에 없는 최소 양수" 재귀 규칙(Type A/B 알고리즘)으로 손으로도 산출 가능.
7. 구성 예: (3,7)/(3,8)-regular girth 10을 작은 N(예 N=219~433)으로, girth 12는 Example 14(N=245, n=1225)로 구성.
8. girth>12 확장: 단일 lifting로 불가 → 비순환 permutation을 쓰는 pre-lifting(2단 lifting)으로 girth 14 및 최소거리 상한 `(nc+1)!` 초과 달성(Example 15,16, N=891/903).
9. 결과: BPSK/AWGN, sum-product 100 iter 시뮬에서 고girth 부호는 저SNR서 약간 열세이나 error-floor 영역서 우세, 긴 부호(Ex 15,16)는 BER 10⁻⁷까지 error-floor 무징후.
10. 한계: 순수 부호설계 이론으로 디코더·HW 미설계, 예시가 저rate·regular 완전연결 protograph 중심, 고rate/펑처링 부호 적용은 별도 검증 필요.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| girth 조건 만족 H-matrix 구성/로드 | ecc_top.cpp `Load_PCM()` | 부호구조(PCM) 재설계 대상, 고정 QC-LDPC 재검증 부담 큼 |
| lifting exponent(circulant shift) 선택 | ecc_data.h `PCM_b`(base+shift) | base+circulant shift 구조와 개념 일치, shift 값 최적화에 직접 대응 |
| error-floor/trapping-set 완화(고girth) | decoder.cpp `LDPC_Decoder()` (성능측면) | 부호설계가 복호 error-floor 개선에 기여, 디코더 알고리즘 변경은 아님 |
| pre-lifting(비순환 permutation) | 대응 없음 | Prime ECC는 QC circulant 고정, 비순환 lifting 구조 미지원 |

적용 가치: **중간** — Prime ECC의 base+circulant-shift QC-LDPC 구조에 girth 조건과 고속 lifting-exponent 알고리즘을 직접 대응시켜 error-floor를 낮출 여지가 있으나, 논문 예시가 저rate·regular라 고rate(~0.9)·펑처링·비대칭 degree 부호에 적용하려면 조건 재유도와 H 재검증 부담이 있다.

### D. JSON 블록

```json
{
  "id": "arxiv:2105.03462v1",
  "title": "Necessary and Sufficient Girth Conditions for Tanner Graphs of Quasi-Cyclic LDPC Codes",
  "year": 2021,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": 0.4,
  "code_length": "1225~13545",
  "soft_quant": "무관",
  "key_contribution": "protograph QC-LDPC의 girth 6~12 필요충분조건을 HHᵀ 부분행렬(C_H) 성질로 유도, lifting exponent를 손으로도 계산 가능한 고속 알고리즘 제시, pre-lifting으로 girth 14 구성",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "부호설계(H 구성)만 다루고 디코더·HW 미설계, 예시가 (2,nv)·(3,nv)-regular 완전연결 protograph·저rate(R≈0.4) 중심",
  "todo_check": "Prime ECC의 고rate(~0.9) QC-LDPC/펑처링·비대칭 degree(VN 17, HCU) 구조에 girth 조건 적용 시 최소 lifting factor N과 z=32 정합성"
}
```
