import gradio as gr
import time

import gradio.utils


def process_pdf(file: gradio.utils.NamedString, progress=gr.Progress()):
    progress(0.2, desc="111")
    print(f"===> {file.name}")
    time.sleep(1)
    progress(0.5, desc="2222")
    time.sleep(1)
    progress(1.0, desc="完成")


with gr.Blocks(
    title="本地问答系统"
) as demo:
    gr.Markdown("# 🧠 智能问答系统")
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📃文档处理区")
            with gr.Group():
                file_input = gr.File(label="上传PDF文档", file_types=[".pdf"])
                upload_btn = gr.Button("开始处理", variant="primary")
                upload_status = gr.Textbox(label="处理状态", interactive=False)
            gr.Markdown("## ❓提问区")
            with gr.Group():
                gr.Textbox(label="输入问题")
        with gr.Column(scale=3):
            gr.Markdown("## 📝 答案展示")
            gr.Textbox(label="智能回答")
            gr.Markdown("回答生成可能需要1~2分钟")

    # 上传文件
    upload_btn.click(
        fn=process_pdf,
        inputs=file_input,
        outputs=upload_status
    )

demo.launch(
    show_error=True,
    ssl_verify=False
)

