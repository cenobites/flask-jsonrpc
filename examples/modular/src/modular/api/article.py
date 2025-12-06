# Copyright (c) 2012-2025, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# * Neither the name of the Cenobit Technologies nor the names of
#    its contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import typing as t
from dataclasses import dataclass

# Added in version 3.11.
from typing_extensions import Self

from flask_jsonrpc import JSONRPCBlueprint

article = JSONRPCBlueprint('article', __name__)


class ArticleException(Exception):
    def __init__(self: Self, *args: object) -> None:
        super().__init__(*args)


class ArticleNotFoundException(ArticleException):
    def __init__(self: Self, message: str, article_id: int) -> None:
        super().__init__(message)
        self.article_id = article_id


@dataclass
class Article:
    id: int
    name: str


@article.errorhandler(ArticleNotFoundException)
def handle_user_not_found_exception(ex: ArticleNotFoundException) -> dict[str, t.Any]:
    return {'message': f'Article {ex.article_id} not found', 'code': '2001'}


@article.method('Article.index')
def index() -> str:
    return 'Welcome to Article API'


@article.method('Article.getArticle')
def get_article(id: int) -> Article:
    if id > 10:
        raise ArticleNotFoundException('Article not found', article_id=id)
    return Article(id=id, name='Founded')
