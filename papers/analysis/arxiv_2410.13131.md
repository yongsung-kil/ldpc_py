### arxiv:2410.13131v1 - Study of Weighted Residual Layered Belief Propagation for Decoding of LDPC Codes (2024, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5 |
| 부호length | 512 |
| 연판정 | 무관 |
| 핵심기여 | LBP에 잔차(residual) 기반 가중치를 결합한 WR-LBP 동적 스케줄링으로 반복 수 절감 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 없음 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | 부분 |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | HW 미설계·시뮬만, 초기 15 iteration 수렴은 오히려 느림, 복잡도표 정성적 |
| 추가확인 | RBP류 동적 스케줄이 z=32 row-병렬 파이프라인/HCU 구조와 상충하지 않는지 |

> 총평: LBP+잔차 가중 스케줄로 저반복 waterfall 성능을 노리는 순수 알고리즘 논문. 아이디어는 이식 가능하나 동적 edge선택이 우리 병렬 HW구조와 정합 부담이 있다.

### B. 알고리즘 요약 (10줄 내외)

1. 시스템: AWGN+BPSK, regular LDPC `k=256, n=512, R=1/2`, 5000 프레임, 3/5 iteration 제한.
2. 문제: IDS(RBP류) 동적 스케줄은 저반복에서 flooding BP보다 우수하나 계산량·greediness가 크다.
3. 모델: 표준 SPA(sum-product) 메시지 `µ_ci→vj`, `µ_vj→ci`, 잔차 `r(µ)=µ^(k)−µ^(k-1)` (식 13).
4. 기법1 - LBP(Layered BP): 행(row)을 레이어로 묶어 인접 레이어 간 순차 메시지 교환.
5. 기법2 - WR-LBP: 잔차에 레이어 가중치 `α(ML)`를 곱해 `r_WR-LBP = α(ML)·µ^(k) − µ^(k-1)` (식 16)로 다음 갱신 edge 선택.
6. 레이어 배정: `ML = max(L(µ), l)` (식 14), `l=0.9`를 실험적으로 채택; sign 함수로 레이어 결정(식 15).
7. 가중치: layer weight `w = 1/2^(l-ML+1)`로 회복 가능성(level of recoverability) 높은 노드 우선.
8. 학습/최적화: `l=0.9`는 empirical simulation로만 결정, NN·DE 등 별도 학습 없음.
9. 결과: Fig.4(5 iter, 3.5dB)에서 최근접 경쟁자 RD RBP 0.9 대비 약 0.001164 BER gain (단, 본문 BER 표기값 일부 혼란).
10. 한계: HW 미설계, 시뮬만, 초기 15 iteration에선 수렴이 오히려 느림.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| WR-LBP 이터레이션 루프/스케줄 | decoder.cpp `LDPC_Decoder()`, `C2V_Cal()` | 잔차 기반 동적 edge 선택을 우리 이터레이션 루프에 삽입 시도 대상 |
| 잔차 계산(C2V) | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | C2V magnitude/sign 갱신 결과로 잔차 계산 필요 |
| 레이어(row) 스케줄링 | decoder.cpp `LDPC_Decoder()` 스케줄 (Dual-Update 대체 후보) | row 단위 z=32 병렬과 레이어 개념이 부분 대응하나 동적선택은 상충 |

적용 가치: **중간** - 저반복 waterfall 개선 아이디어는 관심영역이나, 잔차 기반 축차적 edge 선택이 z=32 행-병렬/파이프라인 HW와 정합이 어렵고 HW 미검증이다.

### D. JSON 블록 (DB 적재용)

```json
{
  "id": "arxiv:2410.13131v1",
  "title": "Study of Weighted Residual Layered Belief Propagation for Decoding of LDPC Codes",
  "year": 2024,
  "venue": "arXiv cs.IT",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.5,
  "code_length": "512",
  "soft_quant": "무관",
  "key_contribution": "LBP에 잔차 기반 레이어 가중치를 결합한 WR-LBP 동적 스케줄링으로 반복 수 절감",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "없음",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "부분",
  "latency": "개선",
  "recommend": "중",
  "caveat": "HW 미설계·시뮬만, 초기 15 iteration 수렴은 느림, 복잡도표 정성적",
  "todo_check": "RBP류 동적 스케줄이 z=32 행-병렬 파이프라인/HCU 구조와 정합 가능한지"
}
```
