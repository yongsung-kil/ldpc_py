### arxiv:2211.10712v1 - Comparison of different coding schemes for 1-bit ADC (2022, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 기타 |
| 부호rate | 0.5~0.9375 |
| 부호length | 1024 |
| 연판정 | 무관 |
| 핵심기여 | AWGN+1-bit ADC(=BSC) 채널에서 Polar/LDPC/Product/BCH FER 비교·부호선택 가이드 제시 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 신규 기법 없음(기존 부호 비교 survey), N~1024 단길이, 1-bit ADC(hard) 채널 특화, LDPC는 후보 중 하나일 뿐 |
| 추가확인 | 없음(교과서/비교 수준, Prime ECC 이식 대상 아님) |

> 총평: 1-bit ADC 채널의 부호 비교 survey로 신규 디코더/부호설계 기여가 없어 NAND QC-LDPC 이식 가치 없음.

### B. 알고리즘 요약

1. 채널: BPSK over BI-AWGN + 대칭 1-bit ADC(`qi=sign(yi)`), 이는 전이확률 `p=Q(sqrt(SNR))`의 BSC와 등가, 용량 `C=1-h(p)`.
2. 문제: 저해상도(1-bit) ADC 수신기용 error-correction 부호가 잘 연구되지 않아, 다양한 부호를 공정 비교하고 rate/length별 권고 제시.
3. 후보 부호: Polar(5G NR / PW / RM / GA), LDPC(DE+ACE, PEG), BCH(narrow-sense primitive), Product(BCH TPC).
4. 디코더: LDPC=Sum-Product(50 iter), Polar=SCL(list 32, CRC 16), BCH=Berlekamp-Massey, TPC=iterative hard(10 iter).
5. 입력형태: hard 디코더는 `ri=(1-qi)/2`, soft 디코더는 `ri=qi*ln((1-p)/p)` — 1-bit라 신뢰도 있는 LLR 획득 불가.
6. LDPC 구성: core matrix `Hcore`(mc x nc)를 DE로 최적 threshold protograph 도출 후 원소를 순열/circulant `Pij`로 치환, ACE로 short cycle 최소화, rate `R=1-mc/nc`.
7. 실험 설정: `N~1024`, rate 집합 {0.5,0.625,0.75,0.8125,0.875,0.9375}, FER vs SNR 비교.
8. 결과(중간 rate/SNR): DE+ACE LDPC와 GA/DE Polar가 최상, PEG LDPC·channel-independent 부호는 열세, TPC 최하.
9. 결과(고rate/고SNR): 채널이 BSC에 근접해 BCH가 최상(R>=0.8125 권고), TPC는 SPC 구성으로 d=4·t=1만 정정하여 최악.
10. 한계: HW 미설계, 시뮬레이션만, 신규 알고리즘 없음(기존 부호 비교·선택 가이드), 무선/IoT/massive-MIMO 맥락.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| LDPC Sum-Product 디코딩 | `decoder.cpp` `LDPC_Decoder()` (Prime ECC는 min-sum이라 상이) | full-tanh Sum-Product은 "대응 없음" 수준, 기여 없음 |
| DE+ACE LDPC 부호설계 | `ecc_top.cpp` `Load_PCM()` (원리적) | 표준 구성법 재사용뿐, 이식성 하 |
| Polar/BCH/TPC 부호 | 대응 없음 (polar/BCH/turbo는 대응 없음 명시) | Prime ECC는 binary QC-LDPC 전용 |
| 1-bit ADC(=BSC) 채널 | `channel.cpp` (Prime ECC는 hard-1bit/soft-2~3bit) | Prime ECC hard-1bit와 개념 겹치나 신규 기여 없음 |

적용 가치: **낮음** — 신규 기법 없는 비교 survey이며, 다루는 부호 다수가 Prime ECC(binary QC-LDPC)와 무관하고 교과서 수준 재사용에 그침.

### D. JSON 블록

```json
{
  "id": "arxiv:2211.10712v1",
  "title": "Comparison of different coding schemes for 1-bit ADC",
  "year": 2022,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "1024",
  "soft_quant": "무관",
  "key_contribution": "AWGN+1-bit ADC(=BSC) 채널에서 Polar/LDPC/Product/BCH FER 비교·부호선택 가이드 제시",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "신규 기법 없음(기존 부호 비교 survey), N~1024 단길이, 1-bit ADC(hard) 채널 특화, LDPC는 후보 중 하나일 뿐",
  "todo_check": "없음(교과서/비교 수준, Prime ECC 이식 대상 아님)"
}
```
