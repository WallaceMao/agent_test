import streamlit as st
from utils.logger import setup_logger

st.set_page_config(
    page_title="AI 招聘机器人",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

logger = setup_logger()


def main():
    logger.info("====> hello")
    st.write("""
    # Hello
    ## abc

    我是谁？abbbeeefewef
    """)


if __name__ == "__main__":
    main()