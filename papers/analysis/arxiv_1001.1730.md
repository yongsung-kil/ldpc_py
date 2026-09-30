### arxiv:1001.1730v1 - Divide & Concur and Difference-Map BP Decoders for LDPC codes (2010, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.77~0.916 |
| 부호length | 1057~2209 |
| 연판정 | soft-4bit+ |
| 핵심기여 | min-sum BP에 difference-map "overshoot 보정" 동역학을 이식해 error-floor를 크게 개선한 DMBP 디코더 |
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
| 한계,주의 | HW 미설계·이론적 근거 부족, DC 디코더는 undetected error 다발·다수 iteration 필요 |
| 추가확인 | DMBP의 파라미터 Z·overshoot 보정을 우리 min-sum 루프에 넣을 때 수렴/latency·양자화 영향 |

> 총평: min-sum 기반 error-floor 개선 아이디어(overshoot 보정)로 우리 decoder.cpp 루프에 이식 시도할 가치는 있으나, HW·복잡도 미검증에 iteration이 오히려 늘어 latency 리스크 큼.

### B. 알고리즘 요약

1. 대상: binary LDPC (random len-1057 rate-0.77, QC-array len-2209 rate-0.916), AWGN/BSC 채널, error-floor 영역이 표적.
2. 문제: 표준 BP는 trapping-set/pseudocodeword 때문에 고SNR에서 error-floor에 갇힌다.
3. 아이디어: Gravel-Elser의 "Divide and Concur"(DC)를 constraint graph 위 message-passing으로 재해석하고, difference-map(DM) 동역학으로 "trap"을 repeller로 바꾼다.
4. DC divide 투영 `PD`: 각 SPC 제약을 만족하는 최근접 hard-decision(홀수면 |m| 최소 비트 flip), 추가로 energy 제약 `-ΣLixi ≤ Emax`.
5. Emax 선택이 특이: `Emax = -(1+ε)Σ|Li|` 로 절대 만족 안 되게 두어 replica가 관측치 근처에 머물게 함(식 6).
6. DM 핵심식 `r_{t+1}=r_t+β[PC(fD)-PD(fC)]`, β=1은 Fienup hybrid input-output와 동일; 3단계(overshoot→concur→overshoot 보정)로 분해.
7. concur 투영 `PC`: 같은 변수 replica들의 평균(=belief). BP의 sum과 달리 average.
8. DMBP: min-sum BP에 (a) belief `bi=Z(Li+Σma→i)` 절충식(식 10), (b) 변수노드 메시지에 DC "overshoot 보정" 규칙(식 4) 이식. min-sum CN 규칙(식 9)은 그대로.
9. 결과: DMBP가 sum-product BP 대비 error-floor 극적 개선(예: len-1057 AWGN BP의 floor 제거), LP 디코더와 유사 성능·BP급 복잡도. 순수 DC는 iteration 많이 필요·undetected error 다발(SNR 7.31dB에서 오류 98%가 저확률 codeword).
10. 한계: HW 미설계, 이론적 근거 부족(직관 기반), 일부 absorbing set은 여전히 못 벗어남. soft real-valued 메시지 사용.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| min-sum CN 연산(식 9) | decoder.cpp CNU_Update_New_Mag(), C2V_Cal_New_Sgn() | DMBP는 min-sum CN 규칙을 그대로 사용 → 우리 CN 연산과 정합 |
| overshoot 보정·belief 절충(식 4,10) | decoder.cpp LDPC_Decoder() 이터레이션 루프, VN_Cal_HD() 등 | VN 메시지 갱신에 이전 iteration 메시지 의존 항 추가 → 루프·메모리 수정 필요 |
| Z 파라미터/LLR 스케일 | ecc_data.h PARAM_LLR, decoder.cpp Get_VNU_Table_Idx() | belief 스케일 Z를 적응형 LLR 테이블과 통합 시 대응 |
| energy 제약(DC 전용) | 대응 없음 | DC 전용, 우리 구조에 대응 모듈 없음 |
```

적용 가치: **중간** — DMBP의 overshoot 보정은 우리 min-sum decoder.cpp에 알고리즘 레벨로 붙일 수 있으나, HW·복잡도·latency 미검증이고 error-floor 개선 외 waterfall/iteration 이득이 없어 이식 리스크가 있음.

### D. JSON 블록

```json
{
  "id": "arxiv:1001.1730v1",
  "title": "Divide & Concur and Difference-Map BP Decoders for LDPC codes",
  "year": 2010,
  "venue": "arXiv [cs.IT]",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "1057~2209",
  "soft_quant": "soft-4bit+",
  "key_contribution": "min-sum BP에 difference-map overshoot 보정 동역학을 이식해 error-floor를 크게 개선한 DMBP 디코더",
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
  "caveat": "HW 미설계·이론적 근거 부족, DC 디코더는 undetected error 다발·다수 iteration 필요",
  "todo_check": "DMBP의 파라미터 Z·overshoot 보정을 우리 min-sum 루프에 넣을 때 수렴/latency·양자화 영향"
}
```
