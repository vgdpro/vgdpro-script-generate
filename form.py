import tkinter as tk
import json


def Get_Data() -> tuple[dict, dict]:
    """獲取語言文件 lang 以及全局變數 data"""
    with open("data/data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    with open(f"data/{data['lang']}.json", "r", encoding="utf-8") as file:
        lang = json.load(file)
    return lang, data


def Creat_Checkbutton(
    root: tk.Tk, txt: str, var: tk.BooleanVar, func
) -> tk.Checkbutton:
    """創建勾選按鈕"""
    lang, data = Get_Data()
    return tk.Checkbutton(root, text=lang[txt], variable=var, command=func)


def Creat_Button(root: tk.Tk, txt: str, func) -> tk.Button:
    """創建按鈕"""
    lang, data = Get_Data()
    return tk.Button(root, text=lang[txt], command=func, width=15)


class Item:
    """用於選擇覆蓋文件使用"""

    def __init__(self, button: tk.Checkbutton, var: tk.BooleanVar, card: dict):
        self.button = button
        self.var = var
        self.card = card


def Select_Cover_Form(cdb_path: str, cards: list[dict]) -> list[dict]:
    """創建選擇覆蓋文件面板"""
    lang, data = Get_Data()

    root = tk.Tk()
    root.title(lang["form.root.title"])
    root.iconbitmap("data/anyway_is_ico.ico")
    
    tk.Label(root, text=lang["form.root.info"] % cdb_path).grid(
        row=0, column=0, padx=10, pady=10, columnspan=10
    )

    next_row = 1
    items_lst: list[list[Item]] = [[]]
    page_ind: tk.IntVar = tk.IntVar(value=0)

    # 翻頁按鈕
    if len(cards) > 20:

        def Page_Change(isnext: bool):
            ind = page_ind.get()
            # hide
            for item in items_lst[ind]:
                item.button.grid_remove()
            # get ind
            ind = max(0, min(ind + (1 if isnext else -1), (len(cards) - 1) // 20))
            # show
            for item in items_lst[ind]:
                item.button.grid()

            page_ind.set(ind)

        Creat_Button(root, "form.button.pre", lambda: Page_Change(False)).grid(
            row=next_row, column=0, padx=10, pady=10
        )
        Creat_Button(root, "form.button.next", lambda: Page_Change(True)).grid(
            row=next_row, column=1, padx=10, pady=10
        )
        next_row += 1

    # 創建勾選框
    for card in cards:
        info = f"{card["cm"]} : {card["name"]}"
        check_var = tk.BooleanVar(value=False)
        check_button = tk.Checkbutton(root, text=info, variable=check_var)
        if len(items_lst[-1]) == 20:
            items_lst.append([])

        lst_len = len(items_lst[-1])
        check_button.grid(
            row=(lst_len % 10) + next_row + 1, column=lst_len // 10, sticky="w"
        )
        items_lst[-1].append(Item(check_button, check_var, card))

        if len(items_lst) > 1:
            check_button.grid_remove()

    # '當前頁全選', '當前頁全取消' 按鈕
    def Change_All(change_var: bool):
        for item in items_lst[page_ind.get()]:
            item.button.select() if change_var else item.button.deselect()
            item.var.set(change_var)

    next_row += 1 + min(len(items_lst[0]), 10)

    Creat_Button(root, "form.button.all_select", lambda: Change_All(True)).grid(
        row=next_row, column=0, padx=10, pady=10
    )
    Creat_Button(root, "form.button.all_cancel", lambda: Change_All(False)).grid(
        row=next_row, column=1, padx=10, pady=10
    )

    # '確認' 按鈕
    def Enter():
        root.quit()
        root.destroy()

    Creat_Button(root, "form.button.confirm", Enter).grid(
        row=next_row + 1, column=0, padx=10, pady=10
    )

    root.mainloop()
    # 處理返回值
    res_lst = []
    for item_lst in items_lst:
        for item in item_lst:
            if item.var.get():
                res_lst.append(item.card)

    return res_lst
