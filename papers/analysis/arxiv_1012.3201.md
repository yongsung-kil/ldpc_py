### arxiv:1012.3201v1 - Cyclic and Quasi-Cyclic LDPC Codes on Row and Column Constrained Parity-Check Matrices and Their Trapping Sets (2010, IEEE Trans. Information Theory (submitted))

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.51~0.77 |
| 부호length | 63~4095 |
| 연판정 | soft-4bit+ |
| 핵심기여 | Circulant 분해로 cyclic↔QC 등가변환 + RC-constrained regular 부호가 min-weight보다 작은 harmful trapping set이 없음을 증명(error-floor를 min-weight가 지배) |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | 부분 |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | FG/finite-field 대수부호 전용(EG/PG 기반)이라 우리 특정 QC-LDPC와 부호구조 상이, HW 미설계·순수 시뮬 |
| 추가확인 | 우리 고rate binary QC-LDPC(z=32)가 RC-constraint+girth6 이상이면 "size≤γ trapping set 없음" 보증이 적용되는지, absorbing set까지 커버되는지 |

> 총평: cyclic↔QC 등가 분해와 "min-weight가 error-floor를 지배"하는 trapping-set 보증 이론은 유익하나, EG/PG 대수부호 특정 클래스라 우리 QC-LDPC에 그대로 이식은 제한적.

### B. 알고리즘 요약

1. `n×n` circulant `Ψ(w)`를 `n=c·l`로 인수분해하고 인덱스 순열 `π`(식 (2)(3))로 `c×c` 크기 `l×l` circulant array `Φ(w)`로 분해(doubly-cyclic 구조).
2. 문제: cyclic LDPC 부호는 FG 기반 한 클래스뿐이라 종류가 적음 → circulant 분해로 cyclic/QC descendant 부호를 대량 파생시켜 repertoire 확장.
3. 모델: RC-constraint(두 행/열이 최대 1곳만 공통 nonzero) → girth ≥ 6, 최소거리 ≥ `γ_min+1`. one-step majority-logic decodable.
4. 핵심기법1: type-1/2/3 cyclic descendant + QC descendant 정의. masking(circulant을 zero matrix로 대체)로 type-3 파생.
5. 핵심식: parity-check polynomial `h(X)=Σσ_i v_i(X)` (식 (26)-(29))로 생성다항식 근 `β_i`를 통해 descendant 부호의 근을 특성화(BCH bound로 min-weight 하한).
6. 핵심기법2: cyclic FG-LDPC(EG/PG)에서 RC-constrained cyclic·QC descendant LDPC 부호 유도(2D 및 고차원 Euclidean/Projective geometry).
7. 구현 디테일: Fourier transform(Vandermonde `V`)으로 descendant circulant의 rank를 대각원소 nonzero 개수로 계산.
8. Trapping-set 분석: RC-constrained `(γ,ρ)`-regular 부호는 크기 ≤ `γ`, odd-degree check ≤ `γ`인 trapping set이 없음. 여러 FG/finite-field 부호는 min-weight보다 작은 elementary trapping set(및 degree-1 check 수)이 없어 error-floor가 min-weight로 지배됨.
9. 결과: (4095,3367),(1365,765,R=0.56),(1365,701,R=0.5135) 등 EG-LDPC와 QC descendant를 SPA/scaled-MS/SRBI-MLGD로 AWGN에서 시뮬 — 낮은 error-floor, 빠른 수렴(MS 5/10/50 iter 곡선 거의 중첩). Fig.13 (992,750) QC부호는 FPGA min-sum 결과 병기.
10. 한계: HW 자체 설계 없음(FPGA는 성능 참조용), 대수부호 특정 클래스(EG/PG) 전용, 우리 QC-LDPC와 구조 상이.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| circulant 분해로 cyclic↔QC H-matrix 변환 | ecc_top.cpp `Load_PCM()` | H-matrix 로드에 대응. QC 등가변환 개념 참고 가능하나 우리 부호는 이미 QC circulant 고정 |
| masking으로 부호 rate/구조 조정 | encoder.cpp `Generate_PCM_encoding()` | 부호 PCM 생성과 개념적 연관(우리는 dual-diagonal 고정) |
| RC-constraint 기반 trapping-set 보증(min-weight 지배) | 대응 없음 | 우리 특정 QC-LDPC의 trapping/absorbing set 보증에 직접 적용은 재검증 필요 |
| SPA/scaled-MS 복호 성능 | decoder.cpp `LDPC_Decoder()`, `CNU_Update_New_Mag()` | 우리 min-sum과 정합(scaled-MS 결과 참고 가능) |

적용 가치: **중간** — cyclic↔QC 등가분해와 "RC-constraint→size≤γ trapping set 부재, error-floor를 min-weight가 지배"라는 보증 이론은 우리 고rate QC-LDPC의 error-floor 근거 확보에 참고 가치가 있으나, EG/PG 대수부호 특정 클래스라 부호구조 직접 이식은 제한적.

### D. JSON 블록

```json
{
  "id": "arxiv:1012.3201v1",
  "title": "Cyclic and Quasi-Cyclic LDPC Codes on Row and Column Constrained Parity-Check Matrices and Their Trapping Sets",
  "year": 2010,
  "venue": "IEEE Trans. Information Theory (submitted)",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": "0.51~0.77",
  "code_length": "63~4095",
  "soft_quant": "soft-4bit+",
  "key_contribution": "Circulant 분해로 cyclic↔QC 등가변환 + RC-constrained regular 부호가 min-weight보다 작은 harmful trapping set이 없음을 증명(error-floor를 min-weight가 지배)",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "부분",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "FG/finite-field 대수부호(EG/PG) 전용이라 우리 특정 QC-LDPC와 구조 상이, HW 미설계·순수 시뮬",
  "todo_check": "우리 고rate binary QC-LDPC(z=32, RC-constraint girth6+)에 size≤γ trapping set 부재 보증이 적용되는지, absorbing set까지 커버되는지"
}
```
