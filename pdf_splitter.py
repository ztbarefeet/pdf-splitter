import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

def split_pdf():
    # 获取用户选择的文件路径
    file_path = filedialog.askopenfilename(
        title="选择要拆分的PDF文件",
        filetypes=[("PDF文件", "*.pdf")]
    )
    if not file_path:
        messagebox.showinfo("提示", "未选择文件")
        return

    # 获取用户输入的分组页数
    try:
        pages_per_group = int(entries['pages'].get())
        if pages_per_group <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("错误", "请输入有效的正整数页数")
        return

    # 读取原始PDF
    try:
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            total_pages = len(reader.pages)
            
            if total_pages < pages_per_group:
                messagebox.showerror("错误", f"PDF总页数({total_pages})小于每组页数({pages_per_group})")
                return

            # 创建输出目录
            output_dir = filedialog.askdirectory(title="选择输出文件夹")
            if not output_dir:
                messagebox.showinfo("提示", "未选择输出文件夹")
                return

            # 拆分逻辑
            for i in range(0, total_pages, pages_per_group):
                writer = PdfWriter()
                end = min(i + pages_per_group, total_pages)
                
                # 添加页面到新PDF
                for page_num in range(i, end):
                    writer.add_page(reader.pages[page_num])

                # 生成输出文件名（原文件名+分组序号）
                output_path = f"{output_dir}/拆分_{i//pages_per_group + 1}.pdf"
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)

            messagebox.showinfo("完成", f"成功拆分！共生成{ (total_pages + pages_per_group - 1) // pages_per_group }个文件")

    except Exception as e:
        messagebox.showerror("错误", f"处理失败：{str(e)}")

# 创建GUI界面
root = tk.Tk()
root.title("PDF分组拆分工具")
root.geometry("300x150")

# 输入框布局
entries = {}
tk.Label(root, text="每组页数：").pack(pady=5)
entries['pages'] = tk.Entry(root)
entries['pages'].pack(pady=5)

# 执行按钮
tk.Button(root, text="开始拆分", command=split_pdf).pack(pady=10)

root.mainloop()