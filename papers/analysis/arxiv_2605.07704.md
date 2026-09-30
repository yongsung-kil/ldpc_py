### arxiv:2605.07704v1 - RFNoC-Based FPGA Offloading for Fully Programmable PHY Acceleration (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 26112 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 5G NR PHY 레이어(LDPC 인코딩/디코딩, rate matching, interleaving, scrambling, LLR 추정, HARQ)를 RFNoC 기반 FPGA로 오프로드하고 OAI 소프트웨어와 통합한 실시간 시스템 구현 |
| HW설계 | O |
| 검증수준 | 실측 |
| 복잡도 | 219137 LUT(51.53%)/235.5 BRAM(23.47%)/64 URAM(80%)/2042 DSP(47.8%) @Zynq UltraScale+ ZU28DR |
| 병렬화 | 부분 |
| Throughput | 0.9 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | LDPC 디코더는 Xilinx hardened IP core(offset min-sum, offset 0.5, max 8 iteration)를 그대로 사용하며 알고리즘 자체 개선 없음; 5G NR 표준 BG1/BG2 QC-LDPC 특화, NAND 미언급 |
| 추가확인 | LLR 추정/디스크램블러/디인터리버 등 주변 파이프라인(BRAM 기반 barrel shifter, 병렬 LLR 처리)이 NAND 컨트롤러의 soft-read 파이프라인 설계에 참고될 여지가 있는지 |

> 총평: 무선통신(5G NR) PHY 레이어 전체를 FPGA/RFNoC로 오프로드하는 시스템 통합 논문으로, LDPC 자체는 표준 hardened IP를 그대로 사용해 부호설계·디코더 알고리즘 기여가 없어 NAND ECC 이식 가치는 낮음.

### B. 알고리즘 요약

1. 대상 시스템은 5G NR PHY 레이어 전체(gNB 측)이며, LDPC 인코딩/디코딩·rate matching·interleaving·scrambling·LLR 추정·HARQ를 USRP X410의 Zynq UltraScale+ FPGA(RFNoC 프레임워크)로 오프로드.
2. 풀려는 문제: 기존 AVX-512 CPU 가속 방식은 고가의 멀티코어 프로세서에 의존하고 재구성이 어려우며, 기존 FPGA 가속 연구는 개별 기능 오프로드나 시뮬레이터 기반 평가에 그쳐 실제 네트워크 종단 검증이 부재했음.
3. 핵심 가정/모델: 5G NR 표준(3GPP TS 38.212)의 BG1(K=10Zc, Ncb=50Zc)/BG2(K=22Zc, Ncb=66Zc) QC-LDPC 부호와 AWGN 유사 채널에서 등화된 신호를 대상.
4. LDPC 인코더는 표준 base graph lifting(`Zc`) 구조 그대로 구현, 디코더는 Xilinx의 hardened LDPC decoder IP core(offset min-sum algorithm, offset=0.5, 최대 8회 반복, 조기종료: parity 만족 또는 hard decision 불변 시)를 사용 - 알고리즘 자체는 표준/기성 IP 그대로.
5. LLR 추정은 max-log 근사 및 gray-mapped QAM 대칭성을 이용한 piecewise-linear 근사식(`LLR_b ≈ (|r|-B)/A·σ²` 형태)을 파이프라인(13-stage, 8×DSP48E2)으로 구현 - 4비트 정수+2비트 소수 고정소수점(-7.75~7.75).
6. 부수 트릭: rate matching/interleaving은 BRAM36 + 16-bit barrel shifter로 순환버퍼 read/write 구현, HARQ rate unmatching은 URAM 기반 16개 가상 순환버퍼(16×1652×128bit)로 재전송 조합 지원.
7. deinterleaver는 4세트×8버퍼 구조(24×BRAM36)로 병렬 읽기 후 128-bit(16 LLR)로 결합해 Xilinx LDPC 디코더 IP의 최대 병렬 처리(16 LLR/cycle)를 채움.
8. 별도 학습/최적화 절차 없음 (표준 규격 기반 고정 설계, HW 파라미터는 클록 250/500MHz로 설정).
9. 결과: FPGA 자원 사용률 LUT 51.53%/BRAM 23.47%/URAM 80%/DSP 47.8%, K=8448/Ncb=26112/G=12672 조건에서 처리량 899.9~900.1 Mbps 달성(상용 스마트폰 실제 5G 접속 검증), HARQ 가상메모리 16개 사용 시 77.9 Mbps 실환경 처리량.
10. 한계: LDPC 알고리즘 자체는 기성 IP 그대로 사용(자체 개선 없음), 디코딩 다중 iteration 시 처리량 저하 가능성 언급, 변조는 CPU에서 처리(FPGA 오프로드 대상 아님).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| offset min-sum LDPC 디코더(Xilinx hardened IP) | `decoder.cpp` `CNU_Update_New_Mag()` | Prime ECC도 min-sum 기반이나 이미 보유(§3)한 기법으로 신규 기여 없음. 표준 5G BG1/BG2 부호 고정이라 재사용 가치 낮음 |
| soft-read LLR 근사식(piecewise-linear max-log) | `channel.cpp` `Set_LLR_Th()` | 무선통신 QAM 복조 특화 근사식으로 NAND read-retry LLR 테이블 설계와 목적/입력 신호가 상이 |
| HARQ 조기종료(parity 만족/hard decision 불변) | `partial_CRC.cpp` `partial_crc_HW_T4()` | 개념적으로 조기종료 유사하나 5G HARQ 재전송 결합 로직으로 NAND ECC 조기종료(CRC)와는 별개 메커니즘 |
| BRAM 기반 barrel shifter 순환버퍼(rate matching) | 대응 없음 | 무선 rate matching 전용 구조, Prime ECC 부호 구조에 대응 없음 |

적용 가치: 낮음 - 5G NR 표준 무선통신 PHY 시스템 통합/오프로드 논문으로 LDPC는 기성 hardened IP를 그대로 사용해 부호설계·디코더 알고리즘 신규 기여가 없음. NAND ECC 이식 관점의 기술적 접점이 거의 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.07704v1",
  "title": "RFNoC-Based FPGA Offloading for Fully Programmable PHY Acceleration",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "26112",
  "soft_quant": "soft-4bit+",
  "key_contribution": "5G NR PHY 레이어(LDPC 인코딩/디코딩, rate matching, interleaving, scrambling, LLR 추정, HARQ)를 RFNoC 기반 FPGA로 오프로드하고 OAI 소프트웨어와 통합한 실시간 시스템 구현",
  "hw_designed": "O",
  "verification": "실측",
  "complexity": "219137 LUT(51.53%)/235.5 BRAM(23.47%)/64 URAM(80%)/2042 DSP(47.8%) @Zynq UltraScale+ ZU28DR",
  "parallelism": "부분",
  "throughput_gbps": 0.9,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "LDPC 디코더는 Xilinx hardened IP core(offset min-sum, offset 0.5, max 8 iteration)를 그대로 사용하며 알고리즘 자체 개선 없음; 5G NR 표준 BG1/BG2 QC-LDPC 특화, NAND 미언급",
  "todo_check": "LLR 추정/디스크램블러/디인터리버 등 주변 파이프라인(BRAM 기반 barrel shifter, 병렬 LLR 처리)이 NAND 컨트롤러의 soft-read 파이프라인 설계에 참고될 여지가 있는지"
}
```
