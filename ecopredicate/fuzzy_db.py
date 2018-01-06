import glob, os

class FuzzyDB():
  """ A database as a dictionary of dictionaries, mapping predicate names
  to map of tuples to fuzzy values.
  """

  def __init__(self):
    self.predicates = dict()

  def add_predicate(self, name, args, truth):
    """Add a predicate to the database."""
    if type(name) is not str:
      name = str(name)
    if type(args) is not tuple:
      args = tuple(args)
    if truth != 0.0:
      if name not in self.predicates:
        self.predicates[name] = dict()
      self.predicates[name][args] = truth

  def predicate_names(self):
    """Names of the predicates in the database."""
    return set(predicates.keys())

  def num_predicates(self):
    """The number or distinct relations, or symbols."""
    return len(self.predicate_names())

  def __len__(self):
    """Returns the total number of predicates in the database."""
    return sum([len(ps) for name, ps in self.predicates.items()])

  def __getitem__(self, name):
    """Returns the tuples for a given predicate name."""
    return self.predicates[name]

  def __contains__(self, name, args):
    """Checks if a predicate is present in the positive or negative set of predicates."""
    return name in self.predicates and tuple(args) in self.predicates[name]
