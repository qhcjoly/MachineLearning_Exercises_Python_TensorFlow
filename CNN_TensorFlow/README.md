# TensorFlow で畳み込みニューラルネットワーク [CNN : Convolutional Neural Network] の実装

TensorFlow での CNN の練習用実装コード集。<br>

TensorFlow での CNN の処理をクラス（任意の層に DNN 化可能な柔軟なクラス）でラッピングし、scikit-learn ライブラリの classifier, estimator とインターフェイスを共通化することで、scikit-learn ライブラリとの互換性のあるようにした自作クラス `ConvolutionalNN` を使用する。<br>


この README.md ファイルには、各コードの実行結果、概要、CNN の背景理論の説明を記載しています。<br>
分かりやすいように `main.py` ファイル毎に１つの完結した実行コードにしています。

参考サイト :
- [Tensorflow での MINIST チュートリアル（公式）](https://www.tensorflow.org/get_started/mnist/beginners)
- [Tensorflow での CIFAR-10 チュートリアル（公式）](https://www.tensorflow.org/tutorials/deep_cnn)


## 項目 [Contents]

1. [使用するライブラリ](#ID_1)
1. [使用するデータセット](#ID_2)
1. [ニューラルネットワークのフレームワークのコードの説明](#ID_3-0)
1. [コード実行結果](#ID_3)
    1. [CNN による MNIST データの識別 : `main1.py`](#ID_3-1)
    1. [CNN による CIFAR-10 データの識別 : `main2.py`](#ID_3-2)
    1. [既存の CNN モデルの再学習処理 : `main3.py`](#ID_3-3)
1. [背景理論](#ID_4)
    1. [CNN の概要](#ID_4-1)
    1. [畳み込み [convolution] 処理について](#ID_4-2)
        1. [畳み込みの数学的な一般的な定義](#ID_4-2-1)
        1. [畳み込みニューラルネットワークにおける畳み込み](#ID_4-2-2)
        1. [畳み込みニューラルネットワークにおける畳み込み処理の具体的な例（画像データとそのフィルタ処理）](#ID_4-2-3)
        1. [より一般化した畳み込み層のアーキテクチャの元での定式化](#ID_4-2-4)
        1. [受容野の観点から見た、畳み込み層](#ID_4-2-5)
    1. [プーリング [pooling] 処理について](#ID_4-3)
        1. [平均プーリング [average pooling]](#ID_4-3-1)
        1. [最大プーリング [max pooling]](#ID_4-3-2)
        1. [Lp プーリング [Lp pooling]](#ID_4-3-3)


<a id="ID_1"></a>

## 使用するライブラリ

> TensorFlow ライブラリ </br>
>> 参考サイト<br>
>> https://qiita.com/tadOne/items/b484ce9f973a9f80036e<br>

>> `tf.nn.conv2d(...)` : ２次元の画像の畳み込み処理のオペレーター<br>
>> https://www.tensorflow.org/api_docs/python/tf/nn/conv2d<br>

>> `tf.nn.max_pool(...)` : マックスプーリング処理のオペレーター<br>
>> https://www.tensorflow.org/api_docs/python/tf/nn/max_pool<br>

>> `tf.nn.sparse_softmax_cross_entropy_with_logits(...)` : 疎なソフトマックス・クロス・エントロピー関数のオペレーター
>> https://www.tensorflow.org/api_docs/python/tf/nn/sparse_softmax_cross_entropy_with_logits

>> `tf.train.MomentumOptimizer(...)` : モーメンタムアルゴリズムの Optimizer
>> https://www.tensorflow.org/api_docs/python/tf/train/MomentumOptimizer

>> ファイル＆画像処理関連
>>> 参考サイト : <br>
http://tensorflow.classcat.com/2016/02/13/tensorflow-how-tos-reading-data/<br>
https://qiita.com/antimon2/items/c7d2285d34728557e81d<br>
>>> `tf.FixedLengthRecordReader(...)` : 固定の長さのバイトを読み取るレコードリーダー<br>
>>> https://www.tensorflow.org/api_docs/python/tf/FixedLengthRecordReader<br>
>>> `tf.train.string_input_producer(...)` : ファイル名（のキュー）を渡すことで、ファイルの内容（の一部（を表す tensor））が得られる<br>
>>> https://www.tensorflow.org/api_docs/python/tf/train/string_input_producer<br>
>>> `tf.decode_raw(...)` : 文字列から uint8 の Tensor に変換する。<br>
>>> https://www.tensorflow.org/api_docs/python/tf/decode_raw<br>


> Numpy ライブラリ
>> `numpy.argmax(...)` : 指定した配列の中で最大要素を含むインデックスを返す関数<br>
>> https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.argmax.html



<a id="ID_2"></a>

## 使用するデータセット
- [MNIST データセット](https://github.com/Yagami360/MachineLearning_Exercises_Python_TensorFlow/blob/master/dataset.md#mnist手書き数字文字画像データ)
    - 多クラスの識別＆パターン認識処理である `main1.py` で使用
- CIFAR-10 データセット
    - 多クラスの識別＆パターン認識処理である `main2.py` で使用


<a id="ID_3-0"></a>

## ニューラルネットワークのフレームワークのコードの説明
> 記載中...<br>
> sphinx or API Blueprint で HTML 形式の API 仕様書作成予定...

- `NeuralNetworkBase` クラス
    - TensorFlow ライブラリを使用
    - ニューラルネットワークの基本的なフレームワークを想定した仮想メソッドからなる抽象クラス。<br>
    実際のニューラルネットワークを表すクラスの実装は、このクラスを継承し、オーバーライドするを想定している。
- `ConvolutionalNN` クラス
    - `NeuralNetworkBase` クラスの子クラス。
    - 畳み込みニューラルネットワーク [CNN : Convolutional Neural Network] を表すクラス。<br>
    TensorFlow での CNN の処理をクラス（任意の層に DNN 化可能な柔軟なクラス）でラッピングし、scikit-learn ライブラリの classifier, estimator とインターフェイスを共通化することで、scikit-learn ライブラリとの互換性のある自作クラス

- `NNActivation` クラス : ニューラルネットワークの活性化関数を表す親クラス。<br>
    ポリモーフィズムを実現するための親クラス
    - `Sigmoid` クラス : `NNActivation` の子クラス。シグモイド関数を表す。
    - `ReLu` クラス : `NNActivation` の子クラス。。Relu関数を表す。
    - xxx
- `NNOptimizer` クラス : ニューラルネットワークモデルの最適化アルゴリズム Optimizer を表す親クラス<br>
    ポリモーフィズムを実現するための親クラス
    - `GDNNOptimizer` クラス : `NNOptimizer` クラスの子クラス。勾配降下法を表すクラス。
    - xxx
- `NNLoss` クラス : ニューラルネットワークにおける損失関数を表す親クラス。<br>
    ポリモーフィズムを実現するための親クラス
    - `L1NormNNLoss` : `NNLoss` クラスの子クラス。損失関数である L1ノルムを表すクラス。
    - xxx
- xxx

<a id="ID_3"></a>

## コードの実行結果

<a id="ID_3-1"></a>

### CNN による MNIST データの識別 : `main1.py`

- MNIST データセットを使用。
    - データは shape = [n_sample, image_width=28, image_height=28] の形状に reshape
        - `X_train, y_train = MLPreProcess.load_mnist( mnist_path, "train" )`
        - `X_test, y_test = MLPreProcess.load_mnist( mnist_path, "t10k" )`
        - `X_train = numpy.array( [numpy.reshape(x, (28,28)) for x in X_train] )`
        - `X_test = numpy.array( [numpy.reshape(x, (28,28)) for x in X_test] )`
- モデルの構造は、<br>
  畳み込み層１ → プーリング層１ → 畳み込み層２ → プーリング層２ → 全結合層１ → 全結合層２
    - 畳み込み層１：<br>
    画像の幅 (image_width)=28, (image_height)=28, チャンネル数 (n_channels) =1, 特徴数 (n_features) = 25, ストライド幅 (n_strides)=1, ゼロパディング
    - プーリング層１：<br>
    マックスプーリング、ストライド幅 (n_pool_strides) = 2
    - 畳み込み層２：<br>
    xxx
    - プーリング層２：<br>
    マックスプーリング、ストライド幅 (n_pool_strides) = 2
    - 全結合層１：<br>
    xxx
    - 全結合層２：<br>
    xxx
    ```python
    class ConvolutionalNN(object):
    def model( self ):
        """
        モデルの定義（計算グラフの構築）を行い、
        最終的なモデルの出力のオペレーターを設定する。

        [Output]
            self._y_out_op : Operator
                モデルの出力のオペレーター
        """
        # 計算グラフの構築
        #----------------------------------------------------------------------
        # 畳み込み層 ~ 活性化関数 ~ プーリング層 ~
        #----------------------------------------------------------------------
        # 重みの Variable の list に、１つ目の畳み込み層の重み（カーネル）を追加
        # この重みは、畳み込み処理の画像データに対するフィルタ処理に使うカーネルを表す Tensor のことである。
        self._weights.append( 
            self.init_weight_variable( 
                input_shape = [4, 4, self._n_channels, self._n_ConvLayer_features[0] ]  # 4, 4 : カーネルの pixcel サイズ（幅、高さ） 
            ) 
        )
        
        # バイアス項の Variable の list に、畳み込み層のバイアス項を追加
        self._biases.append( self.init_bias_variable( input_shape = [ self._n_ConvLayer_features[0] ] ) )

        # 畳み込み層のオペレーター
        conv_op1 = tf.nn.conv2d(
                       input = self._X_holder,
                       filter = self._weights[0],   # 畳込み処理で input で指定した Tensor との積和に使用する filter 行列 (Tensor)
                       strides = [ 1, self._n_strides, self._n_strides, 1 ], # strides[0] = strides[3] = 1. とする必要がある
                       padding = "SAME"     # ゼロパディングを利用する場合はSAMEを指定
                   )

        # 畳み込み層からの出力（活性化関数）オペレーター
        # バイアス項を加算したものを活性化関数に通す
        conv_out_op1 = NNActivation( activate_type = "relu" ).activate( 
                           tf.nn.bias_add( conv_op1, self._biases[0] ) 
                       )
        
        # プーリング層のオペレーター
        pool_op1 = tf.nn.max_pool(
                       value = conv_out_op1,
                       ksize = [ 1, 2, 2, 1 ],  # プーリングする範囲のサイズ
                       strides = [ 1, 2, 2, 1 ], # strides[0] = strides[3] = 1. とする必要がある
                       padding = "SAME"     # ゼロパディングを利用する場合はSAMEを指定
                   )

        # ２つ目の畳み込み層
        self._weights.append( 
            self.init_weight_variable( 
                input_shape = [4, 4, self._n_ConvLayer_features[0], self._n_ConvLayer_features[1] ]  # 4, 4 : カーネルの出力 pixcel サイズ（幅、高さ） 
            ) 
        )
        self._biases.append( self.init_bias_variable( input_shape = [ self._n_ConvLayer_features[1] ] ) )

        conv_op2 = tf.nn.conv2d(
                       input = pool_op1,
                       filter = self._weights[1],   # 畳込み処理で input で指定した Tensor との積和に使用する カーネル行列 (Tensor)
                       strides = [ 1, self._n_strides, self._n_strides, 1 ], # strides[0] = strides[3] = 1. とする必要がある
                       padding = "SAME"     # ゼロパディングを利用する場合はSAMEを指定
                   )
        conv_out_op2 = NNActivation( activate_type = "relu" ).activate( 
                           tf.nn.bias_add( conv_op2, self._biases[1] ) 
                       )
        pool_op2 = tf.nn.max_pool(
                       value = conv_out_op2,
                       ksize = [ 1, 2, 2, 1 ],  # プーリングする範囲のサイズ
                       strides = [ 1, 2, 2, 1 ], # strides[0] = strides[3] = 1. とする必要がある
                       padding = "SAME"     # ゼロパディングを利用する場合はSAMEを指定
                   )
        #----------------------------------------------------------------------
        # ~ 全結合層
        #----------------------------------------------------------------------
        # 全結合層の入力側
        # 重み & バイアス項の Variable の list に、全結合層の入力側に対応する値を追加
        fullyLayers_width = self._image_width // (2*2)    # ? (2 * 2 : pooling 処理の範囲)
        fullyLayers_height = self._image_height // (2*2)  # ?
        fullyLayers_input_size = fullyLayers_width * fullyLayers_height * self._n_ConvLayer_features[-1] # ?
        print( "fullyLayers_input_size : ", fullyLayers_input_size )

        self._weights.append( 
            self.init_weight_variable( 
                input_shape = [ fullyLayers_input_size, self._n_fullyLayers ] 
            )
        )
        self._biases.append( self.init_bias_variable( input_shape = [ self._n_fullyLayers ] ) )

        # 全結合層の出力側
        # 重み & バイアス項のの Variable の list に、全結合層の出力側に対応する値を追加
        self._weights.append( 
            self.init_weight_variable( 
                input_shape = [ self._n_fullyLayers, self._n_labels ] 
            )
        )
        self._biases.append( self.init_bias_variable( input_shape = [ self._n_labels ] ) )

        # 全結合層への入力
        # 1 * N のユニットに対応するように reshape
        pool_op_shape = pool_op2.get_shape().as_list()      # ? [batch_size, 7, 7, _n_ConvLayer_features[-1] ]
        print( "pool_op2.get_shape().as_list() :\n", pool_op_shape )
        fullyLayers_shape = pool_op_shape[1] * pool_op_shape[2] * pool_op_shape[3]
        flatted_input = tf.reshape( pool_op2, [ -1, fullyLayers_shape ] )    # 1 * N に平坦化 (reshape) された値
        #flatted_input = numpy.reshape( pool_op2, (None, fullyLayers_shape) )
        print( "flatted_input :", flatted_input )

        # 全結合層の入力側へのオペレーター
        fullyLayers_in_op = NNActivation( activate_type = "relu" ).activate(
                                tf.add( tf.matmul( flatted_input, self._weights[-2] ), self._biases[-2] )
                            )

        # 全結合層の出力側へのオペレーター
        fullyLayers_out_op = tf.add( tf.matmul( fullyLayers_in_op, self._weights[-1] ), self._biases[-1] )

        self._y_out_op = fullyLayers_out_op

        return self._y_out_op
    ```
- 損失関数は、疎なソフトマックス・クロス・エントロピー関数を使用
    - `cnn1.loss( type = "sparse-softmax-cross-entropy" )`
- モデルの最適化アルゴリズムは、モーメンタムを使用
    - `cnn1.optimizer( type = "momentum" )`
- 学習率 learning_rate は、0.0001 と 0.0005 の２つのモデルで検証

```python
def main():
    ...
    # CNN クラスのオブジェクト生成
    cnn1 = ConvolutionalNN(
               session = tf.Session( config = tf.ConfigProto(log_device_placement=True) ),
               learning_rate = 0.0001,
               epochs = 500,
               batch_size = 100,
               eval_step = 1,
               image_width = 28,                    # 28 pixel
               image_height = 28,                   # 28 pixel
               n_ConvLayer_features = [25, 50],     #
               n_channels = 1,                      # グレースケール
               n_strides = 1,
               n_fullyLayers = 100,
               n_labels = 10
           )

    cnn2 = ConvolutionalNN(
               session = tf.Session( config = tf.ConfigProto(log_device_placement=True) ),
               learning_rate = 0.0005,
               epochs = 500,
               batch_size = 100,
               eval_step = 1,
               image_width = 28,                    # 28 pixel
               image_height = 28,                   # 28 pixel
               n_ConvLayer_features = [25, 50],     #
               n_channels = 1,                      # グレースケール
               n_strides = 1,
               n_fullyLayers = 100,
               n_labels = 10
           )
```

#### 損失関数のグラフ
![cnn_1-2-2](https://user-images.githubusercontent.com/25688193/32940343-b5638ec4-cbc5-11e7-88e7-ec023053d917.png)
> 損失関数として、疎なソフトマックス・クロス・エントロピー関数を使用した場合の、損失関数のグラフ。<br>
> 赤線が学習率 0.0001 の CNN モデル（最適化アルゴリズムとして、モーメンタムアルゴリズム使用）。
> 青線が学習率 0.0005 の CNN モデル（最適化アルゴリズムとして、モーメンタムアルゴリズム使用）。
> 学習率が 0.0001 の場合、エポック数 500 で損失関数が収束しきれていないことが分かる。

#### 学習済みモデルでの正解率の値

- 学習済みモデルでのテストデータでの正解率 : 学習率=0.0001 の場合

|ラベル|Acuraccy [test data]|サンプル数|
|---|---|---|
|全ラベルでの平均|0.857|10,000 個|
|0|1.000|980<br>※全サンプル数でない|
|1|1.000|1135<br>※全サンプル数でない|
|2|1.000|1032<br>※全サンプル数でない|
|3|1.000|1010<br>※全サンプル数でない|
|4|0.982|982<br>※全サンプル数でない|
|5|0.683|892<br>※全サンプル数でない|
|6|1.000|958<br>※全サンプル数でない|
|7|0.948|1028<br>※全サンプル数でない|
|8|0.859|974<br>※全サンプル数でない|
|9|1.000|1009<br>※全サンプル数でない|

→ ５の識別率が低い傾向がある。

- 学習済みモデルでのテストデータでの正解率 : 学習率=0.0005 の場合

|ラベル|Acuraccy [test data]|サンプル数|
|---|---|---|
|全ラベルでの平均|0.958|10,000 個|
|0|1.000|980<br>※全サンプル数でない|
|1|1.000|1135<br>※全サンプル数でない|
|2|0.989|1032<br>※全サンプル数でない|
|3|0.955|1010<br>※全サンプル数でない|
|4|0.975|982<br>※全サンプル数でない|
|5|1.000|892<br>※全サンプル数でない|
|6|1.000|958<br>※全サンプル数でない|
|7|0.977|1028<br>※全サンプル数でない|
|8|0.962|974<br>※全サンプル数でない|
|9|1.000|1009<br>※全サンプル数でない|


#### 識別に正解した画像
![cnn_1-2-1](https://user-images.githubusercontent.com/25688193/32935286-c8eed470-cbb2-11e7-9188-cec154cc50e2.png)
> 識別に正解したテストデータの画像の内、前方から 40 個のサンプル。<br>
> 各画像のタイトルの Actual は実際のラベル値、Pred は予測したラベル値を示す。

#### 識別に失敗した画像
![cnn_1-3-1](https://user-images.githubusercontent.com/25688193/32937266-1a142abe-cbbb-11e7-81fd-1a66077ae3c5.png)
> 学習率 0.0001 の CNN モデルにおいて、<br>
> 識別に失敗したテストデータの画像の内、前方から 40 個のサンプル。<br>
> 各画像のタイトルの Actual は実際のラベル値、Pred は予測したラベル値を示す。

![cnn_1-3-2](https://user-images.githubusercontent.com/25688193/32940429-fa1ec984-cbc5-11e7-842d-f3bfc30a8f21.png)
> 学習率 0.0005 の CNN モデルにおいて、<br>
> 識別に失敗したテストデータの画像の内、前方から 40 個のサンプル。<br>

<br>

<a id="ID_3-2"></a>

### CNN による CIFAR-10 データの識別 : `main2.py`
> コード実装中...

- CIFAR-10 データセットを使用
- **画像は、ランダムに加工した上でトレーニングデータとして利用する**
    - 加工は、画像の一部の切り出し、左右の反転、明るさの変更からなる。
    - 画像の分類精度を向上させるには、画像の枚数が必要となるが、画像を加工することで画像を水増しすることが出来るため、このような処理を行う。





---

<a id="ID_4"></a>

## 背景理論

![image](https://user-images.githubusercontent.com/25688193/30858595-4e038b96-a2fb-11e7-9ac2-4e7131148034.png)
![image](https://user-images.githubusercontent.com/25688193/30904563-47b0fd48-a3ad-11e7-8d6c-c1f3c2751131.png)

<a id="ID_4-2"></a>

### 畳み込み [convolution] 処理について

<a id="ID_4-2-1"></a>

#### 畳み込みの数学的な一般的な定義
![image](https://user-images.githubusercontent.com/25688193/30863721-af4cee86-a30c-11e7-8d6d-b47244badc03.png)

<a id="ID_4-2-2"></a>

#### 畳み込みニューラルネットワークにおける畳み込み
![image](https://user-images.githubusercontent.com/25688193/30867484-0d67583a-a317-11e7-9740-d2449e794990.png)

<a id="ID_4-2-3"></a>

#### 畳み込みニューラルネットワークにおける畳み込み処理の具体的な例（画像データとそのフィルタ処理）
![image](https://user-images.githubusercontent.com/25688193/30872260-6c4409fe-a324-11e7-8758-9a9625a5283d.png)
![image](https://user-images.githubusercontent.com/25688193/30872283-77425900-a324-11e7-9cfc-4f7346cbada9.png)
![image](https://user-images.githubusercontent.com/25688193/30872618-adff2058-a325-11e7-94c5-7620941d8a43.png)
![image](https://user-images.githubusercontent.com/25688193/30874529-9e6564d0-a32b-11e7-904e-a08960e693f3.png)
![image](https://user-images.githubusercontent.com/25688193/30874745-3e52abce-a32c-11e7-9492-71b7f4f072e5.png)
![image](https://user-images.githubusercontent.com/25688193/30874981-f4e58672-a32c-11e7-952e-658c105c4782.png)
![image](https://user-images.githubusercontent.com/25688193/30874489-6f731b90-a32b-11e7-94ad-0025899d76e4.png)

> 参考サイト
>> [定番のConvolutional Neural Networkをゼロから理解する#畳み込みとは](https://deepage.net/deep_learning/2016/11/07/convolutional_neural_network.html#畳み込みとは)


<a id="ID_4-2-4"></a>

#### より一般化した畳み込み層のアーキテクチャの元での定式化
![image](https://user-images.githubusercontent.com/25688193/30882264-5eba369a-a343-11e7-84e3-57b5c66c28e7.png)
![image](https://user-images.githubusercontent.com/25688193/30882273-6c7c3e9a-a343-11e7-8225-893c3bde3700.png)
![image](https://user-images.githubusercontent.com/25688193/30882308-7f8b6a06-a343-11e7-9f50-0288bbfd944b.png)
![image](https://user-images.githubusercontent.com/25688193/30926162-3e669cf6-a3ef-11e7-8732-086483b4a2ec.png)
![image](https://user-images.githubusercontent.com/25688193/30884989-9c766018-a34c-11e7-8cf2-adfd0cc891a1.png)

<a id="ID_4-2-5"></a>

#### 受容野の観点から見た、畳み込み層
![image](https://user-images.githubusercontent.com/25688193/30904710-b736ff00-a3ad-11e7-9a4c-f73f76f71cc3.png)
![image](https://user-images.githubusercontent.com/25688193/30926213-5d706af0-a3ef-11e7-84c9-0216233e73ee.png)
![image](https://user-images.githubusercontent.com/25688193/30926318-abde4d10-a3ef-11e7-900a-8d9eb2842995.png)



<a id="ID_4-3"></a>

### プーリング [pooling] 処理について
![image](https://user-images.githubusercontent.com/25688193/30928885-c94bc0b4-a3f7-11e7-9b83-a86dd44abc95.png)
![image](https://user-images.githubusercontent.com/25688193/30928920-d8cf1b94-a3f7-11e7-86b7-3ab149639139.png)
![image](https://user-images.githubusercontent.com/25688193/30947089-aa6e4b62-a442-11e7-94c5-39b4a52f59e1.png)

<a id="ID_4-3-1"></a>

#### 平均プーリング [average pooling]
![image](https://user-images.githubusercontent.com/25688193/30947132-dfbf6eb8-a442-11e7-9b23-d6eeadc5e951.png)

<a id="ID_4-3-2"></a>

#### 最大プーリング [max pooling]
![image](https://user-images.githubusercontent.com/25688193/30947702-286b95c6-a446-11e7-92a2-6a4cd87dd706.png)

<a id="ID_4-3-3"></a>

#### Lp プーリング [Lp pooling]
![image](https://user-images.githubusercontent.com/25688193/30948182-27d90abe-a449-11e7-869d-4d14fbe22904.png)

<br>

---

### デバッグ Memo

```python
    # MSIT データが格納されているフォルダへのパス
    mist_path = "D:\Data\MachineLearning_DataSet\MIST"

    X_train, y_train = MLPreProcess.load_mist( mist_path, "train" )
    X_test, y_test = MLPreProcess.load_mist( mist_path, "t10k" )

    print( "X_train.shape : ", X_train.shape )
    print( "y_train.shape : ", y_train.shape )
    print( "X_test.shape : ", X_test.shape )
    print( "y_test.shape : ", y_test.shape )
    ...
    session = tf.Session()
    encode_holder = tf.placeholder(tf.int64, [None])
    y_oneHot_enoded_op = tf.one_hot( encode_holder, depth=10, dtype=tf.float32 ) # depth が 出力層のノード数に対応
    session.run( tf.global_variables_initializer() )
    y_train_encoded = session.run( y_oneHot_enoded_op, feed_dict = { encode_holder: y_train } )
    y_test_encoded = session.run( y_oneHot_enoded_op, feed_dict = { encode_holder: y_test } )
    print( "y_train_encoded.shape : ", y_train_encoded.shape )
    print( "y_train_encoded.dtype : ", y_train_encoded.dtype )
    print( "y_test_encoded.shape : ", y_test_encoded.shape )
```
```python
[出力]
X_train.shape :  (60000, 784)
y_train.shape :  (60000,)
X_test.shape :  (10000, 784)
y_test.shape :  (10000,)
y_train_encoded.shape :  (60000, 10)
y_train_encoded.dtype :  float32
y_test_encoded.shape :  (10000, 10)
```
<br>

```python
    # TensorFlow のサポート関数を使用して, MNIST データを読み込み
    mnist = read_data_sets( mist_path )
    print( "mnist :\n", mnist )
    X_train = numpy.array( [numpy.reshape(x, (28,28)) for x in mnist.train.images] )
    X_test = numpy.array( [numpy.reshape(x, (28,28)) for x in mnist.test.images] )
    y_train = mnist.train.labels
    y_test = mnist.test.labels

    print( "X_train.shape : ", X_train.shape )
    print( "y_train.shape : ", y_train.shape )
    print( "X_test.shape : ", X_test.shape )
    print( "y_test.shape : ", y_test.shape )
```
```python
[出力]
mnist :
 Datasets(
 train=<tensorflow.contrib.learn.python.learn.datasets.mnist.DataSet object at 0x0000000002BE99E8>, 
 validation=<tensorflow.contrib.learn.python.learn.datasets.mnist.DataSet object at 0x0000000002BE9EB8>, 
 test=<tensorflow.contrib.learn.python.learn.datasets.mnist.DataSet object at 0x00000000108A5C50>)
X_train.shape :  (55000, 28, 28)
y_train.shape :  (55000,)
X_test.shape :  (10000, 28, 28)
y_test.shape :  (10000,)

fullyLayers_input_size :  78400
pool_op1.get_shape().as_list() :
 [None, 28, 28, 25]
ValueError: Dimensions must be equal, but are 19600 and 78400 for 'MatMul' (op: 'MatMul') with input shapes: [1,19600], [78400,100].
```

```
InvalidArgumentError (see above for traceback): You must feed a value for placeholder tensor 'Placeholder_2' with dtype int32 and shape [100]
	 [[Node: Placeholder_2 = Placeholder[dtype=DT_INT32, shape=[100], _device="/job:localhost/replica:0/task:0/cpu:0"]()]]
```

```python
X_train.shape :  (60000, 28, 28)
y_train.shape :  (60000,)
X_test.shape :  (10000, 28, 28)
y_test.shape :  (10000,)
X_train : 
 [[[0 0 0 ..., 0 0 0]
  [0 0 0 ..., 0 0 0]
  [0 0 0 ..., 0 0 0]
  ..., 
  [0 0 0 ..., 0 0 0]
  [0 0 0 ..., 0 0 0]
  [0 0 0 ..., 0 0 0]]

 [[0 0 0 ..., 0 0 0]
  [0 0 0 ..., 0 0 0]
  [0 0 0 ..., 0 0 0]
  ..., 
 [[0 0 0 ..., 0 0 0]
  [0 0 0 ..., 0 0 0]
  [0 0 0 ..., 0 0 0]
  ..., 
  [0 0 0 ..., 0 0 0]
  [0 0 0 ..., 0 0 0]
  [0 0 0 ..., 0 0 0]]]

y_train : 
 [5 0 4 ..., 5 6 8]
y_train_encoded.shape :  (60000, 10)
y_train_encoded.dtype :  float32
y_test_encoded.shape :  (10000, 10)
```