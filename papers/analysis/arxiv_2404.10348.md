### arxiv:2404.10348v1 - On the Universality of Spatially Coupled LDPC Codes Over Intersymbol Interference Channels (2024, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 0.5 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 일반 ISI-erasure 채널의 BCJR 검출기 입출력 전달함수를 폐형으로 유도해 SC-LDPC의 정확 DE·MAP threshold 계산 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | ISI 채널(turbo equalization) 전용 threshold 이론이라 NAND memoryless 채널·QC 구조와 무관, HW·유한길이 성능 없음 |
| 추가확인 | 없음 |

> 총평: ISI 채널용 SC-LDPC threshold 이론(전달함수·SIR 보편성) — NAND binary QC-LDPC 이식 가치 없음.

### B. 알고리즘 요약 (10줄 내외)

1. 시스템: `(dv,dc)` regular LDPC를 `L` 위치에 배치·coupling memory `m`으로 결합한 SC-LDPC를 ISI 채널(erasure 또는 AWGN)에서 turbo equalization(joint BCJR 검출 + BP 복호)으로 복호.
2. 문제: ISI 채널의 정확 GEXIT/MAP threshold 계산에 필요한 BCJR 검출기 입출력 전달함수가 일반적으로 폐형이 없어 Monte Carlo에 의존해왔다.
3. 모델: 메모리 `ν` ISI 필터 출력 `z`에 소거확률 `ε`(erasure) 또는 AWGN을 가함. 검출기↔복호기 메시지는 소거 시 삼진 알파벳 `{+1,-1,?}`.
4. 핵심기법: forward/backward 상태 메트릭 벡터 `ατ,βτ`가 유한집합 `Mα,Mβ`값을 갖는 Markov chain임을 이용, 전이행렬 `Mα,Mβ`를 해석적으로 구성.
5. 핵심식: 전달함수 `g(δ,ε)=πα·T·πβ` (δ=복호기측 소거확률, `T`=extrinsic 소거확률 행렬) — 이것으로 정확 DE가 가능.
6. 확장: memory `ν=1`(CH-I/DEC), `ν=2`(CH-II), `ν=4`(CH-III) 세 채널의 `g(δ,ε)`를 Table III에 폐형으로 제시.
7. 디테일: DE는 소거 채널에선 소거확률 추적으로 등가, AWGN에선 discretized DE(FFT convolution + 2D lookup)로 밀도 추적.
8. 최적화: 없음(threshold 해석). GEXIT/GB-EXIT로 `εMAP` 상계와 SIR을 계산.
9. 결과: coupling memory 충분 시 threshold saturation 발생, Tanner 밀도↑이면 BP threshold가 SIR에 접근 → 단일 코드로 여러 ISI 채널의 SIR 보편 달성. erasure↔AWGN 성능 역전 anomaly는 엔트로피 `H(Zi|Yi)` 관점에서 해소.
10. 한계: 순수 threshold 이론(무한길이 ensemble). HW·유한길이 BER·복호 알고리즘 개선 없음. ISI 채널 특화.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SC-LDPC 부호구조/coupling | 대응 없음 | Prime ECC는 고정 QC-LDPC(`ecc_top.cpp` `Load_PCM()`), SC 구조 아님 |
| BCJR ISI 검출기 + turbo equalization | 대응 없음 | NAND memoryless 채널, ISI/turbo eq 미사용 |
| erasure DE / 전달함수 threshold | 대응 없음 | 이론 도구, 코드베이스 대응 없음 |

적용 가치: **낮음** — ISI 채널 turbo equalization용 SC-LDPC threshold 이론으로, NAND용 memoryless binary QC-LDPC의 부호설계·디코더·HW 어디에도 이식할 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2404.10348v1",
  "title": "On the Universality of Spatially Coupled LDPC Codes Over Intersymbol Interference Channels",
  "year": 2024,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": 0.5,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "일반 ISI-erasure 채널의 BCJR 검출기 입출력 전달함수를 폐형으로 유도해 SC-LDPC의 정확 DE·MAP threshold 계산",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "ISI 채널(turbo equalization) 전용 threshold 이론이라 NAND memoryless 채널·QC 구조와 무관, HW·유한길이 성능 없음",
  "todo_check": "없음"
}
```
