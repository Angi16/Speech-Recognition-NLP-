

import spacy as _s
from collections import Counter as _c
from operator import itemgetter as _ig


_nlp = _s.load('en')


class QueryExtractor(object):
    def __init__(self):
        pass

    def _split_text(self, text):
        doc = _nlp(text)
        return dict(
            doc = doc,
            nc = list(doc.noun_chunks),
            pos = map(lambda x: (x, x.pos_), doc),
            tag = map(lambda x: (x, x.tag_), doc))

    def get_news_tokens(self, text):
        components = self._split_text(text)
        doc, nc, pos = _ig("doc", "nc", "pos")(components)
        index = zip(*pos)[1].index("ADP") + 1
        multi_adp = (_c(zip(*pos)[1]).get("ADP") or 0) > 1
        source = nc[-1].text.lower() if multi_adp else "nyt"
        index = nc.index([i for i in nc if doc[index].lemma_ in i.lemma_][0])
        query = " ".join(map(lambda x: x.lemma_, nc[index:-1] if multi_adp else nc[index:]))
        return source, query

    def get_knowledge_tokens(self, text):
        components = self._split_text(text)
        doc, nc, pos, tag = _ig("doc", "nc", "pos", "tag")(components)
        try:
            terms = pos[[i[0] for i in enumerate(tag) if i[1][1] == "VBZ"][0] + 1:]
        except:
            return " ".join(map(lambda x: x.text, nc[1:] if len(nc) > 1 else doc[2:] if len(doc) > 2 else doc))
        return " ".join([term[0].text for term in terms if "ADP" not in term[1]])
