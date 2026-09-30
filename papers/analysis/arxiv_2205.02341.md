### arxiv:2205.02341v1 - Soft Syndrome Decoding of Quantum LDPC Codes for Joint Correction of Data and Syndrome Errors (2022, arXiv [quant-ph])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 1054 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 노이즈 신드롬의 아날로그(soft) LLR을 가상 변수노드로 도입해 MSA 체크노드 갱신을 수정, 데이터+신드롬 오류 동시정정 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | Quantum LDPC(CSS/스태빌라이저) 전용, 신드롬 자체가 노이즈라는 양자 특유 문제 - NAND 코드워드 노이즈 모델과 층위가 다름 |
| 추가확인 | soft-syndrome LLR 개념이 NAND의 신뢰 불가한 read/CRC 판정에 유비적으로 쓰일 여지가 있는지만 (직접 이식은 불가) |

> 총평: 양자 LDPC의 노이즈 신드롬 문제를 soft 정보로 푸는 이론/시뮬 연구로, 알고리즘 아이디어(신드롬 신뢰도 LLR)는 흥미롭지만 NAND binary QC-LDPC 디코더에 직접 이식 대상은 아니다.

### B. 알고리즘 요약

1. 시스템: lifted-product(LP) QC-QLDPC 부호(예 `[[1054,140,20]]`, 구성부호는 `[155,64,20]` Tanner code, circulant `L=31`), CSS 구조로 `H_X`, `H_Z` 별도 복호.
2. 문제: 양자 신드롬 측정 자체가 불안정 - 기존엔 신드롬을 이진 flip 확률로 모델링하거나 측정을 반복(single-shot)해야 함.
3. 모델: 이상적 bipolar(±1) 신드롬에 i.i.d. 대칭 가우시안 노이즈 `n_i~N(0,σ²)`를 더한 연속값 `r̃_i = s_i + n_i`, 신드롬 LLR `γ_i = 2r̃_i/σ²`.
4. 핵심기법: syndrome-based Min-Sum(MSA)을 수정 - 각 체크노드에 "가상 변수노드"를 붙여 신드롬 soft 정보 `γ_i`를 메시지 패싱에 주입.
5. 핵심식: 체크노드 갱신 `|µ_{i,j}| = min(min|ν|, |γ_i|)` (단 `|γ_i|>Γ`이면 기존 min 규칙), 부호는 `s_i·∏sgn(ν)`. cutoff `Γ`가 신드롬 신뢰 여부를 가른다.
6. 확장: 신드롬의 sign `s̃_i`와 reliability `γ̃_i`를 반복 중 갱신(식 7,8)해 추정 신드롬을 참 신드롬으로 밀어냄 - 정지조건 모호성 해소.
7. 구현: normalized MSA `β=0.75`, `max=100` iter, cutoff `Γ=5~10`.
8. 결과: 'Hard Syndrome'의 신드롬노이즈 임계 `σ≈0.25` → 'Soft'는 `σ≈0.4`로 상승, 'Hard'의 spurious "second threshold" 현상 제거, 평균 iteration이 'Perfect'에 근접(빠른 수렴).
9. 부수: 신드롬 보호용 별도 코드 없이 message passing만으로 측정오류를 추론, 반복 측정 오버헤드 회피.
10. 한계: 시뮬레이션만(HW 미설계), 양자 depolarizing/CSS 세팅 전용, 회로수준 노이즈는 future work.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 수정된 Min-Sum 체크노드 갱신 | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal()` | 개념적으로만 유사 - 우리 CN min-sum에 신드롬 soft항 개념은 양자 전용이라 그대로 대응 안 됨 |
| 신드롬 신뢰도 LLR `γ_i` | 대응 없음 | NAND 디코더는 코드워드 LLR을 다루며 신드롬 자체 노이즈 개념이 없음 |
| 조기종료(신드롬 정지조건) | partial_CRC.cpp `partial_crc_HW_T4()` | 정지조건이라는 역할은 겹치나 양자 신드롬 정합 문제와 무관 |
| 부호구조(LP-QLDPC) | 대응 없음 | non-classical, CSS/스태빌라이저 부호로 binary QC-LDPC 로더와 무관 |

적용 가치: **낮음** - 양자 CSS 부호의 노이즈 신드롬이라는 도메인 특유 문제로, NAND classical binary QC-LDPC 디코더 코드에 떼어 붙일 실질 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2205.02341v1",
  "title": "Soft Syndrome Decoding of Quantum LDPC Codes for Joint Correction of Data and Syndrome Errors",
  "year": 2022,
  "venue": "arXiv [quant-ph]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "1054",
  "soft_quant": "soft-4bit+",
  "key_contribution": "노이즈 신드롬의 아날로그(soft) LLR을 가상 변수노드로 도입해 MSA 체크노드 갱신을 수정, 데이터+신드롬 오류 동시정정",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "하",
  "caveat": "Quantum LDPC(CSS/스태빌라이저) 전용, 신드롬 자체가 노이즈라는 양자 특유 문제 - NAND 코드워드 노이즈 모델과 층위가 다름",
  "todo_check": "soft-syndrome LLR 개념이 NAND의 신뢰 불가한 read/CRC 판정에 유비적으로 쓰일 여지가 있는지만 (직접 이식은 불가)"
}
```
