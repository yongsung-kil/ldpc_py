### arxiv:2404.14828v2 - GLDPC-PC Codes: Channel Coding Towards 6G Communications (2025, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.625~0.78 |
| 부호length | 1024~4096 |
| 연판정 | 무관 |
| 핵심기여 | GLDPC의 CN을 single-parity 대신 polar 부호로 두고 SO-SCL로 SISO 복호하는 GLDPC-PC 개념 제안, 5G LDPC 대비 error-floor 제거·iteration 감소 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | O |
| latency | 미상 |
| 추천도 | 하 |
| 한계,주의 | CN이 polar 부호+SO-SCL 복호라 min-sum QC-LDPC 파이프라인과 근본 구조 상이, 6G AWGN 무선 타깃·overview 성격 |
| 추가확인 | 없음 |

> 총평: 6G용 GLDPC+polar 컴포넌트 개념 overview — CN이 polar SISO 복호라 NAND binary QC-LDPC 디코더와 근본 구조 달라 이식 부적합.

### B. 알고리즘 요약 (10줄 내외)

1. 시스템: 6G 채널코딩 overview 겸 concept 논문. AWGN 채널, `(1024,640)`/`(2048,1280)`(R=0.625), `(4096,3200)`(R=0.78) GLDPC-PC 부호 예시.
2. 문제: 6G는 5G 대비 복잡도·latency·신뢰도 1~2 자릿수 향상을 요구, 특히 5G LDPC의 error-floor(BLER 10^-4~10^-5)와 short-code 성능 한계.
3. 핵심 아이디어: GLDPC(Tanner CN을 single parity 대신 선형 블록부호로 대체)의 component code로 polar 부호를 사용 → `GLDPC-PC`.
4. 핵심기법: CN 제약을 polar 부호어로 두고, MPA 반복에서 CN update를 polar SISO 복호기로 수행. VN update는 기존 LDPC와 동일(채널 LLR + CN 메시지 합).
5. 핵심 조력자: SISO polar 복호로 `SO-SCL`(soft-output SCL) 채택 — SCL 트리의 unvisited leaf APP를 추정해 Pyndiah 근사보다 정확, 최적 BCJR에 근접.
6. 부호구성: AM `Γ`를 순환 shift 항등행렬 블록으로 구성(product code 유래), 결과 부호길이 `N=n^2`, `(32,26)`/`(64,57)` polar를 component로 사용.
7. 인코딩: PCM Gaussian elimination으로 GM 도출(비sparse→고복잡), QC 구조 시 [14] 방식 선형시간 인코딩 가능하다고 언급.
8. 최적화: 별도 학습 없음. 부호구조 설계(어느 VN이 어느 CN·polar에 묶이는가)는 미해결 과제로 남김("not specifically designed").
9. 결과: SO-SCL GLDPC-PC가 moderate-high SNR에서 5G LDPC/polar/turbo 상회, BLER 10^-4~10^-5에서 양의 gain, error-floor 없이 10^-7까지 waterfall. avg iteration은 5G LDPC의 1/3~1/2, 복잡도는 `L=4`에서 5G LDPC의 2~3배(polar와 유사).
10. 한계: HW 미설계(gate/throughput/latency 미평가), overview 성격, off-the-shelf 구조로 최적화 안됨. 6G AWGN 무선 타깃.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| MPA VN update / 반복 스케줄 | `decoder.cpp` `LDPC_Decoder()`, `VN_Cal_HD()` | VN 처리·이터레이션 루프 골격은 유사하나 부호구조가 다름 |
| CN update = polar SISO(SO-SCL) 복호 | 대응 없음 | Prime ECC CN은 min-sum(`CNU_Update_New_Mag()`), polar SISO/SCL 복호기 없음 |
| GLDPC-PC 부호구조 / polar component AM | 대응 없음 | Prime ECC는 single-parity QC-LDPC(`ecc_top.cpp` `Load_PCM()`), GLDPC 미지원 |
| 조기종료(parity check) | `partial_CRC.cpp`/`full_CRC.cpp` | 반복 종료 개념만 유사, 직접 이식 아님 |

적용 가치: **낮음** — CN이 polar 부호+SO-SCL SISO 복호인 GLDPC 구조는 min-sum single-parity QC-LDPC 파이프라인과 근본적으로 달라, NAND용 Prime ECC에 떼어 이식할 수 없다. error-floor 제거·iteration 감소는 흥미로우나 부호/복호기 전면 교체를 요구.

### D. JSON 블록

```json
{
  "id": "arxiv:2404.14828v2",
  "title": "GLDPC-PC Codes: Channel Coding Towards 6G Communications",
  "year": 2025,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": "0.625~0.78",
  "code_length": "1024~4096",
  "soft_quant": "무관",
  "key_contribution": "GLDPC의 CN을 single-parity 대신 polar 부호로 두고 SO-SCL로 SISO 복호하는 GLDPC-PC 개념 제안, 5G LDPC 대비 error-floor 제거·iteration 감소",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "O",
  "latency": "미상",
  "recommend": "하",
  "caveat": "CN이 polar 부호+SO-SCL 복호라 min-sum QC-LDPC 파이프라인과 근본 구조 상이, 6G AWGN 무선 타깃·overview 성격",
  "todo_check": "없음"
}
```
