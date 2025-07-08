# サンプル

このリポジトリは、Python、OpenCV、`face_recognition` ライブラリを使用した基本的なリアルタイム顔認識の例を示しています。

## 必要条件

- Python 3.6 以降
- `face_recognition` ライブラリ
- OpenCV（`cv2` モジュール）

## 使い方

1. プロジェクトルートにある `known_faces` ディレクトリに認識させたい人物の画像を配置します。拡張子を除いたファイル名が各人物のラベルとして使用されます。
2. 以下のコマンドを実行します。

```bash
python real_time_face_recognition.py
```

3. ウィンドウ上で `q` を押すと終了します。
