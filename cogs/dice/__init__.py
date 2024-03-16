import random
import re

# ! ライセンス
# ! Repository URL: https://github.com/kur0den/dice
"""
The MIT License (MIT)
Copyright © 2024 Kur0den0010

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
class dice:
    def dice(self, input_dice):
        # xdxxx形式で入力されているかの判定
        # 正規表現を作成
        pattern = r"^(d[1-9][0-9]{0,2}|[1-9][0-9]{0,2}d[1-9][0-9]{0,2})$"
        # マッチするかの判定
        if not re.match(pattern, input_dice):
            return False
        # 入力された値の前半と後半を分ける
        input_list = input_dice.split("d")
        # ダイスの数が指定されていない場合は1を挿入
        if input_list[0] == "":
            input_list[0] = "1"

        # ダイスの数と面数をint型に変換
        input_list = list(map(int, input_list))

        # 結果用のリストを作成
        result = []
        f_count = 0
        c_count = 0
        for i in range(input_list[0]):
            rand_int = random.randint(1, input_list[1])
            result.append(rand_int)
            if rand_int <= 5:
                c_count += 1
            elif rand_int >= 95:
                f_count += 1
        # 結果を出力
        return sum(result)

