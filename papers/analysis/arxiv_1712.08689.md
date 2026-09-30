### arxiv:1712.08689v1 - Study of Iterative Detection and Decoding for Large-Scale MIMO Systems with 1-Bit ADCs (2017, arXiv/cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5 |
| 부호length | 512 |
| 연판정 | soft-4bit+ |
| 핵심기여 | box-plus SPA 복호기에 quasi-uniform quantizer+오프라인/온라인 scaling factor로 error floor 완화 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 1-bit ADC MIMO IDD 문맥 특화, box-plus SPA 기반이라 Prime의 min-sum과 계열 상이·LLR scaling은 채널추정 통계 의존 |
| 추가확인 | NAND soft-read LLR에서 quasi-uniform quantizer(d,∆,N)와 scaling factor의 error-floor 이득 재현 여부 |

> 총평: LDPC 기여는 error-floor용 quasi-uniform LLR 양자화+scaling뿐이며 1-bit ADC MIMO/box-plus SPA 문맥에 묶여 NAND QC-LDPC 이식성 낮음.

### B. 알고리즘 요약

1. 대상 시스템은 uplink large-scale MIMO(`K` 유저, `M≫K` 안테나), 1-bit ADC front-end, QPSK, block-length 512·rate 1/2 regular LDPC, block-fading 채널.
2. 문제: 1-bit 양자화가 수신 SNR을 크게 훼손하고, 짧은 regular LDPC는 trapping/absorbing set으로 error floor가 높음.
3. 모델: 1-bit 양자화 `yQ=Q(R{y})+jQ(I{y})`, Bussgang 정리로 `C_sQs=√(2/π)K C_s`, `C_sQ` 를 `sin^-1` 로 유도.
4. 핵심 기법1(검출): LRA-MMSE 필터 `w_k=C_yQk^-1 c_xk yQk` 로 soft parallel interference cancellation, 디코더 extrinsic LLR `Le_k` 로 심볼 soft estimate 갱신.
5. 필터 출력을 Cramer CLT로 복소 가우시안 근사해 likelihood `P(x̂_k|x)` 및 bit LLR `Lc_k` 산출(검출↔복호 IDD 반복).
6. 핵심 기법2(복호): box-plus SPA(식 20, `x⊞y`) 사용 — tanh 포화 회피용 magnitude threshold 적용.
7. 부수 트릭: quasi-uniform quantizer `Q∆*(Lc_k)` (성장률 `d`, step `∆`, 비트수 `N`)로 saturation level 확장해 메시지 trapping 방지 및 1-bit 데이터 보정.
8. 최적화: 오프라인 scaling `α_k`(LLR 히스토그램 `f(Lc_k)=α_k Lc_k`, 1차 iter만)와 온라인 scaling `f_k=α_k L̄c_k / L̄c_k^{2nd}` (2차 iter부터) 로 양자화 LLR 오차 보정.
9. 결과: LRA-MMSE가 traditional MMSE 대비 큰 BER 이득, 2 iteration 후 유의한 향상, quantizer+scaling factor가 추가 이득(파라미터 ∆=0.25, d=1.3, N=6).
10. 한계: HW 미설계·시뮬만, gate/throughput/latency 수치 없음, LDPC 기여가 IDD·1-bit ADC 문맥에 종속.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| box-plus SPA CN 연산 | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | Prime은 min-sum(min1/min2), box-plus SPA와 계열 달라 직접 대응 약함 |
| quasi-uniform quantizer / LLR 양자화 | decoder.cpp `VN_Cal_HD()`, ecc_data.h `PARAM_LLR` | LLR 양자화 테이블 개념은 대응하나 magnitude 양자화 방식이 다름 |
| iteration별 LLR scaling factor | ecc_data.h `PARAM_LLR`, decoder.cpp `Get_VNU_Table_Idx()` | 적응형 LLR threshold 테이블과 유사하나 scaling은 채널추정 통계 의존 |

적용 가치: **낮음** — error-floor용 LLR 양자화/scaling 아이디어는 참고 가능하나 1-bit ADC MIMO·box-plus SPA에 묶여 있고 Prime의 min-sum HW·NAND soft-read와 정합 부담이 크다.

### D. JSON 블록

```json
{
  "id": "arxiv:1712.08689v1",
  "title": "Study of Iterative Detection and Decoding for Large-Scale MIMO Systems with 1-Bit ADCs",
  "year": 2017,
  "venue": "arXiv/cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.5,
  "code_length": "512",
  "soft_quant": "soft-4bit+",
  "key_contribution": "box-plus SPA 복호기에 quasi-uniform quantizer+오프라인/온라인 scaling factor로 error floor 완화",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "1-bit ADC MIMO IDD 문맥 특화, box-plus SPA 기반이라 Prime의 min-sum과 계열 상이·LLR scaling은 채널추정 통계 의존",
  "todo_check": "NAND soft-read LLR에서 quasi-uniform quantizer(d,∆,N)와 scaling factor의 error-floor 이득 재현 여부"
}
```
