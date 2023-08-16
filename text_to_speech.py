# TTS (Text to Speech)
# STT (Speech to Text)

from gtts import gTTS
from playsound import playsound
file_name = 'speaker_sample2.mp3'
# 영어문장
# text = 'Dangerous situation detected !Dangerous situation detected !'
# tts_en = gTTS(text=text, lang='en')
# tts_en.save(file_name)
# playsound(file_name)


# 한글 문장
# text = '위험 상황이 감지되었습니다 ! 위험 상황이 감지되었습니다 !'
# tts_ko.save(file_name)
# playsound(file_name)

# 긴 문장 (파일에서 불러와서 처리)
with open('detect_text.txt', 'r', encoding='utf8') as f:
    text = f.read()

tts_ko = gTTS(text=text, lang='ko')
tts_ko.save(file_name)
playsound(file_name)ㅃ