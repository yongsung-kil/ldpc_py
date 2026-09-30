### arxiv:1904.13245v1 - Design of Protograph Codes for Additive White Symmetric Alpha-Stable Noise Channels (2019, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | protograph |
| 부호rate | 0.5 |
| 부호length | 1000~8000 |
| 연판정 | 무관 |
| 핵심기여 | 임펄스잡음(alpha-stable) 채널용 시뮬기반 P-EXIT + AWD 분석으로 protograph 부호 설계, AR4JA·irregular 대비 BER 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | AWSαSN(임펄스 non-Gaussian) 채널 전용 임계값 최적화, HW 미설계·시뮬만 — NAND(AWGN/RBER) 채널과 부호설계 목적이 다름 |
| 추가확인 | 시뮬기반 P-EXIT 임계값 최적화 절차를 NAND 채널 protograph 설계에 재사용 가능한지 |

> 총평: 임펄스잡음 채널 특화 protograph 부호설계(이론+시뮬)로 채널모델·부호구조가 NAND 고정 binary QC-LDPC(Prime ECC)와 달라 이식성 낮음.

### B. 알고리즘 요약

1. 시스템: rate-1/2 protograph LDPC(base matrix `B`, `S=4`, `T=7`), BPSK, `N=1000~8000`, PEG+circulant permutation으로 lifting, 최대 100 iteration.
2. 문제: 임펄스잡음(실내무선/수중음향/PLC)은 non-Gaussian(symmetric alpha-stable)이라 AWGN용 closed-form P-EXIT를 직접 적용 불가.
3. 채널모델: AWSαSN, 특성함수 `φ(l)=exp(-γ^α|l|^α)`, 특성지수 `α∈(0,2)`(작을수록 impulsive), G-SNR 정의로 `Eb/N0` 환산.
4. 핵심 기법 1: 시뮬기반 EXIT 함수 — AWGN·AWSαSN 모두 BISC라 EXIT 곡선이 BEC/BSC 사이에 있고 AWSαSN이 AWGN에 근접 → AWGN의 `Lin`으로 근사, `Lch=log P(F|+1)/P(F|-1)`는 수치법으로 계산.
5. 핵심 식: 외재정보 `IVND,E = 1 - (1/M)Σ log2(1+e^{-Lout})` (식 13)로 MI 추정, box-plus로 CND MI.
6. 핵심 기법 2: 이 EXIT 함수 기반 시뮬기반 P-EXIT(식 14~17)로 protograph의 복호 임계값 계산·최적화(DE 대비 |ε|≤0.06dB로 검증).
7. 부수: AWD(asymptotic weight distribution) 분석으로 typical minimum distance ratio(r(δ)의 second-zero crossing)>0 확인 → linear minimum distance growth 보장(낮은 error-floor).
8. 최적화 절차: degree-2 VN 비율 조정으로 임계값↓ + AWD로 min-distance 보장, precoding 적용해 임계값 추가 개선, 고차 VN puncturing.
9. 결과: 설계부호 임계값 0.81dB(α=1.8)/1.95dB(α=1)로 AR4JA(0.98/2.27dB)·irregular보다 낮고, BER=10^-5에서 AR4JA 대비 0.1~0.2dB gain, irregular는 10^-6에서 error-floor 발생하나 제안부호는 없음.
10. 한계: HW 미설계, 시뮬만, gate/throughput 미보고, 임펄스잡음 채널 전용(NAND read/soft-quant 무관).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| protograph 부호설계(base matrix, PEG lifting) | ecc_top.cpp `Load_PCM()` | 부호구조 레이어에 닿으나 Prime ECC는 고정 QC-LDPC, 재검증 부담 큼 |
| 시뮬기반 P-EXIT/AWD 임계값 최적화 | 대응 없음 | 부호설계 이론도구, 코드베이스에 대응 모듈 없음 |
| AWSαSN 채널 LLR 계산 | channel.cpp `Set_LLR_Th()` | Prime ECC는 AWGN/RBER 채널만, alpha-stable 미지원 |

적용 가치: **낮음** — 임펄스잡음 채널용 protograph 부호설계라 채널모델과 부호구조가 NAND용 고정 binary QC-LDPC(Prime ECC)와 달라 직접 이식 이득이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1904.13245v1",
  "title": "Design of Protograph Codes for Additive White Symmetric Alpha-Stable Noise Channels",
  "year": 2019,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "protograph",
  "code_rate": 0.5,
  "code_length": "1000~8000",
  "soft_quant": "무관",
  "key_contribution": "임펄스잡음(alpha-stable) 채널용 시뮬기반 P-EXIT + AWD 분석으로 protograph 부호 설계, AR4JA·irregular 대비 BER 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "AWSαSN(임펄스 non-Gaussian) 채널 전용 임계값 최적화, HW 미설계·시뮬만 — NAND(AWGN/RBER) 채널과 부호설계 목적이 다름",
  "todo_check": "시뮬기반 P-EXIT 임계값 최적화 절차를 NAND 채널 protograph 설계에 재사용 가능한지"
}
```
