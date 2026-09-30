### arxiv:1909.09036v2 - Hyper-Graph-Network Decoders for Block Codes (2019, NeurIPS 2019)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.375~0.75 |
| 부호length | 31~384 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 하이퍼네트워크가 각 iteration의 variable-node 서브네트워크 가중치를 생성하는 그래프 신경망 BP 디코더 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | NN 전면 대체 디코더 + 짧은 대수부호(BCH/Polar) 중심, HW 미설계, 고rate NAND QC-LDPC와 무관 |
| 추가확인 | q=1005차 Taylor arctanh 근사와 hypernetwork FC 연산의 실제 HW 비용/면적 |

> 총평: 학습기반 BP 디코더로 성능은 BP 대비 개선되나 NN 전면 대체·짧은 대수부호·HW 미설계로 NAND binary QC-LDPC 이식성은 낮음.

### B. 알고리즘 요약

1. 대상: n=31~384 짧은 블록부호(BCH, LDPC, Polar), AWGN 채널, BP를 unroll한 Trellis 그래프(`L=5` iteration, 10 layer)에서 message passing.
2. 문제: 기존 학습 BP([17],[18])는 edge마다 고정 학습 가중치 `we`만 부여 - 입력 메시지에 적응하지 못함.
3. 핵심 기법 1단: variable-node 계산 Eq.3을 FC 신경망 `g(lv, x, θg)`로 대체 (Eq.6).
4. 핵심 기법 2단(hypernetwork): 별도 네트워크 `f`가 현재 메시지의 절댓값 `|x^{j-1}|`을 받아 `g`의 가중치 `θg^j = f(|x^{j-1}|, θf)`를 iteration마다 생성 (Eq.7).
5. `f`에 절댓값만 입력 - 메시지의 신뢰도(correctness)에 집중, bit 값(sign)은 제거.
6. check-node의 `arctanh`를 q=1005차 Taylor 다항식 근사(Eq.8)로 대체 - asymptote 제거로 학습 발산 방지.
7. 대칭조건(zero-codeword만 학습 가능)을 `g`의 bias 없는 tanh 구조와 홀수차 Taylor 항으로 만족(Lemma 1,2).
8. 학습: iteration별 cross-entropy loss(Eq.9), Adam, lr=1e-4. `f`=4층×32, `g`=2층×16 뉴런(BCH는 128 deep 옵션).
9. 결과: Polar(128,96) BP 대비 0.48dB, MacKay(96,48) 0.15dB, BCH(63,51) 0.45dB 개선; 5 iteration이 [18]의 50 iteration 성능에 필적. non-regular LDPC(WRAN 384,256)도 개선.
10. 한계: 순수 학습 디코더 - HW 미설계, gate/throughput 없음, 짧은 대수부호 중심(고rate NAND QC-LDPC 아님), q=1005 Taylor+hypernetwork 연산 부담.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BP variable-node를 신경망 g로 대체 | 대응 없음 (NN/딥러닝 디코더) | Prime ECC는 min-sum 고정 - NN 디코더 대응 모듈 없음 |
| hypernetwork f의 가중치 생성 | 대응 없음 | 이터레이션별 파라미터를 학습 생성하는 구조 미보유 |
| arctanh Taylor 근사 (check-node) | 대응 없음 (full-tanh Sum-Product) | Prime ECC는 tanh 아닌 min-sum 근사 사용 - 직접 대응 없음 |
| iteration별 학습 파라미터 | ecc_data.h `PARAM_LLR` | 약한 유비: 우리는 iteration별 LLR 테이블(학습 아님)만 존재 |

적용 가치: 낮음 - NN 전면 대체 디코더로 min-sum 기반 Prime ECC와 알고리즘 계열이 다르고 HW 설계·고rate QC-LDPC가 없어 이식 경로가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1909.09036v2",
  "title": "Hyper-Graph-Network Decoders for Block Codes",
  "year": 2019,
  "venue": "NeurIPS 2019",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "31~384",
  "soft_quant": "soft-4bit+",
  "key_contribution": "하이퍼네트워크가 각 iteration의 variable-node 서브네트워크 가중치를 생성하는 그래프 신경망 BP 디코더",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "악화",
  "recommend": "하",
  "caveat": "NN 전면 대체 디코더 + 짧은 대수부호 중심, HW 미설계, 고rate NAND QC-LDPC와 무관",
  "todo_check": "q=1005차 Taylor arctanh 근사와 hypernetwork FC 연산의 실제 HW 비용/면적"
}
```
