import langchain
import os


def setup_langchain():
    langchain.verbose = False
    langchain.debug = False
    langchain.llm_cache = False
