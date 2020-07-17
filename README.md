# RealSense Capture

## 準備

[`librealsense`](https://github.com/IntelRealSense/librealsense) をインストールする必要があります。

## 実行

次のコマンドを実行して撮影を開始します。

```sh
python3 main.py
```

esc キー: 終了
space キー: 撮影

## 撮影されるデータについて

Depth 画像に関して、キャプチャ時に表示される画像と実際にキャプチャされる画像は異なります。
これはキャプチャのプレビューには見やすさを重視し `COLORMAP_JET` を使用しているのに対して、キャプチャする画像には次のような別の処理を行っているためです。

Depth 情報は 0 ~ 65535（2^16） であり、このままではグレースケール画像 0 ~ 255（2^8） に収めることはできません。
そのため、0 ~ 255 を 2 つ使用することで 2^8 \* 2^8 = 2^16 のデータを保存することができます。

```python
depth_save = np.zeros_like(color_image)
depth_save[:,:, 0] = depth_image % 256
depth_save[:,:, 1] = depth_image // 256
```

保存画像から元の Depth 情報を取り出すためには次のようにします。depth の取りうる値は 0 ~ 65535 となります。

```python
depth = depth_save[:,:, 0] + depth_save[:,:, 1] * 256
```
