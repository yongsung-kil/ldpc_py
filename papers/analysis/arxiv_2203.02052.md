### arxiv:2203.02052v3 - A Unified Spatially Coupled Code Design: Threshold, Cycles, and Locality (2022, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | SC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | partitioning matrix 등가류 축소로 SC-LDPC의 threshold(waterfall)와 cycle-6(error-floor)를 결합 최적화하는 통합 설계 프레임워크 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | SC-LDPC 구조 전용(sub-block locality 포함)이라 Prime의 고정 QC-LDPC 블록부호와 구조 불일치, HW/gatecount 없음 |
| 추가확인 | cycle-6/threshold 결합 최적화 아이디어를 SC 없이 순수 block QC-LDPC partitioning에 적용 가능한지 |

> 총평: SC-LDPC의 partitioning matrix 설계를 등가류로 효율 탐색해 waterfall/error-floor를 동시 개선하나, spatial coupling·locality 구조 전용이고 자기 검증은 magnetic recording/AWGN 시뮬뿐이라 NAND block QC-LDPC 이식성은 낮음.

### B. 알고리즘 요약

1. 코드: circulant-based(CB) lifting SC-LDPC, protograph `B=1_{γ×κ}`를 memory `m=1`로 `B0+B1`로 분할, 결합길이 `l`, 시뮬 파라미터 `κ=11, z=67, γ=3, l=5`.
2. 문제: 기존 SC-LDPC 설계가 asymptotic(threshold)와 finite-length(cycle) 중 하나만 다뤄, 두 regime(저SNR waterfall / 고SNR error-floor)을 동시 최적화하지 못함.
3. 핵심관찰: SC 코드 성능은 작은 `partitioning matrix P`(∈{0,1,⋆}^{γ×κ})의 특성으로 결정 → 거대한 full H 대신 P만 탐색.
4. 핵심기법1(탐색공간 축소): 행/열 permutation으로 동치인 P를 하나만 남김. column type 분포 `n(B)`와 stars-and-bars로 `γ=2,3`에 대한 nonequivalent 행렬 수 `|K_{κ,γ}|` closed-form 유도(예 `κ=11,γ=3`이면 6080개, 전체 대비 10^6배 축소).
5. 핵심식 의미: lifted 그래프의 cycle-6은 overlap parameter `t_{...}`로 세고(식 3-4), power matrix 조건 `Σ c_{i,j}=0 (mod z)`(식 10)로 z배 증폭 여부 판정 → cycle 계수를 P 수준에서 빠르게 계산.
6. 핵심기법2(결합설계): 각 P의 cycle-6 수와 EXIT threshold `σ*`를 계산, cycle과 threshold 양쪽에서 열등하지 않은 후보만 남겨 cycle-driven(CD)~threshold-driven(TD) 트레이드오프 리스트 출력.
7. 확장(locality): sub-block locality(SC-LDPCL)로 확장, CCN/LCN 설계 분리. threshold 계산을 `σ*(B0)` 하한 proxy로 대체, local code에 balanced/unbalanced irregular 구성 제안.
8. 최적화: EXIT method로 threshold, brute-force+구조활용으로 cycle 계수. NN/GA 없음.
9. 결과: CD가 CV 대비 cycle-6 54% 감소, BER은 고SNR(5dB)에서 CV 대비 1자릿수 개선; TD는 저SNR(2.5dB)에서 waterfall 개선. PR(magnetic recording) 채널에서도 CD가 14dB에서 1자릿수 개선(min-sum 디코더, 20 global/200 local iter).
10. 한계: HW/gatecount/throughput 없음, code rate/length 본문 서술 없음(미상), SC coupling·sub-block locality 구조가 필수라 non-SC block QC-LDPC로 직접 이식 불가.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| partitioning/H-matrix 부호설계 | ecc_top.cpp Load_PCM() | H-matrix 로드 지점이나, 논문은 SC-LDPC partitioning 전용이라 block QC-LDPC 구조와 상이 |
| cycle/threshold 기반 부호설계 | 대응 없음 | Prime의 QC-LDPC H는 고정, SC coupling·locality 구조는 미보유 (이식난이도 최상 §4) |
| min-sum BP 디코딩 | decoder.cpp LDPC_Decoder() | 논문도 min-sum 사용하나 이는 Prime이 이미 보유(§3 중복) |
```

적용 가치: **낮음** — waterfall/error-floor 동시 최적 설계철학은 유용하나, spatial coupling + sub-block locality 구조 전용이고 Prime의 고정 block QC-LDPC와 정합되지 않으며 HW 설계·rate/length 정보도 부재해 직접 이식 곤란.

### D. JSON 블록

```json
{
  "id": "arxiv:2203.02052v3",
  "title": "A Unified Spatially Coupled Code Design: Threshold, Cycles, and Locality",
  "year": 2022,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "SC-LDPC",
  "code_rate": null,
  "code_length": null,
  "soft_quant": "무관",
  "key_contribution": "partitioning matrix 등가류 축소로 SC-LDPC의 threshold와 cycle-6를 결합 최적화하는 통합 설계 프레임워크",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "하",
  "caveat": "SC-LDPC(sub-block locality 포함) 구조 전용이라 Prime의 고정 block QC-LDPC와 구조 불일치, HW/gatecount 없음",
  "todo_check": "cycle-6/threshold 결합 최적화를 SC 없이 순수 block QC-LDPC partitioning에 적용 가능한지"
}
```
