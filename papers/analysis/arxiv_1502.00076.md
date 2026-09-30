### arxiv:1502.00076v1 - Design of a Unified Transport Triggered Processor for LDPC/Turbo Decoder (2015, arXiv:cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5 |
| 부호length | 648 |
| 연판정 | soft-4bit+ |
| 핵심기여 | Turbo/LDPC 공용 function unit(ALPHA, BetaLLR)을 갖는 TTA 프로그래머블 프로세서 설계 |
| HW설계 | O |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 0.01012Gbps |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | min-sum이 아닌 forward-backward trellis 기반 supercode sum-product를 사용해 Prime ECC의 min-sum CN 구조와 이질적 |
| 추가확인 | Turbo와 공용화를 위한 설계라 LDPC 단독 최적화 대비 throughput/복잡도 손해가 어느 정도인지 미상 |

> 총평: Turbo/LDPC 통합 ASIP 아키텍처 논문으로 부호설계·디코더 알고리즘 자체의 이식 요소가 없어 NAND binary QC-LDPC에는 참고가치 낮음.

### B. 알고리즘 요약

1. 대상 코드: 3GPP турбо 코드(6144비트, sliding window MAP) + IEEE 802.11n QC-LDPC (rate 1/2, N=648).
2. 문제: Turbo와 LDPC 디코더를 별도 HW로 만들면 재사용성이 없어 로밍/멀티모드 지원이 비효율적 → 하나의 프로그래머블 프로세서로 통합.
3. Turbo는 max-log-MAP(트렐리스 forward-backward), LDPC는 min-sum 근사 대신 M개 파리티 행을 이진 2-state trellis(supercode)로 분해한 trellis 기반 sum-product를 사용해 두 알고리즘의 연산 형태를 통일.
4. 핵심 변수: forward metric `αk(s)`, backward metric `βk(s)`, LLR 갱신은 `Lok = 1/2[max*{αk-1(s)+βk(s)} - max*{αk-1(s)+βk(s⊕1)}]`.
5. LDPC의 branch metric은 LLR 값 하나, Turbo는 3개 LLR 조합(`γ1~γ4`)이라는 차이만 있고 연산 구조(`max*` 재귀)는 동일 → 공용 function unit(ALPHA, BetaLLR) 설계 근거.
6. 레이어드 스케줄(layered schedule)을 LDPC 메시지 플로우로 채택, `A(n)` 누적 LLR을 행 단위로 갱신.
7. HW 특화: ALPHA unit(3입력2출력), BetaLLR unit(5입력4출력)을 4개씩 배치해 4개 supercode/butterfly 병렬 처리, LSU/ALU/GCU/레지스터파일/30개 버스로 TTA 구성, LLR 출력은 FIFO(STREAM 유닛).
8. 별도 학습/최적화 절차 없음 (고수준 C 언어로 TCE 툴 기반 프로세서 프로그래밍/설계).
9. 결과: 200MHz에서 Turbo 22.64Mbps(1 iteration), LDPC 10.12Mbps(5 iteration, 10,368 clock cycle/블록).
10. 한계: min-sum 대비 supercode trellis 방식이라 HW 구조가 표준 min-sum 디코더와 다르고, LDPC 단독 구현 대비 throughput이 타 프로그래머블 구현(15.2~257Mbps) 대비 낮음; ASIC 합성/실측 없이 사이클 시뮬 수준.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| supercode 기반 trellis sum-product (min-sum 아님) | 대응 없음 | Prime ECC는 min-sum(`CNU_Update_New_Mag()`) 기반이라 trellis forward-backward 구조와 이질적 |
| 레이어드 스케줄 | `decoder.cpp` `LDPC_Decoder()` | layered 메시지 갱신 개념은 유사하나 구현 방식(공유 유닛 시분할)은 이식 어려움 |
| Turbo/LDPC 공용 프로세서 아키텍처 | 대응 없음 | Prime ECC는 binary LDPC 전용 고정 파이프라인, ASIP형 범용 프로세서 개념과 무관 |

> 적용 가치: 낮음 - 알고리즘이 min-sum이 아닌 trellis 기반이며 목적이 Turbo/LDPC 겸용 ASIP 설계라 NAND 전용 고정 QC-LDPC 파이프라인에 이식할 요소가 거의 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1502.00076v1",
  "title": "Design of a Unified Transport Triggered Processor for LDPC/Turbo Decoder",
  "year": 2015,
  "venue": "arXiv:cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": 0.5,
  "code_length": 648,
  "soft_quant": "soft-4bit+",
  "key_contribution": "Turbo/LDPC 공용 function unit(ALPHA, BetaLLR)을 갖는 TTA 프로그래머블 프로세서 설계",
  "hw_designed": "O",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": 0.01012,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "min-sum이 아닌 forward-backward trellis 기반 supercode sum-product를 사용해 Prime ECC의 min-sum CN 구조와 이질적",
  "todo_check": "Turbo와 공용화를 위한 설계라 LDPC 단독 최적화 대비 throughput/복잡도 손해가 어느 정도인지 미상"
}
```
