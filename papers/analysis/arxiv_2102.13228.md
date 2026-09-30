### arxiv:2102.13228v2 - A High-Throughput Multi-Mode LDPC Decoder for 5G NR (2021, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.083~0.917 |
| 부호length | 2496~6528 |
| 연판정 | 미상 |
| 핵심기여 | 5G BG1 확장 패리티용 간소화 VN(EVN) + 재구성형 Banyan-variant shift network로 작은 Z에서도 다중프레임 병렬로 throughput 유지 |
| HW설계 | O |
| 검증수준 | ASIC합성 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 13.46Gbps@28nm(합성), 2.1Gbps(FPGA) |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 5G BG1 특화 구조(EVN·shift network)라 NAND 고정 QC-LDPC에 그대로 이식 불가, 알고리즘은 표준 Offset Min-Sum |
| 추가확인 | Offset(=0.5) Min-Sum offset 튜닝값 정도만 참고, shift network는 NAND z=32 고정구조와 무관 |

> 총평: 5G NR 다중코드율 지원 throughput 최적화 HW 논문으로, NAND 고정 QC-LDPC ECC에는 이식 가치 낮음.

### B. 알고리즘 요약

1. 5G NR BG1(46×68 base) QC-LDPC 디코더, code rate 11/12~1/3, Z≤`Zmax=96`, code length 2496~6528, partially parallel + flooding 스케줄.
2. 문제: 5G는 넓은 rate/Z 범위를 지원해야 하며, 작은 Z 선택 시 throughput이 `Throughput = frames/s × base matrix size × Z`로 급락 → 이를 보상해야 함.
3. CN: 16-input, tree-structure comparator로 min1/min2와 min index를 serial하게 계산, half-layer(13×Z) 단위 로딩, 2 frame 동시 처리로 stall 회피.
4. Offset Min-Sum: min 계산 후 offset(=0.5)을 빼 Min-Sum 과대추정 보정.
5. Primary VN: 채널 intrinsic + CN 갱신 메시지 누적(accumulation register + feedback loop), overflow 시 saturate.
6. 핵심 신규기여 EVN(Extended VN): 확장 패리티(col 27~68)는 CN 연결이 1개뿐이라 누적/feedback 불필요 → adder+depth-42 메모리로 간소화(EVN 16 LUT/6 FF vs VN 38 LUT/36 FF).
7. shift network: Banyan-variant(reconfigurable) 채택, Z≤N cyclic shift 지원, QSN 대비 다중 독립 subnetwork로 분할 가능.
8. throughput 복원: Z≤Zmax/2·Zmax/4일 때 shift network를 2·4개 독립 network로 분할해 여러 frame 병렬 처리, 최대 8 frame까지.
9. 결과: FPGA(Virtex7) 2.1Gbps@11/12, 5-bit 양자화, 10 iter; 28nm TSMC 합성 526MHz, 13.46Gbps, core 1.03mm², 229mW, 17.01pJ/bit.
10. 한계: 알고리즘 정정성능 개선 없음(표준 OMS), 5G 특정 base graph 구조 종속, ASIC은 합성(post-synthesis)까지만.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Offset Min-Sum CN 연산 | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 이미 min-sum 보유, offset은 참고 수준 |
| Primary VN 누적/양자화 | decoder.cpp `VN_Cal_HD()` 등 | 표준 VN 처리로 신규성 낮음 |
| EVN(확장 패리티 VN) | 대응 없음 | 5G BG1 확장 diagonal 특화, NAND 고정 PCM에 무관 |
| Banyan-variant shift network | 대응 없음 | NAND z=32 고정 라우팅과 정합 불가 |
| 다중프레임 병렬(shift 분할) | 대응 없음 | 가변 Z 지원 목적, NAND 단일 Z와 무관 |

적용 가치: **낮음** — 알고리즘은 이미 보유한 Offset Min-Sum이고, 신규성은 5G 가변 rate/Z 특화 HW(EVN·shift network)라 NAND 고정 binary QC-LDPC에 떼어 쓸 부분이 사실상 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2102.13228v2",
  "title": "A High-Throughput Multi-Mode LDPC Decoder for 5G NR",
  "year": 2021,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": "0.083~0.917",
  "code_length": "2496~6528",
  "soft_quant": "미상",
  "key_contribution": "5G BG1 확장 패리티용 간소화 EVN + 재구성형 Banyan-variant shift network로 작은 Z에서도 다중프레임 병렬로 throughput 유지",
  "hw_designed": "O",
  "verification": "ASIC합성",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": 13.46,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "하",
  "caveat": "5G BG1 특화 구조(EVN·shift network)라 NAND 고정 QC-LDPC에 그대로 이식 불가, 알고리즘은 표준 Offset Min-Sum",
  "todo_check": "Offset(=0.5) Min-Sum offset 튜닝값 정도만 참고, shift network는 NAND z=32 고정구조와 무관"
}
```
