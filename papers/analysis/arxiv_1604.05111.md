### arxiv:1604.05111v1 - Finite-length scaling based on belief propagation for spatially coupled LDPC codes (2016, arXiv/ISIT-계열)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 0.5 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | PPD=BP 등가성 이용, 해소 VN 감소량을 DE로 저복잡도 계산해 SC-LDPC 유한길이 스케일링 법칙 유도 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | BEC 전용 유한길이 성능 예측 이론 — 실채널/양자화/HW/디코더 알고리즘 개선 전무 |
| 추가확인 | 없음 (NAND binary QC-LDPC와 채널·부호계열이 상이하여 이식 가치 없음) |

> 총평: BEC 상 SC-LDPC 부호의 유한길이 waterfall 성능을 OU 프로세스 스케일링 법칙으로 예측하는 순수 이론 논문으로, NAND high-rate binary QC-LDPC 디코더/HW 이식과는 무관.

### B. 알고리즘 요약

1. 대상은 BEC 상 (l,r,L) SC-LDPC 부호(랜덤·프로토그래프 구성), 예제 `(3,6,50)`,`(4,8,100)`, `M`=1000~4000 VN.
2. 문제: SC-LDPC의 유한길이 waterfall 성능 예측을 BP로 하고자 하나, 기존 peeling-decoding(PD) 기반 그래프진화 분석은 복잡도가 매우 큼.
3. 모델: BEC에서 지워진 VN들의 residual graph를 두고, 지워진 VN 수의 감소를 확률과정으로 추적.
4. 핵심기법: parallel peeling decoder(PPD) 정의 후 Theorem III.1로 "PPD와 BP가 매 iteration 동일한 VN을 해소"함을 증명(등가성).
5. 핵심식: deg-1 CN 수 `c1(τ)` 대신 iteration당 해소 VN 수 `L∆ε(τ)`를 대체지표로 도입, `L∆ε(τ) ≤ c1(τ-(ε*-ε))` 상계(Thm IV.1).
6. 복잡도 절감: `∆ε`는 BP density evolution(DE)로 계산 가능 → 그래프진화 대비 급감(예 CN type 104개·4500 iter → DE 18개·6 iter).
7. 통계모델: critical phase에서 `∆ε`의 평균·분산이 일정함을 보이고 이를 Ornstein-Uhlenbeck(OU) 정상 가우시안 마르코프 과정으로 모델링.
8. 스케일링: OU의 first-passage-time(0 도달) 분포를 지수근사해 블록오류확률 `Pb* ≈ 1-exp(-τeff/µ0)`로 유한길이 성능 예측.
9. 결과: `(3,6,100)`,`(4,8,100)`에서 예측 곡선이 SPD 기반 추정 및 시뮬레이션 slope와 거의 일치(단, `L∆ε` 사용 시 약간 overconfident).
10. 한계: BEC 전용 이론, 알고리즘/HW 미설계, soft-decision·양자화·error-floor 논의 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| PPD/BP 등가성, DE 유한길이 분석 | 대응 없음 | BEC peeling·SC-LDPC 이론, 우리 min-sum BP 디코더와 무관 |
| SC-LDPC 부호 구성/스케일링 법칙 | 대응 없음 | 우리는 고정 high-rate binary QC-LDPC, SC(convolutional) 구조 아님 |
| OU 기반 성능 예측 | 대응 없음 | 성능검증은 ecc_top.cpp 통계지만 이론 프레임 자체는 이식 불가 |

적용 가치: **낮음** — BEC 전용 유한길이 스케일링 이론으로 부호계열(SC-LDPC)·채널·HW 모두 우리 대상과 어긋나 이식 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1604.05111v1",
  "title": "Finite-length scaling based on belief propagation for spatially coupled LDPC codes",
  "year": 2016,
  "venue": "arXiv (cs.IT)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": 0.5,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "PPD=BP 등가성 이용, 해소 VN 감소량을 DE로 저복잡도 계산해 SC-LDPC 유한길이 스케일링 법칙 유도",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "BEC 전용 유한길이 성능 예측 이론 — 실채널/양자화/HW/디코더 알고리즘 개선 전무",
  "todo_check": "없음 (NAND binary QC-LDPC와 채널·부호계열이 상이하여 이식 가치 없음)"
}
```
