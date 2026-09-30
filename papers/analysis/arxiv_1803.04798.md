### arxiv:1803.04798v1 - A Branch-Price-and-Cut Algorithm for Optimal Decoding of LDPC Codes (2018, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5 |
| 부호length | 300~8400 |
| 연판정 | hard-1bit |
| 핵심기여 | ML 복호를 정수계획(IPM)으로 보고 branch-price-and-cut(RS 휴리스틱+valid cut)으로 최적 복호 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 없음 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | N/A |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | BSC(hard-decision) 전용·복호시간 수백초(600s time limit), 고오류율 소형코드 정확도 실험, HW/실시간 부적합 |
| 추가확인 | soft-input(AWGN/LLR) 확장 가능성, NAND급 고rate·긴 부호에서 시간 내 최적성 달성 여부 |

> 총평: LDPC ML 복호를 IP로 최적화하는 운용과학(BPC) 접근으로 복호 품질은 높으나 BSC·hard-decision·초 단위 복호라 실시간 NAND HW 디코더로는 이식성 하.

### B. 알고리즘 요약

1. 시스템: BSC(오류확률 `p`)로 전송되는 (J,K)-regular LDPC(예 (5,10)-regular, rate≈0.5), 수신벡터 `r`을 최근접 codeword로 복호하는 ML 문제.
2. 문제: ML 복호는 NP-hard, 반복 message-passing(Gallager A/SP)은 고오류율·cycle 존재 시 최적성 보장 못하고 복호 실패 가능.
3. 모델링: ML 복호를 정수계획으로 정식화 - Hamming 거리 목적(EM)과 log-likelihood 목적(IPM)이 `p<0.5`에서 등가임을 증명(Prop.1).
4. IPM은 각 check node의 feasible local codeword `S∈εj`(짝수 부분집합) 선택변수 `wjS`로 표현, LP완화(LPM)가 LEM보다 강한 하한 제공(Prop.2-3).
5. 핵심기법: branch-and-price - column generation으로 reduced cost `>0`인 `wjS` 열만 생성, subproblem을 `O(n log n)` 정렬 알고리즘(Alg.1/2)으로 최적해.
6. 분기: `fi` 정수성과 `wjS` 정수성이 동치(Prop.4)임을 보여 `fi`에 분기(subproblem 구조 불변).
7. 실현불능 복구: 열 부족으로 branch가 잘못 prune되는 문제를 Farkas pricing(dual ray로 direction subproblem)으로 해결(Prop.5).
8. 개선: Random Sum 휴리스틱(G 행 무작위합, `tmax=10000`)으로 tight upper bound, valid cut(25)로 fractional 해 분리 → BPRS/BPC.
9. 결과: BPC가 CPLEX 기반 EMD보다 gap/BER/#Opt 우수, 240 인스턴스 중 161개 최적. Gallager A는 고오류율에서 대부분 실현불능(BER>0), BPC는 전 사례 원 codeword 복원(BER=0).
10. 한계: BSC hard-decision 전용, 복호시간 수백초(600s 제한 자주 도달), 소형코드(n≤8400) 실험, HW 미설계·실시간 부적합(심우주통신 등 지연 무관 용도 지향).

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| ML 복호(IPM) branch-price-and-cut | decoder.cpp LDPC_Decoder() | 복호 대상은 같으나 min-sum 반복복호를 IP 최적화로 대체, 초 단위 복호라 HW 이식 불가 |
| valid cut / column generation | 대응 없음 | 운용과학(정수계획) 기법, min-sum HW 파이프라인과 무관 |
| Gallager A 비교 baseline | decoder.cpp CNU_Update_New_Mag() 등 | Prime ECC의 min-sum이 이미 우월한 실무 복호기, hard-flip Gallager A는 참고용 |
| BSC hard-decision 입력 | channel.cpp (HD 경로) | Prime ECC는 hard-1bit 지원하나 soft(2SD/3SD)가 주력, BSC 전용은 제한적 |
```

적용 가치: **낮음** — LDPC ML 복호의 최적성 상한(성능 기준선)으로는 참고 가치가 있으나, 초 단위 정수계획 복호라 Prime ECC의 클록레벨 min-sum HW 디코더에 떼어 쓸 수 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1803.04798v1",
  "title": "A Branch-Price-and-Cut Algorithm for Optimal Decoding of LDPC Codes",
  "year": 2018,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.5,
  "code_length": "300~8400",
  "soft_quant": "hard-1bit",
  "key_contribution": "ML 복호를 정수계획(IPM)으로 보고 branch-price-and-cut(RS 휴리스틱+valid cut)으로 최적 복호",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "없음",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "N/A",
  "latency": "악화",
  "recommend": "하",
  "caveat": "BSC(hard-decision) 전용·복호시간 수백초(600s time limit), 고오류율 소형코드 정확도 실험, HW/실시간 부적합",
  "todo_check": "soft-input(AWGN/LLR) 확장 가능성, NAND급 고rate·긴 부호에서 시간 내 최적성 달성 여부"
}
```
