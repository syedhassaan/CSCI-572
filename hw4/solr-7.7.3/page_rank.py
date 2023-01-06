import networkx as nx


graph = nx.read_edgelist("/Users/esha/Documents/CSCI 572/hw4/solr-7.7.3/edges.txt")
page_rank = nx.pagerank(graph, 0.85, None, 30, 1e-06, None, 'weight',None)
with open("external_pageRankFile.txt", "w") as f:
    for key, value in page_rank.items():
        f.write(f"/Users/esha/Documents/CSCI 572/hw4/solr-7.7.3/latimes/{key}={value}\n")

# import networkx as nx


# class PageRank:
#     def __init__(self):
#         path_to_edge_list = "/Users/esha/Documents/CSCI 572/hw4/solr-7.7.3/edges.txt";
#         self.G = nx.read_edgelist(path_to_edge_list, create_using=nx.DiGraph())

#     def compute_page_rank(self):
#         self.page_ranks = nx.pagerank(self.G, alpha=0.85, personalization=None, max_iter=30, tol=1e-06, nstart=None,
#                          weight='weight', dangling=None)

#     def store_to_file(self):
#         rootDir = "/Users/esha/Documents/CSCI 572/hw4/solr-7.7.3/latimes/";
#         with open("external_pageRankFile.txt", "w") as file:
#             for docID, rank in self.page_ranks.items():
#                 file.write(rootDir + docID + "=" + str(rank) + "\n")


# obj = PageRank()
# obj.compute_page_rank()
# obj.store_to_file()