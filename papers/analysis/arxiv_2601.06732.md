### arxiv:2601.06732v1 - Study of Adaptive Reliability-Driven Conditional Innovation Decoding for LDPC Codes (2026, arXiv/IEEE Access 관련)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5 |
| 부호length | 512~2048 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 신뢰도(syndrome Rv)+LLR변화(∆y) 2단 평가로 RBP 갱신 노드를 적응 선택, iteration 대폭 감소 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | 기반이 full-tanh Sum-Product + RBP 동적스케줄, ARM CPU 추정치뿐. Min-Sum/우리 pipeline과 정합 재설계 필요 |
| 추가확인 | Rv/∆y 노드선택을 Min-Sum + z=32 row-병렬 pipeline에 붙일 때 HW 오버헤드(정렬 O(NlogN), 메모리 67%↑) 타당성 |

> 총평: iteration/latency 절감 아이디어(syndrome 기반 신뢰도 노드선택)는 흥미로우나 SPA+RBP 전제라 우리 Min-Sum HW로의 이식엔 상당한 개조 필요.

### B. 알고리즘 요약

1. 시스템: AWGN+BPSK, rate-1/2 regular LDPC `(512,256)`·`(2048,1024)`, `dv=3, dc=6`, 채널 LLR `Ly=2y/σ^2`.
2. 문제: flooding BP는 수렴에 15~50 iter 필요 → latency 큼. 저지연 위해 iteration 최소화가 목표.
3. 제안 AR-CID: (1) 메시지 품질 검사, (2) 메시지 패싱 리파인먼트 2단을 RBP 스케줄에 통합.
4. 신뢰도 지수 `Rv = Σ_{m∈N(v)} sm` (변수노드 v가 관여한 불만족 syndrome 수), 클수록 오류 가능성↑ → 내림차순 정렬해 상위 `λN` 노드만 갱신(`λ=0.2`).
5. 맥락 정보 전이 `∆y = |φ(Ly)-φ(L̃y)|`, `φ(L)=1/(1+e^-L)`; iteration간 belief 변화량으로 미수렴 노드 식별.
6. 결합 지표 `M(v,y)=α·Rv+β·∆y` (`α=0.65, β=0.35`), 임계 `γ∈{0.1,0.15}` 초과 노드만 active set에 포함.
7. C2V 갱신은 표준 Sum-Product `2 tanh^-1(∏ tanh(m/2))`, RBP residual `r=m_new-m_old`을 사전계산 신뢰도로 변형해 우선순위화.
8. 수렴 분석: 두 항이 유계·`∆y→0`으로 고정점 수렴 증명(N→∞), 경계 `M(v,y)≤α·dv`.
9. 결과(시뮬): 목표 BER<1e-6 달성에 AR-CID `Iavg≈4.5` vs RP 10, RBP 15, BP 250; `(2048,1024)`서 RD-RBP 대비 ~0.3dB, RBP 대비 ~0.5dB 이득. latency 4.74ms(ARM Cortex-A53 추정).
10. 한계: HW 미설계(ARM CPU 추정치·시뮬만), 그림 BER 곡선 수치는 텍스트 서술분만 확보. 메모리 ~95KB(BP대비 +67%), 정렬 O(NlogN) 오버헤드.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 디코딩 이터레이션 루프 / 노드선택 스케줄 | decoder.cpp LDPC_Decoder() | active-set 기반 갱신을 이터레이션 루프에 삽입 여지, 단 스케줄 구조 상이 |
| C2V 연산(SPA tanh vs Min-Sum) | decoder.cpp CNU_Update_New_Mag(), C2V_Cal_New_Sgn() | 논문은 full-tanh SPA, 우리는 min-sum → 직접 대응 아님, 재유도 필요 |
| syndrome 기반 조기종료/신뢰도 | partial_CRC.cpp partial_crc_HW_T4(), full_CRC.cpp | syndrome 검사 개념은 유사하나 우리는 CRC 조기종료 사용 |
| VN 처리 / LLR 업데이트 | decoder.cpp VN_Cal_HD() 등, ecc_data.h PARAM_LLR | ∆y(LLR변화) 추적은 VN 단계에 부가 가능 |
```

적용 가치: **중간** — iteration/latency 감소 컨셉은 우리 관심사와 정렬되나, 기반이 full-tanh SPA + RBP 동적 스케줄이고 HW 검증이 없어 Min-Sum + 고정 z=32 row-병렬 pipeline에 그대로 이식하기 어렵고 정렬/메모리 오버헤드 검증이 선행돼야 함.

### D. JSON 블록

```json
{
  "id": "arxiv:2601.06732v1",
  "title": "Study of Adaptive Reliability-Driven Conditional Innovation Decoding for LDPC Codes",
  "year": 2026,
  "venue": "arXiv (cs.IT)",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.5,
  "code_length": "512~2048",
  "soft_quant": "soft-4bit+",
  "key_contribution": "신뢰도(syndrome Rv)+LLR변화(∆y) 2단 평가로 RBP 갱신 노드를 적응 선택, iteration 대폭 감소",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "중",
  "caveat": "기반이 full-tanh Sum-Product + RBP 동적스케줄, ARM CPU 추정치뿐. Min-Sum/우리 pipeline과 정합 재설계 필요",
  "todo_check": "Rv/∆y 노드선택을 Min-Sum + z=32 row-병렬 pipeline에 붙일 때 HW 오버헤드(정렬 O(NlogN), 메모리 67%↑) 타당성"
}
```
