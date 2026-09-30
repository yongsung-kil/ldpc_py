### arxiv:2510.14060v2 - Decoding Correlated Errors in Quantum LDPC Codes (2026, arXiv/quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | correlated detector error model에서 Y타입 4-cycle을 제거하는 graph 증강·재배선(GARI) + hybrid serial-layered NMS + 랜덤스케줄 24-앙상블, FPGA 실시간 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | 양자 QEC(BB코드, circuit-level noise, X/Y/Z 상관 detector error model) 전용 - GARI는 Y타입 4-cycle 제거용이라 binary NAND LDPC엔 대응 개념 없음 |
| 추가확인 | 재사용 가능 요소는 NMS scaling·serial/layered 랜덤 스케줄·12bit 양자화·앙상블 원리로 한정 (부호·그래프 변환은 이식 불가) |

> 총평: 양자 BB코드 상관오류 전용 GARI 그래프변환이 핵심이라 부호 자체는 무관하나, NMS scaling·randomized serial/layered 스케줄·12bit 양자화·랜덤스케줄 앙상블·FPGA 저지연 설계는 고전 binary LDPC 디코더에도 참고 가치 있어 이식성 중.

### B. 알고리즘 요약

1. 대상은 양자 BB(bivariate bicycle) LDPC 코드(`[[72,12,6]]`,`[[90,8,10]]`,`[[144,12,12]]`)의 circuit-level noise 하 correlated detector error model 복호.
2. 문제: 양자 부호는 girth `Θ(1)`(특히 4-cycle)로 MP 디코더가 정확한 추론을 못 하고, 특히 X/Y/Z Pauli 상관(`D_XYZ`)에서 Y타입이 만드는 4-cycle이 성능 저하·early error-floor 유발.
3. 핵심 기법(GARI): decoding matrix의 biclique(모두 1인 부분행렬)에 변수변환 `e¯Z=eZ+U eY`, `e¯X=eX+V eY`을 적용, 새 error/check 노드를 추가해 Y타입 통과 4-cycle을 제거하되 복호문제 등가성 유지.
4. 핵심 성질: 변환 후 `D_XYZ` bottom part는 4-cycle 0개·평균 check degree 감소(예: d=12에서 4-cycle `11.58M`->하부 `0`), non-zero 엔트리도 절반 이하로 감소해 MP 부하 감소.
5. MP 디코더: normalized min-sum(NMS), scaling factor를 `0.96875`(=Σ1/2^i, i=1..5) 또는 `0.9921875`로 두어 bit-shift+adder로 HW 구현, 메시지 12bit 양자화.
6. 스케줄: hybrid serial-layered(horizontal) - 상부 DX/DZ는 randomized serial(병렬 2디코더), 하부는 U/V 2-layer, 정보교환으로 X/Y/Z 상관 반영.
7. 조기종료: logical-Z 보호 시 `DZ e¯X = sZ`만 검사(최대 400 iter), 앙상블은 한 디코더 수렴 즉시 전체 정지(latency 최소화).
8. 앙상블: serial 스케줄 randomization seed가 다른 24개(또는 48개) NMS를 병렬 실행, 동시수렴 시 prior 기반 최우도해 선택.
9. 결과: d=12에서 `p=1e-3`일 때 per-round LER `(6.70±1.93)×10^-9`(BPOSD 대비 ~20배↑, XYZ-Relay-BP-5와 동등), FPGA(VU19P, 16nm) 평균 per-round latency `273 ns`, 99.99%가 sub-µs, iter당 `2.9µs`(357MHz, 10-stage pipeline).
10. 한계: MP 디코더는 대거리에서 error-floor 가능성, 부호는 순수 양자 QEC(BB)라 상관오류 구조·GARI 변환이 binary 단일채널 LDPC엔 그대로 대응 안 됨.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| normalized min-sum(NMS) scaling factor | `decoder.cpp` `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | Prime ECC의 min-sum(min1/min2) CN 연산에 normalization scaling 참고 가능(우리 코드 scaling 미확인) |
| randomized serial/layered 스케줄 | `decoder.cpp` `LDPC_Decoder()` 이터레이션 루프 | Dual-Update(even/odd 교대) 스케줄과 유사 계열, 랜덤 스케줄 아이디어 참고 |
| 조기종료(syndrome 검사) | `partial_CRC.cpp` `partial_crc_HW_T4()`, `full_CRC.cpp` | 개념적 대응(우리는 CRC 기반), 논문은 syndrome 만족 검사 |
| 12bit 메시지 양자화 / VNU | `decoder.cpp` `VN_Cal_HD()` 등, `ecc_data.h` `PARAM_LLR` | magnitude 양자화 테이블과 대응, 저bit 양자화 설계 참고 |
| HW 병렬화/pipeline/라우팅 | 디코더 HW 모델(z=32, HCU, GT) | serial vs layered 라우팅·pipeline·resource sharing 논의 참고 |
| GARI graph 증강·재배선 (biclique/4-cycle 제거) | 대응 없음 | Y타입 상관 detector error model 전용이라 binary 단일채널 QC-LDPC에 대응 개념 없음 |
| BB 양자 부호구조 | 대응 없음 (양자 CSS 부호) | `PCM_b`(binary QC-LDPC)와 부호 클래스 상이 |

적용 가치: **중간** — 부호 자체(BB 양자)와 핵심 GARI 변환은 binary NAND LDPC와 무관하나, NMS normalization·randomized serial/layered 스케줄·12bit 양자화·랜덤스케줄 앙상블·FPGA 저지연/pipeline 설계 노하우는 고전 binary QC-LDPC 디코더 HW에 참고 가치가 있음.

### D. JSON 블록

```json
{
  "id": "arxiv:2510.14060v2",
  "title": "Decoding Correlated Errors in Quantum LDPC Codes",
  "year": 2026,
  "venue": "arXiv/quant-ph",
  "portability": "중",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": null,
  "soft_quant": "무관",
  "key_contribution": "correlated detector error model에서 Y타입 4-cycle을 제거하는 graph 증강·재배선(GARI) + hybrid serial-layered NMS + 랜덤스케줄 24-앙상블, FPGA 실시간",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "중",
  "caveat": "양자 QEC(BB코드, circuit-level noise, X/Y/Z 상관 detector error model) 전용 - GARI는 Y타입 4-cycle 제거용이라 binary NAND LDPC엔 대응 개념 없음",
  "todo_check": "재사용 가능 요소는 NMS scaling·serial/layered 랜덤 스케줄·12bit 양자화·앙상블 원리로 한정 (부호·그래프 변환은 이식 불가)"
}
```
