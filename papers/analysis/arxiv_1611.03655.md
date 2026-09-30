### arxiv:1611.03655v1 - Improving Belief Propagation Decoding of Polar Codes Using Scattered EXIT Charts (2016, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 미상 |
| 부호length | 155~190 |
| 연판정 | soft-4bit+ |
| 핵심기여 | scattered EXIT chart(2D 히스토그램)로 polar/VND 거동을 추정해 polar BP에 붙는 짧은 auxiliary LDPC의 check-irregular degree profile을 최적화 |
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
| 추천도 | 하 |
| 한계,주의 | LDPC가 polar BP에 종속된 보조부호(semi-polarized 채널 보호)라 독립 NAND LDPC와 무관, 부호 rate 명시 없음 |
| 추가확인 | scattered EXIT의 degree-profile 최적화 아이디어가 독립 QC-LDPC 설계로 분리 적용 가능한지 |

> 총평: polar+LDPC concatenation에서 짧은 auxiliary LDPC의 check node degree profile을 scattered EXIT chart로 설계하는 논문. LDPC가 polar BP에 결합된 보조부호이고 무선/이론 세팅이라 NAND 독립 QC-LDPC ECC 이식 가치는 낮음.

### B. 알고리즘 요약

1. 시스템: polar code(N=4096, 전체 rate 1/2)에 짧은 auxiliary LDPC(N_LDPC=155~190)를 concatenation해 semi-polarized 채널을 보호. AWGN.
2. 문제: finite-length polar code는 SC/SCL 대비 BP 복호 성능이 떨어짐. BP는 병렬화 유리하나 성능 미흡 → SCL의 CRC처럼 BP에 맞는 보조부호 필요.
3. 핵심 가정: Bhattacharyya parameter로 채널을 good/semi-polarized/bad로 3분할, 중간(semi-polarized) 채널에만 LDPC 보호를 적용([11] 기반).
4. 핵심 기법: LDPC BP와 polar BP를 교대 iteration으로 결합(폴라 stage1 LLR을 LDPC로 전달, LDPC extrinsic을 R-message로 피드백). polar PE는 min-sum 근사 box-plus `g()`.
5. 핵심 식: scattered EXIT chart — 실제 반복복호 trajectory들의 발생빈도를 EXIT mutual-info 평면 2D 히스토그램으로 누적, 잡음 속 평균적 polar/VND 거동을 추출.
6. 확장/설계: 추출된 polar/VND-curve에 맞춰 CND(check node) degree profile을 매칭. tunnel을 닫되 고BER 교차를 피하려 check-irregular 사용.
7. 구현 디테일: 최종 설계는 (dv=3, dc=10.72) check-irregular(dc 4/5/17을 0.3322/0.1628/0.505 비율)로 155bit LDPC.
8. 최적화: EXIT chart를 가이드로 dc profile 반복 조정, N_LDPC를 155→190으로 늘려 추가 이득.
9. 결과: conventional BP 대비 net coding gain 0.4dB(BER 1e-5), [11] 대비 0.2dB 개선.
10. 한계: HW 미설계, 시뮬만. LDPC는 polar에 종속된 짧은 보조부호이고 부호 rate 명시 없음, polar/VND-curve는 해석적 예측 불가.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| polar BP 디코더 / polar+LDPC concatenation | 대응 없음 | Prime ECC는 순수 binary QC-LDPC, polar 부호 미지원 |
| auxiliary LDPC degree profile 설계(scattered EXIT) | ecc_top.cpp `Load_PCM()` | 부호구성 결과 로드는 가능하나 polar 종속 설계라 직접 이식 불가 |
| box-plus / min-sum g() 근사 | decoder.cpp `CNU_Update_New_Mag()` | min-sum 근사 자체는 이미 보유(중복) |

마지막에 한 문장으로 **적용 가치**: 낮음 — 핵심이 polar code BP 개선을 위한 종속 auxiliary LDPC 설계이고, Prime ECC의 독립 NAND binary QC-LDPC와 부호 구조·복호 아키텍처가 달라 이식 가치가 낮다.

### D. JSON 블록

```json
{
  "id": "arxiv:1611.03655v1",
  "title": "Improving Belief Propagation Decoding of Polar Codes Using Scattered EXIT Charts",
  "year": 2016,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": "미상",
  "code_length": "155~190",
  "soft_quant": "soft-4bit+",
  "key_contribution": "scattered EXIT chart(2D 히스토그램)로 polar/VND 거동을 추정해 polar BP에 붙는 짧은 auxiliary LDPC의 check-irregular degree profile을 최적화",
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
  "recommend": "하",
  "caveat": "LDPC가 polar BP에 종속된 보조부호(semi-polarized 채널 보호)라 독립 NAND LDPC와 무관, 부호 rate 명시 없음",
  "todo_check": "scattered EXIT의 degree-profile 최적화 아이디어가 독립 QC-LDPC 설계로 분리 적용 가능한지"
}
```
