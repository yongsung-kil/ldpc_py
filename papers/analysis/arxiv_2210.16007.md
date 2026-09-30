### arxiv:2210.16007v1 - Design of Protograph LDPC-Coded MIMO-VLC Systems with Generalized Spatial Modulation (2022, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | protograph |
| 부호rate | 0.5~0.75 |
| 부호length | 3600(info bits) |
| 연판정 | 무관 |
| 핵심기여 | MPEXIT로 설계한 rate-compatible EARA protograph 부호 + SSERGSM 성상, MIMO-VLC BICGSM-ID 전용 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 부호가 상관된 MIMO-VLC 채널 + GSM demapper와의 공동 iterative decoding에 최적화됨 (AWGN/NAND 무관) |
| 추가확인 | EARA 부호 구성 원리(lowest-degree VN puncturing, 2-VN pattern extension)가 채널 독립적으로 AWGN QC-LDPC에 이득 주는지 |

> 총평: VLC-MIMO GSM 전용 protograph 부호설계 논문으로 NAND binary QC-LDPC 이식 가치 거의 없음.

### B. 알고리즘 요약

1. 시스템: 4x4 실내 LOS MIMO-VLC, GSM 변조(활성 LED `Na=2`), protograph LDPC 부호화 + BICM-ID(내부 iter `G1=20`, 외부 iter `G2=4`), info block 3600 bits.
2. 문제: 상관된 정적 MIMO-VLC 채널에서 기존 ConGSM 성상과 AWGN용 AR4JA 부호가 최적이 아님 → 성상·부호를 채널맞춤 재설계 필요.
3. 채널 모델: LOS 광 채널 이득 `hij`(각도·거리 종속), i.i.d. AWGN 잡음, OSNR 지표로 성능 측정.
4. 핵심기법 1(성상): SSER — UPAM 심볼을 `beta=2^rho_d`개 부공간으로 확장(식 13) 후 LED 활성패턴별로 서로 다른 심볼 부분집합을 최대 등간격 재배치.
5. 의미: 각 LED 활성패턴이 상이한 UPAM 부분집합을 가져 demapper extrinsic MI를 높이고 ID 수렴을 가속.
6. 핵심기법 2(부호): MPEXIT(유한길이 0/1 코드워드 가정, GSM 채널 MI `Ich(i)` 식 11 반영)로 decoding threshold 평가 → rate-1/2 mother base matrix를 exhaustive search로 최적화.
7. 확장: degree-1 punctured VN + degree-2 VN 1개 제약, 병렬 edge<=3, 2-VN pattern-extension으로 rate `(e+1)/(e+2)` compatible EARA 부호 생성(식 17).
8. 최적화: MPEXIT threshold 최소화 + AWD로 TMDR(linear min-distance growth) 양수 보증.
9. 결과: EARA가 6종 부호 중 최저 threshold(rho=4 dtx=0.3m 5.314 dB); IAR4A 대비 0.67dB, regular 대비 0.4dB BER 이득, RA/RM 연산 최소(2.642e6/6.602e6), error-floor 없음(BER 1e-6).
10. 한계: HW 미설계, 시뮬레이션만, 특정 MIMO-VLC 상관채널+GSM demapper 공동설계에 종속.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| EARA protograph 부호 구성 (base matrix / pattern extension) | 대응 없음 (Prime ECC는 QC-LDPC base+circulant 고정, protograph 아님) | protograph→QC 변환·재검증 부담 큼, 이식성 낮음 |
| MPEXIT 기반 threshold 최적화 | 대응 없음 | 설계 도구이며 Prime ECC 부호 고정이라 미적용 |
| SSERGSM 성상 / GSM demapper | 대응 없음 | VLC 변조 전용, NAND 채널과 무관 |
| BICM-ID iterative demap/decode | `decoder.cpp` `LDPC_Decoder()` (원리적 유사만) | Prime ECC는 GSM demapper와의 외부 iteration 구조 없음 |

적용 가치: **낮음** — protograph/VLC-GSM 특화 부호설계로 NAND binary QC-LDPC 코드베이스에 떼어 쓸 재사용 요소가 사실상 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2210.16007v1",
  "title": "Design of Protograph LDPC-Coded MIMO-VLC Systems with Generalized Spatial Modulation",
  "year": 2022,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "protograph",
  "code_rate": null,
  "code_length": "3600 info bits",
  "soft_quant": "무관",
  "key_contribution": "MPEXIT로 설계한 rate-compatible EARA protograph 부호 + SSERGSM 성상, MIMO-VLC BICGSM-ID 전용",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "부호가 상관된 MIMO-VLC 채널 + GSM demapper와의 공동 iterative decoding에 최적화됨 (AWGN/NAND 무관)",
  "todo_check": "EARA 부호 구성 원리(lowest-degree VN puncturing, 2-VN pattern extension)가 채널 독립적으로 AWGN QC-LDPC에 이득 주는지"
}
```
