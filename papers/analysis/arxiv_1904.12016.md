### arxiv:1904.12016v1 - CVR: A Continuously Variable Rate LDPC Decoder Using Parity Check Extension for Minimum Latency (2019, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.5~0.75 |
| 부호length | 864 |
| 연판정 | soft-4bit+ |
| 핵심기여 | WiMAX ¾-rate PCM에 parity extension을 붙여 5G급 FER에 근접하며 fully-parallel 파이프라인 latency 33%·power 36% 절감 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 2.86~3.06Gbps |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | WiMAX/5G 무선표준 특화 rate-compatible 확장(HARQ용), 6bit LLR·mother code 프래그먼트 조기수신 전제 — NAND 고정 고rate 부호와 무관 |
| 추가확인 | parity extension이 아닌 fully-parallel 파이프라인 latency 절감 아이디어만 별도 이식 가능한지 |

> 총평: 무선표준(WiMAX↔5G) rate-compatible 확장 + fully-parallel OMS FPGA 구현으로, 고정 고rate binary QC-LDPC인 Prime ECC에는 이식성 낮음.

### B. 알고리즘 요약

1. 시스템: WiMAX(802.16e) ¾-rate 144×576 PCM을 half-rate 432×864로 parity extension, AWGN/BPSK, 6bit 양자화, 최대 21 iteration.
2. 문제: fully-parallel 파이프라인 디코더의 첫 프레임 지연과 전력 증가, 그리고 WiMAX 대비 5G에 못 미치는 FER(특히 error-floor).
3. 채널/모델: AWGN, BPSK, syndrome `CH^T=0` 수렴 판정(soft belief propagation).
4. 핵심 기법: 확장 PCM을 A(정보)/B(dual-diag)/C(zero)/D(identity)/E(cyclic-shift, row당 1이 5~6개)/F(row·col당 연결 1개)/G(identity) 블록으로 구성 — G를 identity로 두어 인코딩 단순화 및 임의 rate 선택.
5. 핵심 의미: extension은 puncturing의 반대(하위 rate 부호 생성)로 FER/BER를 개선하고 5G처럼 flooring 없이 error curve가 하강.
6. 확장: mother code(짧은 부호)를 먼저 수신·복호 시작하고 SNR 높으면 extra parity 없이도 조기 종료 → latency 단축(type-II HARQ 유사).
7. 구현: fully-parallel OMS(offset min-sum), extra parity CNU는 enable 신호(frame counter/rate controller, SNR 기반)로 on/off, 3개 입력 버퍼(B0/B1/B2) demux 파이프라인으로 2프레임 동시 복호.
8. 학습/최적화: 없음(구조는 시뮬로 블록별 최적 형태 결정, D=identity·F=single-connection이 최적으로 관찰).
9. 결과: FER=10^-3에서 WiMAX 대비 0.1dB gain, 5G와 0.1dB 차, latency 33% 감소, SNR>3dB에서 power 36% 감소, throughput 2.86~3.06Gbps(80MHz, Xilinx Virtex 7).
10. 한계: gate count 미보고, 무선표준 특화, iteration은 짧은 부호일수록 증가(SNR>3dB에서만 무시가능), NAND read/soft-quant 비용 논의 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Offset Min-Sum CN 갱신 | decoder.cpp `CNU_Update_New_Mag()` | 이미 min-sum 보유(중복 기여) |
| parity extension으로 rate 가변 PCM 구성 | ecc_top.cpp `Load_PCM()` | Prime ECC는 고정 고rate 부호라 rate-compatible 확장 불필요 |
| fully-parallel 파이프라인/CNU enable 제어 | 대응 없음 (Prime ECC는 z=32 row병렬 6-stage 파이프라인) | 병렬 구조 상이, HW 정합 부담 |
| dual-diagonal parity part(B) 인코딩 | encoder.cpp `LDPC_encoder_4KB()` | dual-diagonal은 이미 보유(중복) |

적용 가치: **낮음** — 무선표준 rate-compatible 확장과 fully-parallel HARQ 파이프라인이 핵심이라 고정 고rate NAND binary QC-LDPC(Prime ECC)와 목적·구조가 달라 이식 이득이 적다.

### D. JSON 블록

```json
{
  "id": "arxiv:1904.12016v1",
  "title": "CVR: A Continuously Variable Rate LDPC Decoder Using Parity Check Extension for Minimum Latency",
  "year": 2019,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": "0.5~0.75",
  "code_length": 864,
  "soft_quant": "soft-4bit+",
  "key_contribution": "WiMAX ¾-rate PCM에 parity extension을 붙여 5G급 FER에 근접하며 fully-parallel 파이프라인 latency 33%·power 36% 절감",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": "2.86~3.06",
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "하",
  "caveat": "WiMAX/5G 무선표준 특화 rate-compatible 확장(HARQ용), 6bit LLR·mother code 프래그먼트 조기수신 전제 — NAND 고정 고rate 부호와 무관",
  "todo_check": "parity extension이 아닌 fully-parallel 파이프라인 latency 절감 아이디어만 별도 이식 가능한지"
}
```
