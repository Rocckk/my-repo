import pytest
import sys
print(sys.path)
#from ..src.scrapy_parser.pipelines import ScrapyParserMysqlPipeline

@pytest.mark.parametrize("source",
                         [("https://medium.com/testcult/intro-to-test-framework-pytest-5b1ce4d011ae"),
                          ("https://pytest.readthedocs.io/en/latest/reference.html#pytest-mark-parametrize"),
                          ("flask.pocoo.org/docs/1.0/tutorial/tests/")
                         ])
def test_spider(ScrapyParserMysqlPipeline, source):
    assert ScrapyParserMysqlPipeline.handle_source()



