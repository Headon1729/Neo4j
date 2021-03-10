from py2neo import Node, Relationship, Graph
from config import URL
from paper import Paper

class Graph(Graph):

  _author_set = set()
  _year_set = set()
  _conference_set = set()
  _keyword_set = set()

  def __init__(self, *args, **kwargs):
    '''Initializes graph from data from config (if arguments not specified)'''
    if not args and not kwargs:
      super().__init__(URL)
    else:
      super().__init__(*args, **kwargs)

  def add_paper(self, paper):
    assert isinstance(paper, Paper)
    
    title_node = Node('Title', title=paper.title)
    self.create(title_node)

    year_node = self.create_year_node(paper.year)
    self.create(
      Relationship(title_node, 'PUBLISHED_IN', year_node)
    )

    for author_node in self._author_nodes(paper.author):
      rel = Relationship(author_node, 'PUBLISHED', title_node)
      self.create(rel)

    conference_node = self.create_conference_node(paper.conference)
    self.create(
      Relationship(title_node, 'PRESENTED_IN', conference_node)
    )

    for keyword_node in self._keyword_nodes(paper.keywords):
      self.create(
        Relationship(title_node, 'USES', keyword_node)
      )

  def create_conference_node(self, conference):
    return self._create_node(self._conference_set, 'Conference', name=conference)

  def create_keyword_node(self, keyword):
    return self._create_node(self._keyword_set, 'Keyword', name=keyword)

  def create_author_node(self, author):
    return self._create_node(self._author_set, 'Author', name=author)

  def create_year_node(self, year):
    return self._create_node(self._year_set, 'Year', name=year)

  def add_papers(self, papers):
    assert isinstance(papers, list), 'papers is not a list'
    self._author_set = set()
    for paper in papers:
      self.add_paper(paper)

  def print_all_nodes(self):
    res = self.run('match (n) return n')
    for i in res:
      print(i.get('n'))

  def nodes_count(self):
    count = self.run('match (n) return count(n) as c').data()[0]['c']
    return count

  def _create_node(self, set_, label, **properties):
    property_ = list(properties.values())[0]
    if property_ not in set_:
      node = Node(label, **properties)
      set_.add(property_)
      self.create(node)
    else:
      node = self.nodes.match(label, **properties).first()
    return node

  def _author_nodes(self, authors):
    for author in authors.split(','):
      author = author.strip()
      yield self.create_author_node(author)

  def _keyword_nodes(self, keywords):
    for keyword in keywords.split(','):
      keyword = keyword.strip()
      yield self.create_keyword_node(keyword)
