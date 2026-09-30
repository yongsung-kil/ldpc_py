### arxiv:1503.02986v3 - Strategies for High-Throughput FPGA-based QC-LDPC Decoder Architecture (2015, arXiv:cs.AR)

| 카테고리 | 값 |
|---|---|
| 이식성 | 상 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5 |
| 부호length | 648~1944 |
| 연판정 | soft-4bit+ |
| 핵심기여 | PCM의 compact 표현(βI/βS)으로 invalid block 스킵 + GNPU/LNPU 분리로 min-sum 선형복잡도화 + superlayer 2-layer 파이프라이닝으로 FPGA throughput 극대화 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 미상(FF/BRAM/DSP48/LUT % 자원사용률만 제시, gatecount 없음) |
| 병렬화 | 완전병렬 |
| Throughput | 0.608Gbps |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | 개선 |
| 추천도 | 상 |
| 한계,주의 | scaled min-sum(scaling factor 0.75) 기반이라 Prime ECC의 min1/min2 방식과 유사하나, HW는 Xilinx FPGA 자동생성(LabVIEW CSDS HLS) 기반이라 ASIC/커스텀 RTL과 최적화 지점이 다를 수 있음 |
| 추가확인 | 논문 코드가 규칙적(regular) 구조 가정(8-block 고정, static 주소생성)이라 Prime ECC의 불규칙 degree(17, HCU 비대칭 col) 구조에 그대로 맞는지 확인 필요 |

> 총평: PCM invalid-block 스킵과 GNPU/LNPU 분리형 선형복잡도 min-sum, layer-pipelining은 Prime ECC의 decoder.cpp 파이프라인/HCU 설계와 직접 비교 가능한 이식성 높은 아키텍처 기법.

### B. 알고리즘 요약

1. 대상: IEEE 802.11n(2012) QC-LDPC, rate=1/2, z=27/54/81(N=648/1296/1944), circulant-1 identity 기반 base matrix `Hb`(12x24).
2. 문제: 기존 FPGA fully-parallel 구현은 라우팅 혼잡으로 큰 block size에 부적합, ASIC 커스텀 RTL은 재사용성 낮음 → HLS 기반 고처리량 FPGA 아키텍처 필요.
3. 채널/디코딩 모델: 표준 AWGN LLR 입력, 반복 message-passing(scaled-MSA).
4. 핵심 기법 1: scaled Min-Sum Algorithm (scale factor `a=0.75`)을 [19]의 layered(온더플라이) 스케줄로 사용, CN/VN 메시지를 하나의 Node Processing Unit(NPU)에서 처리.
5. 핵심 식: CTV 메시지 `r_ij = a·sign(Πq)·min|q|`; min 연산을 O(d_ci²)→O(d_ci)로 낮추기 위해 Global pass(1st/2nd min 계산, GNPU)와 Local pass(최종 min 산출, LNPU)로 분리.
6. 핵심 기법 2: PCM `Hb`를 valid block(순환shift 존재)만 남긴 compact 표현 `βI`(block index)/`βS`(shift value)로 재구성, invalid(0) block 처리를 생략해 compaction ratio `λ=J/nb`만큼 throughput 이득(사례: λ=1/3 → 3배).
7. 부수 트릭: superlayer(동일 block column index가 여러 layer에 겹치지 않는 layer 집합) 개념으로 GNPU-LNPU 2-layer 파이프라이닝, `βI` 재배열로 layer 의존성 스태거링, z개 NPU 병렬(z-fold parallelization)로 submatrix `Is` 단위 동시처리.
8. 최적화 절차 없음(설계 규칙 기반, GA/DE 아님); 파이프라이닝 효율 `η_p(2)=|L|/(|L|+1)`을 최대화하는 `|L|`을 짝수 인수 중 탐색(사례 l*=6).
9. 결과: Kintex-7 FPGA, 260MHz(코어 608Mb/s), 200MHz에서 latency 5.7µs; 2x 파이프라인이 1x 대비 1.7배 빠름(337→608Mb/s); 5개 코어 병렬로 2.06Gb/s 별도 시연.
10. 한계: fixed-point(6bit signed, 4frac) 구현이 floating-point 대비 약 0.5dB 성능 열화; regular 8-block 가정으로 실제 코드 구조(L7/L12만 8개 block)에 대해 invalid block 일부 처리로 인한 throughput 손실 존재; ASIC 합성/게이트카운트 미제시.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| PCM compact 표현(βI/βS, invalid block 스킵) | `ecc_top.cpp` `Load_PCM()`, `ecc_data.h`(PCM 구조체) | H-matrix 로드/표현 최적화 아이디어로 이식 가능성 있으나 부호구조 자체(rate/length) 변경은 아님 |
| GNPU(global min1/min2)-LNPU(local min 산출) 분리 | `decoder.cpp` `CNU_Update_New_Mag()` | Prime ECC의 min1/min2 CN 연산과 개념 일치, 선형복잡도 구조 재확인/최적화 참고자료로 활용 가능 |
| superlayer 기반 layer-pipelining(2x) | `decoder.cpp` `LDPC_Decoder()` (이터레이션/레이어 스케줄) | Dual-Update와 유사한 레이어 스케줄링 아이디어, 파이프라이닝 깊이 설계 참고 가능 |
| z-fold NPU 병렬화 | `decoder.cpp` (z_sb=32 row 단위 병렬) | Prime ECC의 z_sb=32 병렬 구조와 동일한 컨셉(circulant 단위 병렬) |
| scaled Min-Sum (scale factor 0.75) | `decoder.cpp` `CNU_Update_New_Mag()` | 이미 보유한 min-sum 변형이나 scaling factor 최적화 참고 가능 |

> 적용 가치: 높음 - min-sum 기반 QC-LDPC decoder의 PCM compact 표현과 GNPU/LNPU 선형복잡도 분리, layer-pipelining 기법이 Prime ECC 디코더 구조와 직접 대응되어 참고 가치가 큼(단, 이미 보유한 min-sum/병렬화 기법과 상당 부분 중복).

### D. JSON 블록

```json
{
  "id": "arxiv:1503.02986v3",
  "title": "Strategies for High-Throughput FPGA-based QC-LDPC Decoder Architecture",
  "year": 2015,
  "venue": "arXiv:cs.AR",
  "portability": "상",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": 0.5,
  "code_length": "648~1944",
  "soft_quant": "soft-4bit+",
  "key_contribution": "PCM의 compact 표현(βI/βS)으로 invalid block 스킵 + GNPU/LNPU 분리로 min-sum 선형복잡도화 + superlayer 2-layer 파이프라이닝으로 FPGA throughput 극대화",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": 0.608,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "개선",
  "recommend": "상",
  "caveat": "scaled min-sum(scaling factor 0.75) 기반이라 Prime ECC의 min1/min2 방식과 유사하나, HW는 Xilinx FPGA 자동생성(LabVIEW CSDS HLS) 기반이라 ASIC/커스텀 RTL과 최적화 지점이 다를 수 있음",
  "todo_check": "논문 코드가 규칙적(regular) 구조 가정(8-block 고정, static 주소생성)이라 Prime ECC의 불규칙 degree(17, HCU 비대칭 col) 구조에 그대로 맞는지 확인 필요"
}
```
