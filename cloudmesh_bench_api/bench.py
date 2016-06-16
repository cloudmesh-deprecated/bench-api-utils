from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractBenchmarkRunner:
    """
    An instance of AbstractBenchmarkRunner manages the lifecycle of a
    benchmark. This involves:

    #. fetching the benchmark
    #. preparing the environment to run the benchmark
    #. launching a virtual cluster
    #. deploying onto the virtual cluster
    #. running the benchmark
    #. cleaning up the virtual cluster

    In addition, the time taken to accomplish various components is
    tracked.


    Intended usage for developers:

    .. python:

       bench = MyBenchmarkRunner()
       bench.fetch()
       bench.prepare()
       bench.deploy()
       bench.run()
       bench.clean()


    Intended usage for users:

    .. python:

       bench = MyBenchmarkRunner(times='times.txt')
       bench.bench(repeat=10)


    The resultant ``times.txt`` can then be processed to generate figures.
    """


    __metaclass__ = ABCMeta

    @abstractmethod
    def _fetch(self, prefix):
        """Fetch everything required to run the current benchmark.

        This may be a ``git clone``, or downloading a tarball and extracting it.

        After this method is called the :func:`path` attribute may be
        accessed to get the path to the root directory of the benchmark.

        :param prefix: the path to a directory into which the
        benchmark should be made available.
        :type prefix: :class:`str`

        :returns: the full path to the fetched benchmark
        :rtype: :class:`str`
        """

        raise NotImplementedError


    def fetch(self, prefix=None):
        """Fetch everything required to run the benchmark

        :param prefix: where to put the directory (default is current working directory)
        :type prefix: :class:`str`
        :returns: location of the benchmark
        :rtype: :class:`str`
        """


        with self._timer.measure('fetch'):
            path = self._fetch(prefix)

        self._path = path
        return self.path

    def path(self):
        """
        :returns: The path to benchmark directory
        :rtype: str
        """
        return self._path
