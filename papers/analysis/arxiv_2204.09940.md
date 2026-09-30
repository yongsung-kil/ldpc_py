### arxiv:2204.09940v1 - On Quantum-Assisted LDPC Decoding Augmented with Classical Post-Processing (2022, arXiv quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 미상 |
| 부호rate | 0.5 |
| 부호length | 32~96 |
| 연판정 | soft-4bit+ |
| 핵심기여 | LDPC 복호를 QUBO로 정식화해 D-Wave 양자 어닐러로 풀고, 여러 shot 결과를 minimum-distance 후처리로 다양성 활용해 개선 |
| HW설계 | X |
| 검증수준 | 실측 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 미상 |
| 추천도 | 하 |
| 한계,주의 | 양자 어닐러(D-Wave)/QUBO 하드웨어 특화, 길이 32/96 초단부호, ancilla qubit 필요, NAND 온칩 min-sum 엔진과 완전 이질 |
| 추가확인 | Lagrange 가중 W1/W2 튜닝과 ancilla qubit 수가 실용 길이에서 어떻게 스케일되는지 (본문은 단부호만 검증) |

> 총평: 양자 어닐러로 LDPC 복호를 QUBO 최적화로 푸는 접근으로, NAND 컨트롤러의 binary min-sum QC-LDPC HW에 이식할 여지가 없다.

### B. 알고리즘 요약

1. 시스템: rate-1/2 LDPC, parity matrix (32,16)·(96,48) 초단부호, BPSK/AWGN, `mG=c` 인코딩.
2. 문제: 고전 BP(sum-product/min-sum) 대비 양자·시뮬레이티드 어닐링이 저·중 SNR에서 더 나은 복호가 가능한지 탐색.
3. 모델: 복호를 Quadratic Unconstrained Binary Optimization(QUBO) `f(q)=Σαi qi + Σαij qi qj`의 ground state 탐색으로 환원.
4. 핵심기법 1단(distance metric): 비트 사후확률 `P(qi=1|ri)=1/(1+exp(2ri/σ²))`로 근접도 `δ=Σ(qi-P(qi=1|ri))²`.
5. 핵심식(constraint metric): 각 check node 짝수 parity를 `Lsat(ci)=((Σqj)-2Le(ci))²`로 강제(ancilla qubit `Le` 사용), `L=ΣLsat`.
6. 핵심기법 2단: 최종 QUBO `F=W1·δ+W2·L`을 Lagrange 가중으로 결합(W2=1 고정, W1 변화)해 D-Wave 어닐러에 전달.
7. 후처리 트릭: 여러 shot에서 valid codeword만 필터 후 수신신호와 minimum-distance 디코딩 → shot 간 "다양성"을 이득으로 해석(기존 최소에너지 단독 선택 대비 개선).
8. 학습/최적화: 없음(어닐러가 물리적으로 lowest-energy 상태로 자연 수렴, message-passing iteration 불필요).
9. 결과: 중간 SNR에서 QA·SA가 BP보다 BER/FER 우수, time-varying SNR에서 정답 codeword 비율 BP 0.848 < QA 0.902 < SA 0.946.
10. 한계: HW 미설계(범용 어닐러 사용), 초단부호만, D-Wave 실기 noise 존재, Rayleigh 확장은 미래과제.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QUBO 어닐링 복호 전체 | 대응 없음 | message-passing이 아닌 QUBO 최적화라 min-sum 파이프라인에 대응 모듈 없음 |
| 비트 사후확률 `P(qi=1|ri)` (LLR류) | channel.cpp `Set_LLR_Th()` | soft-info 개념만 유사, 이후 처리는 완전 상이 |
| parity 제약 만족(짝수 parity) | decoder.cpp `C2V_Cal()` | 논문은 QUBO penalty로 강제, 우리는 CN min-sum → 이질 |

적용 가치: 낮음 - D-Wave 양자 어닐러 하드웨어와 QUBO 정식화에 종속된 복호로, NAND 온칩 binary min-sum QC-LDPC 엔진에 떼어 쓸 대응이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2204.09940v1",
  "title": "On Quantum-Assisted LDPC Decoding Augmented with Classical Post-Processing",
  "year": 2022,
  "venue": "arXiv quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "미상",
  "code_rate": 0.5,
  "code_length": "32~96",
  "soft_quant": "soft-4bit+",
  "key_contribution": "LDPC 복호를 QUBO로 정식화해 D-Wave 양자 어닐러로 풀고 여러 shot 결과를 minimum-distance 후처리로 개선",
  "hw_designed": "X",
  "verification": "실측",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "미상",
  "recommend": "하",
  "caveat": "D-Wave 양자 어닐러/QUBO 하드웨어 특화, 길이 32/96 초단부호, ancilla qubit 필요, NAND min-sum 엔진과 이질",
  "todo_check": "Lagrange 가중 W1/W2 튜닝과 ancilla qubit 수가 실용 길이에서 스케일되는지"
}
```
