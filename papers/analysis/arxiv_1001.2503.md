### arxiv:1001.2503v1 - Check Reliability Based Bit-Flipping Decoding Algorithms for LDPC Codes (2010, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5~0.93 |
| 부호length | 255~2048 |
| 연판정 | hard-1bit |
| 핵심기여 | check node reliability를 정의해 bit-flipping(BF) 비용/신뢰도 갱신에 반영한 soft/hard CRBF 디코더 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | min{M+1, dv(dc-1)+1} ops/iter (gatecount 미상) |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | HW 미설계·병렬화 미논의, iter당 1비트 flip 순차성이 min-sum 파이프라인과 상충 가능 |
| 추가확인 | check reliability 갱신식(9,11)의 HW 비용·다비트 flip 병렬화 가능성, min-sum 대비 실이득 |

> 총평: BF 계열을 SPA/min-sum에 근접시킨 저복잡도 디코더지만, 우리 코드는 이미 min-sum 기반이고 BF는 별도 아키텍처라 직접 이식보다는 저전력 백업 디코더 관점의 참고 가치.

### B. 알고리즘 요약

1. 대상: regular binary (N,K)(dv,dc) LDPC, BPSK/AWGN, 코드 4종(504,252)/(255,175)/(1440,1344)/(2048,1723), rate 0.5~0.93.
2. 문제: BF 계열은 SPA/MSA보다 훨씬 단순하나 성능 격차가 크다. 이를 줄이려 함.
3. 접근: ML 지표에서 출발해 parity 제약을 완화, global cost(GC) `E(x̂)=-Σx̂iyi - αΣŝj`(식4)로 근사. GC 최소화 = 총 신뢰도 최대화.
4. local cost(LC) `Ei = -x̂iyi + γΣ_{j∈M(i)} ŝj`(식6), `-Ei`가 양수면 변수노드 신뢰도. iter마다 LC 최대(가장 불신뢰) 비트를 flip.
5. 핵심 신규 정의: check node reliability `Rmn=max(-R*mn,0)`(식7), `R*mn=max_{n'∈N(m)\n} En'`(식8) — 체크노드가 전달하려는 정보의 불신뢰도를 이웃 변수노드 최대 LC로 측정.
6. 반복형 LC 갱신 `Ei = -x̂i·yi + γΣ Rji·ŝj`(식9), `R*ji=max_{i'∈N(j)\i}(Ei'^{l-1} - γŝj^{l-1}Rji'^{l-1})`(식11) — 신뢰 높은 체크에 큰 가중.
7. soft-CRBF: yi(수신 soft값) 사용. hard-CRBF: Step4에서 yi를 ẑi(hard-decision)로 대체 → 순수 HD 디코더.
8. 절차: iter마다 (a) 최대 LC 비트 flip, (b) syndrome 계산·조기종료, (c) 각 체크 reliability 계산, (d) LC 갱신. Imax=30~70.
9. 결과: soft-CRBF가 WBF/MWBF/IMWBF 대비 0.35~3dB 개선, 일부 코드는 SPA에 근접·우세. hard-CRBF는 표준 BF 대비 0.5~2dB 개선, 일부 코드에서 WBF류도 상회. 복잡도는 SPA보다 크게 낮음.
10. 한계: HW 미설계, 병렬화/처리량 미논의, iter당 1비트 flip 가정(순차). error-floor 명시 분석 없음.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| CRBF 디코딩 알고리즘 전체 | decoder.cpp LDPC_Decoder() 이터레이션 루프 | BF 계열은 우리 min-sum 루프와 별개 아키텍처 → 대체/백업 디코더로만 삽입 가능 |
| bit-flip 비용·신뢰도 갱신(식6,9) | decoder.cpp VN_Cal_HD() 등, decoder.h Get_VNU_* | 변수노드 처리부에 LC/reliability 계산 로직 추가 필요 |
| check reliability 계산(식7,8,11) | decoder.cpp CNU_Update_New_Mag(), C2V_Cal_New_Sgn() | CN 연산을 min-sum 대신 reliability 갱신으로 교체 시 대응 |
| 조기종료(syndrome=0) | partial_CRC.cpp / full_CRC.cpp | 우리는 CRC 조기종료, 논문은 syndrome 체크 → 개념 대응 |
| hard/soft 입력 선택 | channel.cpp Set_R_Offset(), Set_LLR_Th() | hard-CRBF(1bit)/soft-CRBF 입력 경로에 대응 |
```

적용 가치: **낮음** — 우리 엔진은 이미 min-sum(성능 우위) 기반이라 BF 계열 CRBF의 직접 이식 이득이 제한적. hard-CRBF의 저복잡도·1bit read 특성이 저전력 백업 디코더 아이디어로만 참고 가치.

### D. JSON 블록

```json
{
  "id": "arxiv:1001.2503v1",
  "title": "Check Reliability Based Bit-Flipping Decoding Algorithms for LDPC Codes",
  "year": 2010,
  "venue": "arXiv [cs.IT]",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": null,
  "code_length": "255~2048",
  "soft_quant": "hard-1bit",
  "key_contribution": "check node reliability를 정의해 bit-flipping 비용/신뢰도 갱신에 반영한 soft/hard CRBF 디코더",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "min{M+1, dv(dc-1)+1} ops/iter (gatecount 미상)",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "HW 미설계·병렬화 미논의, iter당 1비트 flip 순차성이 min-sum 파이프라인과 상충 가능",
  "todo_check": "check reliability 갱신식(9,11)의 HW 비용·다비트 flip 병렬화 가능성, min-sum 대비 실이득"
}
```
