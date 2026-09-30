### arxiv:2601.22470v1 - 5G LDPC Codes as Root LDPC Codes via Diversity Alignment (2026, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | protograph |
| 부호rate | 0.478(BG1 22/46), 0.417(BG2 10/24) |
| 부호length | 11040(BG1), 480(BG2) |
| 연판정 | 무관 |
| 핵심기여 | Boolean 근사 기반 diversity evolution(DivE)로 5G-NR LDPC의 VN-블록 매핑을 탐색해 정보비트 full diversity 달성 |
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
| 한계,주의 | block-fading(무선) 특화, M=2만, NAND AWGN/RBER 채널과 무관하며 부호구조 변경 없이 매핑만 최적화 |
| 추가확인 | M>2 확장 시 복잡도, high-rate NAND용 QC-LDPC에서 diversity 개념 적용 가능성 |

> 총평: 5G-NR LDPC의 block-fading diversity를 VN-블록 매핑으로 확보하는 무선 특화 이론/시뮬 연구로 NAND binary LDPC ECC 이식성 낮음.

### B. 알고리즘 요약

1. 시스템: 5G-NR protograph QC-LDPC(BG1 `Z=240`,`N=11040`; BG2 `Z=20`,`N=480`)를 M=2 block-fading channel(BPSK)로 전송.
2. 문제: AWGN 최적화된 표준 LDPC는 nonergodic block-fading에서 diversity order가 Singleton-like bound에 못 미쳐 성능 저하.
3. 모델: 각 fading block 계수 `hm ~ CN(0,1)`, diversity order `dc = -lim(logPe/logγ)`, full diversity는 `dc = M`.
4. 핵심기법1(DivE): fading을 Boolean 지시자 `Am = 1_{|hm|^2·γ≥ρ0}`로 근사, min-sum 메시지의 fading 의존성을 CN=AND, VN=OR의 Boolean message passing으로 iteration별 추적.
5. 핵심식: VN 출력 Boolean fading 함수가 `A0+...+A(M-1)` 형태면 full diversity → 각 VN diversity order를 직접 판정.
6. 핵심기법2(generalized rootcheck): iteration 진행 중 incoming 메시지가 full-diversity거나 동일 single-block(`Am`)이면 CN이 generalized rootcheck 형성, 반복으로 full diversity VN 증가.
7. 구현 디테일: 큰 M에서 Boolean 대수 대신 truth table(Karnaugh) 방식 FadingMSD로 2^M realization 수치평가하여 함수 구성.
8. 탐색절차: pre-assignment 3종(stopping set 방지/parity VN 공통블록/punctured VN 처리) 후 greedy randomized block-mapping search, 실패 시 parity VN 추가로 rate 하향.
9. 결과: BG1 8th iter에 정보 22 VN 전부, BG2 7th iter에 10 VN 전부 full diversity; random 매핑 대비 high-SNR slope 급경사·낮은 BLER, 더 높은 rate에서 full diversity 유지.
10. 한계: HW 미설계, 시뮬만, M=2 한정, block-fading(무선) 채널 전제로 NAND 채널과 무관.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| protograph QC-LDPC 구조/부호 로드 | ecc_top.cpp Load_PCM() | 부호구조 참조는 겹치나 block-fading 매핑 개념은 NAND 무관 |
| min-sum 메시지 업데이트(분석용) | decoder.cpp C2V_Cal(), CNU_Update_New_Mag() | 논문은 diversity 분석용 lower bound로만 사용, 알고리즘 개선 아님 |
| VN-블록 매핑/diversity alignment | 대응 없음 | NAND는 block-fading 없음 |
```

적용 가치: 낮음 — block-fading 무선 채널 전용 diversity 최적화로 NAND AWGN/RBER 환경엔 이식 근거 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2601.22470v1",
  "title": "5G LDPC Codes as Root LDPC Codes via Diversity Alignment",
  "year": 2026,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "protograph",
  "code_rate": null,
  "code_length": "11040(BG1), 480(BG2)",
  "soft_quant": "무관",
  "key_contribution": "Boolean 근사 기반 diversity evolution(DivE)로 5G-NR LDPC의 VN-블록 매핑을 탐색해 정보비트 full diversity 달성",
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
  "caveat": "block-fading(무선) 특화, M=2만, NAND AWGN/RBER 채널과 무관하며 부호구조 변경 없이 매핑만 최적화",
  "todo_check": "M>2 확장 시 복잡도, high-rate NAND용 QC-LDPC에서 diversity 개념 적용 가능성"
}
```
