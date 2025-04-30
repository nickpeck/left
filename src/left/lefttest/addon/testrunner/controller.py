from left import LeftController
from .views import ResultsView


class ResultsController(LeftController):

    def results(self, results):
        view = ResultsView()
        self._mount_view(view)
        view.update_state(results=results)
