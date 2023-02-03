# CharacterImageTool
立ち絵のpsdからレイヤー別にpngを出力するプログラムです。

## 使用方法
立ち絵のpsdファイルが1つだけの場合。
```
character_image_tool.py [psd file path]
```
立ち絵のpsdファイルが複数の場合。
```
character_image_tool.py [psd file path 1] [psd file path 2] ... [psd file path N] 
```

## 立ち絵用psdファイルの構成方法
立ち絵用のpsdファイルは以下のように構成する必要があります。
<pre>
.
├── パーツ_1
     ├── パターン_1
     ├── パターン_2
     :
├── パーツ_2
     ├── パターン_1
     :
└── パーツ_3
     ├── パターン_1
     :
</pre>
「**パーツ**」のレイヤーフォルダの中にいろいろな**状態**の「レイヤー」または「レイヤーフォルダ」を置きます。<br>
この状態のpsdファイルをプログラムに読み込ませると「**xxx_パーツ**」というフォルダを作り、<br>
その中に「**xxx_パターン**」の画像を出力します。xxxは下層から順番に割り当てられる番号です。

※パーツがレイヤーフォルダ出ない場合は無視されます。
※パーツがレイヤーフォルダ出ない場合は無視されます。

## 例
"character.psd"というpsdファイルがあるとします。

<img src="https://user-images.githubusercontent.com/73507097/216595025-8ffc0331-0fff-4d47-8a5b-16ebb8ca9351.png" width="50%">

以下が一部省略した"character.psd"のレイヤー構成です
<pre>
root
├── 左眉
     ├── ノーマル
     ├── 怒り
     └── 困り
├── 右眉
├── 左目
     ├── ノーマル
     ├── 驚き１
     ├── 驚き２
     :
├── 右目
├── 口
├── ほっぺ
└── 体
</pre>


"character.psd"をプログラムに読み込ませます。
```
character_image_tool.py ./character.psd
```


出力すると以下の画像のようになります。

![image](https://user-images.githubusercontent.com/73507097/216598754-74a695cf-dd2a-4e4b-a0cc-4a8a1d18d7de.png)

パーツ別にフォルダが出力されており、各フォルダ内にはパターンの画像が出力されます。


## License
MITライセンスです。
