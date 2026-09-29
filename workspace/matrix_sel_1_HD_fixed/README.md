# matrix_sel_1_HD_fixed

날짜: 2026-08-18 | 출처: matrix_sel_1 H-matrix 기준 성능 측정 | 상태: 진행 중

## 목적

4_H_matrix_tool에서 선별한 matrix_sel_1 H-matrix와 짝을 이루는 HD LLR matrix의
fixed_error 채널 기준 FER를 측정한다 (E=390/380/370, 포인트당 프레임 에러 20개).

## 바꾼 것

- 디코더: base_run 그대로 (재정의 없는 BaseDecoder, DECODER_CLASS=None)
- 설정: H_matrix=matrix_sel_1.txt, llr_matrix=LLR_MATRIX_HD_matrix_sel_1.txt,
  fixed_error=[390, 380, 370], max_frame_errors=20, max_frames=200000

## 결과

| E (에러 bit) | FER | post-FEC BER | frames | errors | 평균 iteration |
|------|-----|--------------|--------|--------|---------------|
| | | | | | |

## 결론

{측정 후 기입}
