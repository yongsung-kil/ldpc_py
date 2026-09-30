### arxiv:1108.5547v2 - Instantons causing iterative decoding to cycle (2020, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | regular |
| 부호rate | 0.41 |
| 부호length | 155 |
| 연판정 | 무관 |
| 핵심기여 | min-sum 반복복호를 순환(cycle)시키는 최저가중 instanton을 large-niter까지 탐색하는 2가지 방법 제시 |
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
| 한계,주의 | 순수 error-floor 진단(analysis) 도구일 뿐 디코더/부호 개선 기법이 아님; 특정 [155,64,20] 코드·AWGN 한정 |
| 추가확인 | instanton 정보로 부호/디코더를 실제 개선하는 후속 절차는 본 논문 범위 밖 (미제시) |

> 총평: min-sum 반복복호가 수렴하지 않고 순환하는 채널잡음(instanton)을 대규모 iteration까지 찾는 이론적 진단 기법으로, NAND binary QC-LDPC 이식 대상이 없다.

### B. 알고리즘 요약

1. 대상: Tanner의 `[155, 64, 20]` 그룹구조 LDPC 코드(155×93 순환블록 PCM)와 AWGN 채널, min-sum 반복복호.
2. 문제: 고SNR error-floor를 지배하는 "instanton"(가장 확률 높은 오류유발 잡음)을 large `niter`에서 찾기 어렵다(기존 instanton-amoeba는 ~10 iteration이 한계).
3. 모델: 잡음 `ξ_i = 1 - σ_i x_i`, instanton = 오류유발 집합 `E`의 확률밀도 `P(ξ)` 국소최대점. min-sum은 scalable하여 `E`가 SNR 무관.
4. 핵심기법1(AWGN용): 디코딩 출력 `m_i^(k) = n_i^(k)·h`의 정수계수 벡터 "colored structure" `n_i^(k)`를 수정 min-sum으로 추출.
5. 식 의미: `F_i(ξ)=½Σξ_j² + λ Σ(1-ξ_j)n_i^(niter)`을 최소화 → `ξ=λn_i`, 중심비트 출력이 완전 미결정이 되는 최소 L2노름 잡음.
6. 확장: 여러 colored structure가 경합할 때 `A_cd λ_d = B_c`(식1) 선형계로 Wiberg 공식을 모호(ambiguous)한 경우로 일반화.
7. 구현: L2에서 `t` 이분탐색으로 `ξ` 신중 갱신(Fig.2/3), QR분해로 종속 colored structure 제거.
8. 핵심기법2(instanton array): `ξ(k)`(각 k iteration을 견디는 최저가중 잡음) 배열을 유지, 잡음 섭동 `ξ→cξ+aψ`와 음성피드백 진폭 `a`로 large-niter instanton 탐색.
9. 결과: `niter;max=100`에서 가중 `w(ξA)<11.475333`, 주기 12로 순환하는 inherently dynamic instanton 발견(LP 디코딩의 16.4보다 훨씬 낮음).
10. 한계: 순수 이론·진단; HW·시뮬 성능곡선·부호개선 없음, 코드/채널 특정.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| min-sum 반복복호(진단 대상) | decoder.cpp `LDPC_Decoder()` | 대상 알고리즘은 동일 계열이나 논문은 복호 자체를 개선하지 않음 |
| instanton/error-floor 진단 절차 | 대응 없음 | Prime ECC에 error-floor instanton 탐색 모듈 없음, 오프라인 분석용 |
| colored structure 최적화(QR/Lagrange) | 대응 없음 | 복호기 외부 수치최적화, 코드베이스 대응 모듈 없음 |

적용 가치: 낮음 — error-floor 원인 진단 아이디어는 학술적으로 유용하나, NAND binary QC-LDPC의 부호설계·디코더·HW에 떼어 이식할 기법이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1108.5547v2",
  "title": "Instantons causing iterative decoding to cycle",
  "year": 2020,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "regular",
  "code_rate": 0.41,
  "code_length": "155",
  "soft_quant": "무관",
  "key_contribution": "min-sum 반복복호를 순환시키는 최저가중 instanton을 large-niter까지 탐색하는 2가지 방법 제시",
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
  "caveat": "순수 error-floor 진단 도구일 뿐 디코더/부호 개선 기법이 아님; 특정 [155,64,20] 코드·AWGN 한정",
  "todo_check": "instanton 정보로 부호/디코더를 실제 개선하는 후속 절차는 본 논문 범위 밖"
}
```
