### arxiv_1103.5128v1 - Power Consumption of LDPC Decoders in Software Radio (2011, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.41 |
| 부호length | 155 |
| 연판정 | 무관 |
| 핵심기여 | GPP(소프트웨어 라디오)에서 7종 LDPC 복호(SP/logSP/MS/MMS/WBF/MWBF/IRRWBF)의 복잡도·전력을 Wattch로 추정하고 SNR 기반 알고리즘 다이버시티 전력제어를 제안 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 없음 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | GPP 소프트웨어 전력분석이라 ASIC/RTL 디코더 HW 이식과 무관; 예제 부호가 (155,64) small regular, 통신용 |
| 추가확인 | 없음 (NAND ASIC ECC와 목표·플랫폼 상이) |

> 총평: 소프트웨어 라디오 GPP에서 LDPC 복호 알고리즘별 전력·복잡도를 Wattch로 비교하고 SNR별 알고리즘 전환(algorithm diversity) 전력제어를 제안한 survey성 논문. HW 신규 기법이 없고 이미 보유한 SP/MS/MMS 재정리라 NAND ASIC ECC 이식가치 없음.

### B. 알고리즘 요약

1. 시스템: 소프트웨어 라디오(GPP/DSP)에서 LDPC 복호 실행, AWGN·BPSK, 예제부호 `(155,64)` regular LDPC(순열행렬 기반), 600MHz issue-4 GPP.
2. 문제: GPP는 ASIC/FPGA보다 전력소모가 커서 소프트웨어 라디오용 LDPC 복호의 복잡도·전력·지연을 정량 비교할 필요.
3. 모델: LLR `r=σ⁻²·2y`(식 1,2), 반복 message-passing(CN update / VN update / decision), 정지조건 `Hd^T=0` 또는 100 iteration.
4. 알고리즘 비교: BP계열 SP(식 3~7, `tanh`/`atanh` 사용), log-SP(식 8~14, `log(tanh)`), MS/MMS(식 15~19, `tanh` 제거·min); BF계열 WBF/MWBF(식 20~23, `δ·|rn|` 항), RRWBF/IRRWBF(식 24~32, 신뢰도비 `Rmn`).
5. 핵심 식 의미: MS/MMS는 CN의 `tanh(x/2)` 제거로 곱셈·나눗셈 삭제 → 사이클·에너지 급감; IRRWBF는 RRWBF를 재정식화해 런타임 대폭 단축(Fig.2).
6. 성능(정정): SP/logSP 최고, MS는 SP에 근접, MMS는 MS보다 약간 우수, IRRWBF는 BF계열 중 최고이나 BP계열엔 미달(Fig.3).
7. 전력추정법: 디코더를 C로 작성→Wattch(SimpleScalar) 아키텍처 레벨 전력 시뮬(Fig.4), 100 iteration 고정 후 iteration으로 나눠 iter당 전력 산출(Fig.5~8).
8. 조기종료 반영: SNR별 평균 iteration(Fig.11)을 곱해 early-stopping 에너지 추정(Fig.12); 데이터레이트=`freq/(cycle/iter·iter)·bitlen·(1-BER)`(식 33).
9. 결과: SNR>2dB는 MS/MMS가 최저전력·최고 데이터레이트, SNR<2dB는 IRRWBF가 최저전력; icache 4KB면 충분(dcache miss는 미미, Fig.14-15).
10. 응용/한계: SNR 기반 알고리즘 다이버시티 및 송신전력-수신에너지 공동관리 전력제어 제안. HW(RTL/ASIC) 미설계, GPP 소프트웨어 전력분석·통신 대상.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SP/log-SP/MS/MMS 복호 루프 | decoder.cpp `LDPC_Decoder()`, `C2V_Cal()` | 이미 min-sum 보유 — 알고리즘 재정리 수준, 중복 |
| CN min-sum(min/sign) | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 동일 기법 보유 — 중복 |
| WBF/MWBF/IRRWBF(bit-flipping) | 대응 없음 | Prime ECC는 BP/min-sum 전용, BF 미보유 |
| GPP 전력/캐시/사이클 추정(Wattch) | 대응 없음 | Prime ECC는 bit-exact HW 시뮬, GPP 소프트웨어 전력분석 부재 |
| 조기종료(평균 iteration 활용) | partial_CRC.cpp `partial_crc_HW_T4()` | 개념적 조기종료만 유사, 방식 상이 |

적용 가치: **낮음** — GPP 소프트웨어 라디오의 전력·복잡도 분석이 목표라 NAND ASIC bit-exact ECC와 플랫폼이 다르고, 다룬 BP/MS/MMS는 이미 보유, BF계열은 우리 구조와 무관.

### D. JSON 블록

```json
{
  "id": "arxiv:1103.5128v1",
  "title": "Power Consumption of LDPC Decoders in Software Radio",
  "year": 2011,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.41,
  "code_length": "155",
  "soft_quant": "무관",
  "key_contribution": "GPP에서 7종 LDPC 복호(SP/logSP/MS/MMS/WBF/MWBF/IRRWBF)의 복잡도·전력을 Wattch로 추정하고 SNR 기반 알고리즘 다이버시티 전력제어를 제안",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "없음",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "GPP 소프트웨어 전력분석이라 ASIC/RTL 디코더 HW 이식과 무관; 예제 부호가 (155,64) small regular, 통신용",
  "todo_check": "없음 (NAND ASIC ECC와 목표·플랫폼 상이)"
}
```
