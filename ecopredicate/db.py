import glob, os

class DB():
  """ A database as dictionaries of positive and negative predicates. This
  class is used to load predicates from various file formats, get info on them,
  and write to popular formats.
  """

  def __init__(self):
    self.ppredicates = dict() # Positive predicates
    self.npredicates = dict() # Negative predicates

  def add_predicate(self, name, args, sign=True):
    """Add a predicate to the database."""
    if type(name) is not str:
      name = str(name)
    if type(args) is not tuple:
      args = tuple(args)

    if sign:
      if name not in self.ppredicates:
        self.ppredicates[name] = set()
      self.ppredicates[name].add(args)
    else:
      if name not in self.npredicates:
        self.npredicates[name] = set()
      self.npredicates[name].add(args)

  def predicate_names(self):
    """Union of the predicate names in the positive and negative groups."""
    return set(ppredicates.keys()).union(set(npredicates.keys()));

  def num_predicates(self):
    """The number or distinct relations, or symbols."""
    return len(self.predicate_names())

  def __len__(self):
    """Returns the total number of positive and negative predicates in the database."""
    count = 0
    for name, ps in self.ppredicates.items():
      count += len(ps)
    for name, ps in self.npredicates.items():
      count += len(ps)
    return count

  def get_p(self, name):
    """Returns the set of tuples for a given positive predicate name."""
    return self.ppredicates[str(name)]

  def get_n(self, name):
    """Returns the set of tuples for a given negative predicate name."""
    return self.npredicates[str(name)]

  def get_u(self, name):
    """Get 'unsigned': get the set of positive and negative tuples for a predicate name."""
    return self.get_p(name).union(self.get_n(name))

  def __contains__(self, name, args):
    """Checks if a predicate is present in the positive or negative set of predicates."""
    if str(name) not in self.ppredicates and str(name) not in self.npredicates:
      return False
    return tuple(args) in self.predicates[str(name)] or tuple(args) in self.npredicates[str(name)]

  def infer_domains(self, relations):
    """
    Infer the domains given a set of relations.

    Parameters
    ----------
    relations : dict
        Dictionary from a predicate name to the tuple of arguments)

    Returns
    -------
    dict
        A dictionary from the relations' names to the set of values.

    """
    domains = dict()
    for name, args in relations.items():
      for arg in args:
        if arg not in domains:
          domains[arg] = set()

    for name, args in self.ppredicates.items():
      if name not in relations:
        continue

      for arg in args:
        for i in range(len(arg)):
          d = relations[name][i]
          domains[d].add(arg[i])

    # Do same thing for negative predicates.

    return domains

  def from_csv(self, folder, sep=','):
    """Read all CSV files in a folder, treating them as tables for positive predicates."""
    os.chdir(folder)
    for f in glob.glob("*.csv"):
      name = f[:-4]
      with open(f) as ps:
        for line in ps:
          args = tuple(line.replace(' ', '').replace('\n', '').split(sep))
          self.add_predicate(name, args)

  def from_alchemy_db(self, filename):
    """Read a DB file in Alchemy2's format."""
    with open(filename) as f:
      for line in f:
        tokens = line.replace(' ', '').replace('\n', '').split(',')
        name = tokens[0]
        args = tuple(tokens[1:])
        if name[0] == '!':
          add_predicate(self, name[1:], args, False)
        else:
          add_predicate(self, name, args, True)

  def from_aleph_db(self, filename):
    """Read filename.f and filename.n for positive and negative predicates, respectively."""
    with open(filename + '.f') as f:
      for line in f:
        tokens = line.replace(' ', '').replace('\n', '').split(',')
        name = tokens[0]
        args = tuple(tokens[1:])
        add_predicate(self, name, args, True)

    with open(filename + '.n') as f:
      for line in f:
        tokens = line.replace(' ', '').replace('\n', '').split(',')
        name = tokens[0]
        args = tuple(tokens[1:])
        add_predicate(self, name, args, False)

  def to_csv(self, sep=','):
    """Prints the predicates to a set of csv files. For now ignores negative examples."""
    for name, args in self.ppredicates.items():
      f = open(name + '.csv', 'w')
      for arg in args:
        f.write(sep.join([str(a) in arg]) + '\n')
      f.close()

  def to_aleph_files(self, filename):
    """Outputs the predicates to a .f file for positive predicates and a .n file for negative predicates."""
    f = open(filename + '.f', 'w')
    for name, args in self.ppredicates.items():
      for arg in args:
        f.write(name + '(' + ', '.join(arg) + ').\n')
    f.close()

    n = open(filename + '.n', 'w')
    for name, args in self.npredicates.items():
      for arg in args:
        n.write(name + '(' + ', '.join(arg) + ').\n')
    n.close()

  def to_alchemy_file(self, filename):
    """Outputs the predicates to a file in Alchemy's db format."""
    f = open(filename + '.f', 'w')
    f.write(self.__str__())
    f.close()

  def __str__(self):
    s = ''
    for name, args in self.ppredicates.items():
      for arg in args:
        s += name + '(' + ', '.join(arg) + ')\n'
    for name, args in self.npredicates.items():
      for arg in args:
        s += '!' + name + '(' + ', '.join(arg) + ')\n'
    return s
