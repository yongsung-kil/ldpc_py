### arxiv:1001.3421v2 - Multilevel Decoders Surpassing Belief Propagation on the Binary Symmetric Channel (2011, arXiv [cs.IT] / ISIT 2010)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.4~0.82 |
| 부호length | 155~4085 |
| 연판정 | hard-1bit |
| 핵심기여 | trapping-set 지식으로 유도한 3-bit multilevel 메시지 갱신규칙(LT/NLT)로 error-floor에서 BP/min-sum 상회 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | BP/min-sum 대비 소수(fraction), gatecount 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 상 |
| 한계,주의 | BSC 전용·3-left-regular(dv=3) 코드 한정, HW 미설계, 규칙 유도가 trapping-set ontology 지식에 의존 |
| 추가확인 | 우리 고rate QC-LDPC(VN degree 17)에 3-bit LT/NLT 규칙 확장 가능성, soft-2/3bit 채널 확장 여부 |

> 총평: min-sum과 동일 CN 연산·3-bit 메시지로 error-floor에서 BP를 능가하고 iteration까지 줄이는 매우 매력적 접근이나, BSC·dv=3 한정과 규칙 유도의 코드 종속성이 우리 고rate·고degree QC-LDPC 이식의 큰 장벽.

### B. 알고리즘 요약

1. 대상: BSC 위 binary LDPC, 3-left-regular(dv=3), 코드 3종(Tanner n=155 R=0.4 / QC n=768 R=0.75 dmin=12 / MacKay n=4085 R=0.82).
2. 문제: 기존 양자화 BP/min-sum은 asymptotic threshold 최적화라 유한길이·고SNR error-floor에서 trapping set 때문에 나쁘고, 양자화 자체가 floor를 유발.
3. 새 관점: 메시지가 belief의 양자화가 아니라 유한 레벨 집합 `M={0,±Li}`; 갱신규칙을 BP 근사가 아니라 trapping-set/ontology 지식으로 유도해 특정 오류패턴 정정을 보장.
4. 디코더 정의 `F=(M,Y,Φv,Φc)`; BSC 채널값 `Y={±C}`, `yi=(-1)^{ri}C`. 시간불변·대칭 규칙.
5. CN 규칙 `Φc = Πsgn(mj)·min|mj|` — min-sum CN과 정확히 동일.
6. VN 규칙 2종: LT `Φv=Q(Σmj+yi)`(임계값 집합 T로 양자화 Q), NLT `Φv=Q(Σmj+ωc·yi)`(채널가중 `ωc=Ω(m)`가 비선형이라 같은 합이라도 다른 출력 → 기존 양자화 min-sum과 구별).
7. 핵심 개념 isolation assumption: trapping set 유발 부분그래프를 고립시켜 독립 분석(Gallager independence보다 약한 조건). isolation theorem으로 degree-1 체크 메시지 `µl=Φv(µl-1,µl-1,C)` 결정.
8. 규칙 유도: trapping-set ontology 계층에서 critical number 증가·수렴 iteration 최소화를 기준으로 3-bit LT(7-level)·NLT(5-level) 규칙을 유일하게 정의(예: LT는 L1<C<2L1, L2=2L1+C 등).
9. 결과: 3-error 패턴 예제에서 min-sum이 4 iter·미보장인데 7-level LT는 3 iter에 수렴·모든 3-error 정정; Tanner 코드 5-error 전부 정정(LP도 실패), 세 코드 모두 error-floor에서 BP 능가하며 복잡도는 BP/min-sum의 일부.
10. 한계: BSC 전용, 3-left-regular(dv=3) 한정, HW 미설계, 규칙 유도가 코드별 trapping-set 지식 의존(다만 같은 3-bit 규칙이 여러 코드에 통함=universality 시사).

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| CN 규칙 Φc (=min-sum) | decoder.cpp CNU_Update_New_Mag(), C2V_Cal_New_Sgn() | CN 연산이 우리 min-sum과 동일 → CN부 재사용 가능 |
| VN 규칙 Φv (LT/NLT 임계 양자화) | decoder.cpp VN_Cal_HD() 등, decoder.h Get_VNU_* | VN 갱신을 belief 합 대신 임계기반 3-bit map으로 교체 필요 |
| 3-bit 메시지/임계 테이블 | ecc_data.h PARAM_LLR, decoder.cpp Get_VNU_Table_Idx() | 레벨/임계 집합을 LLR 테이블 형태로 이식 가능 |
| trapping-set 기반 규칙 유도 | 대응 없음 (corner.cpp는 수렴실패 추적만) | 규칙 유도 과정 자체는 오프라인, 우리 코드 대응 모듈 없음 |
| H-matrix/부호구조 | ecc_top.cpp Load_PCM() | dv=3 전제라 우리 고degree QC-LDPC와 부정합 |
```

적용 가치: **중간** — CN이 min-sum과 동일하고 VN을 3-bit 임계 map으로 바꾸면 error-floor·iteration 동시 개선 가능성이 커 매력적이나, BSC·dv=3 한정과 규칙의 trapping-set 종속성 때문에 우리 고rate·VN degree 17 QC-LDPC로의 확장 검증 부담이 큼.

### D. JSON 블록

```json
{
  "id": "arxiv:1001.3421v2",
  "title": "Multilevel Decoders Surpassing Belief Propagation on the Binary Symmetric Channel",
  "year": 2011,
  "venue": "arXiv [cs.IT] / ISIT 2010",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": null,
  "code_length": "155~4085",
  "soft_quant": "hard-1bit",
  "key_contribution": "trapping-set 지식으로 유도한 3-bit multilevel 메시지 갱신규칙(LT/NLT)로 error-floor에서 BP/min-sum 상회",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "BP/min-sum 대비 소수(fraction), gatecount 미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "상",
  "caveat": "BSC 전용·3-left-regular(dv=3) 코드 한정, HW 미설계, 규칙 유도가 trapping-set ontology 지식에 의존",
  "todo_check": "우리 고rate QC-LDPC(VN degree 17)에 3-bit LT/NLT 규칙 확장 가능성, soft-2/3bit 채널 확장 여부"
}
```
