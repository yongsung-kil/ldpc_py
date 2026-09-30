### arxiv:2509.04625v2 - Nexus: Efficient and Scalable Multi-Cell mmWave Baseband Processing with Heterogeneous Compute (2026, arXiv cs.NI)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 미상 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | vRAN에서 Intel ACC100 eASIC를 VF로 다중코어 공유, RAF기반 전력인지 스케줄러로 멀티셀 mmWave 베이스밴드 실시간 처리 |
| HW설계 | X |
| 검증수준 | 실측 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 5.37Gbps |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | LDPC는 ACC100 블랙박스 오프로드 대상일 뿐 부호설계·복호알고리즘·HW LDPC 기여 전무 |
| 추가확인 | 없음 (시스템 스케줄링 논문, LDPC ECC 내부와 무관) |

> 총평: 5G vRAN 컴퓨트 자원 스케줄링 시스템 논문으로 LDPC를 가속기 태스크로만 취급, NAND binary LDPC ECC 이식과 무관.

### B. 알고리즘 요약

1. 시스템: 단일 서버(CPU 56코어 + Intel ACC100 eASIC)에서 다중 FR2 mmWave 셀의 업링크 베이스밴드(PHY)를 가상화 처리하는 vRAN 시스템 Nexus.
2. 풀려는 문제: vRAN에서 무선자원 공유는 많이 연구됐으나 CPU코어/가속기 같은 "컴퓨트 자원"의 멀티셀 공유·스케줄링은 미개척.
3. 핵심 모델: 셀설정 `σ(M,B,ρt,ρf,χ)`(MIMO/대역폭/트래픽/전송BW/MCS)과 자원할당 `θ(Cdsp,Cacc|C,V)`로 문제 정식화, 3-slot(0.375ms) 데드라인이 제약.
4. 핵심 기법 1단: ACC100을 16개 VF로 분할해 다중 워커코어가 공유(SW/HW/hybrid 오프로드 경로), LDPC 복호를 VF에 오프로드.
5. 핵심 식: 전력 `P(θ)=7·C+1.2·V`를 데드라인 제약 하에 최소화하는 자원할당 `θ★` 탐색.
6. 핵심 기법 2단: Random Forest(RAF) 분류기 `f(σ,θ)∈[0,1]`가 각 할당이 데드라인 충족(feasible)할 확률 예측, 축소된 15개 후보집합에서 최저전력 feasible 선택.
7. 부수 트릭: 멀티셀 경합을 선형 보정 `p̂(N)=p−(β0+β1·(N−1))`로 반영해 셀 수 증가 시 신뢰도 저하 모델링.
8. 학습 절차: 9K 프로파일링 실험을 monotonicity 규칙으로 120,596 샘플로 증강, 60/20/20 split으로 RAF 학습.
9. 결과: 16셀 동시 처리 5.37Gbps 집계 throughput, RAF 정확도 ≈99.1%, μs급 추론(1.42μs@10trees), DL대비 2자릿수 빠름.
10. 한계: LDPC ECC 자체의 부호·복호·HW에 대한 기여 없음(가속기 블랙박스), NAND와 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| ACC100 VF 오프로드 LDPC 복호 | 대응 없음 | LDPC를 블랙박스 가속기로만 사용, 내부 알고리즘 미공개 |
| RAF 자원 스케줄러 / 전력모델 | 대응 없음 | vRAN 컴퓨트 스케줄링, ECC 시뮬레이터 범위 밖 |
| 멀티셀 경합 보정모델 | 대응 없음 | 시스템 레벨 이슈, 복호 성능과 무관 |

적용 가치: **낮음** — 5G vRAN 시스템 스케줄링 논문으로 NAND용 binary QC-LDPC 부호설계/디코더/HW 어느 레이어에도 이식 가능한 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2509.04625v2",
  "title": "Nexus: Efficient and Scalable Multi-Cell mmWave Baseband Processing with Heterogeneous Compute",
  "year": 2026,
  "venue": "arXiv cs.NI",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "미상",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "vRAN에서 Intel ACC100 eASIC를 VF로 다중코어 공유, RAF기반 전력인지 스케줄러로 멀티셀 mmWave 베이스밴드 실시간 처리",
  "hw_designed": "X",
  "verification": "실측",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": 5.37,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "LDPC는 ACC100 블랙박스 오프로드 대상일 뿐 부호설계·복호알고리즘·HW LDPC 기여 전무",
  "todo_check": "없음 (시스템 스케줄링 논문, LDPC ECC 내부와 무관)"
}
```
