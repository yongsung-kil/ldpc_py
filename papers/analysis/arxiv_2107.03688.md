### arxiv:2107.03688v1 - An Embedded Iris Recognition System Optimization using Dynamically Reconfigurable Decoder with LDPC Codes (2021, arXiv cs.CV)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.667 |
| 부호length | 960~2016 |
| 연판정 | soft-4bit+ |
| 핵심기여 | IEEE 802.16 QC-LDPC 다중 디코더를 FPGA Dynamic Partial Reconfiguration으로 시분할 전환(fast/low-power/accuracy 모드)해 임베디드 홍채인식에 적용 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | 동등 |
| 추천도 | 하 |
| 한계,주의 | 디코더 알고리즘은 기존 layered Min-Sum(IEEE 802.16) 재사용, 기여는 홍채인식 시스템 통합 + DPR 모드전환이라 ECC 코어 개선 없음 |
| 추가확인 | DPR 기반 다중 코드 시분할 디코더가 NAND 멀티-rate/멀티-모드 ECC 엔진 전환 전략에 시사점 있는지 |

> 총평: IEEE 802.16 QC-LDPC layered Min-Sum 디코더를 FPGA DPR로 모드 전환해 홍채인식에 붙인 응용/HW 통합 논문. LDPC 코어 자체는 표준이라 NAND ECC 이식 가치 낮음.

### B. 알고리즘 요약

1. 시스템: 임베디드 홍채인식 SoC-FPGA(Xilinx ZCU106), 1280-pixel 홍채코드를 QC-LDPC로 부호화/복호. IEEE 802.16 코드 (1920,1280)/(2016,1680)/(960,640) 등, rate `2/3A`, iteration 50.
2. 문제: 동일 홍채의 등록/검증 샘플 간 변동(노이즈)이 인식 오류 유발, 기존 방식은 OpenCV/NN 의존으로 HW 비친화.
3. 모델: 등록 시 참조 홍채의 parity `P0`를 저장, 검증 시 다중 샘플 산술평균 `X3` + `P0`를 QC-LDPC 복호로 오류정정 후 Hamming distance 매칭.
4. 핵심 기법: QC-LDPC 디코더는 layered decoding 구조([16][18] 재사용)로 CN/VN 프로세서 수를 H-matrix에 맞춰 조정, 병렬성 확보.
5. 핵심 식: 별도 신규 수식 없음 — 표준 Min-Sum message passing, quantization 2/4/8bit fix-point 비교.
6. 확장: FPGA Dynamic Partial Reconfiguration(DPR)로 단일 코드 디코더들을 시분할 통합, 회로 부분 재구성(375KB bitstream, 1.75ms 전환).
7. 구현 디테일: unsigned→signed 변환(−128), 8bit soft-input 유지로 hard 대비 1–2dB net coding gain, Q2/Q4/Q8 자원·전력 트레이드오프.
8. 최적화: 실험으로 최적 코드 선정 — (1920,1680)가 대부분 우수, 코드 길이 증가는 오히려 성능 손실.
9. 결과: FPGA 합성 자원/전력/latency 표 제시 (예: (1920,1280) Q4 13mW, (960,640) PARL Q8 84mW), TAR 개선 실측. 3모드(fast/low-power/accuracy) 정의.
10. 한계: 디코더 알고리즘은 기존 IEEE 802.16 layered Min-Sum 그대로, 기여는 홍채 파이프라인 통합·DPR 모드전환이며 ECC 코어·정정능력 개선 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC-LDPC layered Min-Sum 복호 | decoder.cpp `LDPC_Decoder()`, `CNU_Update_New_Mag()` | 낮음 — Prime가 이미 보유한 min-sum, 표준 IEEE 802.16 코드라 신규성 없음 |
| 2/4/8bit soft-input 양자화 | channel.cpp `Set_LLR_Th()`, ecc_data.h `PARAM_LLR` | 낮음 — Prime는 2SD/3SD, soft-4bit+ 미지원 방향과 상이 |
| FPGA DPR 다중 디코더 시분할 | 대응 없음 | HW 배포전략(FPGA 재구성)이라 bit-exact 시뮬 코어와 무관 |
| 홍채 이미지처리/매칭 | 대응 없음 | 생체인식 응용계층, ECC와 무관 |

적용 가치: **낮음** — QC-LDPC라 부호종류는 정합하나 디코더는 기존 layered Min-Sum(IEEE 802.16) 재사용이고 신규 기여는 홍채인식 시스템 통합과 FPGA DPR 모드전환이라, NAND binary QC-LDPC ECC 코어 개선으로 떼어 쓸 요소가 거의 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2107.03688v1",
  "title": "An Embedded Iris Recognition System Optimization using Dynamically Reconfigurable Decoder with LDPC Codes",
  "year": 2021,
  "venue": "arXiv cs.CV",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": 0.667,
  "code_length": "960~2016",
  "soft_quant": "soft-4bit+",
  "key_contribution": "IEEE 802.16 QC-LDPC 다중 디코더를 FPGA Dynamic Partial Reconfiguration으로 시분할 전환(fast/low-power/accuracy 모드)해 임베디드 홍채인식에 적용",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "동등",
  "recommend": "하",
  "caveat": "디코더 알고리즘은 기존 layered Min-Sum(IEEE 802.16) 재사용, 기여는 홍채인식 시스템 통합 + DPR 모드전환이라 ECC 코어 개선 없음",
  "todo_check": "DPR 기반 다중 코드 시분할 디코더가 NAND 멀티-rate/멀티-모드 ECC 엔진 전환 전략에 시사점 있는지"
}
```
