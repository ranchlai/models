# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import librosa
import numpy as np
import paddle
import paddleaudio


def test_case1():
    hop_length = 160
    win_length = 400
    window = 'hann'
    pad_mode = 'constant'
    power = 2.0
    sample_rate = 16000
    center = True
    n_mels = 64
    f_min = 0.0
    f_max = 7600
    signal, sr = paddleaudio.load('./test/unit_test/test_audio.wav')
    signal_tensor = paddle.to_tensor(signal)
    paddle_cpu_feat = paddleaudio.functional.melspectrogram(
        signal_tensor,
        sr=16000,
        n_fft=win_length,
        hop_length=hop_length,
        win_length=win_length,
        window=window,
        center=center,
        n_mels=n_mels,
        pad_mode=pad_mode,
        f_min=f_min,
        f_max=f_max,
        htk=True,
        norm='slaney',
        dtype='float64')

    librosa_feat = librosa.feature.melspectrogram(signal,
                                                  sr=16000,
                                                  n_fft=win_length,
                                                  hop_length=hop_length,
                                                  win_length=win_length,
                                                  window=window,
                                                  center=center,
                                                  n_mels=n_mels,
                                                  pad_mode=pad_mode,
                                                  power=2.0,
                                                  norm='slaney',
                                                  htk=True,
                                                  fmin=f_min,
                                                  fmax=f_max)
    err = np.mean(np.abs(librosa_feat - paddle_cpu_feat.numpy()))
    assert err < 3.0e-08


def test_case2():
    hop_length = 160
    win_length = 400
    window = 'hann'
    pad_mode = 'constant'
    power = 2.0
    sample_rate = 16000
    center = True
    n_mels = 64
    f_min = 0.0
    f_max = 7600
    signal, sr = paddleaudio.load('./test/unit_test/test_audio.wav')
    signal_tensor = paddle.to_tensor(signal)
    paddle_cpu_feat = paddleaudio.functional.melspectrogram(
        signal_tensor,
        sr=16000,
        n_fft=win_length,
        hop_length=hop_length,
        win_length=win_length,
        window=window,
        center=center,
        n_mels=n_mels,
        pad_mode=pad_mode,
        f_min=f_min,
        f_max=f_max,
        htk=True,
        norm='slaney',
        dtype='float64')

    librosa_feat = librosa.feature.melspectrogram(signal,
                                                  sr=16000,
                                                  n_fft=win_length,
                                                  hop_length=hop_length,
                                                  win_length=win_length,
                                                  window=window,
                                                  center=center,
                                                  n_mels=n_mels,
                                                  pad_mode=pad_mode,
                                                  power=2.0,
                                                  norm='slaney',
                                                  htk=True,
                                                  fmin=f_min,
                                                  fmax=f_max)
    err = np.mean(np.abs(librosa_feat - paddle_cpu_feat.numpy()))
    assert err < 3.0e-08
