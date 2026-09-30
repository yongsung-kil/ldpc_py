### arxiv:2506.13507v1 - Dynamic Layered Decoding Scheduling for LDPC Codes Aided by Check Node Error Probabilities (2025, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.386~0.4681 |
| 부호length | 1170~2640 |
| 연판정 | 무관 |
| 핵심기여 | 체크노드 error probability 오름차순 우선 업데이트 동적 LBP 스케줄(Dyn-EBP/PEBP), penalty로 중복업데이트 억제 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | 부분 |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | Fibonacci heap 기반 동적 재정렬은 HW 병렬 layered 파이프라인과 정합 어려움, BP(tanh)/full precision 가정이라 min-sum·양자화 재검증 필요 |
| 추가확인 | fixed 5-iter BLER만 그림 제공(수치 게인은 본문 서술 없음), min-sum·QC layer 실HW 스케줄에서의 이득 유지 여부 |

> 총평: error probability 기반 동적 layered 스케줄로 고정 iteration에서 수렴 효율을 높이나 BP 기반·동적 heap 재정렬로 HW 정합 부담이 있어 이식성 중.

### B. 알고리즘 요약

1. 대상: BI-AWGN 채널, 5G NR LDPC BG1 QC-LDPC, 블록길이 `1170~2640`, rate `0.386~0.4681`, iteration 5 고정.
2. 문제: flooding BP는 수렴 느리고 기존 동적 스케줄(residual/syndrome 기반)은 heuristic이라 이득 제한적.
3. 통찰: 효율적 스케줄은 error probability 낮은 체크노드를 우선 업데이트해야 함([11] 근거).
4. 핵심식: 체크노드 error prob `p^ci_ε = (1/2)(1 - ∏_{j∈N(ci)}(1 - 2/(1+e^|Lj|)))` (Lemma 2, λ=1), VN error prob은 `1/(1+e^|Lj|)`.
5. 의미: 체크노드가 이웃 VN들의 오류를 정정할 가능성을 LLR 크기로 정량화, 낮을수록 신뢰도 높음.
6. Dyn-EBP: 우선순위집합 `P`를 error prob 오름차순 유지, 각 iteration마다 체크노드를 정확히 1회씩 업데이트(업데이트 후 즉시 제거).
7. Dyn-PEBP: 1회 제약을 완화, penalty `p̃ = p^ci_ε + γ·li`(업데이트 횟수 li, γ∈[0,1])로 중복 업데이트 억제, γ=1이면 Dyn-EBP와 동일.
8. 구현: Fibonacci heap(INSERT/MINIMUM/DECREASE-KEY 상수시간)으로 재정렬 비용 절감, 반복당 복잡도 `O(E·d̄v·d̄c)`.
9. 결과: 5G NR BG1, iter=5에서 Dyn-EBP/PEBP(γ=0.35)가 LBP·LPHD·RD-RBP·[11] 대비 BLER 우위(그림 3), QC layer 평균 error prob로 스케줄.
10. 한계: HW 미설계·시뮬만, BP(tanh) full precision 가정, 정량 게인 수치는 본문 서술 없이 그림에만 존재.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 동적 layered 스케줄(체크노드 업데이트 순서) | decoder.cpp `LDPC_Decoder()` 이터레이션 루프 | dual-update(even/odd 교대) 스케줄 대체·보완 후보 |
| error probability 계산(LLR 기반) | decoder.cpp `VN_Cal_HD()`, `ecc_data.h` `PARAM_LLR` | LLR 값에서 파생, 양자화 LLR 테이블과 연동 필요 |
| QC layer 단위 스케줄 | decoder.cpp `C2V_Cal()` (z=32 row 병렬) | QC 리프팅 layer 단위 처리와 개념 정합 |

적용 가치: **중간** — 알고리즘 레이어(스케줄) 변경으로 이식점은 명확하나, Fibonacci heap 동적 재정렬과 BP 가정이 Prime ECC의 고정 파이프라인·min-sum·양자화와 정합에 추가 작업이 필요하다.

### D. JSON 블록

```json
{
  "id": "arxiv:2506.13507v1",
  "title": "Dynamic Layered Decoding Scheduling for LDPC Codes Aided by Check Node Error Probabilities",
  "year": 2025,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": "0.386~0.4681",
  "code_length": "1170~2640",
  "soft_quant": "무관",
  "key_contribution": "체크노드 error probability 오름차순 우선 업데이트 동적 LBP 스케줄(Dyn-EBP/PEBP), penalty로 중복업데이트 억제",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "부분",
  "latency": "개선",
  "recommend": "중",
  "caveat": "Fibonacci heap 기반 동적 재정렬은 HW 병렬 layered 파이프라인과 정합 어려움, BP(tanh)/full precision 가정이라 min-sum·양자화 재검증 필요",
  "todo_check": "fixed 5-iter BLER만 그림 제공(수치 게인은 본문 서술 없음), min-sum·QC layer 실HW 스케줄에서의 이득 유지 여부"
}
```
