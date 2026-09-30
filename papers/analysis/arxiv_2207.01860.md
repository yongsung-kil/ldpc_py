### arxiv:2207.01860v1 - High-throughput decoder of quasi-cyclic LDPC codes with limited precision for continuous-variable quantum key distribution systems (2022, arXiv quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.1~0.2 |
| 부호length | 80000~96000 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 유한정밀도 디코더의 잔여오류비트를 신뢰도(|Lqn|) 임계값으로 지우는 post-processor로 FER 저감 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 0.36092Gbps(rate0.2)/0.19465Gbps(rate0.1) |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | X |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | CV-QKD 초저rate(0.1~0.2)/저SNR(<0dB) 특화, MET-LDPC 대상 - NAND 고rate binary QC-LDPC와 체제 상이 |
| 추가확인 | erase 임계값 ∆ 설정법과 정정능력향상이 정밀도 손실 보상 이상인지(부동소수점 대비) 검증 필요 |

> 총평: FPGA layered BP + 신뢰도 기반 잔여오류 erase post-processor. CV-QKD 초저rate 특화라 NAND 이식가치 낮으나 신뢰도 임계 post-processing 아이디어만 참고 가능.

### B. 알고리즘 요약

1. CV-QKD 정보조정용 QC MET-LDPC 부호(rate 0.1/0.2, length 96000/80000, BI-AWGN, SNR<1)의 실시간 FPGA 복호기 설계가 목표.
2. 문제: on-chip 자원 제약으로 고정소수점 정밀도(w=8/10bit)를 낮추면 waterfall 영역에서도 FER가 급증해 실시간 SKR 생성 불가.
3. 채널/모델: BI-AWGN, LLR 초기화 `Lqn(0)=2Rn/σ²`, layered BP(flooding 대비 적은 iteration으로 동등 성능).
4. 핵심기법1: layered BP로 VNU→CNU→total-message 순차 갱신, `Φ(x)=-ln(tanh(x/2))` 기반 CN 갱신, syndrome `s=uH^T`로 조기판정.
5. 핵심 관찰: 실패 codeword의 오류심볼은 신뢰도값 `∆=|Lqn|`이 정답심볼보다 작다(히스토그램으로 확인).
6. 핵심기법2: 잔여오류비트 erase 모듈 - `|Lqn|<∆`인 심볼을 의심집합에 넣어 지움(rate0.2는 ∆=40, rate0.1은 ∆=180 고정).
7. 구현 디테일: fixed-point w=1+I+F, partial-parallel+pipeline, RAM_L/RAM_R 이중 RAM + shift-right/left로 QC 순환시프트, read/write 충돌 회피용 H 설계.
8. 학습/최적화: density evolution로 degree distribution 최적화 후 PEG로 QC MET-LDPC 구성.
9. 결과: Virtex-7 FPGA에서 360.92/194.65 Mbps throughput, erase 모듈로 SKR 425.64%/139.13% 개선, erase 비용은 ~2.4~3 iteration 상당.
10. 한계: 초저rate/저SNR CV-QKD 특화, MET-LDPC 전용, erase가 정밀도 손실을 사후 보정할 뿐 부동소수점 성능엔 미달, latency 추가.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| layered BP CN/VN 갱신 | decoder.cpp `LDPC_Decoder()`, `C2V_Cal()` | Prime은 min-sum, 논문은 full-`tanh` Φ 함수라 알고리즘 상이 |
| 신뢰도 기반 잔여오류 erase post-processor | 대응 없음 | Prime의 조기종료(partial/full CRC)와 목적 다름, 별도 post-processing 없음 |
| 고정소수점 정밀도/양자화 | decoder.cpp `VN_Cal_HD()` 등, `ecc_data.h` `PARAM_LLR` | Prime은 magnitude 양자화 테이블, 논문은 w-bit fixed-point |
| RAM_L/RAM_R + shift 라우팅 | 대응 없음 | Prime HW 모델(z=32, GT/HCU)과 메모리 구조 상이 |

적용 가치: **낮음** - MET-LDPC 초저rate CV-QKD 특화이며 핵심인 잔여오류 erase는 저정밀도 보상용이라 Prime의 고rate binary QC-LDPC 파이프라인에 그대로 이식하기 어렵다.

### D. JSON 블록

```json
{
  "id": "arxiv:2207.01860v1",
  "title": "High-throughput decoder of quasi-cyclic LDPC codes with limited precision for continuous-variable quantum key distribution systems",
  "year": 2022,
  "venue": "arXiv quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "80000~96000",
  "soft_quant": "soft-4bit+",
  "key_contribution": "유한정밀도 디코더의 잔여오류비트를 신뢰도(|Lqn|) 임계값으로 지우는 post-processor로 FER 저감",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": 0.36092,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "X",
  "latency": "악화",
  "recommend": "하",
  "caveat": "CV-QKD 초저rate(0.1~0.2)/저SNR(<0dB) 특화, MET-LDPC 대상 - NAND 고rate binary QC-LDPC와 체제 상이",
  "todo_check": "erase 임계값 ∆ 설정법과 정정능력향상이 정밀도 손실 보상 이상인지(부동소수점 대비) 검증 필요"
}
```
