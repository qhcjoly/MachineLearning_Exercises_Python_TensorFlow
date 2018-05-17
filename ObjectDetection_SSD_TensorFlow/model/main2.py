# -*- coding:utf-8 -*-
# Anaconda 5.0.1 環境 
# + TensorFlow 1.4.0 インストール済み
#     <Anaconda Prompt>
#     conda create -n tensorflow python=3.5
#     activate tensorflow
#     pip install --ignore-installed --upgrade tensorflow
#     pip install --ignore-installed --upgrade tensorflow-gpu
# + OpenCV 3.3.1 インストール済み
#     pip install opencv-python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# TensorFlow ライブラリ
import tensorflow as tf
from tensorflow.python.framework import ops

# OpenCV ライブラリ
import cv2

# 自作モジュール
from util.MLPreProcess import MLPreProcess
from util.MLPlot import MLPlot

from model.NNActivation import NNActivation              # ニューラルネットワークの活性化関数を表すクラス
from model.NNActivation import Sigmoid
from model.NNActivation import Relu
from model.NNActivation import Softmax

from model.NNLoss import NNLoss                          # ニューラルネットワークの損失関数を表すクラス
from model.NNLoss import L1Norm
from model.NNLoss import L2Norm
from model.NNLoss import BinaryCrossEntropy
from model.NNLoss import CrossEntropy
from model.NNLoss import SoftmaxCrossEntropy
from model.NNLoss import SparseSoftmaxCrossEntropy

from model.NNOptimizer import NNOptimizer                # ニューラルネットワークの最適化アルゴリズム Optimizer を表すクラス
from model.NNOptimizer import GradientDecent
from model.NNOptimizer import GradientDecentDecay
from model.NNOptimizer import Momentum
from model.NNOptimizer import NesterovMomentum
from model.NNOptimizer import Adagrad
from model.NNOptimizer import Adadelta
from model.NNOptimizer import Adam

from model.NeuralNetworkBase import NeuralNetworkBase
from model.VGG16Network import VGG16Network

from model.BaseNetwork import BaseNetwork
from model.BaseNetwork import BaseNetworkVGG16
from model.BaseNetwork import BaseNetworkResNet

from model.DefaultBox import DefaultBox
from model.DefaultBox import DefaultBoxSet
from model.BoundingBox import BoundingBox

from model.SingleShotMultiBoxDetector import SingleShotMultiBoxDetector


def main():
    """
    TensorFlow を用いた SSD [Single Shot muitibox Detector] の実装
    """
    print("Enter main()")

    # ライブラリのバージョン確認
    print( "TensorFlow version :", tf.__version__ )
    print( "OpenCV version :", cv2.__version__ )

    # Reset graph
    ops.reset_default_graph()

    # Session の設定
    #session = tf.Session()
    
    #======================================================================
    # データセットを読み込み or 生成
    # Import or generate data.
    #======================================================================

    #======================================================================
    # データセットをトレーニングデータ、テストデータ、検証データセットに分割
    #======================================================================

    #======================================================================
    # データを変換、正規化
    # Transform and normalize data.
    # ex) data = tf.nn.batch_norm_with_global_normalization(...)
    #======================================================================
    
    #======================================================================
    # アルゴリズム（モデル）のパラメータを設定
    # Set algorithm parameters.
    # ex) learning_rate = 0.01  iterations = 1000
    #======================================================================
    learning_rate1 = 0.001
    adam_beta1 = 0.9            # For the Adam optimizer
    adam_beta2 = 0.999          # For the Adam optimizer

    #======================================================================
    # 変数とプレースホルダを設定
    # Initialize variables and placeholders.
    # TensorFlow は, 損失関数を最小化するための最適化において,
    # 変数と重みベクトルを変更 or 調整する。
    # この変更や調整を実現するためには, 
    # "プレースホルダ [placeholder]" を通じてデータを供給（フィード）する必要がある。
    # そして, これらの変数とプレースホルダと型について初期化する必要がある。
    # ex) a_tsr = tf.constant(42)
    #     x_input_holder = tf.placeholder(tf.float32, [None, input_size])
    #     y_input_holder = tf.placeholder(tf.fload32, [None, num_classes])
    #======================================================================
    ssd = SingleShotMultiBoxDetector(
              session = tf.Session(),
              image_height = 300,
              image_width = 300,
              n_channels = 3,
              n_classes = 21,
              n_boxes = [ 4, 6, 6, 6, 6, 6 ]
          )

    #======================================================================
    # モデルの構造を定義する。
    # Define the model structure.
    # ex) add_op = tf.add(tf.mul(x_input_holder, weight_matrix), b_matrix)
    #======================================================================
    ssd.model()
    ssd.print( "after model()" )

    # 特徴マップに対応した一連のデフォルト群の生成
    ssd.generate_default_boxes_in_fmaps()
    ssd.print( "after generate_default_boxes_in_fmaps()" )

    #======================================================================
    # 損失関数を設定する。
    # Declare the loss functions.
    #======================================================================
    ssd.loss( nnLoss = None )

    #======================================================================
    # モデルの最適化アルゴリズム Optimizer を設定する。
    # Declare Optimizer.
    #======================================================================
    ssd.optimizer( Adam( learning_rate = learning_rate1, beta1 = adam_beta1, beta2 = adam_beta2 ) )

    #-------------------------------------------------------------------
    # 生成したデフォルトボックス群の表示（学習処理前）
    #-------------------------------------------------------------------
    image = np.full( (300, 300, 3), 256, dtype=np.uint8 )
    image = ssd._default_box_set.draw_rects( image, group_id = 1 )
    
    cv2.namedWindow( "image", cv2.WINDOW_NORMAL)
    cv2.imshow( "image", image )
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #======================================================================
    # モデルの初期化と学習（トレーニング）
    # ここまでの準備で, 実際に, 計算グラフ（有向グラフ）のオブジェクトを作成し,
    # プレースホルダを通じて, データを計算グラフ（有向グラフ）に供給する。
    # Initialize and train the model.
    #
    # ex) 計算グラフを初期化する方法の１つの例
    #     with tf.Session( graph = graph ) as session:
    #         ...
    #         session.run(...)
    #         ...
    #     session = tf.Session( graph = graph )  
    #     session.run(…)
    #======================================================================

    #======================================================================
    # モデルの評価
    # (Optional) Evaluate the model.
    #======================================================================
    
    #======================================================================
    # ハイパーパラメータのチューニング (Optional)
    #======================================================================


    #======================================================================
    # デプロイと新しい成果指標の予想 (Optional)
    #======================================================================


    print("Finish main()")
    return
    

if __name__ == '__main__':
     main()