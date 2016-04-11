# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jieba
import xapian

db = xapian.WritableDatabase("index", xapian.DB_CREATE_OR_OPEN)


def search(keywords, offset=0, limit=35, enquire=xapian.Enquire(db)):
    query_list = []
    for word in jieba.cut_for_search(keywords):
        query = xapian.Query(word)
        query_list.append(query)

    if len(query_list) != 1:
        query = xapian.Query(xapian.Query.OP_AND, query_list)
    else:
        query = query_list[0]

    enquire.set_query(query)
    match = enquire.get_mset(offset, limit, None)
    return match

if __name__ == "__main__":
    matches = search("贷款利率降低了")

    print "%i results found." % matches.get_matches_estimated()
    print "Results 1-%i" % matches.size()

    for m in matches:
        print "%i: %i%% docid=%i[%s]" % (m.rank + 1, m.percent, m.docid, m.document.get_data())
