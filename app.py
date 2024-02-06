from transformers import pipeline
import gradio as gr
import numpy as np
import requests
import os

transcriber = pipeline("automatic-speech-recognition", model="omarxadel/hubert-large-arabic-egyptian")

def transcribe(stream, new_chunk):
    sr, y = new_chunk
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    if stream is not None:
        stream = np.concatenate([stream, y])
    else:
        stream = y
    return stream, transcriber({"sampling_rate": sr, "raw": stream})["text"]


demo = gr.Interface(
    transcribe,
    ["state", gr.Audio(source="microphone", streaming=True)],
    ["state", "text"],
    live=False,
)

demo.launch()
