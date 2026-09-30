### arxiv:2404.10367v1 - Robust Performance Over Changing Intersymbol Interference Channels by Spatial Coupling (2024, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 0.494 |
| 부호length | 300000 |
| 연판정 | 무관 |
| 핵심기여 | 단일 (5,10)/(6,12) regular SC-LDPC가 채널별 최적화 없이 여러 ISI 채널 + BCJR/LMMSE 검출기에 robust하게 SIR 근접 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | ISI/turbo equalization 전용, SC 구조 + window decoding(latency 300k symbol)로 NAND QC-LDPC와 구조·채널 모두 불일치 |
| 추가확인 | 없음 |

> 총평: ISI 채널 turbo equalization에서 SC-LDPC의 채널 변화 robustness 실증 — NAND memoryless QC-LDPC 이식 가치 없음.

### B. 알고리즘 요약 (10줄 내외)

1. 시스템: BPSK 부호어를 memory `ν` ISI 채널(CH-I/II/III, AWGN)로 전송, 수신단은 turbo equalization(검출기↔BP 복호기 반복). 검출기는 최적 BCJR 또는 준최적 LMMSE 2종.
2. 문제: 고전 irregular LDPC 부호설계는 특정 채널에 degree distribution `λ(x),ρ(x)`를 최적화하므로 채널이 바뀌면(또는 송신단이 채널을 모르면) 성능이 크게 악화(SIR 대비 최대 ~3dB gap).
3. 대비군: EXIT chart + DE 2단계 탐색으로 각 채널·검출기별 최적 irregular 부호 설계(Table II/III) — matched 채널엔 우수하나 mismatched엔 취약.
4. 핵심기법: 높은 node degree의 regular `(dv,dc)` 부호((5,10),(6,12))를 골라 spatial coupling(coupling memory `m`) 적용 → threshold saturation으로 BP threshold가 uncoupled MAP threshold(≈SIR)에 접근.
5. 핵심식: joint BP DE 업데이트 `p(Lv→c)=p(LH→v)⋆λ(p(Lc→v))`, 검출기 밀도 `T(·,σ)`는 AWGN에선 폐형 없어 Monte Carlo로 평가.
6. 확장: 준최적 LMMSE 검출기에도 coupling 적용, GEXIT area bound가 무의미해지는 이유(준최적 검출기는 entropy↑)를 논증.
7. 트릭: LMMSE coupled threshold를 EXIT chart positive-gap 조건으로 근사(`γArea`), 검출기 출력 entropy `hE,DET`를 a-priori entropy의 3차 다항식으로 피팅.
8. 최적화: irregular 부호는 EXIT fitting + DE로 탐색; SC 부호는 최적화 불필요(universality)가 핵심 주장.
9. 결과: (6,12) `m=6`, `L=500`, `N=10000`(R=0.494), window `W=30`, `IC=30`/`ID=20`. 단일 SC 부호가 CH-II·CH-III 모두 우수. LMMSE도 coupling 시 BCJR과 gap이 dB 이하로 좁혀짐(CH-III에서 uncoupled 5dB+ → coupled fraction of dB).
10. 한계: 순수 threshold+유한길이 시뮬 논문. HW 없음, gate/throughput 없음. ISI turbo eq 특화, window decoding latency 300k symbol.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SC-LDPC + window decoding | 대응 없음 | Prime ECC는 고정 QC-LDPC(`ecc_top.cpp` `Load_PCM()`), SC/window decoding 아님 |
| turbo equalization(BCJR/LMMSE 검출기) | 대응 없음 | NAND memoryless RBER/AWGN 채널, ISI 검출기 미사용 |
| irregular degree distribution EXIT 설계 | 대응 없음 | Prime ECC 부호는 고정, degree distribution 재설계 대상 아님 |

적용 가치: **낮음** — ISI 채널 turbo equalization용 SC-LDPC의 채널 robustness 실증으로, NAND용 binary QC-LDPC의 부호설계·디코더·HW 어디에도 이식 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2404.10367v1",
  "title": "Robust Performance Over Changing Intersymbol Interference Channels by Spatial Coupling",
  "year": 2024,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": 0.494,
  "code_length": "300000",
  "soft_quant": "무관",
  "key_contribution": "단일 (5,10)/(6,12) regular SC-LDPC가 채널별 최적화 없이 여러 ISI 채널 + BCJR/LMMSE 검출기에 robust하게 SIR 근접",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "ISI/turbo equalization 전용, SC 구조 + window decoding(latency 300k symbol)로 NAND QC-LDPC와 구조·채널 모두 불일치",
  "todo_check": "없음"
}
```
