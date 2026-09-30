### arxiv:2209.01424v1 - Dynamic Write-Voltage Design and Read-Voltage Optimization for MLC NAND Flash Memory (2022, China Communications)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 직접 |
| 대상 | other |
| 부호종류 | protograph |
| 부호rate | 0.89 |
| 부호length | 미상 |
| 연판정 | soft-2~3bit |
| 핵심기여 | LDPC 최소Hamming거리 반영 cost function으로 write-voltage 갱신 + LLR-aware cost로 read-voltage(entropy θ) 저복잡도 최적화 |
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
| 추천도 | 중 |
| 한계,주의 | 디코더/부호 자체는 손대지 않음(BP 그대로), MLC 2bit/page 채널·voltage 모델에 특화되어 우리 채널 모듈 이식 시 재모델링 필요 |
| 추가확인 | soft-read threshold/LLR 산출부(channel.cpp)가 우리 NAND 채널 파라미터로도 cost function이 유효한지 검증 필요 |

> 총평: 디코더가 아닌 write/read-voltage(soft-read LLR) 최적화 논문 — 부호설계/복호는 표준 BP 그대로라 이식은 채널·LLR 계층에 한정, NAND 직접 타깃이라 관련성은 높음.

### B. 알고리즘 요약

1. 시스템: MLC(2bit/cell) NAND, 채널코딩은 rate-0.89 protograph LDPC(PEG 구성), BP 복호 max iter 50, soft-decision(6 read-voltage → 7구간 LLR).
2. 문제: PE cycle·retention에 따라 threshold-voltage PDF가 비대칭·비정상적으로 변해 고정 write/read voltage로는 BER 열화.
3. 채널 모델: programming noise+RTN+retention noise(+CCI는 post-comp로 무시)를 합쳐 4상태 Gaussian `psi(x)` (평균/분산 PE·T 종속)로 근사.
4. write-voltage 기법: MSB/LSB 페이지 RBER 비대칭과 LDPC `dmin`을 반영한 cost function `Cwrite = 2^(-1.5 dmin)·ωlsb + 4^(-dmin)·ωmsb` 정의(ML-decoding BER 상한 Eq.10/11 단순화).
5. 식 의미: `dmin`(코드 최소거리) 가중으로 페이지별 RBER를 BER 상한에 근사시켜, 부호 강함을 write-voltage 결정에 직접 반영.
6. 최적화: `V1*,V2*`를 bisection search로 교대 고정·탐색(Algorithm 1, q≤50)하여 `Cwrite` 최소화.
7. read-voltage 기법: entropy 함수 `H(v)`로 6개 read voltage를 θ로 매개, error bit의 noise level `αPe`·expected LLR `αllr`로 새 cost `Cread`(Eq.22~24) 구성.
8. 학습: BP로 얻은 BER-θ 열에 linear regression으로 가중치 `c1,c2` 추정, gradient-descent로 `θ* = argmin Cread` 탐색.
9. 결과: PE=18000에서 제안 write-voltage BER 2.2e-6 (MRD 1.0e-5, min-RBER 7.5e-5 대비 우수); read-voltage는 MMI보다 약간·CNN/ART/entropy 대비 크게 우수, 복잡도 O(8(Q+1))로 entropy-기반 O(8 dc I η B) 대비 대폭 절감.
10. 한계: HW 미설계·MATLAB 시뮬만, MLC 2bit 채널·voltage 모델에 특화, 디코더/부호 자체 개선은 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| read-voltage/soft-read LLR 산출·threshold 최적화 | channel.cpp `Set_R_Offset()`, `Set_LLR_Th()` | soft-2~3bit LLR threshold 결정을 cost function으로 대체 가능 (직접 대응) |
| write-voltage 설계 (프로그램 전압) | 대응 없음 | 우리 시뮬은 RBER/AWGN 에러 주입만, 프로그램 전압 모델 없음 |
| BP 복호 / LDPC 부호 | decoder.cpp `LDPC_Decoder()` | 논문은 표준 BP만 사용 — 우리 min-sum 대비 신규 기여 없음 |

적용 가치: 중간 — 디코더/부호는 새 게 없으나, soft-read LLR/threshold를 저복잡도 cost function으로 결정하는 아이디어는 `channel.cpp` LLR 테이블 튜닝에 참고할 만하되 MLC 전용 채널 모델 재이식이 필요.

### D. JSON 블록

```json
{
  "id": "arxiv:2209.01424v1",
  "title": "Dynamic Write-Voltage Design and Read-Voltage Optimization for MLC NAND Flash Memory",
  "year": 2022,
  "venue": "China Communications",
  "portability": "중",
  "nand_relevance": "직접",
  "target": "other",
  "code_type": "protograph",
  "code_rate": 0.89,
  "code_length": "미상",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "LDPC dmin 반영 cost function으로 write-voltage 갱신 + LLR-aware cost로 read-voltage(entropy) 저복잡도 최적화",
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
  "recommend": "중",
  "caveat": "디코더/부호 자체는 손대지 않고 BP 그대로, MLC 2bit voltage 모델 특화로 채널 모듈 재이식 필요",
  "todo_check": "soft-read threshold/LLR 산출부가 우리 NAND 채널 파라미터로도 cost function이 유효한지 검증"
}
```
