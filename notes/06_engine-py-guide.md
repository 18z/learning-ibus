### 六、engine.py 概覽。


engine.py 主體就是 class Unimoji。

```python
 __gtype_name__ = 'UniEmoji'

    def __init__(self):
        super(UniEmoji, self).__init__()
        self.is_invalidate = False
        self.preedit_string = u""
        self.lookup_table = IBus.LookupTable.new(10, 0, True, True)
        self.prop_list = IBus.PropList()

        debug("Create UniEmoji engine OK")
```

```python
    def do_process_key_event(self, keyval, keycode, state):
        debug("process_key_event(%04x, %04x, %04x)" % (keyval, keycode, state))

        # ignore key release events
        is_press = ((state & IBus.ModifierType.RELEASE_MASK) == 0)
        if not is_press:
            return False

        if self.preedit_string:
            if keyval == IBus.Return:
                if self.lookup_table.get_number_of_candidates() > 0:
                    self.commit_candidate()
                else:
                    self.commit_string(self.preedit_string)
                return True
            elif keyval == IBus.Escape:
                self.preedit_string = u""
                self.update_candidates()
                return True
            elif keyval == IBus.BackSpace:
                self.preedit_string = self.preedit_string[:-1]
                self.invalidate()
                return True
            elif keyval in num_keys[1:]:
                index = num_keys.index(keyval) - 1
                page_size = self.lookup_table.get_page_size()
                if index > page_size:
                    return False
                page, pos_in_page = divmod(self.lookup_table.get_cursor_pos(),
                                           page_size)
                new_pos = page * page_size + index
                if new_pos > self.lookup_table.get_number_of_candidates():
                    return False
                self.lookup_table.set_cursor_pos(new_pos)
                self.commit_candidate()
                return True
            elif keyval == IBus.Page_Up or keyval == IBus.KP_Page_Up:
                self.page_up()
                return True
            elif keyval == IBus.Page_Down or keyval == IBus.KP_Page_Down:
                self.page_down()
                return True
            elif keyval == IBus.Up:
                self.cursor_up()
                return True
            elif keyval == IBus.Down:
                self.cursor_down()
                return True
            elif keyval == IBus.Left or keyval == IBus.Right:
                return True

        if keyval == IBus.space and len(self.preedit_string) == 0:
            # Insert space if that's all you typed (so you can more easily
            # type a bunch of emoji separated by spaces)
            return False

        # Allow typing all ASCII letters and punctuation, except digits
        if ord(' ') <= keyval < ord('0') or \
           ord('9') < keyval <= ord('~'):
            if state & (IBus.ModifierType.CONTROL_MASK | IBus.ModifierType.MOD1_MASK) == 0:
                self.preedit_string += unichr(keyval)
                self.invalidate()
                return True
        else:
            if keyval < 128 and self.preedit_string:
                self.commit_string(self.preedit_string)

    return False
```

```python
self.preedit_string
# 在真正將字輸入至標的文件前，使用者輸入的字 (在此階段可以選字)。
```

```python
self.lookup_table.get_number_of_candidates()
# 查詢候選字數量。
```

```python
self.commit_candidate()
# 直接將選好的 candidate 輸入至標的文件中。
```

```python
self.commit_string()
# 將使用者輸入且調整好的字串正式輸入至標的文件中。
```

```python
self.update_candidate()
# 最關鍵函式，在此函式中可定義候選字庫，更新使用者輸入字串。
```

```python
self.invalidate()
```

```python
self.lookup_table.get_page_size()
self.lookup_table.set_cursor_pos()
# 取得候選字表的狀態。
```

```python
self.page_up()
self.page_down()
# 以頁為單位翻動候選字表。
```

```python
self.cursor_up()
self.cursor_down()
# 移動候選字表裡的游標。
```

```
發現判斷是按壓哪個 key 可用類似 IBus.Up 的方法來判斷。
```
