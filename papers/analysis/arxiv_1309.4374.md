### arxiv:1309.4374v1 - An Energy Efficient Decoding Scheme for Wireless Body Area Sensor Networks (2013, EUSPN-2013 확장판)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.5~0.75 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 목표 BER(10^-4) 도달 시점에서 반복을 조기 중단하는 AID(Adaptive Iterative Decoding)로 WBAN 디코더 에너지 소비를 20~25% 절감 (arXiv:1309.0752v1의 확장판, 동일 결과) |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 1.5Gbps |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | WBAN 무선 채널(AWGN) 전력모델 특화, NAND ECC와 무관, LDPC 부호 스펙(H-matrix, QC 여부 등) 구체 서술 없음. 본문 스스로 [2]=arXiv:1309.0752v1의 확장 논문임을 명시 |
| 추가확인 | 두 논문(1309.0752, 1309.4374)이 사실상 동일 결과·수치를 공유하는 확장판 관계임을 DB 필터링 시 중복 표기 필요 |

> 총평: 저자들이 명시한 대로 arXiv:1309.0752v1의 확장판이며 배경설명(ARQ/HARQ, block/convolutional code 비교 등)만 보강되었을 뿐 핵심 기법·수치 결과는 동일. NAND ECC 이식 가치는 원 논문과 마찬가지로 낮음.

### B. 알고리즘 요약

1. 대상 시스템은 Wireless Body Area Network(WBAN) 센서 노드로, AWGN 채널에서 code rate `Rc=0.5` 또는 `0.75`의 LDPC 부호를 사용하는 반복 message-passing(BP) 디코더 (arXiv:1309.0752v1과 동일 설정).
2. 문제의식: 짧은 거리 무선통신에서는 송신 전력보다 디코딩 전력이 크며, ARQ/HARQ 재전송 대신 강력한 ECC를 쓸수록 디코더 처리 에너지가 증가하는 트레이드오프가 존재.
3. 채널/에너지 모델: 노드당 에너지 `Etot ≈ PL/PR + Enode·l·Rdec/Rc` (Enode=반복당 PE 소비 에너지, l=반복수)로 반복수 l이 총 에너지를 지배.
4. 핵심 기법(AID, Adaptive Iterative Decoding): 목표 BER(`10^-4`)을 미리 설정하고, 그 BER에 도달하는 반복 횟수를 임계값으로 삼아 그 이후 반복을 중단.
5. 표준 LDPC 디코더 흐름(Fig.4: LLR 계산 → parity check → 최대반복 도달 시 종료)에 "BER>10^-4?" 판정 분기를 추가한 흐름(Fig.6)으로 대체.
6. 부수 관찰: SNR-BER 관계에서 `Rc=0.75`는 목표 BER에 SNR 3.5dB·16회 반복, `Rc=0.5`는 SNR 2.5dB·12회 반복이 필요함을 시뮬레이션으로 도출 (원 논문과 동일 수치).
7. 학습/최적화 절차 없음 — 사전 시뮬레이션으로 목표 BER 도달 반복수를 파악한 뒤 그 값을 임계값으로 고정.
8. 결과: 고정 50회 반복 대비 16회에서 조기 종료 시 총 에너지 1.3J→1.05J, `Rc=0.5`에서는 0.5J로 22% 절감, 전체 20~25% 에너지 절감 (원 논문과 동일).
9. 한계: HW 구현·부호 구조(H-matrix, QC 여부, 길이) 서술 전무, 검증은 시뮬레이션(60GHz, 1.5Gbps, PE당 10pJ)에 국한.
10. 원 논문(1309.0752v1) 대비 차이는 배경/related work 서술 확장뿐이며, 핵심 알고리즘·수식·결과는 동일 재수록.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 반복 조기종료(목표 BER 도달 시 중단) | `partial_CRC.cpp` `partial_crc_HW_T4()`, `full_CRC.cpp` | 개념적으로 유사하나 Prime ECC는 이미 CRC 기반 4-termination point 조기종료를 구현하여 중복 기여 |
| 반복별 LLR/BP 계산 | `decoder.cpp` `LDPC_Decoder()` | 표준 BP 수식(교과서 수준)만 서술 |
| WBAN 에너지 모델 | 대응 없음 | NAND 컨트롤러 전력모델과 무관한 무선 RF 전력 모델 |

> 적용 가치: 낮음 — arXiv:1309.0752v1의 확장/재수록판으로 신규 이식 요소 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1309.4374v1",
  "title": "An Energy Efficient Decoding Scheme for Wireless Body Area Sensor Networks",
  "year": 2013,
  "venue": "EUSPN-2013 (확장판)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": "0.5~0.75",
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "목표 BER(10^-4) 도달 시점에서 반복을 조기 중단하는 AID(Adaptive Iterative Decoding)로 WBAN 디코더 에너지 소비를 20~25% 절감 (arXiv:1309.0752v1의 확장판, 동일 결과)",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": 1.5,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "하",
  "caveat": "WBAN 무선 채널(AWGN) 전력모델 특화, NAND ECC와 무관, LDPC 부호 스펙(H-matrix, QC 여부 등) 구체 서술 없음. 본문 스스로 [2]=arXiv:1309.0752v1의 확장 논문임을 명시",
  "todo_check": "두 논문(1309.0752, 1309.4374)이 사실상 동일 결과·수치를 공유하는 확장판 관계임을 DB 필터링 시 중복 표기 필요"
}
```
