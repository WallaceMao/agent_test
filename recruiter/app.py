import asyncio
import os

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from utils.logger import setup_logger
from streamlit_option_menu import option_menu
import time

logger = setup_logger()


def save_uploaded_file(uploaded_file: UploadedFile | list[UploadedFile] | None = None):
    pass


async def process_resume(file_path: str) -> dict:
    """通过AI招聘流程处理简历"""
    await asyncio.sleep(3)
    return {"status": "completed"}


def main():
    st.set_page_config(
        page_title="AI招聘助手",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    with st.sidebar:
        st.image("https://img.icons8.com/resume", width=50)
        st.title("AI 招聘助手")
        selected_options = option_menu(
            menu_title="导航",
            options=["上传简历", "关于"],
            icons=['cloud-upload', 'info-circle'],
            menu_icon='cast',
            default_index=0
        )
    if selected_options == '上传简历':
        st.header("📄简历分析", divider=True)
        st.write("上传一份简历")
        uploaded_file = st.file_uploader(
            "选择一个PDF简历文件",
            type=["pdf"],
            help="上传pdf简历来进行分析"
        )

        if uploaded_file:
            try:
                with st.spinner("保存中..."):
                    file_path = save_uploaded_file(uploaded_file)

                st.info("文件上传成功")

                # 创建一个占位
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    status_text.text("分析简历中...")
                    progress_bar.progress(25)

                    result = asyncio.run(process_resume(file_path))

                    if result["status"] == "completed":
                        progress_bar.progress(100)
                        status_text.text("分析简历完成...")

                    # 在tab中显示分析结果
                    tab1, tab2, tab3, tab4 = st.tabs(
                        [
                            "📊 分析 Analysis",
                            "💼 工作匹配 Job Matches",
                            "🎯 筛选 Screening",
                            "💡 推荐 Recommendation",
                        ]
                    )

                    with tab1:
                        st.subheader("技能分析")

                    with tab2:
                        st.subheader("匹配的岗位")

                    with tab3:
                        st.subheader("筛选结果")

                    with tab4:
                        st.subheader("最终推荐")

                except Exception as e:
                    st.error(f"处理简历发生错误： {str(e)}")
                    logger.error(f"errorInProcessingResume: {str(e)}", exc_info=True)
                finally:
                    # 清理上传的文件
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        logger.error(f"errorCleaningTempFile: {str(e)}")

            except Exception as e:
                st.error(f"上传文件错误： {str(e)}")
                logger.error(f"上传错误： {str(e)}", exc_info=True)
    else:
        st.header("关于AI招聘助手")
        st.markdown("""
        ### 欢迎使用，功能特点
        - 1
        - 2
        """)


if __name__ == "__main__":
    main()
    # pass
