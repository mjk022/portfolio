# Music Transformer로 "쇼팽 스타일 캐롤" 만들기

대학원 「인공지능의 원리와 응용」(2025-2) 팀 과제(G조)입니다. Keras 공식 예제 [Music Generation with Transformer Models](https://keras.io/examples/generative/midi_generation_with_transformer/)를 분석하고, 특정 작곡가 스타일로 학습시킨 뒤 캐롤 멜로디를 이어 연주하도록 변형했습니다.

## 1. Music Transformer 핵심 정리

기반 논문: Huang et al., [Music Transformer](https://arxiv.org/abs/1809.04281) (2018)

- **MIDI 토큰화**: Note on / Note off / Time shift / Velocity 이벤트를 정수 토큰으로 바꿔 시퀀스로 학습합니다.
- **Decoder-only 구조**: 번역처럼 입력→출력 변환(조건부 확률)이 아니라 음악 시퀀스 자체의 결합 확률을 학습하므로, Cross-attention 없이 Masked self-attention만 사용합니다.
- **상대적 위치 어텐션**: 음악은 "몇 번째 음인가"보다 "음과 음 사이가 얼마나 떨어져 있는가"가 중요합니다. 토큰 간 거리 `d = i − j`에 해당하는 상대 위치 임베딩을 어텐션 점수에 더합니다.
- **Skewing**: 상대 위치 점수 행렬을 비스듬히 밀어 정렬해, 메모리를 크게 쓰지 않고 상대 위치 어텐션을 계산합니다.

## 2. 변형: 작곡가 스타일 캐롤

1. **사전학습**: [MAESTRO v3](https://magenta.tensorflow.org/datasets/maestro) 피아노 연주 데이터 중 특정 작곡가 곡만 골라 학습
   - 베토벤 → 캐롤과 어울리지 않는 연주가 나와 **쇼팽**으로 변경
2. **프롬프트**: 캐롤 MIDI를 토큰으로 바꿔 앞부분을 seed로 입력
3. **생성**: 마지막 1024 토큰을 입력으로 다음 토큰 확률을 예측하고, greedy(argmax)로 골라 붙이는 과정을 1024번 반복

결과적으로 "캐롤의 멜로디 분위기 + 쇼팽의 화성 감각"을 섞은 음악을 목표로 했습니다.

## 파일

- `music_transformer_chopin_carol.ipynb`: 쇼팽 곡 필터링 → 학습 → 캐롤 프롬프트 기반 생성 (최종 버전)
- `samples/`: 쇼팽 곡을 seed로 생성한 MIDI 샘플 5개

## 실행 시 참고

- Google Colab(GPU)에서 실행했습니다.
- `maestro-v3.0.0-midi.zip`과 캐롤 MIDI zip을 Colab에 직접 업로드해야 합니다. 캐롤 원곡 MIDI와 이를 seed로 만든 결과물은 저작권 때문에 포함하지 않았습니다.
- 노트북의 일부 변수명(`mozart_*`)은 이전 모차르트 실험의 흔적이며, 실제로는 `Chopin`으로 필터링합니다.
- MAESTRO 데이터는 CC BY-NC-SA 4.0 라이선스입니다.
