### arxiv:1508.06823v1 - Framework for Application Mapping over Packet-switched Network of FPGAs: Case studies (2015, FSP 2015 (2nd Int'l Workshop on FPGAs for Software Programmers))

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 미상 |
| 핵심기여 | LDPC min-sum 디코더를 3가지 케이스 스터디 중 하나로 삼아 메시지 패싱 알고리즘을 NoC 기반 멀티-FPGA로 자동 스케일링하는 프레임워크 제안 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | LDPC는 finite projective geometry 부호(N=7, s=1) 소규모 예시일 뿐이며 부호설계/디코더 알고리즘 개선이 아니라 NoC 매핑 프레임워크가 논문의 핵심 |
| 추가확인 | 실제 대상 부호(rate/length)가 명시되지 않아 NAND ECC급 QC-LDPC와 무관함을 재확인 필요 |

> 총평: LDPC min-sum 디코더는 멀티-FPGA NoC 자동화 프레임워크를 시연하는 예시 애플리케이션일 뿐이며, 부호설계·디코더 알고리즘·HW 아키텍처 개선과는 무관해 Prime ECC 이식 가치가 낮음.

### B. 알고리즘 요약 (10줄 내외)

1. 논문은 데이터플로우 성격의 애플리케이션(알고리즘)을 메시지 패싱 모델로 표현해 단일 FPGA의 packet-switched NoC에 매핑하고, 이를 다시 여러 FPGA로 무봉합 파티셔닝하는 반자동 프레임워크를 제안한다.
2. 해결하려는 문제는 상용 HLS 툴이 좋은 품질의 HW를 만들지만 애플리케이션이 스케일업(멀티 FPGA)될 때의 확장성을 다루지 못한다는 것이다.
3. Phase-1에서 도메인 전문가가 알고리즘을 메시지 패싱 형태로 표현하면, 처리 요소(Processing Element, PE)를 손수 설계하거나 HLS(Vivado)로 합성한다.
4. Phase-2는 CONNECT NoC 생성기로 PE들을 네트워크에 자동 연결하고, FPGA 경계를 가로지르는 NoC 링크를 quasi-SERDES(GPIO 기반 직렬화) 링크로 자동 치환해 멀티-FPGA 파티셔닝을 수행한다.
5. LDPC 케이스 스터디는 finite projective geometry 기반 LDPC 부호(Kou-Lin-Fossorier, GF(2, 2^s), s=1)의 min-sum 디코딩을 예시로 사용하며, Check node(`v = min(u_i)`)와 Bit node(`sum = u0+Σv_i`, `u_i = sum - v_i`) 처리를 각각 별도 PE로 구현한다.
6. N=7인 소규모 부호에 대해 bit node·check node 각 7개를 4×4 mesh CONNECT NoC로 연결해 시연했다(Fig.9).
7. 다른 두 케이스 스터디(Particle Filter 객체 추적, GF(2) 상 sub-quadratic 행렬-벡터 곱)와 동일한 Data Collector/Data Processing/Data Distributor 3모듈 wrapper 구조를 재사용해 PE를 NoC-aware하게 만든다.
8. LDPC 사례는 학습/최적화 절차 없음 - 단순 wrapper 자동 생성 스크립트만 적용.
9. 결과는 wrapper 유무에 따른 리소스 사용량 비교(Table I, II)뿐이며 BER/iteration/처리량 등 디코더 성능 지표는 보고되지 않는다.
10. 한계: LDPC 자체의 정정능력·error-floor·복잡도 개선이 목적이 아니고, N=7의 매우 작은 부호로 개념검증만 수행했으며 throughput/gatecount 등 실질적 HW 지표는 제시되지 않는다.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| min-sum check/bit node 처리 | `decoder.cpp` `LDPC_Decoder()`, `CNU_Update_New_Mag()` | 개념적으로 표준 min-sum과 동일하나 HW/알고리즘 개선 없음 |
| NoC 기반 멀티-FPGA 스케일링 | 대응 없음 | Prime ECC는 단일 코드베이스 시뮬레이터로 멀티칩 NoC 개념 없음 |
| Data Collector/Distributor wrapper 자동화 | 대응 없음 | 시스템 레벨 통합 도구로 ECC 코어 로직과 무관 |
```

> 적용 가치: **낮음** - LDPC는 프레임워크 시연용 예시일 뿐이며 부호설계·디코더 알고리즘·HW 최적화 기여가 없어 Prime ECC 3.1에 이식할 요소가 없음.

### D. JSON 블록 (DB 적재용)

```json
{
  "id": "arxiv:1508.06823v1",
  "title": "Framework for Application Mapping over Packet-switched Network of FPGAs: Case studies",
  "year": 2015,
  "venue": "FSP 2015 (2nd Int'l Workshop on FPGAs for Software Programmers)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "미상",
  "key_contribution": "LDPC min-sum 디코더를 3가지 케이스 스터디 중 하나로 삼아 메시지 패싱 알고리즘을 NoC 기반 멀티-FPGA로 자동 스케일링하는 프레임워크 제안",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "LDPC는 finite projective geometry 부호(N=7, s=1) 소규모 예시일 뿐이며 부호설계/디코더 알고리즘 개선이 아니라 NoC 매핑 프레임워크가 논문의 핵심",
  "todo_check": "실제 대상 부호(rate/length)가 명시되지 않아 NAND ECC급 QC-LDPC와 무관함을 재확인 필요"
}
```
