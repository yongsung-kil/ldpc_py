---
summary: matrix_sel_1 H-matrix와 짝 LLR 파일의 HD(hard decision) 정정 한계를 fixed_error 채널로 탐침했으나 본 측정은 결과표가 비어 있다
result: partial
tags: [probe, fixed-error, hd, incomplete]
date: 2026-08-18
source:
  - workspace/matrix_sel_1_HD/_probe/260818_225547_probe/summary.txt
  - workspace/matrix_sel_1_HD/_probe/260818_225612_probe_sweep/summary.txt
  - workspace/matrix_sel_1_HD/_probe.json
  - workspace/matrix_sel_1_HD_fixed/README.md
  - workspace/matrix_sel_1_HD_fixed/config.json
adopted_as: (없음)
---

## 시도 내용

- ㉮ 대상: `Input/H_matrix/matrix_sel_1.txt` (base 15x145, z=256, N=37120, K=33280, rate 0.8966, column degree {2:14, 3:69, 4:20, 11:42}, row degree {51:3, 52:12})와 짝 `Input/LLR/LLR_MATRIX_HD_matrix_sel_1.txt` (max_iter 120, 그룹 8개 전부 CSW 타입, 57 row)
- ㉯ 디코더: `BaseDecoder` 그대로 (재정의 0개), seed 0, 채널 fixed_error (프레임당 에러 bit 수 E 고정)
- ㉰ 1차 probe: E=380, max_frames 128, max_frame_errors 3, frames_per_batch 64
- ㉱ 2차 probe_sweep: E=[500, 460, 440, 420, 400], max_frame_errors 5, max_frames 1024, frames_per_batch 512
- ㉲ 본 측정 `workspace/matrix_sel_1_HD_fixed/`: E=[390, 380, 370] 계획

## 결과

- ㉮ E=380: 128프레임 중 에러 0, avg_iter 20.2, 9.7 f/s, 196 it/s, 13초
- ㉯ E=500: 512/512 실패, FER 1.00, post-FEC BER 1.51e-02, avg_iter 120, 4분 38초. 남은 4포인트 결과와 CSV가 없어 중단된 실행으로 추정
- ㉰ 정정 한계는 E=380과 E=500 사이. 어디인지는 미측정
- ㉱ 본 측정: README 상태 "진행 중", 결과표 빈칸. 미완
- ㉲ 함정 (설명값과 실값 어긋남): README와 config `_desc`는 "max_frame_errors 20, max_frames 200000"인데 config 값은 15와 2000000. `_probe.json`의 `_desc`도 "20개"인데 값은 5. 결과를 해석할 때는 `_desc`가 아니라 summary.txt의 `run` 줄을 본다
- ㉳ 이 짝은 저장소에서 유일하게 CSW 적응 row 선택이 실제로 동작하는 파일이다 (toy 파일은 그룹당 row 1개)
- ㉴ 두 summary의 `code commit: ecec8ae+dirty`는 원본 저장소 해시라 이 사본의 git 이력에 없다. 이 사본에 `.gitignore`가 없어 probe 결과물이 커밋에 들어 있다
- 교훈:
  - ㉠ 재개할 때는 E=400 부근부터 좁혀 들어간다 (380 생존, 500 전멸)
  - ㉡ config의 `_desc`는 설명일 뿐 검증되지 않는다. 값과 어긋날 수 있으니 실행 전 대조한다
  - ㉢ 실행 폴더 이름과 summary.txt가 유일한 실행 기록이다. 중단된 실행은 CSV를 남기지 않는다

## 대안 선택 (있을 경우)

- ㉮ (없음. 본 측정 재개 대기)
- 관련 문서
  - ㉠ [20260930_doc-code-drift-checklist.md](../assets/20260930_doc-code-drift-checklist.md) (설명값과 실값 어긋남 유형)
  - ㉡ [20260930_run-dir-and-output-files.md](../tech/20260930_run-dir-and-output-files.md)
  - ㉢ `../../docs/profile/constraints.md`
