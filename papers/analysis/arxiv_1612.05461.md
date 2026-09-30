### arxiv:1612.05461v1 - Least reliable messages based early termination method for LT soft decoder (2016, Electronics Letters)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.5 |
| 부호length | 4000 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 최소신뢰(LRM) mv→c 메시지 소집단의 sign 변화만 관찰하는 저복잡도 조기종료(ETM)로 CSR 대비 avg iteration·연산량 대폭 절감 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | LT/Raptor rateless 코드·full tanh SPA 대상, HW 미구현, DC-LRM/ΓLC 등 파라미터 채널SNR별 튜닝 필요 |
| 추가확인 | Prime ECC 기존 Partial/Full CRC 조기종료 대비 LRM 방식이 이점 있는지, min-sum 디코더에 sign-tracking 적용 시 효과 |

> 총평: BP 디코더 범용 조기종료 기법으로 LDPC에도 적용 가능하나 Prime ECC는 이미 CRC 조기종료를 보유해 기여 중복 소지가 있음.

### B. 알고리즘 요약

1. 시스템: LT(Luby transform) rateless 부호의 BP 디코더, code rate 1/2, 데이터 패킷 4000, 고정 iteration 100, BIAWGN 채널.
2. 문제: BP는 조기 수렴하나 고정 iteration까지 계속 돌아 연산량·latency·에너지 낭비 → 조기종료(ETM) 필요, 기존 CSR ETM은 매 iteration마다 재인코딩·비교로 복잡.
3. 핵심 아이디어: `mv→c` 메시지 중 절댓값 LLR이 작은(=least reliable) 소집단(LRM)만 관찰, 이들이 가장 늦게 수렴하므로 이 부분의 sign 변화가 멈추면 전체 수렴으로 판단.
4. LRM 선정: 전체 `mv→c` 중 최소 절댓값 `NB = B*Nmv→c` 개를 quickselect로 1회만 추출(디코딩 전체에서 단 한 번).
5. 종료 조건: LRM의 sign이 연속 `ΓLC` iteration 동안 변화 없으면 종료. ΓLC를 작게 할수록 avg iteration 감소.
6. DC-LRM: 초기 채널 LLR 전파를 위해 몇 iteration 후에야 LRM 관찰 시작, SNR별로 45/28/22/18/15 (0.5~2.5dB) 룩업테이블화.
7. 이점: 매 iteration의 Decision() 불필요, sign 변화 카운트만 수행 → ETM 섹션 연산 대폭 절감.
8. 결과: LRM(ΓLC=1,B=5%)이 CSR(ΓLC=5) 대비 BER 열화 없이 avg iteration 감소(예 1.0dB: 45.19→43.73), ETM 연산시간 약 92% 감소(예 0.5dB: 86.18ms→6.91ms).
9. 적용성: BP로 복호되는 LDPC·polar·Raptor 등 코드族에 쉽게 적용 가능하다고 주장.
10. 한계: HW 미구현(future work), full tanh SPA 기반, rateless(LT) 대상, BER 곡선은 그림에만 존재.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 조기종료(ETM) 로직 | partial_CRC.cpp `partial_crc_HW_T4()`, full_CRC.cpp | Prime ECC는 이미 Partial+Full CRC 조기종료 보유, LRM은 대체 후보이나 기여 중복 소지 |
| sign 변화 추적(VN hard-decision 안정성) | decoder.cpp `VN_Cal_HD()`, `LDPC_Decoder()` 루프 | min-sum 디코더 VN 처리에 sign-tracking 조기종료를 얹을 수 있으나 CRC와 비교 검증 필요 |
| avg iteration 감소 | decoder.cpp `LDPC_Decoder()` 이터레이션 루프 | iteration/latency 절감은 Prime ECC 관심사와 부합 |

적용 가치: **중간** — 조기종료 아이디어는 이식 가능하나 Prime ECC의 CRC 기반 조기종료와 겹치고, 대상이 rateless·full-SPA라 min-sum HW와의 정합·이점 검증이 필요하다.

### D. JSON 블록

```json
{
  "id": "arxiv:1612.05461v1",
  "title": "Least reliable messages based early termination method for LT soft decoder",
  "year": 2016,
  "venue": "Electronics Letters",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": 0.5,
  "code_length": "4000",
  "soft_quant": "soft-4bit+",
  "key_contribution": "최소신뢰(LRM) mv→c 메시지 소집단의 sign 변화만 관찰하는 저복잡도 조기종료로 CSR 대비 avg iteration·연산량 대폭 절감",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "중",
  "caveat": "LT/Raptor rateless 코드·full tanh SPA 대상, HW 미구현, DC-LRM/ΓLC 파라미터 SNR별 튜닝 필요",
  "todo_check": "Prime ECC 기존 CRC 조기종료 대비 LRM 이점 유무, min-sum 디코더에 sign-tracking 적용 시 효과"
}
```
