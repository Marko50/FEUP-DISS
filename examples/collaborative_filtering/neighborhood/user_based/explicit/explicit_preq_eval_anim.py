import sys
import getopt
from algorithms.collaborative_filtering.neighborhood.\
    explicit_feedback import UserBasedExplicitCF
from evaluators.prequential.\
    explicit_feedback import PrequentialEvaluatorExplicit
from graphic import EvaluationAnimation
from stream import FileStream

path = getopt.getopt(sys.argv[1:], "")[1][0]
fs = FileStream(path, sep="\t")
cf = UserBasedExplicitCF()
ev = PrequentialEvaluatorExplicit(cf)
fs.process_stream_eval_anim(ev, EvaluationAnimation)