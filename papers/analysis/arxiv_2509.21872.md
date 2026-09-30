### arxiv:2509.21872v1 - Hidden Markov Model Decoding for LDPC Codes (2025, arXiv eess.SP)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5 |
| 부호length | 128~512 |
| 연판정 | soft-4bit+ |
| 핵심기여 | LDPC를 1차 HMM으로 재구성해 forward-backward smoothing으로 복호, 단프레임 threshold를 BP 대비 크게 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | 부분 |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | HW 미설계·시뮬만, rate 0.5 단프레임 AWGN 특화, 최대 100 random walk×5 iter로 복잡도·latency 큼 |
| 추가확인 | random walk 수 대비 실제 latency/처리량, 고rate 단축부호에서 threshold 이득 유지 여부 |

> 총평: 단프레임 rate-1/2 regular LDPC의 threshold를 BP 대비 개선하는 HMM 복호기지만, 고rate·soft 제한 NAND QC-LDPC HW와 정합성이 낮고 random-walk 반복 비용이 커서 이식가치는 낮다.

### B. 알고리즘 요약

1. 대상은 rate `R=1/2`, `G=[I P]` 구조의 short regular LDPC(`H⊤` 열당 6개, 행당 3개 1), AWGN+BPSK, 프레임 128/512 bit.
2. 문제: 단프레임 LDPC는 Tanner graph BP가 loop/trapping-set 때문에 threshold가 나쁘고, Polar+SCL-CRC 대비 열세 → BP의 잠재력 미발현을 극복하려 함.
3. 모델: 각 constraint(패리티 검사)를 HMM의 compound state로 보고, 상태는 두 encoded bit `(d_i,d_j)`(4값), 나머지 `s-2` bit는 latent, 채널은 memoryless AWGN.
4. 핵심 기법1: time-homogeneous 1차 HMM으로 encoded frame을 random walk 순회, 인접 state가 공유 bit 1개를 갖도록 강제해 Markov 성질 확보, 고정 전이행렬 `T`(식3).
5. 핵심 식: emission `P(y|d)`(식6)를 패리티 제약하 latent bit 16조합 합으로 계산 — parity check를 관측모델에 직접 내장.
6. 확장: 두 bit를 각각 포함하는 추가 패리티 검사 `yh1..yh4`를 결합한 extended emission(식9)로 난해 프레임 복호율↑.
7. 구현 트릭: 실패 시 HMM 출력 LLR을 Tanner/BP에 넘겨 결합, decision feedback으로 iteration 간 LLR 갱신(오류전파 존재).
8. 최적화: 신뢰도 통계 `γ_i=std(x)/mean(x)`(식10)로 bit 정렬 후 하위 최대 20%(2%씩) LLR을 0으로 리셋해 재복호(5단계 알고리즘).
9. 결과: 512bit에서 140,000 프레임 중 stage1 139,641 / stage3 350 / stage4 7 복호, 2프레임만 실패; threshold가 Polar(SCL-CRC L=8/256)에 근접.
10. 한계: HW 미설계, 시뮬만, 최대 100 random walk×5 iter로 복잡도·latency 큼, 대프레임·고rate·soft-read 비용 미고려.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| HMM forward-backward 복호 알고리즘 전체 | 대응 없음 | Prime ECC는 min-sum message passing, HMM 상태추정 프레임워크와 근본적으로 다름 |
| decision feedback LLR 갱신 | decoder.cpp `LDPC_Decoder()` 이터레이션 루프 | 개념상 iteration 루프에 대응하나 HMM 상태·전이행렬 개념은 미대응 |
| 신뢰도 통계 γ 기반 unreliable bit 리셋 | decoder.cpp `Get_VNU_Table_Idx()`, `ecc_data.h` `PARAM_LLR` | 적응형 LLR 테이블과 유사 취지지만 std/mean 통계·다수 random walk 필요로 이식 부담 |
| HMM+Tanner 결합 조기종료 | partial_CRC.cpp, `full_CRC.cpp` | 종료 판정만 개념 유사, HMM 자체는 대응 없음 |

적용 가치: **낮음** — HMM 상태추정 복호는 Prime ECC의 min-sum QC-LDPC HW 파이프라인과 정합되지 않고, rate-1/2 단프레임·soft-heavy·다중 random walk 비용이 NAND ECC 제약과 상충한다.

### D. JSON 블록

```json
{
  "id": "arxiv:2509.21872v1",
  "title": "Hidden Markov Model Decoding for LDPC Codes",
  "year": 2025,
  "venue": "arXiv eess.SP",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.5,
  "code_length": "128~512",
  "soft_quant": "soft-4bit+",
  "key_contribution": "LDPC를 1차 HMM으로 재구성해 forward-backward smoothing으로 복호, 단프레임 threshold를 BP 대비 크게 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "부분",
  "latency": "악화",
  "recommend": "하",
  "caveat": "HW 미설계·시뮬만, rate 0.5 단프레임 AWGN 특화, 최대 100 random walk×5 iter로 복잡도·latency 큼",
  "todo_check": "random walk 수 대비 실제 latency/처리량, 고rate 단축부호에서 threshold 이득 유지 여부"
}
```
