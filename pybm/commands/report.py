from typing import List

from pybm import PybmConfig
from pybm.command import CLICommand
from pybm.config import get_reporter_class
from pybm.exceptions import PybmError
from pybm.reporters import BenchmarkReporter
from pybm.status_codes import ERROR, SUCCESS
from pybm.util.path import get_subdirs


class ReportCommand(CLICommand):
    """
    Report benchmark results from specified sources.
    """
    usage = "pybm report <run> <anchor-ref> <compare-refs> [<options>]\n"

    def __init__(self):
        super(ReportCommand, self).__init__(name="report")
        config = PybmConfig.load(".pybm/config.yaml")
        self.reporter: BenchmarkReporter = get_reporter_class(config)

    def add_arguments(self):
        self.parser.add_argument("run",
                                 type=str,
                                 metavar="<run>",
                                 help="Benchmark run to report results for. "
                                      "To report the preceding run, use the "
                                      "\"latest\" keyword. To report results "
                                      "of the n-th preceding run "
                                      "(i.e., n runs ago), "
                                      "use the \"latest^{n}\" syntax.")
        self.parser.add_argument("anchor_ref",
                                 metavar="<anchor-ref>",
                                 help="Mandatory. Reference to display "
                                      "results for or compare results "
                                      "against. In compare mode, "
                                      "this ref is the baseline for all "
                                      "comparisons, so any relative "
                                      "changes shown are always with respect "
                                      "to this ref.")
        self.parser.add_argument("compare_refs",
                                 nargs="*",
                                 default=None,
                                 metavar="<compare-refs>",
                                 help="Optional additional benchmarked refs "
                                      "to compare against the anchor. "
                                      "An error is raised if any of the given "
                                      "refs are not present in the run.")
        self.parser.add_argument("--target-filter",
                                 type=str,
                                 default=None,
                                 metavar="<regex>",
                                 help="Regex filter to selectively report "
                                      "benchmark target files. If specified, "
                                      "only benchmark files matching the "
                                      "given filter will be included "
                                      "in the report.")
        self.parser.add_argument("--benchmark-filter",
                                 type=str,
                                 default=None,
                                 metavar="<regex>",
                                 help="Regex filter to selectively report "
                                      "benchmarks from the matched target "
                                      "files. If specified, only benchmarks "
                                      "matching the given filter will be "
                                      "included in the report.")
        self.parser.add_argument("--context-filter",
                                 type=str,
                                 default=None,
                                 metavar="<regex>",
                                 help="Regex filter for additional context to "
                                      "report from the benchmarks. If "
                                      "specified, only context values "
                                      "matching the given context filter "
                                      "will be included in the report.")

    def run(self, args: List[str]) -> int:
        if not args:
            self.parser.print_help()
            return ERROR

        self.add_arguments()
        options = self.parser.parse_args(args)

        # TODO: Parse run to fit schema
        run = options.run
        anchor_ref = options.anchor_ref
        compare_refs = options.compare_refs

        if not compare_refs:
            result_dir = self.reporter.result_dir
            # TODO: Make this dynamic to support other run identifiers
            result = sorted(get_subdirs(result_dir))[-1]
            result_path = result_dir / result / anchor_ref
            if result_path.exists():
                self.reporter.report(ref=anchor_ref,
                                     result=result,
                                     target_filter=options.target_filter,
                                     benchmark_filter=options.benchmark_filter,
                                     context_filter=options.context_filter)
            else:
                raise PybmError(f"No benchmark results found for ref "
                                f"{anchor_ref!r} in the requested run.")
        else:
            raise PybmError("Comparison for multiple refs is not implemented "
                            "at this time.")

        return SUCCESS
