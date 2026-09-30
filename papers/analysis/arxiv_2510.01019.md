### arxiv:2510.01019v1 - Layered Normalized Min-Sum Decoding with Bit Flipping for FDPC Codes (2025, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.625~0.824 |
| 부호length | 128~1024 |
| 연판정 | soft-4bit+ |
| 핵심기여 | FDPC 부호용 layered NMS(충돌그래프 컬러링 스케줄링)에 syndrome-guided bit-flipping 리스트 후처리를 결합해 FER 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | 부분 |
| latency | 악화 |
| 추천도 | 중 |
| 한계,주의 | 대상이 FDPC(non-QC, 2s√N×N) 부호이며 HW 미설계·시뮬만, SGBF가 실패 시 최대 T=128회 재복호로 최악 latency 큼 |
| 추가확인 | layered 스케줄링·SGBF를 우리 QC-LDPC(z=32) H-matrix에 적용 시 이득 유지 여부, T별 평균/최악 latency |

> 총평: layered NMS의 충돌그래프 컬러링 스케줄링과 syndrome+LLR 결합 신뢰도 기반 bit-flipping 후처리는 우리 min-sum 디코더에 개념 이식 여지가 있으나, 대상 부호가 FDPC(비 QC-LDPC)이고 HW 미검증·최악 T배 재복호 부담이라 이식성 중.

### B. 알고리즘 요약

1. 대상은 FDPC 부호(base `Hb`는 `2√N×N`, 열가중치 2, order-s는 s-1 순열 stack), rate 0.625~0.824, 길이 128~1024, BI-AWGN+BPSK.
2. 문제: FDPC는 지금까지 flooding BP로만 평가돼 수렴이 느림; layered 스케줄링과 후처리로 수렴·FER을 개선하려 함.
3. 모델: LLR `L(ci)=2yi/σ2`, 표준 NMS check 갱신에 정규화계수 `α=0.75`.
4. 핵심 기법1 (LNMS): check node 충돌그래프(`A=HHT-diag(HHT)`)를 greedy graph coloring해 비충돌 layer `Lk`로 나누고, 각 layer 처리 직후 VN 즉시 갱신(식3~6)해 수렴 가속.
5. 핵심 식: layer별 delta `Δ=L(r_j^t)-L(r_j^{t-1})`를 a posteriori LLR에 즉시 반영(식6) — flooding 대비 정보전파 가속.
6. 핵심 기법2 (SGBF): LNMS 실패 시 per-bit 불만족 체크 수 `ei`(식9)와 LLR을 결합한 신뢰도 `reli=|L(qi)|/(1+max(ei,1))`(식10)로 최하위 T개 bit 선정.
7. 부수 기법: 선정 T개 각각 단일 bit LLR 부호 flip한 후보를 LNMS로 재복호, 최소 syndrome weight 후보 선택(`t*=argmin wt`).
8. 학습/최적화: 없음(RL 스케줄링은 관련연구로만 언급), 결정론적 greedy coloring·고정 α.
9. 결과: FDPC(256,192), T=128, 5 iter에서 standalone LNMS 대비 FER 10^-3에서 약 0.5dB, polar/5G-LDPC 대비 0.75~1.5dB 이득; layer 수 4.
10. 한계: HW 미설계, 시뮬만, SGBF 복잡도가 T에 선형(실패 시 T회 재복호)이라 최악 latency 큼, 대상 부호가 FDPC(비 QC-LDPC).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| LNMS message passing (min-sum, α 정규화) | decoder.cpp `LDPC_Decoder()`, `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | min-sum CN 연산과 동일 계열, 우리도 이미 보유 |
| 충돌그래프 컬러링 layered 스케줄링 | decoder.cpp `LDPC_Decoder()` 이터레이션 루프 | Dual-Update(even/odd 교대) 스케줄과 유사 취지, layer 분할·즉시갱신 개념 이식 여지 |
| syndrome+LLR 신뢰도 bit-flipping 후처리(SGBF) | 대응 없음 | Prime ECC에 bit-flipping 리스트 post-processing 미존재(조기종료는 CRC 기반) |
| syndrome 계산·조기종료 | partial_CRC.cpp, `full_CRC.cpp` | 종료 판정 개념 유사, syndrome-weight 선택은 미대응 |
| H-matrix / FDPC 부호구조 | ecc_top.cpp `Load_PCM()` | 대상이 FDPC(비 QC-LDPC)라 부호 자체는 이식 부적합, 우리는 QC-LDPC 고정 |

적용 가치: **중간** — layered 스케줄링과 syndrome+LLR 결합 신뢰도 기반 bit-flipping 후처리는 우리 min-sum 디코더에 개념 이식 여지가 있으나, 대상 부호가 FDPC(비 QC-LDPC)이고 HW 미검증·최악 T배 재복호 latency가 NAND ECC 제약과 상충한다.

### D. JSON 블록

```json
{
  "id": "arxiv:2510.01019v1",
  "title": "Layered Normalized Min-Sum Decoding with Bit Flipping for FDPC Codes",
  "year": 2025,
  "venue": "arXiv cs.IT",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": "0.625~0.824",
  "code_length": "128~1024",
  "soft_quant": "soft-4bit+",
  "key_contribution": "FDPC 부호용 layered NMS(충돌그래프 컬러링 스케줄링)에 syndrome-guided bit-flipping 리스트 후처리를 결합해 FER 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "부분",
  "latency": "악화",
  "recommend": "중",
  "caveat": "대상이 FDPC(non-QC, 2s√N×N) 부호이며 HW 미설계·시뮬만, SGBF가 실패 시 최대 T=128회 재복호로 최악 latency 큼",
  "todo_check": "layered 스케줄링·SGBF를 우리 QC-LDPC(z=32) H-matrix에 적용 시 이득 유지 여부, T별 평균/최악 latency"
}
```
