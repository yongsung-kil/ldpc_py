### arxiv:0805.1662v1 - Eliminating Trapping Sets in Low-Density Parity Check Codes by using Tanner Graph Covers (2008, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | regular |
| 부호rate | 0.41~0.5 |
| 부호length | 155~5280 |
| 연판정 | 무관 |
| 핵심기여 | 그래프 이중커버 + 에지 스와핑으로 지배적 trapping set 제거해 error floor 저감(길이 2배, 정규성/디코더 유지) |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | 악화 |
| 추천도 | 중 |
| 한계,주의 | 코드 길이 2배 필요 + 이중커버가 QC circulant 구조 비보존 → 고정길이 고rate NAND QC-LDPC 직접 적용 곤란 |
| 추가확인 | QC 구조/길이 고정 조건에서 지배적 trapping set만 선택적으로 제거하는 변형 가능성 |

> 총평: error floor 저감이라는 관심 주제이나 방법의 본질이 길이 2배·이중커버 재구성이라 고정 고rate QC-LDPC 이식성은 낮음.

### B. 알고리즘 요약

1. 대상은 임의의 이진 LDPC 코드 `C`(길이 `n`, rate `r`); BSC/Gallager B 및 AWGN/min-sum(500 iter)로 검증.
2. 문제: high-SNR error floor는 Tanner 그래프의 지배적 `(a,b)` trapping set(작은 critical number)에 의해 지배됨.
3. 모델: FER를 `log(FER)≈log(c_i)+i·log(α)`로 근사, 기울기 `i`(최소 critical number = instanton 크기)가 error floor를 지배.
4. 핵심기법: 같은 코드 두 복사본으로 `H^(2)=[[H,0],[0,H]]` 초기화 후, trapping set을 이루는 에지 `e`를 두 복사본 사이에서 "swap"(이중커버 구성).
5. 스와핑은 `H^(2)=[[H',B],[B,H']]`, `H'+B=H` 형태로 지배적 trapping set을 깨뜨려 critical number를 상향.
6. 알고리즘: critical number 오름차순 정렬 → 최소 trapping set의 에지 swap → 나머지 에지 freeze(재도입 방지) → 반복.
7. 트릭: 하나의 trapping set에만 속한 에지를 swap하면 랜덤 없이 전부 제거 보장(예: Margulis (4,4) 1320개).
8. 이론: Thm1 rate `r^(2)≥r`(full rank면 `=r`), Thm2 최소거리 `2d_min≥d^(2)_min≥d_min`; `H',B` 분할로 convolutional LDPC 확장 가능.
9. 결과: Margulis (2640,1320)→(5280,2640)에서 (4,4) 제거, Tanner (155,64)→(310,126)에서 critical number 3→4, AWGN 기울기 14→20으로 개선.
10. 한계: HW 미설계, 시뮬만, 길이가 2배로 증가하고 지배적 trapping set을 사전에 알아야 함.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 이중커버 H^(2) 구성/에지 스와핑 | ecc_top.cpp Load_PCM() | trapping set 제거 위한 H 재구성이나 길이 2배·비QC로 로드 구조와 불합치 |
| error floor 개선된 코드 복호 | decoder.cpp LDPC_Decoder() | 디코더 알고리즘 변경 없이 코드만 교체(개선효과는 코드측) |
| Gallager B / min-sum 검증 | decoder.cpp CNU_Update_New_Mag() | min-sum은 이미 보유, 본 기법은 디코더 불변 |
```

적용 가치: 낮음 — error-floor 관점은 유효하나 길이 2배 및 QC circulant 비보존으로 고정 고rate NAND QC-LDPC에 직접 이식 곤란.

### D. JSON 블록

```json
{
  "id": "arxiv:0805.1662v1",
  "title": "Eliminating Trapping Sets in Low-Density Parity Check Codes by using Tanner Graph Covers",
  "year": 2008,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "regular",
  "code_rate": null,
  "code_length": "155~5280",
  "soft_quant": "무관",
  "key_contribution": "그래프 이중커버 + 에지 스와핑으로 지배적 trapping set 제거해 error floor 저감(길이 2배, 정규성/디코더 유지)",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "악화",
  "recommend": "중",
  "caveat": "코드 길이 2배 필요 + 이중커버가 QC circulant 구조 비보존 → 고정길이 고rate NAND QC-LDPC 직접 적용 곤란",
  "todo_check": "QC 구조/길이 고정 조건에서 지배적 trapping set만 선택적으로 제거하는 변형 가능성"
}
```
