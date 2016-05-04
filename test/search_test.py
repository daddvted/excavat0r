# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import xapian

# query_string = "社保卡"
# string = "社会|保险|保险卡|社会保险卡"
# string = "成都|住房|公积金"
# string = "公积金|利率|降低"
string = "城镇职工|病床|家庭"

db = xapian.WritableDatabase("../dat/index/C", xapian.DB_CREATE_OR_OPEN)
enquire = xapian.Enquire(db)

parser = xapian.QueryParser()
parser.set_database(db)

query_list = []
for s in string.split("|"):
    query = parser.parse_query(s, xapian.QueryParser.FLAG_AUTO_SYNONYMS)
    query_list.append(query)

final_query = xapian.Query(xapian.Query.OP_AND, query_list)
enquire.set_query(final_query)

matches = enquire.get_mset(0, 30)

print "%i Found." % matches.get_matches_estimated()
print ",".join(str(m.docid) for m in matches)



# def search(keywords, offset=0, limit=35, enquire=xapian.Enquire(db)):
#     query_list = []
#     for word in jieba.cut_for_search(keywords):
#         query = xapian.Query(word)
#         query_list.append(query)
#
#     if len(query_list) != 1:
#         query = xapian.Query(xapian.Query.OP_AND, query_list)
#     else:
#         query = query_list[0]
#
#     enquire.set_query(query)
#     match = enquire.get_mset(offset, limit, None)
#     return match
#
# if __name__ == "__main__":
#     matches = search("贷款利率降低了")
#
#     print "%i results found." % matches.get_matches_estimated()
#     print "Results 1-%i" % matches.size()
#
#     for m in matches:
#         print "%i: %i%% docid=%i[%s]" % (m.rank + 1, m.percent, m.docid, m.document.get_data())
