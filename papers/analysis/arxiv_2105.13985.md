### arxiv:2105.13985v1 - LDPC Codes with Soft Interference Cancellation for Uncoordinated Unsourced Multiple Access (2021, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 미상 |
| 부호rate | 0.25 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | polar+SCLD 대신 BP-복호 LDPC 외부부호 + SISO-MMSE로 soft 정보를 교환하는 반복 SoIC 수신기 |
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
| 한계,주의 | UMAC(무선 다중접속) 특화 수신기 아키텍처로 NAND single-user ECC와 무관, MMSE 추정과 결합된 반복구조가 핵심 |
| 추가확인 | LDPC 부호설계(DE로 최적화된 degree 분포)만 떼어내 고rate NAND 부호에 재사용 가능한지 |

> 총평: LDPC를 무선 UMAC 반복 수신기의 외부부호로 쓴 통신 논문. 표준 BP + MMSE 결합이 본질이라 NAND binary LDPC ECC 이식 가치 낮음.

### B. 알고리즘 요약

1. 시스템: 무선 unsourced multiple access(UMAC), `Ktot` 중 `Ka`개 활성 유저가 공통 codebook으로 `B=100`비트 메시지를 `n=30000` 채널사용에 전송.
2. 문제: 기존 [8] polar+SCLD는 SCLD가 soft-output을 못 내 hard-input MMSE만 가능 → 활성유저 다수(>250)에서 성능 급락.
3. 모델: 수신 `y = Σ xk(wk) + z`, AWGN `N(0,σ²)`, 유저별 전력제약, per-user 오류확률 `Pe` 기준.
4. 핵심 기법: 메시지를 preamble `wp`(spreading 시퀀스 선택) + `wc`(LDPC 부호화)로 분할, spreading 시퀀스와 텐서곱 `xk=vk⊗ajk`로 확산.
5. 핵심 식: SISO MMSE 추정 `Tj,i = S:,jᵀ(S P S ᵀ+σ²I)⁻¹ Y` (11) → 부호심볼 soft 추정, 이를 등가 AWGN 채널 LLR로 변환 (13).
6. 확장: 에너지검출기(SSD)로 활성 시퀀스 검출 → SISO-MMSE SoIC → LDPC BP 복호 → 유효 codeword SIC 제거 후 재반복.
7. 구현 디테일: BP는 표준 tanh/tanh⁻¹ sum-product 규칙 (14)~(16), MMSE는 `np×np` 역행렬로 복잡도 `O(Ka⁴)` 수준.
8. 최적화: LDPC degree 분포를 density evolution으로 반복 SoIC 프로세스에 정합되게 설계 (`Ka=250` 기준 경험적 최적화).
9. 결과: `Ka≤75`에서 FBL achievability bound보다 우수(최초), `Ka>200`에서 [8] 대비 대폭 개선. 단 복잡도는 [8]보다 한 자릿수 증가.
10. 한계: HW 미설계, 시뮬만, 무선 다중접속·MMSE 결합 특화라 NAND single-user 고rate ECC와 직접 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| LDPC BP 복호(sum-product tanh) | decoder.cpp `LDPC_Decoder()` | 낮음 — Prime는 min-sum 근사, 이 논문은 full-tanh 표준 BP |
| SISO-MMSE / SoIC 반복 추정 | 대응 없음 | 무선 다중접속 수신기 컴포넌트, NAND ECC에 없음 |
| DE 기반 LDPC degree 설계 | ecc_top.cpp `Load_PCM()` | 낮음 — 부호설계 레이어지만 UMAC 반복정합용, 고rate NAND와 목적 상이 |
| spreading/에너지검출/SIC | 대응 없음 | 채널접속 계층, ECC와 무관 |

적용 가치: **낮음** — LDPC를 무선 UMAC 반복 수신기의 외부부호로 사용한 통신 논문으로, 핵심 기여(SISO-MMSE SoIC, DE 정합 설계)가 NAND single-user binary QC-LDPC 파이프라인과 무관하고 복호도 표준 tanh BP다.

### D. JSON 블록

```json
{
  "id": "arxiv:2105.13985v1",
  "title": "LDPC Codes with Soft Interference Cancellation for Uncoordinated Unsourced Multiple Access",
  "year": 2021,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "미상",
  "code_rate": 0.25,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "polar+SCLD 대신 BP-복호 LDPC 외부부호 + SISO-MMSE로 soft 정보를 교환하는 반복 SoIC 수신기",
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
  "caveat": "UMAC(무선 다중접속) 특화 수신기 아키텍처로 NAND single-user ECC와 무관, MMSE 추정과 결합된 반복구조가 핵심",
  "todo_check": "LDPC 부호설계(DE로 최적화된 degree 분포)만 떼어내 고rate NAND 부호에 재사용 가능한지"
}
```
