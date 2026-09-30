### arxiv:1904.06666v5 - Mutual Information-Maximizing Quantized Belief Propagation Decoding of Regular LDPC Codes (2022, arXiv / IEEE)

| 카테고리 | 값 |
|---|---|
| 이식성 | 상 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5~0.84 |
| 부호length | 2048~8000 |
| 연판정 | soft-2~3bit |
| 핵심기여 | MI최대화 RCQ 파라미터(재구성함수·SDQ) 체계적 설계로 3bit 메시지 FAID가 부동소수 BP 능가 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 상 |
| 한계,주의 | regular LDPC 전제(QC 최적화 미포함), HW/RTL 미설계·AWGN BPSK 시뮬만, σd 설계값 의존 |
| 추가확인 | high-rate QC-LDPC + NAND soft-read(2/3SD)에서 σd·비트폭(qc,qv) 재튜닝 시 부동소수 BP 대비 이득 유지 검증 |

> 총평: MI최대화 3/4bit 양자화 BP가 부동소수 BP를 고rate·저iteration서 능가, NAND용 저비트 디코더에 직접 이식가치 높아 이식성 상.

### B. 알고리즘 요약

1. 대상은 regular `(dv,dc)` LDPC(예제: (6,32) len2048 rate0.84, (3,6) len8000 rate0.5), AWGN BPSK, NAND flash처럼 메모리·복잡도 제약 큰 시스템 겨냥.
2. 문제: LUT 기반 MIM-FAID(MIM-LUT)는 2입력1출력 LUT를 cascade하며 MI·에러율 성능 열화, 초기 FAID는 (3,6)에 특화·수동최적화 필요.
3. 모델: 이진입력 DMC로 채널·메시지 양자화를 통일, C2V/V2C 메시지를 유한알파벳 `S`,`R`(3bit=8, 4bit=16)로 표현.
4. 핵심기법: RCQ(reconstruction-calculation-quantization) 구조 - CN은 `φc`로 심볼→계산값 재구성, `Φc`(부호 XOR + 크기 합산)로 결합, SDQ `Γc`로 재양자화하여 `I(X;S)` 최대화.
5. 핵심식: 최적 재구성함수 `φc*(r)=-sgn(g(r))log|g(r)|` (식33)이 `I(X;S)` 최대화(Theorem 1), BP의 CN함수 `f(θ)=log((e^θ+1)/(e^θ-1))`와 `f(|LLR|)=-log|g(r)|`로 연결.
6. VN 확장: `φv*(s)=log(PS|X(s|0)/PS|X(s|1))`, `φch*`는 각각 LLR과 등가(Theorem 2), `Φv=φch(l)+Σφv(si)` 합산 후 SDQ `Γv`로 `I(X;R)` 최대화.
7. 구현 디테일: 정수영역 `D=Z`에서 최적 RF를 스케일(식35,39)해 near-optimal 근사, qc/qv 비트폭 오버플로 방지, 저장복잡도 `O(|R|+|S|)`로 무시가능.
8. 최적화 절차: DE로 각 iteration pmf 추적, DP로 최적 SDQ(`Λc`,`Λv`) 탐색(Algorithm1/2, 복잡도 `O(dc·2^qc·|R|)` 등), 설계임계 `σ*`(식11)로 σd 선정.
9. 결과: (6,32) 부호에서 4bit MIM-QBP가 부동소수 BP·4bit MIM-LUT 능가, 3bit도 고SNR서 부동소수 BP 상회(3bit MIM-LUT 대비 +0.15dB), (3,6)서 4bit가 부동소수 BP와 0.05dB 이내.
10. 한계: HW/RTL 미설계·gate/throughput 미측정, regular LDPC·AWGN BPSK 시뮬 전제, QC 구조·NAND soft-read 직접 실험 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| CN 재구성·양자화 UF (`φc`,`Φc`,`Γc`) | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | min-sum CN을 MI최대화 RCQ로 대체 가능, waterfall/error-floor 개선 기대 |
| VN 재구성·양자화 UF (`φv`,`φch`,`Γv`) | decoder.cpp `VN_Cal_HD()` 등, `decoder.h` `Get_VNU_*` | HD/2SD/3SD VN 양자화를 MI최대화 테이블로 교체 |
| iteration별 최적 LLR/임계 테이블 (`Γ`, σ* 설계) | ecc_data.h `PARAM_LLR`, `decoder.cpp` `Get_VNU_Table_Idx()` | 적응형 LLR 테이블을 MI기준으로 체계적 재설계 |
| 채널 pmf / soft-read 양자화 | channel.cpp `Set_LLR_Th()`, `Set_R_Offset()` | 2/3SD read 임계 설계에 MI최대화 DMC 양자화 적용 |
| DE/DP 기반 파라미터 자동설계 | local_opt.cpp (LLR 자동최적화) | 수동튜닝 대신 MI최대화 자동설계 파이프라인 대체 |

적용 가치: **높음** — 3bit 양자화로 부동소수 BP를 능가하는 MI최대화 RCQ 설계법은 Prime ECC의 min-sum/적응형 LLR 테이블을 체계적으로 재설계·개선할 직접 후보이며, NAND 저비트 read 비용과 정합.

### D. JSON 블록

```json
{
  "id": "arxiv:1904.06666v5",
  "title": "Mutual Information-Maximizing Quantized Belief Propagation Decoding of Regular LDPC Codes",
  "year": 2022,
  "venue": "arXiv / IEEE",
  "portability": "상",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": "0.5~0.84",
  "code_length": "2048~8000",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "MI최대화 RCQ 파라미터(재구성함수·SDQ) 체계적 설계로 3bit 메시지 FAID가 부동소수 BP 능가",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "상",
  "caveat": "regular LDPC 전제(QC 최적화 미포함), HW/RTL 미설계·AWGN BPSK 시뮬만, σd 설계값 의존",
  "todo_check": "high-rate QC-LDPC + NAND soft-read(2/3SD)에서 σd·비트폭(qc,qv) 재튜닝 시 부동소수 BP 대비 이득 유지 검증"
}
```
