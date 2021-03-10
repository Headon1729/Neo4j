import warnings
warnings.filterwarnings("ignore")
from paper import Paper
from neo_4_j import Graph


if __name__ == '__main__':
  filepath = './abcd.xlsx'
  papers = Paper.papers_from_excel(filepath)
  graph = Graph()
  graph.delete_all()
  graph.add_papers(papers)
  graph.print_all_nodes()
  print('\n\tTotal nodes:', graph.nodes_count(), '\n')

