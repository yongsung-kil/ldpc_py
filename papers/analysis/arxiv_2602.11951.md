### arxiv:2602.11951v1 - Robust Composite DNA Storage under Sampling Randomness, Substitution, and Insertion–Deletion Errors (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 기타 |
| 부호rate | 0.3235~0.75 |
| 부호length | 480~816 |
| 연판정 | soft-4bit+ |
| 핵심기여 | composite DNA storage를 multinomial channel로 모델링하고 3차원 확률 simplex 상 constellation으로 표현, sampling randomness/substitution/insertion-deletion 각각에 대한 LLR 유도 및 constellation update 규칙 제안 |
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
| 한계,주의 | DNA storage(4-ary nucleotide, multinomial channel) 전용 채널 모델로 NAND binary channel과 물리적 성격이 근본적으로 다름; 기존 5G/WRAN/802.11 표준 LDPC를 그대로 재사용(부호 자체는 무수정) |
| 추가확인 | LLR 유도 아이디어(다중 관측 심볼→사후확률→LLR)가 NAND의 multi-level cell(MLC/TLC) soft-read LLR 근사와 개념적 유사성이 있는지 검토 필요 |

> 총평: DNA 저장 특화 채널 모델(multinomial, composite letter) 위에서 기존 표준 binary LDPC 코드의 LLR 입력만 재설계한 응용 논문으로, 부호/디코더/HW 기여가 없어 NAND ECC 이식 가치는 낮음.

### B. 알고리즘 요약

1. Composite DNA storage는 하나의 저장 위치에 단일 염기 대신 4개 뉴클레오타이드(A,C,T,G)의 혼합 비율 `{ρ_A,ρ_C,ρ_T,ρ_G}`을 심어 알파벳을 확장하는 방식으로, 이를 `multinomial channel`로 모델링하고 3차원 확률 simplex 상의 디지털 변조 constellation과 유사하게 취급한다.
2. 문제: DNA 합성/시퀀싱 시 발생하는 sampling randomness(제한된 n개 strand 샘플링에 따른 관측 편차) 때문에 관측된 뉴클레오타이드 빈도가 원래 constellation point에서 벗어나 오류가 생기며, 이를 실용적 채널 코드(LDPC)로 보정하고자 함.
3. 채널 모델: 입력 `ρ_s`에 대해 n회 독립 샘플링한 관측 `d_i=(d_i,1,d_i,2,d_i,3)`가 `Multinomial(n, ρ_s)` 분포를 따른다고 가정(`P(d_i|ρ_s) = n!/∏(n·d_i,j)! · ∏ρ_s,j^{n·d_i,j}`).
4. 핵심 기법: 각 constellation point `ρ_s`에 대한 사후확률 `P(ρ_s|d_i) ∝ P(d_i|ρ_s)`(균일 사전확률 가정)로부터 L-bit segment의 각 비트에 대해 LLR을 `LLR_{i,l} = log[Σ_{u_s,l=0}P(d_i|ρ_s) / Σ_{u_s,l=1}P(d_i|ρ_s)]`로 계산해 표준 binary LDPC 디코더(log-SPA/min-sum) 입력으로 사용.
5. Substitution 확장: 각 뉴클레오타이드가 확률 `ε`로 무작위 치환되는 채널에서 constellation point를 `ρ̂_s = ρ_s(1-4ε/3) + (ε/3)[1,1,1,1]`로 갱신해 (4),(9)에 대입 — 0/0 부정형(원래 0이던 성분에 substitution으로 비영값 발생) 문제도 함께 해결.
6. Insertion-Deletion(ID) 확장: 스트랜드 길이 E가 보존된 경우(삽입/삭제 없음 또는 삽입=삭제 1회씩)만 고려하는 근사로, 위치 i의 "no-shift" 확률 `p_ns,i`를 유도(식 14~18)하고 이를 기반으로 constellation을 `ρ̂_s`로 재가중 갱신(식 19) — 저자도 이를 suboptimal 근사로 명시.
7. 부수 트릭: L=3/4 constellation은 최적화 없이 임의로 선택했고([11]에서 최적화 가능함을 언급), 디코더는 log-SPA, 최대 20 iteration만 사용.
8. 학습/최적화 절차는 없음(순수 확률 모델링 + LLR 유도).
9. 결과: 5G(R1=0.3235), WRAN 802.22(R2=0.5), 802.11(R3=0.75) 표준 LDPC 코드를 그대로 사용해 BLER-vs-샘플수(n) 곡선 제시; sampling-only 채널에서 n 증가 시 낮은 BLER 달성, substitution(ε=0.01~0.4)/ID(p_i=p_d=0.001~0.002) 채널에서는 성능 저하하지만 실용적 수준 유지, 기존 limited-magnitude 오류 모델([8])의 코드 대비 우수.
10. 한계: 부호 자체는 기존 표준 LDPC(5G/WRAN/802.11) 그대로 사용(무수정)하며 HW 설계·복잡도 분석 없음; ID 채널 근사는 최대 1회 삽입/삭제만 가정한 suboptimal 모델이고, 채널이 DNA 4-ary multinomial 특화라 binary NAND 채널과 물리적 성격이 다름.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| LLR 유도(multinomial 사후확률 기반) | `channel.cpp` `Set_LLR_Th()` | DNA multinomial 채널 전용 LLR 계산으로, NAND AWGN/RBER 채널의 LLR 양자화 테이블 구조와 목적은 유사하나 채널 모델 자체가 상이해 직접 이식 불가 |
| 표준 binary LDPC 디코딩(log-SPA/min-sum) | `decoder.cpp` `LDPC_Decoder()` | 기존 표준 코드·알고리즘 재사용일 뿐 신규 디코더 기여 없음 |
| 부호 설계/구조 | 대응 없음 | 5G/WRAN/802.11 기성 부호를 그대로 채택, 신규 QC-LDPC 구성 없음 |

적용 가치: 낮음 — DNA storage 전용 multinomial 채널 모델의 LLR 유도이며 binary NAND 채널과 물리적 기반이 달라 직접 이식 불가, 부호/디코더/HW 요소도 기성품 재사용에 그침.

### D. JSON 블록

```json
{
  "id": "arxiv:2602.11951v1",
  "title": "Robust Composite DNA Storage under Sampling Randomness, Substitution, and Insertion–Deletion Errors",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "기타",
  "code_rate": "0.3235~0.75",
  "code_length": "480~816",
  "soft_quant": "soft-4bit+",
  "key_contribution": "composite DNA storage를 multinomial channel로 모델링하고 3차원 확률 simplex 상 constellation으로 표현, sampling randomness/substitution/insertion-deletion 각각에 대한 LLR 유도 및 constellation update 규칙 제안",
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
  "caveat": "DNA storage(4-ary nucleotide, multinomial channel) 전용 채널 모델로 NAND binary channel과 물리적 성격이 근본적으로 다름; 기존 5G/WRAN/802.11 표준 LDPC를 그대로 재사용(부호 자체는 무수정)",
  "todo_check": "LLR 유도 아이디어(다중 관측 심볼→사후확률→LLR)가 NAND의 multi-level cell(MLC/TLC) soft-read LLR 근사와 개념적 유사성이 있는지 검토 필요"
}
```
