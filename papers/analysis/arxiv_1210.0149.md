### arxiv:1210.0149v1 - LDPC Decoding with Limited-Precision Soft Information in Flash Memories (2012, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 상 |
| NAND관련성 | 직접 |
| 대상 | both |
| 부호종류 | irregular |
| 부호rate | 0.9021 |
| 부호length | 9118 |
| 연판정 | soft-2~3bit |
| 핵심기여 | 다중 read word-line voltage를 mutual information 최대화(MMI)로 선정하고, 이를 constant-ratio(CR) 방식으로 단순화; quantized 환경에 맞춰 absorbing set을 피하도록 LDPC 차수분포를 재설계 |
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
| 추천도 | 상 |
| 한계,주의 | HW 설계·복잡도·throughput 분석 없이 순수 알고리즘/시뮬 수준이며 word-line voltage 재프로그래밍이 실제 NAND 컨트롤러에서 read latency에 미치는 영향은 다루지 않음 |
| 추가확인 | Prime ECC의 2SD/3SD LLR threshold 테이블 설계 시 MMI 기반 word-line voltage 선정 방식과 constant-ratio 근사를 실제로 채택하고 있는지, 채택 안 했다면 CR 방식의 개선 여지 |

> 총평: soft-read 비용(read 횟수)과 정정성능 트레이드오프를 MMI 이론으로 최적화하고 quantization 특화 LDPC 설계(absorbing set 회피)까지 다뤄, Prime ECC의 LLR 양자화·soft-read 설계와 직결되는 이식성 상 논문.

### B. 알고리즘 요약

1. NAND flash SLC/4-level MLC를 PAM+Gaussian 채널로 모델링하고, 다중 read(서로 다른 word-line voltage)로 LDPC 디코더에 limited-precision soft information(1.5bit/2bit 등)을 제공한다.
2. 기존 flash 시스템은 hard decision(1비트)만 제공해 LDPC의 소프트 복호 이득을 활용하지 못하는 문제를 해결하려 한다.
3. read channel은 등가 discrete memoryless channel(DMC)로 모델링하며, word-line voltage(threshold) 선택이 곧 quantization 경계를 결정한다.
4. 핵심 기법: read channel 입출력 간 mutual information(MI)을 최대화하는 word-line voltage를 수치 최적화(MMI, `I(X;Y)=H(Y)-H(Y|X)`)로 선정한다.
5. MI를 최대화하는 quantization이 곧 frame error rate(FER)를 최소화한다는 가설을 시뮬로 확인(단, 코드가 "잘 설계된" 경우에 한함).
6. constant-ratio(CR) 방법: 인접 두 조건부 pdf 비율을 상수 `R`로 고정해 MMI 탐색 공간을 축소, quasi-concave 문제로 단순화 - 성능 손실 거의 없음.
7. retention noise 모델([5])까지 확장해 6개월 등 장기 보존 시나리오에서도 MMI/CR 방식이 유효함을 검증.
8. quantization 인지 코드 설계: AWGN 최적 차수분포는 hard-decoding 시 (4,2)/(5,1)/(5,2) absorbing set에 취약 → degree-3 variable node를 degree-4로 올려(Code 2) absorbing set을 회피, hard-decoding 성능을 크게 개선.
9. 결과: 2회 read만으로 hard-decoding 대비 soft-precision과의 FER 갭 절반 이상 해소; rate 0.9021 LDPC(Code 2)가 동일 rate BCH 대비 우월(예외: Code1은 error floor가 BCH와 교차하는 4×10⁻⁵ 지점 존재).
10. 한계: 순수 시뮬레이션/정보이론 분석이며 HW(A/D 변환기, word-line voltage 재프로그래밍) 구현·복잡도·throughput은 다루지 않음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| MMI 기반 word-line voltage(soft-read threshold) 선정 | `channel.cpp` `Set_R_Offset()`, `Set_LLR_Th()` | 직접 대응: 2SD/3SD soft-read threshold 설계 최적화에 그대로 적용 가능 |
| Constant-Ratio(CR) 단순화 방법 | `channel.cpp` `Set_LLR_Th()` | MMI 전수탐색 대비 HW 친화적 근사로, threshold 테이블 설계 단순화에 이식 가능 |
| quantization 인지 LDPC 차수분포 재설계(absorbing set 회피) | `ecc_top.cpp` `Load_PCM()` | H-matrix 자체를 바꾸는 부호설계로 이식 난이도 높음(고정 QC-LDPC), 다만 error-floor 개선 아이디어는 참고 가치 |
| 다중 read 횟수별 LLR 정밀도 테이블(1.5bit/2bit/soft) | `ecc_data.h` `PARAM_LLR`, `decoder.cpp` `Get_VNU_Table_Idx()` | 직접 대응: iteration/read 횟수별 LLR 테이블 설계와 개념 일치 |

> 적용 가치: 높음. Prime ECC가 이미 지원하는 soft-2~3bit read의 threshold/LLR 설계를 이론적으로 뒷받침하는 MMI/CR 최적화 기법으로, 코드 변경 없이 파라미터 설계(`channel.cpp`)에 바로 적용 가능.

### D. JSON 블록

```json
{
  "id": "arxiv:1210.0149v1",
  "title": "LDPC Decoding with Limited-Precision Soft Information in Flash Memories",
  "year": 2012,
  "venue": "arXiv",
  "portability": "상",
  "nand_relevance": "직접",
  "target": "both",
  "code_type": "irregular",
  "code_rate": 0.9021,
  "code_length": 9118,
  "soft_quant": "soft-2~3bit",
  "key_contribution": "다중 read word-line voltage를 mutual information 최대화(MMI)로 선정하고, 이를 constant-ratio(CR) 방식으로 단순화; quantized 환경에 맞춰 absorbing set을 피하도록 LDPC 차수분포를 재설계",
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
  "recommend": "상",
  "caveat": "HW 설계·복잡도·throughput 분석 없이 순수 알고리즘/시뮬 수준이며 word-line voltage 재프로그래밍이 실제 NAND 컨트롤러에서 read latency에 미치는 영향은 다루지 않음",
  "todo_check": "Prime ECC의 2SD/3SD LLR threshold 테이블 설계 시 MMI 기반 word-line voltage 선정 방식과 constant-ratio 근사를 실제로 채택하고 있는지, 채택 안 했다면 CR 방식의 개선 여지"
}
```
