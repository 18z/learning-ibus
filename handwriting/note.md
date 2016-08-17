## ibus-UniEmoji 追 code 心得紀錄
此份心得先將各種片段思路記錄下來。

```
寫在前頭，這份筆記為筆者花盡心思寫下來的。
會研究 iBus 其實當初是因為想要看懂中洲韻輸入法 Python 版。
然而在閱讀中洲韻輸入法原始碼時，筆者不斷受到困擾。
此困擾即月讀程式碼時所產生之疑問，是因為 Pyhton 語法不夠純熟或是因為對 iBus 輸入法框架不了解。
為此，筆者不斷搜尋 iBus 底下其他語言輸入法，例如：ibus-anthy。
希望藉由交叉比對，找出 ibus 框架的脈絡，釐清問題來源。
不幸的是，看了一陣子 ibus-anthy 輸入法後，雖感覺比中洲韻輸入法更容易理解，
但感覺還是不夠簡潔，所以對於 iBus 脈絡掌握度還是不高，
所幸，筆者不願放棄，持續研究 iBus 底下的其他輸入法，希望找到更簡潔易懂的程式碼
天道籌勤，終於在研究 ibus-UniEmoji 時讓我看到了曙光。
經過一段時間的研究與程式碼調適，雖說尚未完全掌握 iBus 脈落，但也相距不遠了

筆者非常開心，並嘗試改寫一個自己的實驗輸入法 learning-ibus。
learning-ibus 撰寫過程中發生了一件趣事，
筆者後來發現了 ibus-tmpl 專案，也就是提供給 ibus 輸入法開發者的脈絡參考。
為此筆者感到又高興又懊惱，高興是原來真的有提供範例讓開發者參考，懊惱的是筆者沒做足功課，
一開始就發現此範例，少走些彎路。

但筆者後來反向思考，若能不參考範例，而想辦法自行理出脈絡，這樣的經驗，或許是更可貴的。

註：iBus Python 的 library 作者黃鵬已不繼續維護，雖知如此筆者還是持續研究，
    原因無它，就想知道輸入法背後是怎麼運作而已。:D
```

```
update_lookup_table 單純翻頁。
update_candidate 則是更新 content。
update_preedit_text 只有在 update_candidate 出現。

line 479 ~ 481
★   非常關鍵：text(matched) 會先用 IBus.Text.new_form_string 處理
    之後分別塞入 self.candidates 及 lookup_table 中。

★★  update_candidate 最關鍵。
    函式中，先把 matched string 塞入 lookup_table 及 candidates。

    之後再
    1.  update_auxiliary_text       (更新顯示字串)
    2.  update_preedit_text         (更新 preedit_string)
    3.  _update_lookup_table        (更新顯示 candidate 的表)
    4.  self.is_invalidate = False

什麼時候用到 update_candidate ?
    1.  commit_string (commit 出去後清空 preedit)
    2.  按 escape 時 (清空 preedit)
    3.  invalidate 時 (在 backsapce 時用到，更新候選字並廢止已打字)
    4.  一邊打字一邊就會更新了 (推測是內建 lib 函式)

★★  candidate 要被塞入 candidates 及 lookup_table 前
    要用特定 format

    display_str = u'{}: {} [{}]'.format(ascii_match, unicode_name, self.preedit_string)

    其中
        ascii_match 就是選字表的數字，按下數字即可commit 所選擇的字串?
        unicode_name 就是真正的候選字。
        self.preedit_string 就是我們打的字。

    格式設定好以後還要經過 IBus.Text.new_from_string() 處理

    處理完畢，才能塞入 candidates 及 lookup_table。
```


