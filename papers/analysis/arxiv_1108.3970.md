### arxiv:1108.3970v2 - A Design Methodology for Folded, Pipelined Architectures in VLSI Applications using Projective Space Lattices (2012, arXiv cs.AR)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 미상 |
| 핵심기여 | Projective-Geometry 기반 circulant 이분그래프 DFG를 임의 factor로 folding하며 interconnect가 fold 간 정적으로 유지(edge overlay)되고 memory-conflict-free한 semi-parallel VLSI 설계 방법론 + C++ 합성툴 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | PG(finite geometry) 유래 circulant 이분그래프 전용 folding이며, Prime ECC의 QC-LDPC(base+circulant) 및 min-sum 파이프라인과 구조·부호가 상이 |
| 추가확인 | folding schedule의 memory-conflict-free 아이디어가 QC-LDPC z=32 병렬 라우팅에 부분 참고 가능한지(단, PG 전용 circulance 가정 의존) |

> 총평: PG 이분그래프 기반 folded/pipelined VLSI 설계 방법론(부호가 아닌 아키텍처 논문)으로, LDPC 디코더는 예시 응용일 뿐이며 NAND용 QC-LDPC min-sum 디코더/HW에 직접 이식할 알고리즘·부호 산출물은 없음.

### B. 알고리즘 요약

1. 대상: Data Flow Graph가 Projective Geometry(점-초평면 incidence) 기반 balanced regular circulant 이분그래프인 응용(LDPC/expander 디코딩, 행렬연산)의 semi-parallel(folded) VLSI 아키텍처.
2. 풀려는 문제: 완전병렬은 노드 수(수만 개)만큼 LPU가 필요해 면적·비용 과다 → 면적 절감·확장성 위해 folding하되 interconnect 재구성 오버헤드 없이 스케줄링.
3. 핵심 가정: PG 이분그래프의 circulance(`(i+j) mod n`)와 modulo 산술 → 노드 수 `J=(p^{s(n+1)}-1)/(p^s-1)`, degree `γ=(p^{sn}-1)/(p^s-1)`.
4. 핵심 기법 1(Theorem 1): `J`의 임의 인수 `q`로 folding해도 `J/q` LPU/LMU로 folded perfect access pattern 생성 가능(Karmarkar perfect access primitive 확장), memory-conflict-free.
5. 핵심 식 의미: `(a_yjk mod J/q)=(a_xjk mod J/q)` → 서로 다른 fold의 edge가 완전히 overlay되어(Theorem 3) fold 전환 시 배선·MUX 재구성이 불필요(정적 interconnect).
6. 핵심 기법 2: 소수 `J`는 dummy 노드 `α`를 추가해 circulance 유지하며 factorizable하게 확장(Algorithm 1).
7. 구현 디테일: dual-port PMU에 2-input씩 처리, `γ/2` bin·linear 주소 counter, 2-to-ρˆ/ρˆ-to-2 스위치를 LUT 스케줄로 구동, SpecC식 4단계 refinement로 RTL 방출.
8. 파이프라이닝: graph/architecture/micro 3레벨 다단 파이프라인으로 folding에 의한 throughput 손실 회복(2nd design option은 coarse-grained 파이프라인).
9. 결과: P(3,GF(4)) 15-노드 bit-flipping 디코더 prototype(fold=3, 5+5 PPU/PMU)에서 iteration당 63 cycle(unfolded 35), throughput 감소를 q=3에서 1.8배로 완화; 별도 soft-decision LDPC 디코더(특허)와 (1953,1197,761) expander(RS 부분부호) DVD-R 디코더를 Xilinx Virtex-5 FPGA에 구현; C++ 합성툴 공개.
10. 한계: PG 유래 circulant 이분그래프 전용, 특정 부호(부호rate/length/연판정 명시 없음), gatecount/throughput 수치 본문 미기재, min-sum 등 LDPC 복호 알고리즘 자체는 다루지 않음(아키텍처만).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| folding/memory-conflict-free scheduling(PG circulant) | 대응 없음 | Prime ECC는 z=32 row 병렬 QC-LDPC 고정 파이프라인으로 PG 유래 folding 스케줄러가 없음 |
| 정적 interconnect / edge overlay(스위치 재구성 제거) | 디코더 HW 모델(decoder.cpp, z=32/HCU/GT) | 라우팅 절감 아이디어는 유사하나 PG circulance 가정 의존이라 QC circulant와 정합 부담 |
| PG-LDPC / expander(RS 부분부호) 부호구조 | H-matrix 로드(ecc_top.cpp) | Prime ECC의 binary QC-LDPC(base+shift)와 부호군이 상이 |
| bit-flipping / soft-decision 디코딩(예시 응용) | `LDPC_Decoder()`(decoder.cpp) | 논문은 알고리즘이 아닌 아키텍처 골격만 제공, min-sum 대체 요소 없음 |

적용 가치: **낮음** — PG circulant 이분그래프 전용 folded VLSI 설계 방법론이라, NAND용 QC-LDPC min-sum 디코더/HW의 부호·병렬구조와 정합되지 않고 떼어낼 알고리즘 산출물이 없음(라우팅 정적화 아이디어만 참고 수준).

### D. JSON 블록

```json
{
  "id": "arxiv:1108.3970v2",
  "title": "A Design Methodology for Folded, Pipelined Architectures in VLSI Applications using Projective Space Lattices",
  "year": 2012,
  "venue": "arXiv cs.AR",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "기타",
  "code_rate": "미상",
  "code_length": "미상",
  "soft_quant": "미상",
  "key_contribution": "Projective-Geometry 기반 circulant 이분그래프 DFG를 임의 factor로 folding하며 interconnect가 fold 간 정적으로 유지(edge overlay)되고 memory-conflict-free한 semi-parallel VLSI 설계 방법론 + C++ 합성툴",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "PG(finite geometry) 유래 circulant 이분그래프 전용 folding이며, Prime ECC의 QC-LDPC(base+circulant) 및 min-sum 파이프라인과 구조·부호가 상이",
  "todo_check": "folding schedule의 memory-conflict-free 아이디어가 QC-LDPC z=32 병렬 라우팅에 부분 참고 가능한지(단, PG 전용 circulance 가정 의존)"
}
```
