### arxiv:0904.0747v1 - Bethe Free Energy Approach to LDPC Decoding on Memory Channels (2009, arXiv / submitted to IEEE Trans. Commun.)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5~0.875 |
| 부호length | 495~4095 |
| 연판정 | 무관 |
| 핵심기여 | PR/ISI 채널에서 Bethe free energy로 joint 검출+복호 BP 방정식 유도, turbo equalization 능가 및 error floor 없음 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | pair-wise ISI(L=1, h(D)=1-αDⁿ)에만 exact, NAND memoryless 채널엔 표준 BP로 환원되어 이점 소멸 |
| 추가확인 | NAND inter-cell interference를 pair-wise ISI로 근사 가능한지(그럴 때만 의미) |

> 총평: PR/ISI 기록·통신 채널용 joint equalization+decoding으로, memoryless NAND에는 표준 BP로 축소되어 이식 가치 낮음.

### B. 알고리즘 요약

1. 시스템: 선형 ISI(PR) 채널 `h(D)=1-αDⁿ`(-1≤α≤1) + AWGN 상의 LDPC 부호(regular/quasi-regular, rate 0.5~0.875, length 495~4095), Dicode `h(D)=1-D` 중심 평가.
2. 문제: PR 채널에서 검출과 복호를 분리(turbo equalization)하면 BCJR의 순차성 탓에 지연·복잡도가 큼; 이를 joint로 풀고자 함.
3. 모델: LDPC 체크노드 `fα` + ISI 노드 `fℵ`를 결합한 tripartite factor graph로 joint inference 정의.
4. 핵심 기법: Bethe free energy `F=U-H`를 belief에 대해 최소화하여 편미분→ 변수↔체크 field `ηiα`, 변수↔ISI field `ηiℵ`에 대한 BP 방정식 (28)(29) 유도.
5. 식 의미: ISI 항 `tanh⁻¹(tanh ηiℵ · tanh Qℵ)`가 pair-wise 메모리(`Qp=s²Σhk·hk+p`)를 정확 반영; ISI 없으면(Qℵ=0) 표준 memoryless BP로 환원.
6. 확장: `h(D)=1-αDⁿ` 일반 PR로 확장, 단 3개 이상 변수 얽힌 ISI는 loop 발생으로 suboptimal.
7. 구현 디테일: 초기 `μiβ,ζiℵ=0`, 이전 iteration 값으로 갱신하여 심볼 단위 fully-parallel 구조 모사; 코드워드 앞뒤 심볼 상태 known 가정.
8. 최적화 절차: 없음(고정 반복 message-passing, 20~80 iteration).
9. 결과: Dicode 채널에서 turbo equalization 대비 BER=10⁻⁷~10⁻⁸서 0.15~0.8 dB 이득, BER 10⁻⁹ 이하까지 error floor 관측 안 됨; 지연은 iteration 수에만 의존(codeword length 무관).
10. 한계: HW 미설계·시뮬만, full-tanh sum-product 기반, PR/ISI 채널 특화(NAND 무관).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| joint 검출+복호 BP 이터레이션 | decoder.cpp `LDPC_Decoder()`, `C2V_Cal()` | PR-BP는 표준 BP에 ISI node 항 추가일 뿐; NAND는 memoryless라 해당 항 불필요 |
| full-tanh sum-product 연산 | 대응 없음 | Prime ECC는 min-sum 사용, full-`tanh` Sum-Product 미채용 |
| ISI/PR 채널 항 `Qℵ`, 초기 likelihood `ui` | channel.cpp `Set_LLR_Th()` | Prime ECC 채널은 AWGN/RBER memoryless, PR 메모리 항 미지원 |

적용 가치: **낮음** — NAND는 memoryless 채널이라 PR-BP가 표준 BP로 환원되고, full-tanh·ISI 노드 machinery는 Prime ECC(min-sum, memoryless)와 정합되지 않음.

### D. JSON 블록

```json
{
  "id": "arxiv:0904.0747v1",
  "title": "Bethe Free Energy Approach to LDPC Decoding on Memory Channels",
  "year": 2009,
  "venue": "arXiv (submitted to IEEE Trans. Commun.)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": null,
  "code_length": "495~4095",
  "soft_quant": "무관",
  "key_contribution": "PR/ISI 채널에서 Bethe free energy로 joint 검출+복호 BP 방정식 유도, turbo equalization 능가 및 error floor 없음",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "하",
  "caveat": "pair-wise ISI(L=1, h(D)=1-αDⁿ)에만 exact, NAND memoryless 채널엔 표준 BP로 환원되어 이점 소멸",
  "todo_check": "NAND inter-cell interference를 pair-wise ISI로 근사 가능한지(그럴 때만 의미)"
}
```
