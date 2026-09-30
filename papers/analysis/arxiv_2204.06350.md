### arxiv:2204.06350v2 - Low-density parity-check codes: comparing cluster graph to factor graph representations (2023, IEEE Communications Letters(추정)/arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 220 |
| 연판정 | 무관 |
| 핵심기여 | LDPC를 factor graph 대신 cluster graph(LTRIP)로 표현+layered 스케줄로 BER·수렴반복 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | cluster/sepset joint-distribution 연산으로 복잡도 급증, HW 미설계·저자 스스로 향후과제로 명시 |
| 추가확인 | (16,8)·(220,110) 소규모 코드뿐, 고rate·긴 QC-LDPC로의 확장성 및 실제 연산비용 |

> 총평: BER 0.2dB·반복수 개선을 보이나 cluster graph joint-message 방식이 min-sum HW와 근본적으로 이질적이라 NAND ECC 이식성은 하.

### B. 알고리즘 요약

1. 시스템: BPSK/AWGN 채널, irregular LDPC를 예시로 (16,8) 및 결과용 (220,110) 코드 사용, 저rate 소규모.
2. 문제: factor graph(Tanner graph) 기반 LBP는 cycle로 인해 수렴·정확도 보장이 없음.
3. 핵심 아이디어: LDPC를 더 일반적인 PGM인 `cluster graph`로 표현 — cluster(변수 집합) + sepset(공유변수)이 joint distribution 메시지를 주고받아 상관관계를 보존.
4. 그래프 구성: `LTRIP`(layered trees running intersection property) 알고리즘으로 factor 집합에서 cluster graph를 자동 컴파일, RIP 만족.
5. junction tree 대비: junction tree는 대형코드에서 NP-complete·cluster scope 증가, cluster graph는 원 factor를 그대로 보존해 확장 가능.
6. 추론: `LBU`(loopy belief update, Lauritzen-Spiegelhalter)로 cluster/sepset belief 사용, SP·MP 두 방식 지원.
7. 스케줄(Alg.1): 큰 parity cluster를 source로 forward/backward layered sweep, 큰 cluster를 마지막 층에 격리해 연산량 최소화 + loop 영향 저감.
8. 구현트릭: symmetric KL divergence로 cluster 비활성화(조기중단), sparse table, zero-prob state 제거, MP시 미세 noise로 unique max 보장.
9. 결과: (220,110)에서 SP·MP 모두 cluster가 factor graph 대비 BER 10^-3 기준 0.2dB coding gain, 평균 반복수도 감소, error floor 없음.
10. 한계: HW 미구현(향후과제), 최적 message ordering 미해결, joint-distribution 연산으로 계산복잡도 큼.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| cluster graph 추론(LBU/SP/MP) | decoder.cpp `LDPC_Decoder()`, `C2V_Cal()` | 개념상 복호 루프에 대응하나 min-sum 기반과 이질적 |
| layered 메시지 스케줄 | decoder.cpp `LDPC_Decoder()` 이터레이션 루프 | 스케줄만 유사, cluster 구조 전제라 직접 이식 곤란 |
| joint-distribution/sepset belief | 대응 없음 | Prime ECC는 스칼라 LLR min-sum, joint table 미보유 |
| AWGN 채널 | channel.cpp `Set_R_Offset()` | 채널모델만 공통 |

적용 가치: **낮음** — cluster graph의 joint-distribution 메시지 방식은 Prime ECC의 스칼라 min-sum/HW 파이프라인과 근본적으로 달라, HW 미설계 상태에서 이식 시 연산·메모리 폭증이 불가피.

### D. JSON 블록

```json
{
  "id": "arxiv:2204.06350v2",
  "title": "Low-density parity-check codes: comparing cluster graph to factor graph representations",
  "year": 2023,
  "venue": "arXiv cs.IT (IEEE Comm. Letters 형식)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": "220",
  "soft_quant": "무관",
  "key_contribution": "LDPC를 cluster graph(LTRIP)로 표현+layered 스케줄로 BER·수렴반복 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "악화",
  "recommend": "하",
  "caveat": "cluster/sepset joint-distribution 연산으로 복잡도 급증, HW 미설계",
  "todo_check": "소규모 코드뿐, 고rate·긴 QC-LDPC 확장성 및 실제 연산비용 검증 필요"
}
```
