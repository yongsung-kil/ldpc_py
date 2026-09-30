### arxiv:1908.01607v1 - Protograph LDPC Code Design for Asynchronous Random Access (2019, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | protograph |
| 부호rate | 0.5 |
| 부호length | 960 |
| 연판정 | 무관 |
| 핵심기여 | 비동기 랜덤액세스 간섭패턴에 맞춘 대칭제약 protograph LDPC 부호설계로 채널부하 17% 향상 |
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
| 한계,주의 | 위성/M2M 비동기 RA 채널의 불균등보호(codeword 앞뒤 간섭) 특화, NAND 균일채널과 무관 |
| 추가확인 | 없음 (부호구조가 특정 간섭패턴 종속이라 고rate NAND QC-LDPC에 재사용 불가) |

> 총평: SIC 기반 비동기 랜덤액세스용 불균등보호 protograph 부호설계로, NAND 균일 AWGN/RBER 채널의 고rate binary QC-LDPC와 채널 가정이 달라 이식 가치가 없다.

### B. 알고리즘 요약

1. 위성/M2M 비동기 랜덤액세스(RA) 프로토콜(사용자당 `d=2` replica, SIC 수신), QPSK, rate `Rc=1/2` protograph LDPC, 코드워드 `n=2ns`(유한길이 예 `(960,480)`)를 다룬다.
2. 문제: 두 패킷 충돌 시 간섭이 코드워드의 앞 또는 뒤에 집중되므로, 앞뒤를 더 강하게 보호하는 부호가 SIC 성능을 높인다.
3. 모델: surrogate 채널 - 코드워드의 fraction `α`는 잡음+간섭(power `2σ²`), `1-α`는 잡음만(`2σn²`); 집합간섭을 Gaussian `CN(0,2σι²)`로 근사(block interference channel).
4. 핵심 기법: base matrix `BA=[BP|BTx]`에 대칭제약 `b(mb-i-1),(nb-pb-j-1)=bi,j`(식 6)를 부과해 코드워드 앞/뒤 간섭에 동일 강건성 확보(불균등오류보호).
5. 핵심 식: gain function `g = σι²_th(α,b)/σι²_o · σι²_th(α,e)/σι²_o`(식 7)를 여러 `α`에 대해 최대화, outage capacity `Co(α,σn²,σ²)`(식 3)로 Shannon limit 산출.
6. 확장: single non-Gaussian QPSK 간섭 LLR(식 4,5)을 quantized density evolution으로 처리 - 위상랜덤 QPSK 간섭이 threshold 최상, Gaussian 간섭이 최악.
7. 최적화: differential evolution(교차확률 0.6, 개체수 200, 4000세대)로 base matrix 탐색, 5G eMBB Raptor-like 부호는 열 permutation `π`로 gain 최대화.
8. 디코딩: 표준 belief propagation, 최대 50 iteration; 성능 예측은 decoding region(threshold 모델 확장)과 유한길이 PHY 시뮬로 검증.
9. 결과: ad-hoc 부호가 5G 부호 대비 PLR `10⁻²`에서 지원 채널부하 17% 향상(0.9→1.0 b/s/Hz); PHY 추상화 모델은 성능을 ~10% 과대평가.
10. 한계: 부호설계뿐 HW/디코더 변경 없음, 채널 가정이 위성 비동기 RA 특화, 시뮬만.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 대칭제약 protograph 부호설계 (앞뒤 불균등보호) | `ecc_top.cpp` `Load_PCM()` | 부호구조 로드 지점이나, 특정 RA 간섭패턴 종속 base matrix라 고정 QC-LDPC 재검증 부담 크고 부적합 |
| differential evolution base matrix 최적화 | 대응 없음 | Prime ECC는 QC-LDPC H-matrix 고정, protograph DE 탐색과 무관 |
| QPSK 간섭 LLR / density evolution threshold | `channel.cpp` `Set_LLR_Th()` | 채널모델이 QPSK 다중접속 간섭 특화라 NAND AWGN/RBER와 불일치 |

적용 가치: **낮음** — 비동기 RA 채널의 불균등오류보호 protograph 부호설계로, NAND 균일채널 고rate binary QC-LDPC의 부호구조·채널 가정과 근본적으로 달라 이식 가치가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1908.01607v1",
  "title": "Protograph LDPC Code Design for Asynchronous Random Access",
  "year": 2019,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "protograph",
  "code_rate": 0.5,
  "code_length": "960",
  "soft_quant": "무관",
  "key_contribution": "비동기 랜덤액세스 간섭패턴에 맞춘 대칭제약 protograph LDPC 부호설계로 채널부하 17% 향상",
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
  "caveat": "위성/M2M 비동기 RA 채널의 불균등보호(codeword 앞뒤 간섭) 특화, NAND 균일채널과 무관",
  "todo_check": "없음 (부호구조가 특정 간섭패턴 종속이라 고rate NAND QC-LDPC에 재사용 불가)"
}
```
