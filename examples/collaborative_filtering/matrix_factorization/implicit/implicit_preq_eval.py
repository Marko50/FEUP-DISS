import sys
import getopt
from algorithms.collaborative_filtering.matrix_factorization\
    .implicit_feedback import MatrixFactorizationImplicit
from evaluators.prequential.implicit_feedback import (
    PrequentialEvaluatorImplicit)
from stream.file_stream import FileStream

path = getopt.getopt(sys.argv[1:], "")[1][0]
fs = FileStream(path, sep="\t")
cf = MatrixFactorizationImplicit(lf=10)
ev = PrequentialEvaluatorImplicit(cf)
fs.process_stream(ev)
