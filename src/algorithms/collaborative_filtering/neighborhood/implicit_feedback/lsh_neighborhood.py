from src.algorithms.collaborative_filtering.model import CollaborativeFiltering
from numpy.random import permutation
from pandas import DataFrame
from functools import reduce

SIGNATURE_MATRIX_KEY = "signature_matrix"
BUCKETS_KEY = "buckets"


class LSHBased(CollaborativeFiltering):

    def __init__(self, matrix, signature_matrix=[], buckets=[], n_perms=6,
                 n_bands=2):
        super().__init__(matrix)
        self.n_permutations = n_perms
        self.n_bands = n_bands
        self._init_model(signature_matrix, SIGNATURE_MATRIX_KEY,
                         self._init_signature_matrix)
        self._init_model(buckets, BUCKETS_KEY, self._init_buckets)

    def _init_signature_matrix(self):
        signatures = self._calculate_signatures(self.matrix)
        self.model[SIGNATURE_MATRIX_KEY] = DataFrame(signatures)

    def _calculate_signatures(self, matrix):
        signatures = []
        for i in range(self.n_permutations):
            permutated_matrix = DataFrame(permutation(matrix))
            sign = self._generate_signature(permutated_matrix)
            signatures.append(sign)
        return signatures

    def _generate_signature(self, perm_matrix):
        signature = []
        for col in range(len(perm_matrix.columns)):
            column = perm_matrix[col]  # Assuming the data structure complies.
            identifier = self._min_hash(column)
            signature.append(identifier)
        return signature

    def _min_hash(self, column):
        return next((i for i, x in enumerate(column) if x is not None), None)

    def _init_buckets(self):
        self.model[BUCKETS_KEY] = dict()
        for i in self.model[SIGNATURE_MATRIX_KEY].columns:
            column = self.model[SIGNATURE_MATRIX_KEY][i]
            candidates = self._group_by_bands(column)
            for candidate in candidates:
                self._add_to_bucket(candidate, i)

    def _add_to_bucket(self, h, element):
        if h in self.model[BUCKETS_KEY]:
            self.model[BUCKETS_KEY][h].add(element)
        else:
            self.model[BUCKETS_KEY][h] = {element}

    def _group_by_bands(self, column):
        return [tuple(column[c:c + self.n_bands])
                for c in range(0, len(column), self.n_bands)]

    def _update_signature_matrix(self, item_id):
        df = DataFrame(self.matrix)
        column = df[item_id]
        sign = [self._min_hash(permutation(column))
                for _ in range(self.n_permutations)]
        self.model[SIGNATURE_MATRIX_KEY][item_id] = sign

    # Assuming users in the rows and items in the columns
    def new_stream(self, stream):
        user_id, item_id = stream[0], stream[1]
        self.matrix[user_id][item_id] = 1
        self._update_signature_matrix(item_id)
        self._init_buckets()

    def recommend(self, user_id):
        ratings = self.matrix[user_id]
        actual_ratings = [item_id for item_id in ratings
                          if ratings[item_id] is not None]
        signatures = [self.model[SIGNATURE_MATRIX_KEY][item_id]
                      for item_id in actual_ratings]
        rec = set()
        for sign in signatures:
            candidates = self._group_by_bands(sign)
            reduce(lambda accumulator, candidate: accumulator.union(
                self.model[BUCKETS_KEY][candidate]), candidates, rec)
        return rec.difference(set(actual_ratings))
