### arxiv:2602.21124v1 - Quantum Approximate Optimization for Decoding of Low-Density Parity-Check Codes (2026, arXiv quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.33~0.5 |
| 부호length | 6~8 |
| 연판정 | soft-4bit+ |
| 핵심기여 | LDPC 복호를 패리티+채널 LLR Ising Hamiltonian 최소화로 정식화해 QAOA로 전역 최적화 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | N/A |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | 양자회로(QAOA) 기반이라 고전 HW 디코더에 이식 불가, 검증 부호가 [6,2]~[8,4] 초단길이뿐 |
| 추가확인 | 실용 블록길이(수천 bit)로의 확장성 및 큐빗 수·회로깊이 요구량 |

> 총평: 양자 QAOA 디코더로 아이디어는 참신하나 초단길이 시뮬뿐이고 고전 NAND binary QC-LDPC HW와 완전히 다른 계산 패러다임이라 이식 불가.

### B. 알고리즘 요약

1. 대상: 고전 선형블록/LDPC 부호, BPSK+AWGN 채널, 실험 부호는 `[n,k]=[6,2],[7,3],[8,4]`의 초단길이.
2. 문제: BP는 국소 message-passing이라 short cycle·trapping set에서 수렴 실패/국소최적에 빠짐.
3. 모델: 비트 `xi∈{0,1}`를 Ising 스핀 `Zi=(-1)^xi∈{+1,-1}`로 매핑, 패리티 제약 `∏_{i∈c}Zi=1`.
4. 핵심 1단 - 패리티 Hamiltonian `Hparity(Z)=Σ_c (1/2)(1-∏_{i∈c}Zi)`: 모든 패리티 만족 시 0, 위반 시 양의 에너지.
5. 핵심 2단 - 채널 Hamiltonian `Hchannel(Z)=Σ_i (|hi|/2)(1-sign(hi)Zi)`, `hi`=채널 LLR; 채널 관측과 일치할수록 저에너지.
6. 총 비용 `H=Hparity+Hchannel`의 최소값이 곧 패리티 만족 + 채널 최대일치 codeword (Theorem 1).
7. QAOA ansatz `|γ,β⟩=Π_j e^{-iβj HM} e^{-iγj HP}|s⟩`, 믹싱 `HM=Σ Xj`, 초기 `|+⟩^⊗n`, 회로깊이 `l=10`.
8. 최적화: parameter-shift rule로 gradient 해석적 계산, momentum 기반 gradient descent로 `(γ,β)` 갱신.
9. 결과: `σ∈{1,1.5,2}`에서 100회 시행, 성공확률이 BP 대비 우세(예 [6,2] σ=1: BP 0.82→QAOA 0.83, σ=2: 0.44→0.62).
10. 한계: HW 미설계, 검증 부호가 n=6~8 초단길이뿐, 실블록길이 확장성 미검증.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QAOA 양자 디코더 (Ising Hamiltonian 최소화) | 대응 없음 | 양자회로 기반이라 고전 min-sum HW 디코더에 대응 불가 |
| 채널 LLR penalty (`Hchannel`) | channel.cpp `Set_LLR_Th()` | LLR 사용 개념만 공유, 양자 penalty로는 이식 불가 |
| 패리티 제약 인코딩 (`Hparity`) | decoder.cpp `LDPC_Decoder()` | 동일 패리티 개념이나 알고리즘 구조 완전 상이 |

적용 가치: **낮음** — 양자 QAOA 디코더로 고전 binary QC-LDPC HW 파이프라인과 계산 패러다임이 근본적으로 달라 이식 불가.

### D. JSON

```json
{
  "id": "arxiv:2602.21124v1",
  "title": "Quantum Approximate Optimization for Decoding of Low-Density Parity-Check Codes",
  "year": 2026,
  "venue": "arXiv quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "6~8",
  "soft_quant": "soft-4bit+",
  "key_contribution": "LDPC 복호를 패리티+채널 LLR Ising Hamiltonian 최소화로 정식화해 QAOA로 전역 최적화",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "N/A",
  "latency": "악화",
  "recommend": "하",
  "caveat": "양자회로(QAOA) 기반이라 고전 HW 디코더에 이식 불가, 검증 부호가 [6,2]~[8,4] 초단길이뿐",
  "todo_check": "실용 블록길이로의 확장성 및 큐빗 수·회로깊이 요구량"
}
```
