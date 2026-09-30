### arxiv:0906.3410v1 - Quasi-cyclic LDPC codes with high girth (2009, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5~0.85 |
| 부호length | 200~19500 |
| 연판정 | 무관 |
| 핵심기여 | QC-LDPC Tanner graph의 girth≥10 보장 circulant exponent/separation 필요충분조건 완전 분류(weight-1/2 circulant), algebraic 구조로 random 수준 성능 달성 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | 동등 |
| 추천도 | 하 |
| 한계,주의 | weight-1/2 circulant·저rate(1/2 (2,4)/(3,6)) 예제 중심, 고rate NAND QC-LDPC 적용엔 조건 재검증 필요하고 girth-10 (3,6)도 BER 1e-9서 error floor |
| 추가확인 | Prime ECC 고rate weight-1 circulant base matrix에 girth≥10 조건 적용 시 error-floor 개선폭 및 기존 PEG/도구 대비 이점 |

> 총평: QC-LDPC(우리 부호 계열)의 girth 설계 조건 완전 분류로 error-floor에 직접 닿으나, 시연이 저rate regular라 고rate NAND엔 추가 설계·검증 필요.

### B. 알고리즘 요약

1. 대상: binary QC-LDPC 부호(H = circulant 블록 조립, weight-1/2 circulant), rate 0.5~0.85, length N≈200~19500.
2. 문제: algebraic(QC) 구조는 인코딩·해석에 유리하나 규칙성이 short cycle을 유발해 성능 저하; girth 보장 조건이 미정립.
3. 모델: H를 `m×m` circulant 부분행렬로 표준분해(`Mm,α,β,γ`, `Cm,α,β,γ`), 행렬 상 `2s-cycle`을 그래프가 아닌 행렬 entry 배치로 재정의.
4. 핵심 기법: `2s-cycle`이 존재할 수 있는 모든 (r,c) 배치 configuration을 `weights vector`(합=2s, 홀수 2개 불가)와 isolation lemma(3.10)로 완전 열거(길이<10).
5. 식 의미: circulant 다항식 `p=xᵃ+xᵇ`의 separation `s(p)=min(b−a,a+m−b)`가 cycle 존재를 결정 → Fan/Fossorier 조건 `Σ(ε(p1,k)−ε(p2,k))≡0 mod m`을 weight-2까지 일반화.
6. 확장: weight-2 circulant까지 포함(weight≥3은 내부 6-cycle이라 배제), circulant을 블록 대각선에 배치해 조건 판정 간소화 + HW 복잡도 절감 여지.
7. 구현 디테일: (2,4)-regular / (3,6)-regular girth-10 두 신규 family를 δ(대각선 거리) 조건으로 구성, degenerate case(δ=α/2,α/3,α/4)만 별도 처리.
8. 최적화 절차: 없음(조건을 만족/불만족시켜 결정론적 구성, random-walk 최적화 불필요).
9. 결과: girth-10 QC 부호가 동일 파라미터 random/MacKay/PEG 부호 대비 BLER 대등~우수; 특히 random 부호가 조기 error floor에 걸리는 구간에서 QC 부호는 floor 지연(Fig 18, 20).
10. 한계: HW 미설계·BLER 시뮬만, 저rate regular 예제 중심, girth-10 (3,6) 부호도 BER 1e-9서 error floor 관측.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| girth≥10 QC 부호구조/H-matrix 조건 | ecc_top.cpp `Load_PCM()` + H-matrix | Prime ECC의 QC base matrix(shift) girth 설계·검증에 exponent/separation 조건 적용 가능(error-floor 방지) |
| short-cycle 회피 → error-floor 개선 | decoder.cpp `LDPC_Decoder()` | error-floor는 복호 성능이나 개선은 부호설계에서 발생, 디코더 알고리즘 자체는 무변경 |

적용 가치: **중간** — QC-LDPC(우리 부호 계열)의 girth 조건은 error-floor에 직접 닿지만, 시연이 저rate regular라 고rate NAND base matrix 적용엔 조건 재도출·재검증이 필요.

### D. JSON 블록

```json
{
  "id": "arxiv:0906.3410v1",
  "title": "Quasi-cyclic LDPC codes with high girth",
  "year": 2009,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "200~19500",
  "soft_quant": "무관",
  "key_contribution": "QC-LDPC Tanner graph의 girth≥10 보장 circulant exponent/separation 필요충분조건 완전 분류(weight-1/2 circulant), algebraic 구조로 random 수준 성능 달성",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "동등",
  "recommend": "하",
  "caveat": "weight-1/2 circulant·저rate(1/2 (2,4)/(3,6)) 예제 중심, 고rate NAND QC-LDPC 적용엔 조건 재검증 필요하고 girth-10 (3,6)도 BER 1e-9서 error floor",
  "todo_check": "Prime ECC 고rate weight-1 circulant base matrix에 girth≥10 조건 적용 시 error-floor 개선폭 및 기존 PEG/도구 대비 이점"
}
```
