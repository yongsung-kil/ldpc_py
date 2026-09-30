### arxiv:2401.14749v1 - Topology-Aware Exploration of Energy-Based Models Equilibrium: Toric QC-LDPC Codes and Hyperbolic MET QC-LDPC Codes (2024, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | Ising/Boltzmann 에너지모델 평형을 circulant 치환으로 매핑해 토러스/쌍곡 위상 기반 QC-LDPC 구성 통일이론 제시 |
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
| 한계,주의 | BER/시뮬/HW 전무한 순수 위상수학 개념논문이라 정정성능·구현 검증이 없어 이식 판단 불가 |
| 추가확인 | trapping-set enumerator(TS(a,0)/TS(a,b))·circulant 크기가 error-floor 부호설계에 시사점 있는지만 별도 확인 |

> 총평: QC-LDPC circulant 구조를 Ising 평형·물질과학·NLP Transformer에 연결하는 초학제 위상이론 논문으로, 디코더/HW/BER가 전무해 NAND binary QC-LDPC ECC 이식 대상이 되지 못한다.

### B. 알고리즘 요약

1. 시스템: 부호가 아니라 "위상-인지 에너지기반 모델"이 주제. QC-LDPC의 circulant permutation matrix `P^k`(식2,3)와 exponent matrix `E(H)`를 Ising/Boltzmann machine 에너지 `E_θ(x)=-b^Tx-x^TWx`(식9)와 대응.
2. 문제: 불균일 전하가 불규칙 격자에 있을 때 Ising Hamiltonian 평형(ground state) 달성 -> 전하를 circulant로, 거리를 circulant shift로 치환해 균일 격자로 변환.
3. 모델: 전하 상호작용 `Jij=k·qi/r²`(식23)을 양자화, circulant 크기 `e=P(R1,R3)`, shift `qi/Ri=n`(식24,25)로 표현. codeword=에너지 최소점, pseudocodeword(trapping set)=국소최소.
4. 핵심 기법1: 토러스/원형 쌍곡면 위상에서 균일격자 평형 존재를 Lemma1~2, Theorem1로 증명. 1D/2D 입자계를 LCM으로 circulant 크기 통일(식31,39)해 PCM `H` 구성.
5. 의미: circulant(automorphism) 크기가 등가 에너지최소점 개수를 결정 -> QC 대칭이 에너지 landscape를 규정.
6. 핵심 기법2: MET/spatial-coupled/finite-geometry QC-LDPC로 확장. Fossorier-Kou-Lin 유한기하 부호(식52)를 질소/탄소 원자 전자구름(1s²2s²2p²)에 대응(SHBF cycle gauge, 식59).
7. 부수: SC convolutional QC-LDPC를 Klein bottle 위상, Polar/Turbo와의 등가성(그래프 관점)으로 연결.
8. 학습/최적화: 분배함수 Z를 determinant/permanent 및 Bethe-permanent 근사(식13~16)로 추정, DNN quasi-Newton 학습에 활용 주장.
9. 결과: 정량 결과 없음. GeIRA/Cage-graph QC-LDPC가 NLP Transformer(MEGA/ChordMixer/CDIL) 구조와 등가라는 정성적 대응만 제시(LRA 벤치 언급).
10. 한계: BER/FER 곡선·시뮬레이션·HW·복잡도 수치 전무, 순수 개념/증명 논문으로 재현 가능한 부호설계 레시피나 성능 근거 부재.

### C. Prime ECC 관련 모듈 핀포인트

대상이 code-design(순수 위상이론)이며 디코더 성능·정정능력 검증이 없어 C섹션 성능 항목은 N/A.

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC-LDPC circulant/PCM 구성 | ecc_top.cpp `Load_PCM()` | 낮음: 추상 위상 구성이라 고정 고rate PCM에 적용할 구체 레시피 없음 |
| MET/protograph QC 구조 | ecc_top.cpp `Load_PCM()` | 낮음: 이론적 대응만, binary 고rate 재검증 근거 없음 |
| trapping-set/pseudocodeword 이론 | 대응 없음 | error-floor 시사점은 있으나 Prime에 직접 함수 대응 없음 |
| Boltzmann/Ising·NLP DNN 매핑 | 대응 없음 | NN/에너지모델은 Prime binary QC-LDPC HW와 무관 |

적용 가치: **낮음** — QC-LDPC를 Ising/DNN/물질과학과 잇는 초학제 위상수학 논문으로, 디코더·HW·정정성능이 전무하여 NAND용 binary QC-LDPC ECC 코드베이스에 떼어 쓸 실질 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2401.14749v1",
  "title": "Topology-Aware Exploration of Energy-Based Models Equilibrium: Toric QC-LDPC Codes and Hyperbolic MET QC-LDPC Codes",
  "year": 2024,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": null,
  "soft_quant": "무관",
  "key_contribution": "Ising/Boltzmann 에너지모델 평형을 circulant 치환으로 매핑해 토러스/쌍곡 위상 기반 QC-LDPC 구성 통일이론 제시",
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
  "caveat": "BER/시뮬/HW 전무한 순수 위상수학 개념논문이라 정정성능·구현 검증이 없어 이식 판단 불가",
  "todo_check": "trapping-set enumerator(TS(a,0)/TS(a,b))·circulant 크기가 error-floor 부호설계에 시사점 있는지만 별도 확인"
}
```
