import sys
import getopt
from algorithms.collaborative_filtering.neighborhood.\
    implicit_feedback.user_based import UserBasedClustering
from evaluators.prequential.\
    implicit_feedback import PrequentialEvaluatorImplicit
from stream.file_stream.implicit import FileStreamImplicit
from graphic import EvaluationStatic


path = getopt.getopt(sys.argv[1:], "")[1][0]
output = getopt.getopt(sys.argv[1:], "")[1][1]
fs = FileStreamImplicit(path, sep="\t")
cf = UserBasedClustering()
ev = PrequentialEvaluatorImplicit(cf)
stat = EvaluationStatic(fs.stream, ev)
stat.process(path=output)
