### arxiv:1902.10391v3 - One and Two Bit Message Passing for SC-LDPC Codes with Higher-Order Modulation (2019, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | SC-LDPC |
| 부호rate | 0.5~0.83 |
| 부호length | 60000 |
| 연판정 | soft-2~3bit |
| 핵심기여 | CN<->VN 교환 메시지를 1~2비트로 양자화하되 4진(QMP: ±L/±H 신뢰도 구분) min-sum + DE 최적 가중치로 내부 data flow를 줄여 라우팅 혼잡 완화 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | HW 미설계·시뮬만, AWGN+고차변조(ASK/PAS) 광통신 타깃이라 NAND 채널·라벨링과 직접 정합 안됨, 4진 메시지 가중치 2세트 DE 의존 |
| 추가확인 | NAND RBER/hard-soft read 채널에서 QMP 임계 이득 유지 여부, block-based(비-SC) 고rate QC-LDPC에 4진 메시지 적용 시 이득과 gate/라우팅 절감 실측 |

> 총평: 메시지 비트폭을 1~2비트로 줄여 디코더 data flow/라우팅 혼잡을 완화하는 디코더 알고리즘으로 개념적으로 min-sum과 정합하나, 광통신 고차변조/SC-LDPC 세팅이라 NAND 고rate QC-LDPC 이식엔 재정합이 필요하다.

### B. 알고리즘 요약

1. 대상: protograph 기반 SC-LDPC(regular `dv=4/6`, rate 2/3~5/6), 고차변조(M-ASK/QAM)+확률적 진폭성형(PAS), AWGN 광링크, SE 1.0~1.5 bpcu.
2. 문제: >1Tbps 디코더는 내부 data flow `F=2·nc·q·d̄v`가 라우팅 혼잡을 유발 -> 메시지 비트수 `q`를 줄여야 하지만 성능 손실 최소화 필요.
3. 핵심 가정: BMD 비트채널은 고차변조에서 비대칭 -> scrambling으로 `L̃k=Lk(1-2Bk)` 대칭화(channel adapter)해 all-zero 가정 DE 적용.
4. 핵심 기법 1단(QMP): CN<->VN 메시지를 4진 `{-H,-L,+L,+H}`(저/고 신뢰도 구분)로 양자화, CN에서 min-sum(`min|m|·∏sign`) 규칙 적용.
5. 식 의미: 양자화 함수 `Ψ`가 threshold `T`로 부호와 신뢰도(L/H)를 동시 표현 -> 같은 2비트로 TMP보다 세분화된 신뢰도 전달.
6. 핵심 기법 2단: VN update에서 채널 LLR `ldec`에 신뢰도별 가중치 2세트(`w_L`, `w_H`)를 곱해 CN 메시지 결합, `w`는 외재채널 LLR `|l2(y)|`로 정의.
7. 부수 트릭: 단일 상수 `T=1.3`을 전 iteration 공유해도 성능 손실 거의 없음; 가중치 양자화/공유도 미미한 손실.
8. 학습/최적화: protograph DE로 window decoding(`W=15`) 임계 계산 및 최적 가중치 도출, MC 대신 surrogate AWGN 채널 근사(`H(B̆k|Y̆)=H(Bk|Y)`)로 초기화 간소화.
9. 결과: SE 1.5 bpcu에서 QMP가 BMP 대비 ~0.7dB, TMP 대비 ~0.1dB(저rate 4U-0.50은 0.24dB) 이득, unquantized BP와의 gap ~0.75dB; nc=60000 유한길이서 DE 예측과 일치.
10. 한계: HW 미설계, 시뮬만, 광통신 고차변조/PAS 전용 세팅, SC-LDPC 중심(block QC-LDPC 직접 대상 아님).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 1~2비트 양자화 메시지 passing / VN 양자화 | decoder.cpp `VN_Cal_HD()` 등, `decoder.h` `Get_VNU_*` | 메시지 비트폭 축소(4진)는 VN 처리/양자화부와 개념적으로 대응 |
| CN min-sum 연산 | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | QMP CN이 min·sign-XOR으로 이미 보유 min-sum과 동일 골격 (중복) |
| iteration별/신뢰도별 가중치 테이블 | ecc_data.h `PARAM_LLR`, `decoder.cpp` `Get_VNU_Table_Idx()` | DE 도출 `w_L`/`w_H` 가중치가 iteration별 LLR 테이블 구조에 대응 |
| 채널 soft-info / LLR 초기화 | channel.cpp `Set_LLR_Th()` | BMD 비트채널 대칭화·surrogate 초기화가 채널 LLR threshold 설정과 관련 |
| data flow/라우팅 혼잡 완화 (HW 동기) | 대응 없음(정량 HW 미설계) | 라우팅 혼잡 개선을 알고리즘 동기로만 언급, RTL/gatecount 대응 없음 |

적용 가치: **중간** -- 메시지 비트폭을 줄여 라우팅/data flow를 완화하는 방향은 NAND HW 디코더에 매력적이고 VN/LLR 테이블 모듈과 정합하나, min-sum CN은 이미 보유 기법이며 광통신 고차변조/SC-LDPC/PAS 세팅이라 NAND 고rate QC-LDPC·hard/soft-read 채널로의 재정합과 HW 실증이 선행되어야 한다.

### D. JSON 블록

```json
{
  "id": "arxiv:1902.10391v3",
  "title": "One and Two Bit Message Passing for SC-LDPC Codes with Higher-Order Modulation",
  "year": 2019,
  "venue": "arXiv cs.IT",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "SC-LDPC",
  "code_rate": "0.5~0.83",
  "code_length": "60000",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "CN<->VN 교환 메시지를 1~2비트로 양자화하되 4진(QMP: ±L/±H 신뢰도 구분) min-sum + DE 최적 가중치로 내부 data flow를 줄여 라우팅 혼잡 완화",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "HW 미설계·시뮬만, AWGN+고차변조(ASK/PAS) 광통신 타깃이라 NAND 채널·라벨링과 직접 정합 안됨, 4진 메시지 가중치 2세트 DE 의존",
  "todo_check": "NAND RBER/hard-soft read 채널에서 QMP 임계 이득 유지 여부, block-based(비-SC) 고rate QC-LDPC에 4진 메시지 적용 시 이득과 gate/라우팅 절감 실측"
}
```
