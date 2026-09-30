### arxiv:2602.01555v1 - Design of Root Protograph LDPC Codes Simultaneously Achieving Full Diversity and High Coding Gain (2026, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호rate | 0.5 |
| 부호종류 | protograph |
| 부호length | 7744, 16896 |
| 연판정 | 무관 |
| 핵심기여 | full diversity 보장 protograph 템플릿 정의 후 RCA-DE 적합도의 GA로 AWGN 코딩게인까지 동시 최적화 |
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
| 한계,주의 | block-fading(무선) M=2 + rate-1/2 특화, NAND high-rate AWGN/RBER 채널과 무관 |
| 추가확인 | GA+RCA-DE 부호설계 루프 자체는 재사용성 있으나 NAND용 목적함수·high-rate로의 전환 가능성 |

> 총평: DivE 제약 템플릿 + RCA-DE 유도 GA로 block-fading full diversity와 AWGN 코딩게인을 동시 달성하는 무선용 부호설계로, NAND binary QC-LDPC ECC 이식성 낮음.

### B. 알고리즘 요약

1. 시스템: protograph QC-LDPC(rate-1/2, `(N,R)=(7744,1/2)`,`(16896,1/2)`, PEG lifting `Z=176`)를 M=2 block-fading(BPSK)과 AWGN 양쪽에서 평가.
2. 문제: 기존 root/GRP LDPC는 full diversity는 얻으나 protograph 구조 제약이 심해 AWGN 코딩게인 손실; 단일 부호로 둘 다 달성 가능한가.
3. 모델: M=2 BFC `ri = hi·si + ni`, `hi~CN(0,1)`, Singleton-like bound상 full diversity 최대 rate `R=1/2`.
4. 핵심기법1(DivE): fading Boolean 근사 `Am=1_{|hm|^2γ≥ρ0}`로 min-sum 메시지의 fading 함수를 CN=AND/VN=OR로 iteration별 추적, 최종 Boolean 함수의 diversity order 판정.
5. 핵심식: VN 최종함수가 `F_i = A0+A1`이면 full diversity → generalized rootcheck 조건이면 `A1·A1=A1`,`(A0+A1)·A1=A1`로 CN이 `A1` 전달, VN OR로 full diversity 획득.
6. 핵심기법2(protograph 템플릿): 고정/설계가능(designable `b∈{0,1}`) 엔트리와 특정 block mapping(`[0,n/4)∪[3n/4,n)`→block0)로 H(T) 부호족 전체가 최대 `n/4` iteration 내 full diversity 보장(Theorem 1).
7. 구현 디테일: 큰 M에서는 Boolean 대수 대신 fadingMSD로 2^M 상태 수치평가하여 truth table 구성.
8. 최적화절차: H(T) 내 designable 엔트리만 GA로 탐색, 적합도=RCA-DE decoding threshold; VN/CN 기반 crossover + mutation, rate·degree-1 제약 validity check, 수렴 후 PEG lifting.
9. 결과: BFC에서 root-protograph와 동등 slope이나 추가 coding gain, AWGN threshold gap Δcap=0.126dB(제안) vs 0.253(5G-NR) vs 0.915(root), 두 길이 모두 baseline 초과.
10. 한계: HW 미설계, 시뮬만, M=2·rate-1/2 한정, block-fading 무선 전제.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| protograph→QC-LDPC lifting/부호 로드 | ecc_top.cpp Load_PCM() | 부호구조 로드는 대응되나 block-fading 템플릿·rate-1/2는 NAND high-rate와 불일치 |
| min-sum 메시지 업데이트(분석용) | decoder.cpp C2V_Cal(), CNU_Update_New_Mag() | diversity 분석 도구로만 사용, 디코더 알고리즘 개선 아님 |
| GA+DE 기반 부호설계 루프 | 대응 없음 | Prime ECC는 특정 H-matrix 고정, 설계 자동화 모듈 없음 |
```

적용 가치: 낮음 — block-fading M=2/rate-1/2 무선 부호설계로 NAND high-rate AWGN/RBER 환경에 직접 이식 근거 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2602.01555v1",
  "title": "Design of Root Protograph LDPC Codes Simultaneously Achieving Full Diversity and High Coding Gain",
  "year": 2026,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "protograph",
  "code_rate": 0.5,
  "code_length": "7744, 16896",
  "soft_quant": "무관",
  "key_contribution": "full diversity 보장 protograph 템플릿 정의 후 RCA-DE 적합도의 GA로 AWGN 코딩게인까지 동시 최적화",
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
  "caveat": "block-fading(무선) M=2 + rate-1/2 특화, NAND high-rate AWGN/RBER 채널과 무관",
  "todo_check": "GA+RCA-DE 부호설계 루프 자체는 재사용성 있으나 NAND용 목적함수·high-rate로의 전환 가능성"
}
```
