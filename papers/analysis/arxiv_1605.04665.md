### arxiv:1605.04665v1 - A New Density Evolution Approximation for LDPC and Multi-Edge Type LDPC Codes (2016, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 0.1~0.7 |
| 부호length | 100000 |
| 연판정 | 무관 |
| 핵심기여 | full-DE와 Gaussian 근사를 결합한 hybrid-DE로 저rate/punctured MET-LDPC 임계값을 정확·고속 추정 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | BI-AWGN 점근 임계값 계산용 설계도구, 실제 복호기/HW/NAND soft-read 무관 |
| 추가확인 | hybrid-DE가 고rate NAND QC-LDPC 부호설계 오프라인 임계값 툴로 재활용 가능한지 |

> 총평: BP 임계값을 정확·고속 추정하는 hybrid density evolution 설계도구 논문으로, 저rate/punctured MET-LDPC 대상이라 고rate NAND binary QC-LDPC 이식가치는 낮다.

### B. 알고리즘 요약

1. 대상은 MET-LDPC(및 irregular LDPC) 부호의 BI-AWGN 임계값 계산으로 rate 0.1~0.7, 유한길이 검증은 length-100000.
2. 풀려는 문제: full-DE는 정확하나 PDF당 9800점 양자화로 느리고, 단일파라미터 Gaussian 근사는 저rate/punctured에서 부정확.
3. 모델: BP 메시지 LLR PDF를 추적, symmetry `f(x)=e^x f(−x)`로 `σ²=2m` 단일파라미터화 - 단 초기 iteration에선 비대칭.
4. 분석: check-to-variable 메시지 `u`는 저SNR·큰 check degree·punctured 노드에서 대칭 Gaussian에서 크게 이탈(KL divergence로 측정).
5. Gaussian 근사 3종 확장: mean 기반(App1, `φ(x)`), BER 기반(App2, `Q`함수), reciprocal-channel(App3, `ψ(m)`).
6. 핵심기법: hybrid-DE - 초기엔 full-DE로 PDF 추적, 메시지가 대칭 Gaussian에 근접한 뒤 Gaussian 근사(App1)로 전환.
7. 전환기준: option1=최대 full-DE iteration 수 상한(hard), option2=목표 KL divergence 도달(soft), 둘 병행.
8. 최적화: joint optimization으로 부호설계 시 hybrid-DE 비용함수가 full-DE 형상을 잘 추종(App들은 국소최대 위치 어긋남).
9. 결과: App1/3은 rate>0.6, App2는 rate>0.7에서만 5% 이내 정확; hybrid-DE는 최대 10배 CPU 이득에 5% 이내 오차, 저rate에서도 full-DE 근접.
10. 한계: BI-AWGN 점근 임계값 계산용 Matlab 설계도구뿐, 실제 복호기 구현·HW·NAND read 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| hybrid-DE 임계값 추정 | 대응 없음 | Prime ECC는 bit-exact 복호 검증용, DE 점근 임계값 계산 모듈 없음 |
| BP tanh-rule / Gaussian 근사 | 대응 없음 | 실기 복호기는 min-sum(`decoder.cpp` `CNU_Update_New_Mag()`) 사용, 이 논문은 full-tanh DE 해석 |
| MET 부호설계 최적화 | ecc_top.cpp `Load_PCM()` | 설계단계 오프라인 툴, 고정 고rate QC-LDPC 코드베이스와 직접 대응 없음 |

적용 가치: **낮음** — 저rate/punctured MET-LDPC 대상 DE 임계값 추정 설계도구라 고rate 고정 binary QC-LDPC 실기 코드베이스에 이식할 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1605.04665v1",
  "title": "A New Density Evolution Approximation for LDPC and Multi-Edge Type LDPC Codes",
  "year": 2016,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": "0.1~0.7",
  "code_length": "100000",
  "soft_quant": "무관",
  "key_contribution": "full-DE와 Gaussian 근사를 결합한 hybrid-DE로 저rate/punctured MET-LDPC 임계값을 정확·고속 추정",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "BI-AWGN 점근 임계값 계산용 설계도구, 실제 복호기/HW/NAND soft-read 무관",
  "todo_check": "hybrid-DE가 고rate NAND QC-LDPC 부호설계 오프라인 임계값 툴로 재활용 가능한지"
}
```
