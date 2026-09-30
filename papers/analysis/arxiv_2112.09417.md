### arxiv:2112.09417v1 - Concatenated Code Design for Constrained DNA Data Storage with Asymmetric Errors (2021, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | protograph |
| 부호rate | 0.5, 0.8 |
| 부호length | 300~1000 bit (정보블록) |
| 연판정 | 무관 |
| 핵심기여 | VL-RLL 제약부호 + protograph LDPC 하이브리드 구조와 DNA 비대칭치환채널용 LLR 계산으로 시퀀싱 에러 정정 |
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
| 한계,주의 | LDPC는 표준 AR4JA protograph + 재래식 BP 재사용, 기여는 DNA 제약부호·비대칭채널 LLR 유도에 국한 (NAND 무관) |
| 추가확인 | DNA 비대칭채널 LLR 유도가 NAND asymmetric RBER 모델에 시사점 있는지 (원거리) |

> 총평: DNA 데이터 저장용 제약부호 아키텍처 논문으로 LDPC 부분은 표준 protograph+BP 재사용에 그치고, 신규성은 DNA 시퀀싱 비대칭채널 특화 LLR·인코딩 파이프라인이라 NAND binary QC-LDPC 이식가치 낮음.

### B. 알고리즘 요약

1. 시스템: DNA 데이터 저장 — homopolymer run ≤3nt 제약 하에서 A/T/C/G 비대칭 치환에러 정정, 정보블록 300bit(Illumina)/1000bit(Nanopore).
2. 문제: 기존 strand-level outer code는 단일 뉴클레오타이드 에러도 방치, VL-RLL 제약부호의 error-propagation이 재래식 block code보다 심각.
3. 모델: Nanopore(`p1=4α,p2=α,p3=0.01,p4≈0`)·Illumina(`pa=1.5β,pb=β`) 두 비대칭 치환에러 채널 모델과 용량 유도.
4. 핵심기법1: `(4,0,2)` 제약계용 VL-RLL 부호(basic set `{1,2,3,01,...,003}`, Huffman 매핑)로 `1.976 bits/nt` 부호효율 달성.
5. 핵심 설계: LDPC 인코딩을 제약매핑 **이후**로 이동 — 저장 실체(제약부호워드)에서 채널에러를 먼저 정정해 역-VL-RLL의 에러전파 차단.
6. 핵심기법2: 리던던시용 modified VL-RLL(`11111X→003` fuzzy bit)로 동기화 문제 회피, `Rred≈2 bits/nt`.
7. 부수 디테일: quaternary→binary interim mapping(A00/T01/G10/C11), 이웃 2뉴클레오타이드 결합으로 transition symbol '3'의 매핑확률 `pw=41/42` 유도.
8. 복호: 비대칭채널 확률로 각 부호비트 초기 LLR `L0=log(Pr(b=0)/Pr(b=1))` 산출 후 표준 belief propagation(BP) 복호 — AR4JA protograph LDPC(rate 1/2, 4/5) 사용.
9. 결과: [11] 대비 재래식 BP만으로도 BER 우위, 전체 부호효율 `~1.988(Nanopore)/1.981(Illumina) bits/nt`(상한 2에서 1% gap).
10. 한계: HW 미설계·시뮬만, LDPC는 표준 AR4JA+BP 재사용, DNA 시퀀싱 채널 전용(향후 채널 맞춤 LDPC 최적화 예정).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 표준 belief propagation(BP) 복호 | `decoder.cpp` `LDPC_Decoder()` (원거리) | 우리는 min-sum 근사, 논문은 full-BP·DNA 채널 전용 — 직접 이식성 낮음 |
| DNA 비대칭채널 초기 LLR 계산 | `channel.cpp` `Set_LLR_Th()` (원거리) | asymmetric 채널 LLR 개념만 유사, DNA A/T/C/G 4-심볼 특화라 NAND read와 무관 |
| AR4JA protograph 부호구조 | `ecc_top.cpp` `Load_PCM()` (원거리) | protograph≠우리 고정 QC-LDPC, 부호설계 이식 부담 큼 |
| VL-RLL 제약부호 / 매핑 파이프라인 | 대응 없음 | DNA homopolymer 제약 전용, NAND ECC에 무관 |

적용 가치: **낮음** — LDPC 요소는 표준 AR4JA protograph+재래식 BP 재사용이고 신규 기여는 DNA 시퀀싱 제약부호·비대칭채널 LLR로, NAND binary QC-LDPC 디코더/HW에 떼어 쓸 실체가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2112.09417v1",
  "title": "Concatenated Code Design for Constrained DNA Data Storage with Asymmetric Errors",
  "year": 2021,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "protograph",
  "code_rate": "0.5/0.8",
  "code_length": "300~1000bit(정보블록)",
  "soft_quant": "무관",
  "key_contribution": "VL-RLL 제약부호 + protograph LDPC 하이브리드 구조와 DNA 비대칭치환채널용 LLR 계산으로 시퀀싱 에러 정정",
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
  "caveat": "LDPC는 표준 AR4JA protograph + 재래식 BP 재사용, 기여는 DNA 제약부호·비대칭채널 LLR 유도에 국한 (NAND 무관)",
  "todo_check": "DNA 비대칭채널 LLR 유도가 NAND asymmetric RBER 모델에 시사점 있는지 (원거리)"
}
```
