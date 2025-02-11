from io import StringIO

import gradio as gr
import time

import gradio.utils
from pdfminer.high_level import extract_text_to_fp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
CHROMA_CLIENT = chromadb.PersistentClient(
    path="./db/chroma_db",
    settings=chromadb.Settings(anonymized_telemetry=False)
)
COLLECTION = CHROMA_CLIENT.get_or_create_collection("rag_docs")


def extract_pdf_text(filepath: str):
    """从pdf中提取文字"""
    output = StringIO()
    with open(filepath, 'rb') as file:
        extract_text_to_fp(file, output)
    return output.getvalue()


def process_pdf(file: gradio.utils.NamedString, progress=gr.Progress()):
    """处理上传的pdf文件"""
    try:
        progress(0.2, desc="解析PDF...")
        print(f"===> {file.name}")
        text = extract_pdf_text(file.name)

        progress(0.4, desc="分隔文本...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
        chunks = text_splitter.split_text(text)

        progress(0.6, desc="生成嵌入...")
        embeddings = EMBED_MODEL.encode(chunks)

        progress(0.8, desc="存储向量...")
        existed_ids = COLLECTION.get()['ids']
        if existed_ids:
            COLLECTION.delete(ids=existed_ids)
        ids = [str(i) for i in range(len(chunks))]
        COLLECTION.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks
        )

        progress(1.0, desc="完成")
        return f"PDF处理完成，已存储{len(chunks)}个文本块"
    except Exception as e:
        return f"处理失败： {str(e)}"


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

