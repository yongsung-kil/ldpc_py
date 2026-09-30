### arxiv:2211.14382v1 - Parallel decoder for Low Density Parity Check Codes: A MPSoC study (2022, arXiv/cs.DC)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.5 |
| 부호length | 504 |
| 연판정 | soft-2~3bit |
| 핵심기여 | Reduced Min-Sum(RMSA) LDPC 디코더를 HeMPS MPSoC/NoC에 check-node 그룹핑으로 매핑, master-slave 병렬화 speedup 측정 |
| HW설계 | O |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | check-node를 SW task로 그룹핑해 범용 MPSoC/NoC에 매핑한 플랫폼 연구로, ASIC/RTL 고정파이프라인인 우리 z=32 HW 구조와 무관 |
| 추가확인 | 실제 처리율이 kbps 수준(HeMPS 100MHz)이라 NAND ECC급 Gbps 요건과 격차 확인 |

> 총평: 통신용 rate-1/2 LDPC를 범용 MPSoC/NoC 플랫폼에 SW로 매핑한 병렬화 연구 — NAND 고전 binary QC-LDPC HW(z=32, HCU/GT)와 아키텍처가 달라 이식 가치 낮음.

### B. 알고리즘 요약

1. 시스템: rate-1/2 LDPC(252×504 PCM, PEG 구성)를 HeMPS 오픈소스 MPSoC(HERMES NoC + Plasma MIPS PE, 2D mesh)에서 복호.
2. 문제: iterative LDPC 복호는 코드 크기에 따라 복잡도가 커 병렬 구현이 필요하나, 기존 ASIC/FPGA/GPU는 설계시간·면적 비용이 큼.
3. 모델: 채널 출력 LLR `Λ(xi)=log(P(0|y)/P(1|y))`를 입력으로 하는 표준 message-passing.
4. 핵심 기법: Reduced Min-Sum Algorithm(RMSA) — min-sum 식 재배열로 메모리 footprint 축소(성능은 다소 손해), CN update는 `sign` 곱 × `min|·|`.
5. 식 의미: CN 연산이 서로 독립적이라 한 iteration 내 모든 check node를 병렬 실행 가능(병렬화 근거).
6. 매핑: check node들을 그룹화해 slave PE에 분배, master PE가 variable node(step1,3,4)+scatter/gather 담당하는 star 구조.
7. 구현 디테일: 100MHz Plasma IP, 16KB page/코어, blocking message passing(128B 제한), max iter 30, LLR은 master에 하드코딩.
8. 학습/최적화: 없음(플랫폼 매핑·측정 연구).
9. 결과: HeMPS에서 5-PE까지 speedup 최대 1.25배(throughput ~4kbps), 이후 통신비용으로 성능 저하; 데스크톱 MPI 비교는 최대 2.09배(~462kbps).
10. 한계: HW 미ASIC화(SystemC 시뮬), 정정능력 개선 없음(RMSA는 오히려 성능 손해), 처리율 kbps로 매우 낮고 NAND 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| RMSA(min-sum 변형) CN/VN 연산 | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 우리가 이미 min-sum(min1/min2+sign) 보유, RMSA는 성능 손해라 신규 기여 없음 |
| check-node 그룹핑 병렬 매핑(NoC) | 대응 없음 | 우리는 z=32 row-병렬 고정 HW 파이프라인, 범용 MPSoC task 매핑과 무관 |
| MPI/NoC 통신 | 대응 없음 | `mpi.cpp`는 stub, HW 라우팅과 별개 |

적용 가치: 낮음 — 이미 보유한 min-sum의 SW 병렬 매핑 연구이고, 정정성능·처리율·아키텍처 모두 NAND QC-LDPC HW 이식에 부합하지 않음.

### D. JSON 블록

```json
{
  "id": "arxiv:2211.14382v1",
  "title": "Parallel decoder for Low Density Parity Check Codes: A MPSoC study",
  "year": 2022,
  "venue": "arXiv (cs.DC)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": 0.5,
  "code_length": "504",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "Reduced Min-Sum LDPC 디코더를 HeMPS MPSoC/NoC에 check-node 그룹핑으로 매핑, master-slave 병렬 speedup 측정",
  "hw_designed": "O",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "하",
  "caveat": "범용 MPSoC/NoC에 SW task로 매핑한 플랫폼 연구로, 고정 z=32 HW 파이프라인인 우리 구조와 무관",
  "todo_check": "처리율이 kbps 수준이라 NAND ECC급 Gbps 요건과 격차 확인"
}
```
