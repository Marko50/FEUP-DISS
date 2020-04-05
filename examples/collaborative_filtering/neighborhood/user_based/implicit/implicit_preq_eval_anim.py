import sys
import getopt
from algorithms.collaborative_filtering.neighborhood.\
    implicit_feedback import UserBasedImplicitCF
from evaluators.prequential.\
    implicit_feedback import PrequentialEvaluatorImplicit
from graphic import EvaluationAnimation
from stream import FileStream

path = getopt.getopt(sys.argv[1:], "")[1][0]
fs = FileStream(path, sep="\t")
cf = UserBasedImplicitCF()
ev = PrequentialEvaluatorImplicit(cf)
fs.process_stream_eval_anim(ev, EvaluationAnimation)