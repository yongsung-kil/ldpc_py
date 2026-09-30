### arxiv:2101.10145v1 - Codes approaching the Shannon limit with polynomial complexity per information bit (2021, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.0000809~0.0156 |
| 부호length | 8256 |
| 연판정 | 무관 |
| 핵심기여 | weight-3 parity의 LDPC형 변조부호 Cm에 polar 다단 프리코딩을 결합해 극저SNR AWGN에서 정보bit당 다항복잡도(m·ln m)로 Shannon 한계(-1.59dB)에 근접 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 극저SNR·vanishing-rate(IoT 저전력) 전용, rate가 지수적으로 소멸 — NAND 고rate와 정반대. weak-independence 가정 의존, HW 미설계 |
| 추가확인 | 없음 |

> 총평: 극저SNR/저rate AWGN에서 polar+weight-3-LDPC로 Shannon 한계 근접을 노린 순수 코딩이론 — NAND 고rate binary QC-LDPC와 rate/채널 정반대라 이식 가치 없음.

### B. 알고리즘 요약

1. 시스템: BI-AWGN 극저SNR(IoT 저전력, snr -20dB급), 기본부호 `Cm` = 생성행렬 `Gm=[Im|Jm]`(Jm은 weight-2 열 전부), rate `R=2/(m+1)`(m=128→n=8256), parity check weight 3.
2. 풀려는 문제: 기존 capacity-achieving 부호(biorthogonal/RM/polar)는 rate가 m에 지수적으로 소멸 → 대역폭·복호복잡도 지수 폭증. 다항복잡도로 Shannon 한계 근접이 목표.
3. 핵심 가정: all-one 코드워드 전송, `zi,j~N(δ,δ)`, iteration간 r.v.가 "weak-independence"(조건부 기댓값→무조건 기댓값)라는 가정 하에 해석.
4. 핵심 기법: BP형 soft 알고리즘 `Ψsoft` — 정보bit `a0,i`만 추정(`hi,j`, offset `ui,j=tanh(zi,j)`), parity check `a0,i=a0,j·ai,j`로 상호 재평가, `L~ln m/ln c` iteration.
5. 핵심 식: 고정점 방정식 `x=(1/√2π)∫tanh(t√(xc))·e^{-(t-√(xc))²/2}dt` — `c>1`(SNR>-6dB)에서만 비자명 근 `x*∈(0,1)` 존재(수렴 임계).
6. 확장: multilevel — 정보 m bit를 b 블록으로 나눠 각 블록을 rate 증가하는 polar 부호 `Bi`로 보호, `Ψsoft`↔polar를 왕복 복호(frozen bit 활용).
7. 구현 디테일: `ui,j`를 `zi,j`로 근사(z→0), tanh↔atanh 변환, 정보bit만 갱신해 복잡도 절감.
8. 분석 도구: ML 하한(Theorem1, `2Q(√c)-2Q²(√c)`)과 BP 상하한(Theorem4, 재귀 `P_{l+1}=S+P·T`)을 폐형식 유도.
9. 결과: `C128`(n=8256) 시뮬이 해석 bound와 거의 일치, uncoded 대비 3dB 이득, 다단 구성으로 b=25000시 -1.5917dB(Shannon 한계 gap 1E-5).
10. 한계: extreme-noise·vanishing-rate 전용, weak-independence 가정 의존, HW/throughput/양자화 전무, moderate length는 future work.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BP형 soft 디코더 Ψsoft (tanh 기반 message passing) | decoder.cpp LDPC_Decoder(), C2V_Cal() | 알고리즘 위치는 대응하나 full-tanh·정보bit-only·극저SNR 전용이라 min-sum HW와 부정합 |
| weight-3 parity LDPC형 부호 Cm (Gm=[Im|Jm]) | ecc_top.cpp Load_PCM() | 부호구조 로드 지점 대응하나 rate·구조가 QC-LDPC와 전혀 다름 |
| polar 다단 프리코딩 / RM·polar 결합 | 대응 없음 | Prime ECC는 순수 binary QC-LDPC — polar/RM 계층 없음 |
| soft LLR (hi,j=2zi,j) | channel.cpp Set_LLR_Th() | 개념적 대응뿐, 양자화·soft-read 비용 논의 없음 |
```

적용 가치: **낮음** — 극저SNR·vanishing-rate AWGN 전용 코딩이론이며 full-tanh BP + polar 결합 구조가 Prime ECC(고rate binary QC-LDPC, min-sum HW, NAND soft-read)와 rate·채널·알고리즘 전 축에서 어긋나 이식 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2101.10145v1",
  "title": "Codes approaching the Shannon limit with polynomial complexity per information bit",
  "year": 2021,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "8256",
  "soft_quant": "무관",
  "key_contribution": "weight-3 parity LDPC형 변조부호에 polar 다단 프리코딩 결합, 극저SNR AWGN에서 다항복잡도로 Shannon 한계 근접",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "극저SNR·vanishing-rate(IoT) 전용, rate가 지수적 소멸 — NAND 고rate와 정반대, weak-independence 가정 의존, HW 미설계",
  "todo_check": "없음"
}
```
