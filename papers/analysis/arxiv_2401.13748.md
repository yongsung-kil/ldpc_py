### arxiv:2401.13748v1 - Log-Log Domain Sum-Product Algorithm for Information Reconciliation in Continuous-Variable Quantum Key Distribution (2024, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | protograph |
| 부호rate | 0.01~0.1 |
| 부호length | 128000~998400 |
| 연판정 | soft-4bit+ |
| 핵심기여 | log-LLR(log-log) 도메인 SPA로 CN 메시지의 소수부 비트폭 25%+ 절감 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | 동등 |
| 추천도 | 하 |
| 한계,주의 | ultra-low-rate BI-AWGN(CV-QKD) 전용 SPA·비트폭 절감이라 고rate NAND min-sum엔 부적합 |
| 추가확인 | CN 근사식(6)의 tanh 스케일링 통찰이 min-sum scaling factor 튜닝에 참고될 여지만 확인 |

> 총평: CV-QKD ultra-low-rate MET-LDPC용 SPA 메모리 최적화 기법으로, 고rate binary min-sum 기반 Prime ECC와 코드종류·rate·알고리즘 모두 상이해 이식성 낮음.

### B. 알고리즘 요약

1. 시스템: CV-QKD reverse reconciliation의 BI-AWGN 합성채널, MET/TBP-LDPC 부호(rate `R=0.01`, `N=998400` / `R=0.1`, `N=128000`), 초저 SNR·고 FER(~0.1) 운용.
2. 문제: 초저rate 부호는 CN extrinsic 메시지가 매우 작아 fixed-point에서 0으로 반올림 -> 고정밀 요구 -> FPGA 메모리 폭증.
3. 모델: 채널 `r=t+n`, 나눗셈 후 `y=(-1)^C + n'`, BI-AWGN. LLR을 부호 `α`와 크기 `γ`로 분리, 로그크기 `L̃=ln(γ)`.
4. 핵심 기법1: SPA CN update의 box-plus 보정항 `s(γmin,γmax)`를 Taylor+geometric 급수로 근사(식5,6) -> `L_c ≈ Πα · γm · Π tanh(γℓ/2)`, `m=argmin|L|`.
5. 의미: tanh가 큰 LLR에서 포화하므로 최소크기 `γm`만 지배 -> min-sum 유사 구조 + tanh 스케일링으로 정확도 보전.
6. 핵심 기법2: log-log 도메인 SPA(식8) - 로그크기 도메인에서 CN을 덧셈으로 처리, VN은 log-sum/diff-exp `f±=max+ln(1±exp(-|Δ|))` 사용.
7. 구현 디테일: CN의 `ln(tanh(exp(x)/2))`를 4구간 piecewise-linear `g(x)`(식11)로 대체(LUT 불필요), 상수 offset `b`(=5) 도입해 log-LLR sign 비트 제거.
8. 학습/최적화: offset `b`를 시뮬로 튜닝, fixed-point `(1,x,y)` 표기에서 소수부 `y` 최소화.
9. 결과: R=0.01은 FP(1,3,6) log-LLR이 SPA FP(1,3,8) 대비 소수부 25% 절감하며 성능 우수; R=0.1은 FP(1,3,4)로 40%+ 절감, floating SPA와 0.05dB 차, error-floor도 낮음.
10. 한계: HW 미구현(복잡도 정성 비교만), CV-QKD 초저rate 전용, gatecount/throughput 미제시.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| log-log 도메인 SPA CN update | decoder.cpp `CNU_Update_New_Mag()` | 낮음: Prime은 min-sum, 논문은 SPA 계열 CN 근사라 알고리즘 상이 |
| VN log-sum/diff-exp 양자화 | decoder.cpp `VN_Cal_HD()` 등 | 낮음: soft-4bit+ 고정밀 log 도메인, NAND 2/3SD와 불일치 |
| CN tanh 스케일링 통찰 | decoder.cpp `CNU_Update_New_Mag()` | 낮음: scaled min-sum 계수 튜닝에 이론적 참고 정도 |
| MET/protograph 부호구조 | ecc_top.cpp `Load_PCM()` | 낮음: Prime은 고정 고rate QC-LDPC |

적용 가치: **낮음** — CV-QKD ultra-low-rate SPA의 메모리 비트폭 절감 기법으로, 고rate binary QC-LDPC min-sum HW인 Prime ECC와 부호·알고리즘·양자화 방식이 모두 달라 이식 여지가 미미하다.

### D. JSON 블록

```json
{
  "id": "arxiv:2401.13748v1",
  "title": "Log-Log Domain Sum-Product Algorithm for Information Reconciliation in Continuous-Variable Quantum Key Distribution",
  "year": 2024,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "protograph",
  "code_rate": null,
  "code_length": "128000~998400",
  "soft_quant": "soft-4bit+",
  "key_contribution": "log-LLR(log-log) 도메인 SPA로 CN 메시지의 소수부 비트폭 25%+ 절감",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "동등",
  "recommend": "하",
  "caveat": "ultra-low-rate BI-AWGN(CV-QKD) 전용 SPA·비트폭 절감이라 고rate NAND min-sum엔 부적합",
  "todo_check": "CN 근사식(6)의 tanh 스케일링 통찰이 min-sum scaling factor 튜닝에 참고될 여지만 확인"
}
```
