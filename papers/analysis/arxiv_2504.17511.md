### arxiv:2504.17511v1 - Subcode Ensemble Decoding of Polar Codes (2025, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.5 |
| 부호length | 64~256 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 폴라 코드용 새 pre-transformation(PT-C)으로 subcode ensemble decoding(ScED)을 구현해 고정 list 크기에서 SCL 성능 향상 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | N/A |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 폴라 코드 SCL 전용 기법이며 LDPC/QC-LDPC 부호 구조와 무관, HW 미설계·시뮬만 |
| 추가확인 | ScED 원논문[7]의 LDPC/BP 버전이 binary LDPC에 직접 적용 가능한지 별도 검토 |

> 총평: 폴라 코드 SCL 디코딩용 ensemble 기법으로, NAND binary QC-LDPC 디코더에는 이식 대상이 아님(추천도 하).

### B. 알고리즘 요약

1. 시스템: BI-AWGN 채널, 5G 폴라 코드 `C(64,32)` 및 `C(256,k)`(`k∈{64,128,192}`), CRC-6/CRC-11을 PT-A로 사용.
2. 문제: 짧은 블록 폴라 코드의 SCL 디코딩은 list 크기를 키워야 성능이 오르나 HW 면적이 급증(L 8→16 시 면적 5배 이상)해 고정 list에서 성능 개선이 필요.
3. 핵심 기법 - Subcode Ensemble Decoding(ScED): `M`개 병렬 경로가 각기 다른 subcode `Ci⊆C`를 디코딩하고 ML-in-the-list로 최종 추정 선택, subcode들이 원부호를 덮도록(`∪Ci=C`) 선택.
4. 핵심 아이디어: pre-transformation을 affine map `T(up)=upA+b`로 일반화하고 encoding/decoding 역할에 따라 PT-A/PT-B/PT-C로 분류.
5. 신규 기여 PT-C: 인코딩엔 안 쓰이고 디코딩 시에만 target bit를 dynamic frozen으로 만들어 폴라 subcode를 생성 → 폴라 코드에서 ScED 가능케 함.
6. 이론적 근거(Theorem 1): stand-alone SC가 맞으면 해당 subcode SC도 같은 결정을 함(`x∈CT`일 때) → ScED 평균 성능이 SC 이상임을 보장.
7. PT-C 파라미터 분석: depth `dp=2`가 `dp=1`보다 우수, 신뢰도 낮은 bit-channel을 target으로 하면 decoded URP 비율이 높음.
8. 앙상블 설계: `r=30000` 후보 PT-C에서 URP-SCL 커버리지 최대화 heuristic으로 `M`개 부분집합 선택(path metric 조건 추가).
9. 결과: 목표 FER `10^-3`에서 ScED-M-SCL-L이 SCL-L 대비 0.1~0.25 dB 이득, 짧은 코드는 M=2 경로로 SCL-2L 성능에 근접(절반 list 크기).
10. 한계: 폴라 SCL 전용, HW 미설계(면적/throughput 미보고), soft-info 기반 SCL 채널만 가정.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Subcode ensemble / SCL 디코딩 | 대응 없음 | Prime ECC는 min-sum 기반 binary QC-LDPC 디코더로 폴라/SCL 구조 부재 |
| pre-transformation(PT-A/B/C) | 대응 없음 | 폴라 부호 특유의 frozen bit 변형, QC-LDPC H-matrix와 무관 |
| ML-in-the-list 결정 | 대응 없음 | Prime ECC는 CRC 조기종료(partial_CRC.cpp) 사용, list 결정 없음 |

적용 가치: **낮음** — 폴라 코드 전용 ensemble/PT 기법으로 NAND binary QC-LDPC의 부호설계/디코더/HW 어디에도 대응 모듈이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2504.17511v1",
  "title": "Subcode Ensemble Decoding of Polar Codes",
  "year": 2025,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": 0.5,
  "code_length": "64~256",
  "soft_quant": "soft-4bit+",
  "key_contribution": "폴라 코드용 새 pre-transformation(PT-C)으로 subcode ensemble decoding을 구현해 고정 list 크기에서 SCL 성능 향상",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "N/A",
  "latency": "개선",
  "recommend": "하",
  "caveat": "폴라 코드 SCL 전용 기법이며 LDPC/QC-LDPC 부호 구조와 무관, HW 미설계·시뮬만",
  "todo_check": "ScED 원논문[7]의 LDPC/BP 버전이 binary LDPC에 직접 적용 가능한지 별도 검토"
}
```
