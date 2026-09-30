### arxiv:2406.01426v1 - High Throughput Polar Code Decoders with Information Bottleneck Quantization (2024, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.5 |
| 부호length | 128~1024 |
| 연판정 | soft-4bit+ |
| 핵심기여 | Fast-SSC Polar 디코더에 IB 기반 비균일 양자화(RCQ)를 적용해 4bit로 5bit FP 수준 성능 달성 |
| HW설계 | O |
| 검증수준 | ASIC합성 |
| 복잡도 | 0.822mm2@12nm (P(1024,512), area 아닌 gatecount는 미상) |
| 병렬화 | 완전병렬 |
| Throughput | 0.768 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | 동등 |
| 추천도 | 하 |
| 한계,주의 | Polar 전용(Fast-SSC 트리 노드 f/g/REP/SPC), binary QC-LDPC와 알고리즘 구조 상이 |
| 추가확인 | IB/RCQ 양자화 아이디어 자체를 LDPC min-sum LLR 테이블에 접목 가능한지(단 논문 본문은 LDPC IB가 이미 잘 연구됐다고 명시) |

> 총평: Polar 코드 대상 IB 양자화 HW 논문으로, binary QC-LDPC ECC에 직접 이식할 부분은 없고 양자화 철학만 참고 가치.

### B. 알고리즘 요약

1. 대상은 5G/6G용 Polar 코드 `P(N,K)`, N=128/1024, R=0.5, AWGN+BPSK 채널, 완전 unrolled·pipelined 고throughput 디코더.
2. 문제: 저bit-width 양자화는 면적/전력/throughput에 유리하나 정정성능이 열화 → 좋은 trade-off 필요.
3. 핵심 기법: Information Bottleneck(IB) 방법으로 관측 LLR `Y`(10bit, 1024 bin)를 상호정보 `I(T;X)` 손실 최소화하며 `|T|=16`(4bit)로 압축하는 비균일 양자화 매핑 `p(t|y)` 생성.
4. 각 PFT edge마다 density evolution으로 100K+ 샘플을 모아 결합분포 `p(x;y)`를 얻고 Symmetric IB 알고리즘으로 edge별 압축 매핑 계산.
5. LUT 폭발 문제(g함수 LUT 크기 `2·|T|^2`)를 RCQ 스킴으로 해결: 연산 전 작은 up-scale LUT로 균일 FP 복원 → FP 도메인 연산 → down-scale LUT로 재양자화.
6. 채널 대칭성(BPSK)을 이용해 magnitude만 저장 → LUT를 절반(`2^{Q-1}`)으로 축소, g함수 LUT 총 32엔트리로 감소.
7. Fast-SSC 노드별 처리: f함수/SPC는 IB 도메인에서 직접(LUT 불필요), g/REP/h1은 RCQ 적용, SM↔TC 표현 변환으로 비교는 magnitude, 덧셈은 TC로 수행.
8. 구현: 12nm FinFET, Design Compiler 합성 + IC-Compiler P&R, 7개 설계(N=128@500MHz, N=1024@750MHz).
9. 결과: P(1024,512)에서 IB 4bit가 FP 5bit 대비 면적 -15%, area eff +18%, energy eff +15%, FER 1e-7에서 오히려 성능 우위. FP 6bit 대비 0.2dB 손실 감수 시 area eff +41%.
10. 한계: Polar/Fast-SSC 전용 아키텍처(트리 노드 기반), 정정능력 향상이 아닌 저bit 유지가 목적, LDPC로의 직접 전이는 미다룸.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| IB 비균일 양자화 매핑 (LLR→bin) | channel.cpp `Set_LLR_Th()`, `ecc_data.h` `PARAM_LLR` | 양자화 철학만 유사, Polar edge별 LUT는 QC-LDPC LLR 테이블과 구조 상이 |
| RCQ up/down-scale LUT | 대응 없음 | Prime ECC는 min-sum magnitude 양자화 테이블 사용, RCQ LUT 미도입 |
| Fast-SSC f/g/REP/SPC 노드 | 대응 없음 | Polar 트리 디코딩 전용, LDPC min-sum CN/VN과 무관 |
| 완전 unrolled pipeline | `decoder.cpp` pipeline (6-stage) | 개념적 유사(pipeline)나 Polar unrolled tree ≠ LDPC iterative 구조 |

적용 가치: **낮음** — Polar 전용 디코더로 binary QC-LDPC에 이식할 알고리즘 요소가 없고, IB 양자화 자체는 논문도 LDPC에서 이미 성숙했다고 명시하여 신규성 낮음.

### D. JSON 블록

```json
{
  "id": "arxiv:2406.01426v1",
  "title": "High Throughput Polar Code Decoders with Information Bottleneck Quantization",
  "year": 2024,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": 0.5,
  "code_length": "128~1024",
  "soft_quant": "soft-4bit+",
  "key_contribution": "Fast-SSC Polar 디코더에 IB 기반 비균일 양자화(RCQ)를 적용해 4bit로 5bit FP 수준 성능 달성",
  "hw_designed": "O",
  "verification": "ASIC합성",
  "complexity": "0.822mm2@12nm",
  "parallelism": "완전병렬",
  "throughput_gbps": 0.768,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "동등",
  "recommend": "하",
  "caveat": "Polar 전용(Fast-SSC 트리 노드 f/g/REP/SPC), binary QC-LDPC와 알고리즘 구조 상이",
  "todo_check": "IB/RCQ 양자화 아이디어를 LDPC min-sum LLR 테이블에 접목 가능한지(단 논문은 LDPC IB가 이미 성숙했다고 명시)"
}
```
