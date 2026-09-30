### arxiv:1004.3742v1 - Threshold Saturation on BMS Channels via Spatial Coupling (2010, arXiv/cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 0.4294~0.4882 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | spatial coupling으로 BP threshold가 MAP threshold까지 saturate됨을 일반 BMS 채널서 경험적으로 입증 |
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
| 한계,주의 | 점근적 ensemble 이론(유한길이·HW 없음), 완전한 증명 미완, rate loss 완화 시 iteration 증가 |
| 추가확인 | 유한길이·고rate NAND 부호에서 threshold saturation 이득이 실질적으로 남는지 |

> 총평: convolutional/SC-LDPC의 threshold saturation을 일반 BMS로 확장한 순수 점근이론 논문 - 개념적 기반이나 저rate(1/2)·유한길이·HW 부재로 NAND용 고rate binary QC-LDPC 이식성 하.

### B. 알고리즘 요약

1. 대상: spatially coupled LDPC ensemble `(l,r,L,w)`(=convolutional LDPC), 일반 BMS 채널(BAWGN 포함), (3,6)-regular 성분 ensemble 중심.
2. 문제: convolutional LDPC의 우수한 BP threshold가 왜 좋은지 - BEC에서 밝혀진 threshold saturation이 일반 BMS 채널서도 성립하는지 규명.
3. 모델: 변수노드를 위치 `[-L,L]`에 배치, 각 연결을 `[i,i+w-1]` 범위서 균일 선택(smoothing `w`); 경계노드는 완전정보 `Δ_{+∞}`.
4. 핵심기법: coupled ensemble의 density evolution FP를 파라미터 `x_i = c ⊛ g(x_{i-w+1},...,x_{i+w-1})`로 정의, EBP GEXIT 곡선을 FP 집합으로 수치 구성.
5. 핵심식: GEXIT 곡선을 `(1,1)`에서 좌측으로 적분해 면적이 code rate와 같아지는 지점이 MAP threshold 상한(Maxwell construction) - BP threshold가 이 값까지 상승함을 관찰.
6. 확장: forward DE가 admissible schedule과 무관한 유일 FP로 수렴함을 단조성(정리 Lemma 5)으로 증명, unimodal "special" FP의 빠른 transition 관찰(Fig.4).
7. 구현 디테일: 해당 없음(HW 무관, 순수 DE/GEXIT 수치계산).
8. 최적화(rate loss 완화): 경계를 일부만 known 설정, one-sided termination, circular ensemble `(l,r,K,w,κ)` 도입으로 boundary rate loss를 절반 수준까지 감소.
9. 결과: (3,6,L)서 L≳10부터 BP threshold(≈0.4792)가 (3,6) MAP threshold에 근접; BEC 곡선과 동일 거동; rate loss는 `2L+1`에 반비례 감소.
10. 한계: 일반 BMS에 대한 완전한 해석적 증명 미완, 점근 ensemble 이론이라 유한길이·HW 미고려, rate loss 완화 시 iteration 수 증가 trade-off.

### C. Prime ECC 관련 모듈 핀포인트

대상이 code-design(순수 점근 이론)이라 C섹션 디코더 성능 항목은 전부 N/A.

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| spatial coupling / SC-LDPC ensemble | 대응 없음 | Prime ECC는 block QC-LDPC 고정 - convolutional/SC 구조 미보유 |
| density evolution / GEXIT threshold 분석 | 대응 없음 | 점근 성능 해석 도구, 코드베이스 내 대응 모듈 없음 |

적용 가치: 낮음 - threshold saturation은 부호이론적으로 중요한 개념이나, Prime ECC는 고rate 고정 block binary QC-LDPC이고 본 논문은 저rate(~1/2) SC-LDPC의 점근 threshold 이론이라 떼어 이식할 대상이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1004.3742v1",
  "title": "Threshold Saturation on BMS Channels via Spatial Coupling",
  "year": 2010,
  "venue": "arXiv/cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "spatial coupling으로 BP threshold가 MAP threshold까지 saturate됨을 일반 BMS 채널서 경험적으로 입증",
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
  "caveat": "점근적 ensemble 이론(유한길이·HW 없음), 완전한 증명 미완, rate loss 완화 시 iteration 증가",
  "todo_check": "유한길이·고rate NAND 부호에서 threshold saturation 이득이 실질적으로 남는지"
}
```
