### arxiv:0707.3925v1 - Use of a d-Constraint During LDPC Decoding in a Bliss Scheme (2007, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.906~0.955 |
| 부호length | 1728~6912 |
| 연판정 | soft-4bit+ |
| 핵심기여 | RLL d=1 제약을 factor graph의 별도 d-constraint 노드로 모델링하여 min-sum LDPC 디코딩에 결합, PSNR 약 0.25dB 이득 |
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
| 한계,주의 | RLL(Bliss scheme) 채널 특유의 run-length 제약을 전제로 한 기법으로 NAND에는 해당 제약이 존재하지 않음 |
| 추가확인 | d-constraint 노드가 순수 RLL 부호 구조에 종속적인지, 다른 형태의 사이드 정보(예: NAND 특유의 제약)로 일반화 가능한지 |

> 총평: 광저장 Bliss scheme의 RLL 제약을 LDPC factor graph에 보조 제약 노드로 결합하는 기법으로, NAND 바이너리 LDPC에는 대응하는 RLL 제약이 없어 이식 가치가 낮음.

### B. 알고리즘 요약

1. 시스템: Bliss scheme(변조 디코더가 ECC 디코더 뒤에 위치)에서 RLL 인코딩된 systematic 채널 비트열에 대해 LDPC parity를 생성, 광저장(Blu-ray급) 채널 대상, 코드율 `RLDPC=0.906~0.955`, 길이 `N=1728~6912`.
2. 문제: RLL 인코딩된 systematic 비트열은 `d=1` 최소 run-length 제약(`...010...`, `...101...` 서브시퀀스 불가)을 만족하는 중복 정보를 갖지만, 표준 LDPC 디코더는 이를 활용하지 않음.
3. 가정: RLL `d=1` 제약은 인접 3비트(`d+2`)로 판별 가능한 local constraint이며, LDPC factor graph에 sparse하게 추가 가능.
4. 핵심 기법: 기존 min-sum LDPC 팩터 그래프(변수노드 VN, 체크노드 CN)에 `d-constraint 노드`를 추가, 변수노드 n마다 인접 3비트(`an-1,n`, `an,n`, `an+1,n`) 메시지를 받아 위반 여부에 따라 `bn-1,n`, `bn,n`, `bn+1,n`을 출력.
5. 핵심 식: `|COr(x,y)| ∈ {0, min(|x|,|y|)}`, 부호는 Table I~III로 결정 — 두 입력이 모두 강한 신뢰도로 위반을 나타낼 때만 0이 아닌 "force" 메시지를 출력해 위반 방향을 억제.
6. 확장: 기존 min-sum 반복식(VAR/CHK)에 d-constraint 메시지 `bn-1,n, bn,n, bn+1,n`을 VN 업데이트 입력에 추가 항으로 포함(식 6).
7. 구현 디테일: Yeo et al. 스케줄(체크/제약 노드 갱신 직후 연결 변수노드 갱신하는 "mini iteration")을 사용해 반복 횟수를 약 절반으로 절감, 16 iteration 고정.
8. 학습/최적화 절차: 없음(고정 규칙 기반 메시지 함수).
9. 결과: `d=1` 제약 노드 추가 시 PSNR 약 0.25dB 이득, 동일 BER 달성을 위한 채널 비트 길이 약 0.6% 감소(저장 밀도 0.6% 증가에 해당).
10. 한계: RLL(광저장 Bliss scheme) 채널 특유의 run-length 제약에 기반, HW 미설계·순수 시뮬레이션(최대 50만 코드워드), NAND처럼 RLL 제약이 없는 채널에는 직접 적용 불가.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| d-constraint 노드 (RLL 제약 반영 factor graph 확장) | 대응 없음 | Prime ECC는 RLL 제약이 없는 순수 NAND binary QC-LDPC로, 해당 제약 노드 개념 자체가 대응 불가 |
| min-sum VAR/CHK 반복식 | `decoder.cpp` `LDPC_Decoder()`, `C2V_Cal()` | 기본 min-sum 골격은 이미 동일하게 보유(§3), 신규 기여 아님 |
| Yeo et al. 스케줄(mini-iteration, 체크노드별 즉시 갱신) | `decoder.cpp` `LDPC_Decoder()` 이터레이션 루프 | 스케줄링 방식 자체는 참고 가능하나 본 논문의 독자 기여 아님(인용 문헌) |

> 적용 가치: 낮음 — RLL 채널 특유의 side-information을 활용하는 기법으로, NAND 고전 binary QC-LDPC에는 대응하는 제약 구조가 없어 이식 불가.

### D. JSON 블록

```json
{
  "id": "arxiv:0707.3925v1",
  "title": "Use of a d-Constraint During LDPC Decoding in a Bliss Scheme",
  "year": 2007,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": null,
  "code_length": "1728~6912",
  "soft_quant": "soft-4bit+",
  "key_contribution": "RLL d=1 제약을 factor graph의 별도 d-constraint 노드로 모델링하여 min-sum LDPC 디코딩에 결합, PSNR 약 0.25dB 이득",
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
  "caveat": "RLL(Bliss scheme) 채널 특유의 run-length 제약을 전제로 한 기법으로 NAND에는 해당 제약이 존재하지 않음",
  "todo_check": "d-constraint 노드가 순수 RLL 부호 구조에 종속적인지, 다른 형태의 사이드 정보로 일반화 가능한지"
}
```
