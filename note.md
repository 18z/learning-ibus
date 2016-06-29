## ibus-UniEmoji 追 code 心得紀錄
此份心得先將各種片段思路記錄下來。

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
        ascii_match 就是選字表的數字，按下數字即可commit 所選擇的字串。
        unicode_name 就是真正的候選字。
        self.preedit_string 就是我們打的字。

    格式設定好以後還要經過 IBus.Text.new_from_string() 處理

    處理完畢，才能塞入 candidates 及 lookup_table。
```


